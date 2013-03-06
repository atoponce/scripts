#!/bin/bash
# Replace $KEY with your own KEYID
KEY="22EEE0488086060F"
echo "Getting initial list of signatures..."
gpg --with-colons --fast-list-mode --list-sigs $KEY | awk -F ':' '$1 ~ /sig|rev/ {print $5}' | sort -u > ${KEY}.ids
echo "Refreshing your keyring..."
gpg --recv-keys $(cat ${KEY}.ids) > /dev/null 2>&1
echo "Creating public keyring..."
gpg --export $(cat ${KEY}.ids) > ${KEY}.gpg
echo "Creating dot file..."
gpg --keyring ./${KEY}.gpg --no-default-keyring --list-sigs | sig2dot > ${KEY}.dot 2> ${KEY}.err
echo "Creating PostScript document..."
neato -Tps ${KEY}.dot > ${KEY}.ps
echo "Creating graphic..."
convert ${KEY}.ps ${KEY}.gif
echo "Finished."
