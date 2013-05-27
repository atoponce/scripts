#!/bin/zsh

# Convert traditional SSH private key format to PCKS#8 with 3DES
# See http://martin.kleppmann.com/2013/05/24/improving-security-of-ssh-private-keys.html
# Need the private key file as an argument

[ -z $1 ] && echo "Provide the private key as an argument." && exit 1
[ ! -e $1 ] && echo "$1 does not exist." && exit 2

function topkcs8 {
    umask 0077
    mv $1 ${1}.old
    openssl pkcs8 -topk8 -v2 des3 -in ${1}.old -out $1
}

CRYPTO=$(head -n 1 $1 | awk '{print $2}')

case $CRYPTO in
    "EC" | "DSA" | "RSA")
        topkcs8 $1
        ;;
    "ENCRYPTED")
        echo "$1 already converted."
        exit 3
        ;;
    *)
        echo "$1 not readable or not a valid format."
        exit 4
        ;;
esac

exit 0
