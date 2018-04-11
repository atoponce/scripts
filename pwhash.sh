#!/bin/sh

read -p "Enter password: " pw
echo # blank line

echo "     Apache: $(htpasswd -bn '' $pw | tr -d ':\n')"
echo "      MySQL: $(printf "$pw" | sha1sum | awk '{print $1}' | xxd -r -p | 
                     sha1sum | sed 's/^/*/g' | awk '{print $1}' | tr a-f A-F)"
echo "   descrypt: $(echo "$pw" | mkpasswd -P 0)"
echo "   md5crypt: $(echo "$pw" | mkpasswd -m md5 -P 0)"
echo "sha256crypt: $(echo "$pw" | mkpasswd -m sha-256 -P 0)"
echo "sha512crypt: $(echo "$pw" | mkpasswd -m sha-512 -P 0)"
echo "     bcrypt: $(htpasswd -bnB '' $pw | tr -d ':\n' | sed 's/^\$..\$/$2b$/g')"
