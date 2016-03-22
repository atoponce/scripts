#!/bin/bash

if [[ ! -x /usr/bin/rhash ]]; then
    echo "rhash(1) needs to be installed."
    echo "apt-get install rhash."
    exit 1
fi

if [[ ! -x /usr/local/bin/b2sum ]]; then
    echo "b2sum(1) needs to be installed."
    echo "git clone https://github.com/BLAKE2/BLAKE2.git"
    exit 1
fi

if [[ ! -x /usr/local/bin/skein256sum ]]; then
    echo "skein256sum(1) needs to be installed."
    echo "git clone https://jxself.org/git/skeinsum.git"
    exit 1
fi

if [[ ! -x /usr/local/bin/skein512sum ]]; then
    echo "skein512sum(1) needs to be installed."
    echo "git clone https://jxself.org/git/skeinsum.git"
    exit 1
fi

if [[ ! -x /usr/local/bin/skein1024sum ]]; then
    echo "skein1024sum(1) needs to be installed."
    echo "git clone https://jxself.org/git/skeinsum.git"
    exit 1
fi

if [[ ! $(dpkg-query -W python-zxcvbn) ]]; then
    echo "python-zxcvbn needs to be installed."
    echo "sudo apt-get install python-zxcvbn"
    exit 1
fi

if [[ -z "$1" ]]; then
    echo "Usage: $0 filename"
    exit 2
fi

function  xor() {
    R=()
    R1=($(echo "$1" | sed -r 's/(..)/0x\1 /g'))
    R2=($(echo "$2" | sed -r 's/(..)/0x\1 /g'))
    for I in $(seq 1 ${#R1[@]}); do R[$I]=$((R1[$I]^R2[$I])); done
    printf "%02x" "${R[@]}"
}

KEY=""
while [[ $(printf "$KEY" | wc -c) -lt 32 || $(python -c "import zxcvbn;\
    p = zxcvbn.password_strength('$KEY')['entropy']; print int(p)") -lt 128 ]]
    do
        read -p "Enter a key with at least 128-bits of entropy and 32-chars: " >&2 KEY
done

# All the hashes, in output digest bit-length order
HASHES=('rhash --md4' 'rhash --md5' 'rhash --snefru128' 'rhash --sha1' \
        'rhash --ripemd160' 'rhash --has160' 'rhash --btih' 'rhash --tiger' \
        'rhash --sha224' 'rhash --sha3-224' 'b2sum -a blake2s' \
        'b2sum -a blake2sp' 'rhash --sha256' 'rhash --sha3-256' \
        'rhash --gost' 'rhash --gost-cryptopro' 'rhash --snefru256' \
        'rhash --edonr256' 'skein256sum' 'rhash --sha384' 'rhash --sha3-384' \
        'b2sum -a blake2b' 'b2sum -a blake2bp' 'rhash --sha512' \
        'rhash --sha3-512' 'rhash --whirlpool' 'rhash --edonr512' \
        'skein512sum' 'skein1024sum')

for IX in ${!HASHES[*]}; do
    # First, add a hashed passphrase
    if [[ ${HASHES[$IX]} =~ "rhash"* || ${HASHES[$IX]} =~ "b2sum"* ]]; then
        R1="$(printf $KEY | ${HASHES[$IX]} /dev/stdin | cut -d ' ' -f 1 | tr A-F a-f)"
    else
        R1="$(printf $KEY | ${HASHES[$IX]} | cut -d ' ' -f 1 | tr A-F a-f)"
    fi
    #echo "${HASHES[$IX]}: $R1"
    # Next, hash the provided path with the passphrase
    R2="$(${HASHES[$IX]} $1 | cut -d ' ' -f 1 | tr A-F a-f)"
    #echo "${HASHES[$IX]}: $R2"
    # XOR the two digests into one
    R="$R$(xor $R1 $R2)"
    #echo "xor: $(xor $R1 $R2)"
    #echo
done

# Print the final combined hash in base64
echo "$R" | fold -w 1 | xxd -r -p | base64
