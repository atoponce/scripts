#!/bin/sh

# Generate an OpenSSH moduli file suitable for replacing /etc/ssh/moduli.
#
# This script executes in two parts:
#
# 1. Generate candidate primes for DH key exchange
# 2. Run the candidates through the Miller-Rabin primality test.
# 
# By default, only 1024, 1536, 2048, 3072, 4096, 6144, & 8192-bit primes exist.
# Inestead, 1024-bits to 8192-bits, in 512-bit intervals are generated.
# Generating the candidates takes about 25 minutes on an older 8-core Xeon.
# Generating the safe primes takes about 40 hours on the same machine.
# Currently requires procfs, which limits use to GNU/Linux. Sorry BSD.
#
# Author: Aaron Toponce
# Date: Wed Jan 7, 2015
# License: Public Domain

NSOCK=$(grep 'physical id' /proc/cpuinfo | sort -u | wc -l)
NCORE=$(grep 'cpu cores' /proc/cpuinfo | sort -u | cut -d ':' -f 2)
NPROC=$((${NSOCK}*${NCORE}))

# generate the candidate primes files first
BITS=1024
while [ $BITS -le 8192 ]; do
    TMP=0
    while [ $TMP -lt $NPROC ]; do
        if [ $TMP -lt $((${NPROC}-1)) ]; then
            ssh-keygen -G /dev/stdout -b $BITS | gzip -1c > moduli.${BITS}.gz &
        else
            ssh-keygen -G /dev/stdout -b $BITS | gzip -1c > moduli.${BITS}.gz
        fi
        BITS=$((${BITS}+512))
        TMP=$((${TMP}+1))
    done
done

# now work on getting to the safe primes
BITS=1024
while [ $BITS -le 8192 ]; do
    TMP=0
    TOTAL_LINES=$(gzip -dc moduli.${BITS}.gz | wc -l)
    LINES_PER_FILE=$(((${TOTAL_LINES}+${NPROC}-1)/${NPROC}))
    
    gzip -dc moduli.${BITS}.gz | split -a 1 -dl $LINES_PER_FILE \
        --filter="gzip -1c > moduli.${BITS}.\$FILE.gz"

    while [ $TMP -lt $NPROC ]; do
        if [ $TMP -lt $((${NPROC}-1)) ]; then
            gzip -dc moduli.${BITS}.x${TMP}.gz | \
                ssh-keygen -T moduli.${BITS}.safe.${TMP} &
        else
            # This job could finish before the previous backgrounded ones
            # So, more ssh-keygen(1) PIDs may be briefly working than $NPROC
            gzip -dc moduli.${BITS}.x${TMP}.gz | \
                ssh-keygen -T moduli.${BITS}.safe.${TMP}
        fi
        TMP=$((${TMP}+1))
    done

    # because the non-backgrounded PID may finish first, dupes may exist
    cat moduli.${BITS}.safe.* >> moduli.tmp
    BITS=$((${BITS}+512))
done

# remove any possible duplicates
sort -u moduli.tmp > moduli

echo # blank line
echo "Finished. The 'moduli' file is ready for install to /etc/ssh/moduli."
