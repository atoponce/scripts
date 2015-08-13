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

if [[ -z "$1" ]]; then
    echo "Usage: $0 filename"
    exit 2
fi

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

# Fisher-Yates shuffle the array. Adds some entropy
L=${#HASHES[*]}
while [[ "$L" -gt 1 ]]; do
    L=$((L-1))
    J=$(($(od -vAn -N4 -tu4 < /dev/urandom)%${L}))
    TMP="${HASHES[${L}]}"
    HASHES[${L}]="${HASHES[${J}]}"
    HASHES[${J}]="${TMP}"
done

# First, reseed the CSPRNG by hashing /proc/interrupts
for IX in ${!HASHES[*]}; do
    R="$R$(${HASHES[$IX]} /proc/interrupts | awk '{print $1}' | tr A-F a-f)"
done

# Finally, reseed the CSPRNG by hashing the provided path
for IX in ${!HASHES[*]}; do
    R="$R$(${HASHES[$IX]} $1 | cut -d ' ' -f 1 | tr A-F a-f)"
done

# For a final dash of entropy, shuffle the output digests
echo -n "$R" | fold -w 1 | shuf | tr -d '\n'; echo
