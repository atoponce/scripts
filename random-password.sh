#!/bin/bash

# Requires https://github.com/atoponce/nodepassgen to be installed in $PATH
# For a mutt header Easter Egg. It's stupid.
# I guess you could run this stand-alone for a random nodepassgen password.
# Released to the public domain

random_number () {
    shuf -i "$1"-"$2" -n 1 --random-source=/dev/urandom
}

declare -a alternate_options=(\
    "Colors" "Elvish" "Klingon" "PGP" "Rockyou" "Simpsons" "Trump")
declare -a bitcoin_options=(\
    "Chinese" "English" "French" "Italian" "Japanese" "Korean")
declare -a diceware_options=(\
    "Basque" "Beale" "Bulgarian" "Catalan" "Chinese" "Czech" "Danish" "Dutch"\
    "Dutch-Alt" "English" "Esperanto" "Finnish" "French" "German" "Hungarian"\
    "Italian" "Japanese" "Maori" "Norwegian" "Polish" "Portuguese" "Russian"\
    "Slovenian" "Spanish" "Swedish" "Turkish")
declare -a eff_options=(\
    "Distant" "Long" "Short")
declare -a pseudowords_options=(\
    "Bubble Babble" "Korean K-pop" "Secret Ninja")
declare -a random_options=(\
    "Base94" "Base85" "Base64" "Base62" "Base58" "Base52" "Base36" "Base32"\
    "Base26" "Base16" "Base10" "Base8" "Base2" "Coins" "DNA" "Emoji")

case "$(random_number 1 7)" in
    1)
        gen="alternate"
        ;;
    2)
        gen="bitcoin"
        ;;
    3)
        gen="diceware"
        ;;
    4)
        gen="eff"
        ;;
    5)
        gen="pseudowords"
        ;;
    6)
        gen="random"
        ;;
    7)
        gen="system"
        ;;
esac

case "$gen" in
    "alternate")
        length=$(echo ${#alternate_options[@]})
        entry=$(random_number 0 "$((length-1))")
        wordlist="${alternate_options[$entry]}"
        ;;
    "bitcoin")
        length=$(echo ${#bitcoin_options[@]})
        entry=$(random_number 0 "$((length-1))")
        wordlist="${bitcoin_options[$entry]}"
        ;;
    "diceware")
        length=$(echo ${#diceware_options[@]})
        entry=$(random_number 0 "$((length-1))")
        wordlist="${diceware_options[$entry]}"
        ;;
    "eff")
        length=$(echo ${#eff_options[@]})
        entry=$(random_number 0 "$((length-1))")
        wordlist="${eff_options[$entry]}"
        ;;
    "pseudowords")
        length=$(echo ${#pseudowords_options[@]})
        entry=$(random_number 0 "$((length-1))")
        wordlist="${pseudowords_options[$entry]}"
        case "$wordlist" in
            "Bubble Babble")
                arg=""
                ;;
            "Korean K-pop")
                arg="--kpop"
                ;;
            "Secret Ninja")
                arg="--ninja"
                ;;
        esac
        nodepassgen -o pseudowords "$arg" -m 128 | awk '{print $2}'
        exit 0
        ;;
    "random")
        length=$(echo ${#random_options[@]})
        entry=$(random_number 0 "$((length-1))")
        wordlist="${random_options[$entry]}"
        ;;
esac

nodepassgen -o "$gen" --"$gen" "$wordlist" -m 128 -H | awk '{print $2}'
