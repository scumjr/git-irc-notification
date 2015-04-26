#!/bin/sh

SOCKADDR="/tmp/.gitircsocket"
IFS=' '

while read old_value new_value ref_name
do
    if [ "$ref_name" = 'refs/heads/master' ]
    then
		git rev-list --reverse "$old_value..$new_value" | while read commit
		do
			if [ $(git rev-parse --is-bare-repository) = true ]
			then
				repo=$(basename "$PWD" .git)
			else
				repo=$(basename $(readlink -nf "$PWD/.."))
			fi
			git show --quiet --pretty="format:%Cred[$repo]%Creset %Cblue[%an]%Creset %s" "$commit" | nc -U $SOCKADDR
		done
    fi
done

exit 0
