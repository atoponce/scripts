#!/bin/zsh

# Author: Aaron Toponce
# Date: Sept 20, 2012
# License: Public Domain
#
# ZSH script to create true random diceware passphrases. Requires
# diceware.wordlist.asc to be present in the same directory as the script.
# Can be found at http://world.std.com/~reinhold/diceware.wordlist.asc

BASEDIR="$(echo "${0%/*}")"
WORDLIST="$BASEDIR/diceware.wordlist.asc"

if [[ ! -f "$WORDLIST" ]]; then
    echo "The diceware.wordlist.asc file must be present in the same"
    echo "directory as the diceware.zsh script."
    echo # Blank line
    echo "http://world.std.com/~reinhold/diceware.wordlist.asc"
    exit 1
fi

# Function to generate each Diceware word from the list
function five-dice-roll {
    echo -n $(< /dev/urandom tr -dc 1-6 | head -c 5)
}

# Function to find the Diceware word based on our dice roll
function diceware-word {
    awk "/$(five-dice-roll)/ {print \$2}" "$WORDLIST"
}

if [[ "$1" = <-> ]]; then NUM="$1"; else NUM=6; fi

for i in {1.."$NUM"}; do
    DICEPASS="${DICEPASS}$(diceware-word)"
done

echo "$DICEPASS"
