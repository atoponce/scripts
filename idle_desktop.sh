#!/bin/bash

# to be put in crontab. meant to see if X is idle for 10 minutes. if so, lock.

if [ $(xprintidle) -ge $((1000*60*10)) ]; then
    if ! ps -ef | grep -q 'i3loc[k]'; then
        bash /home/atoponce/src/scripts/lock.sh
    fi
fi
