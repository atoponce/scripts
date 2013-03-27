#!/bin/zsh
#
# Author: Aaron Toponce
# Date: Mar 27, 2013
# License: Public Domain
#
# Script to remove an SSH host key from your ~/.ssh/known_hosts file.
# Requires that dig(1) be installed, and requires an argument to be passed,
# which is a FQDN.

NAME=$(basename $0 2> /dev/null)

function usage {
    echo "Usage: $NAME HOST"
    echo "Remove an SSH host key from your ~/.ssh/known_keys file."
    echo "Requires an argument to be passed."
    exit 1
}

if [ -z "$1" ]; then
    usage
else
    SUB="${1%%.*}" # top subdomain
    DOM="${1#*.}" # domain

    if [ "$SUB" = "$DOM" ]; then
        echo "Please provide a FQDN."
        exit 2
    else
        ssh-keygen -R $SUB
        ssh-keygen -R $SUB.$DOM
        ssh-keygen -R $(dig +short $SUB.$DOM)
    fi
fi

