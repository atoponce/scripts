#!/bin/zsh

# Convert traditional SSH private key format to PCKS#8 with 3DES
# See http://martin.kleppmann.com/2013/05/24/improving-security-of-ssh-private-keys.html
# Need the private key file as an argument

[ -z $1 ] && echo "Provide the private key as an argument." && exit 100
[ ! -e $1 ] && echo "$1 does not exist." && exit 2

mv $1 ${1}.old
openssl pkcs8 -topk8 -v2 des3 -in ${1}.old -out $1
chmod 0600 $1
exit 0
