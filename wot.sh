#!/bin/bash

# Author: Aaron Toponce
# License: Public Domain
# Date: Mar 6, 2013
#
# Creates a graphical Web of Trust for your own key. Assumes you have the
# GnuPG, signing-party (sig2dot), graphviz and imagemagick packages
# installed, as it makes no sanity checks. All files will be created in the
# same directory as where you run the script, and are not cleaned up after
# execution.
#
# An example:
#
#   http://aarontoponce.org/pubring.gif

# Replace $KEY with your own KEYID
KEY="22EEE0488086060F"

# No need to edit anything here.
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
