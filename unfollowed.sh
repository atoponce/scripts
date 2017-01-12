#!/bin/bash

GW="0000000000@sms-to-email-gateway.example.com"

if [[ ! -f ~/Private/old.txt ]]; then
    /usr/local/bin/t followers | sort > ~/Private/old.txt
    exit
fi

/usr/local/bin/t followers | sort > ~/Private/new.txt
comm -23 ~/Private/old.txt ~/Private/new.txt > ~/Private/diff.txt

if [[ -s ~/Private/diff.txt ]]; then 
    cat ~/Private/gone.txt | mail -s "Unfollowed $(date +%F)" $GW
    mv ~/Private/new.txt ~/Private/old.txt
    rm ~/Private/diff.txt ~/Private/gone.txt
fi
