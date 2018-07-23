#!/bin/sh
#
# inseminate: an Entropy-as-a-Service client
#
#  inseminate is a fork of pollinate by Dustin Kirkland found at:
#       https://github.com/dustinkirkland/pollinate/blob/master/pollinate
#
# Put in crontab as follows:
#       * * * * * sh inseminate > /dev/random
#
#  Copyright (C) 2015 Aaron Toponce <aaron.toponce@gmail.com>
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, version 3 of the License.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.

# Construct a user agent, with useful debug information
curl_ver="$(curl -V | head -n 1 | awk '{print $2}')"
lsb="$(lsb_release -is)/$(lsb_release -rs)"
platform="$(uname -o)/$(uname -r)/$(uname -m)"
user_agent="inseminate/0.4 curl/$curl_ver $lsb $platform"

# Setup the challenge with a response
challenge=$(head -c 64 /dev/urandom | sha512sum | awk '{print $1}')
challenge_response=$(echo -n "$challenge" | sha512sum | awk '{print $1}')
f1=$(echo -n "challenge=$challenge")

# Get the data
results=$(curl -A "$user_agent" -o- -s -m 3 -d "$f1" https://entropy.ubuntu.com)
response=$(echo "$results" | head -n 1)

[ "$challenge_response" = "$response" ] && echo "$results" | tail -n 1
