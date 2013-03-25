#!/bin/zsh

# Author: Aaron Toponce
# Date: Mar 09, 2013
# License: Public Domain
#
# When building the diceware.zsh script, I discovered that my die is
# weighted. From one byte of randomness mod 6 there are 43 possible 0-3s
# and only 42 possible 4-5s. This script, combined with some math that you
# must do on your own, shows that it's biased away from 5 and 6 by 2%. So,
# you could update the command to read more bytes. Reading 2 bytes would
# produce a bias away from 5 and 6 by 9 thousandths of one percent. Reading
# 3 bytes would produce a bias away from 5 and 6 of 4 one-hundred
# thousandths by one percent. I would be willing to bet that standard
# fabricated dice have a larger bias towards some numbers than that. So,
# for practical purposes, reading only 10 bytes, would be more than
# sufficient, and certainly "close enough".

function dice-roll {
    RND=$(echo -n $((0x$(head -c 10 /dev/random | xxd -ps))))
    if [[ "$RND" -lt 252 ]]; then
        DIE=$(((RND%6)+1))
        DICE="${DICE}$DIE"
        I=$((I+1))
    fi
    echo -n "$DICE"
}

dice-roll
