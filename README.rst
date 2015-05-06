IRC bot which sends commit messages on a channel when a git push is done on a
local repository.

Eg::

    < gitbot> [repo] [John Doe] story 182: Fix benchmarks for speed
    < gitbot> [repo] [Paul Robert] revert 86b09c33


Configuration
=============

The configuration is a JSON file. ``SOCKADDR`` variable in ``gitirc.sh`` must
reflect value in JSON file.

By default, only pushes on ``master`` branch are tracked. If you want to track
several branches, modify the condition on ``ref_name`` in ``gitirc.sh``. For
example, to watch ``master`` and ``dev`` : ::

    if [ "$ref_name" = 'refs/heads/master' ] || [ "$ref_name" = 'refs/heads/dev' ]


Installation
============

Install ``gitirc.sh`` as a post-receive hook in ``$GIT_DIR/hooks``::

    cp ~/git-irc-notification/gitirc.sh $repo/hooks/post-receive

If several repos are being watched, a symbolic link may be cleaner::

    for repo in r1.git r2.git; do
      ln -s ~/git-irc-notification/gitirc.sh $repo/hooks/post-receive
    done

Once hook is installed, run: ::

    ./gitirc.py config.json


Requirements
============

``python-irclib``, ``netcat``


Thanks
======

https://doc.wikimedia.org/puppetsource/modules/tcpircbot/files/tcpircbot.py
