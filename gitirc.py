#!/usr/bin/env python2

import ircbot
import json
import os
import select
import socket
import sys

# required, otherwise irclib.ServerConnection.privmsg() fails when text contains
# non-ascii char
reload(sys)
sys.setdefaultencoding('utf8')


class Bot(ircbot.SingleServerIRCBot):
    def __init__(self, network, nickname, channel, **options):
        ircbot.SingleServerIRCBot.__init__(self, [network], nickname, nickname)
        self.channel = channel
        self.options = options

    def connect(self, *args, **kwargs):
        '''
        Intercepts call to ircbot.SingleServerIRCBot.connect to add support
        for ssl and ipv6 params.
        '''

        kwargs.update(self.options)
        ircbot.SingleServerIRCBot.connect(self, *args, **kwargs)

    def on_welcome(self, serv, ev):
        self.serv = serv
        serv.join(self.channel)

    def report(self, l):
        if self.serv:
            self.serv.privmsg(self.channel, l.rstrip())


def read_unix_data(s):
    c, _ = s.accept()
    try:
        data = c.recv(4096)
    except:
        data = ''
    c.close()

    return data


def create_unix_socket(config):
    sockaddr = os.path.expanduser(config['sockaddr'])

    if os.path.exists(sockaddr):
        os.unlink(sockaddr)

    s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    s.bind(sockaddr)
    s.listen(1)

    return s


def main(config):
    unix_socket = create_unix_socket(config)
    bot = Bot(**config['irc'])
    bot._connect()

    while True:
        irc_socket = bot.connection._get_socket()
        readable, _, _ = select.select([irc_socket, unix_socket], [], [])
        for sock in readable:
            if sock is unix_socket:
                data = read_unix_data(unix_socket)
                if data:
                    bot.report(data)
            elif sock is irc_socket:
                bot.connection.process_data()

    unix_socket.close()


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print 'Usage: %s <config.json>' % sys.argv[0]
        sys.exit(0)

    with open(sys.argv[1]) as fp:
        config = json.load(fp)

    try:
        main(config)
    except (KeyboardInterrupt, SystemExit):
        sockaddr = os.path.expanduser(config['sockaddr'])
        if os.path.exists(sockaddr):
            os.unlink(sockaddr)
