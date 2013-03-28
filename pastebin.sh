#!/bin/sh

# Author: Aaron Toponce
# Date: Mar 28, 2013
# License: Public Domain

# Just a collection of aliases for using my pastebin found at
# http://ae7.st/p/. Each alias should be self-documenting. Each alias
# returns a URL of the paste.

function paste-gen {
    TEXT=$(cat $1)
    curl -d author=eightyeight -d pasteEnter="$TEXT" http://ae7.st/p/api |\
    awk -F '"' '/url/ {print $4}'
}
