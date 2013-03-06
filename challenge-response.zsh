#!/bin/zsh

# Some ZSH foo in this script:
#   - FOO=("${(@f)$(command)}") uses the 'f' expansion flag to split on
#     newlines; useful for arrays where a string could contain spaces
#   - FOO="${BAR[(ws,:,)10]}" returns only the 10th colon-delimited field from
#     every element in the $BAR array

# Only user-editable variables
# Provide only absolute paths
GPG="/usr/bin/gpg"
HASHCASH="/usr/bin/hashcash"
KEYRING="/home/aaron/.gnupg/dev/scale11x-keyring.gpg"

# DO NOT EDIT BELOW HERE
BASEDIR="$(dirname $KEYRING)"
touch "$BASEDIR/tokens.txt"
: > "$BASEDIR/tokens.txt"

if [ ! -x "$GPG" ]; then
    echo "GnuPG is not installed. Please install it before continuing."
    exit 1
fi

if [ ! -x "$HASHCASH" ]; then
    echo "Hashcash is not installed. Please install it before continuing."
    exit 2
fi

if [ ! -w "$BASEDIR" ]; then
    echo "Permission denied: $BASEDIR is not writable by the current process."
    exit 3
fi

if [ ! -f "$KEYRING" ]; then
    echo "$KEYRING does not exist."
    exit 4
fi

KEYS=("${(@f)$("$GPG" --fixed-list-mode --with-colons --list-keys --no-default-keyring --keyring="$KEYRING" | awk -F ':' '$1 == "pub" {print $5}')}")

for KEY in $KEYS; do 
    "$GPG" --recv-keys $KEY &> "$BASEDIR/challenge-response.out"
    UIDS=("${(@f)$("$GPG" --fixed-list-mode --with-colons --list-keys "$KEY" | awk -F ':' '$1 == "uid" && $2 ~ /(-|f|m|o|q|u)/')}")
    for U in $UIDS; do
        RESOURCE="${U[(ws,:,)10]}"
        TOKEN="$("$HASHCASH" -m $RESOURCE -Z 2)" # Mint a valid hashcash token to prevent faking the challenge/response
        HASH="$(echo -n $TOKEN | sha1sum - | sed 's/\s\+\-$//g')"
        echo "\"$KEY\",\"$RESOURCE\",\"$TOKEN\",\"$HASH\"" | tee >> "$BASEDIR/tokens.txt"
    done
done
