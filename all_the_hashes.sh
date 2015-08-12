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

# hash the file in order of output digest size
# 128-bit
rhash --md4             "$1"
rhash --md5             "$1"
rhash --snefru128       "$1"

# 160-bit
rhash --sha1            "$1"
rhash --ripemd160       "$1"
rhash --has160          "$1"
rhash --btih            "$1"

#192-bit
rhash --tiger           "$1"

# 224-bit
rhash --sha224          "$1"
rhash --sha3-224        "$1"

# 256-bit
b2sum -a 'blake2s'      "$1"
b2sum -a 'blake2sp'     "$1"
rhash --sha256          "$1"
rhash --sha3-256        "$1"
rhash --gost            "$1"
rhash --gost-cryptopro  "$1"
rhash --snefru256       "$1"
rhash --edonr256        "$1"
skein256sum             "$1"

# 384-bit
rhash --sha384          "$1"
rhash --sha3-384        "$1"

# 512-bit
b2sum -a 'blake2b'      "$1"
b2sum -a 'blake2bp'     "$1"
rhash --sha512          "$1"
rhash --sha3-512        "$1"
rhash --whirlpool       "$1"
rhash --edonr512        "$1"
skein512sum             "$1"

# 1024-bit
skein1024sum            "$1"
