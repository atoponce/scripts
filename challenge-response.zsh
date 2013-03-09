#!/bin/zsh

# Author: Aaron Toponce
# License: Public Domain
# Date: Mar 06, 2013
#
# Script for generating a challenge/response token for keysigning parties.
#
# After attending the party, download the public keyring from the party, or
# create one from the fingerprints on your handout. Then run this script
# against that keyring. It will generate a "tokens.txt" file. The syntax of
# that file will be as follows:
#
#       "KEYID","UID","TOKEN","SHA1 HASH"
#
# Verify that the KeyID matches what is on your printout (should be
# sufficient). Email the user with the minted Hashcash token (not the SHA1
# hash). When the user replies, with the token in the body of the mail,
# take the SHA1 of that token. If it matches what is in "tokens.txt", sign
# the UID on that key.
# 
# It complicates things, I understand, but has the benefit that those who
# are serious about getting their key(s) signed will reply, and you won't
# needlessly sign keys that won't sign yours back.
#
# TODO:
#   * Add automation with mutt(1) to send an encrypted message with
#     everything in place automatically.
#
# Some ZSH foo in this script:
#   - FOO=("${(@f)$(command)}") uses the 'f' expansion flag to split on
#     newlines; useful for arrays where a string could contain spaces
#   - FOO="${BAR[(ws,:,)10]}" returns only the 10th colon-delimited field from
#     every element in the $BAR array

# Only user-editable variables. Provide only absolute paths
GPG="/usr/bin/gpg"
HASHCASH="/usr/bin/hashcash"
KEYRING="${HOME}/.gnupg/dev/scale11x-keyring.gpg"

# DO NOT EDIT BELOW HERE
BASEDIR="$(dirname $KEYRING)"
touch "$BASEDIR/tokens.txt"
: > "$BASEDIR/tokens.txt"

if [ ! -x "$GPG" ]; then echo "GnuPG is not installed. Please install it before continuing."; exit 1; fi
if [ ! -x "$HASHCASH" ]; then echo "Hashcash is not installed. Please install it before continuing."; exit 2; fi
if [ ! -w "$BASEDIR" ]; then echo "Permission denied: $BASEDIR is not writable by the current process."; exit 3; fi
if [ ! -f "$KEYRING" ]; then echo "$KEYRING does not exist."; exit 4; fi

KEYS=("${(@f)$("$GPG" --fixed-list-mode --with-colons --list-keys --no-default-keyring --keyring="$KEYRING" | awk -F ':' '$1 == "pub" {print $5}')}")

for KEY in $KEYS; do 
    "$GPG" --import $KEYRING &> "$BASEDIR/challenge-response.out"
    UIDS=("${(@f)$("$GPG" --fixed-list-mode --with-colons --list-keys "$KEY" | awk -F ':' '$1 == "uid" && $2 ~ /(-|f|m|o|q|u)/')}")
    for U in $UIDS; do
        RESOURCE="${U[(ws,:,)10]}"
        TOKEN="$("$HASHCASH" -m $RESOURCE -Z 2)" # Mint a valid hashcash token to prevent faking the challenge/response
        HASH="$(echo -n $TOKEN | sha1sum - | sed 's/\s\+\-$//g')"
        echo "\"$KEY\",\"$RESOURCE\",\"$TOKEN\",\"$HASH\"" | tee >> "$BASEDIR/tokens.txt"
    done
done
