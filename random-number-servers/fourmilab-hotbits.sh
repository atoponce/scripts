#!/bin/sh
# 512-bits random data from Fourmilab Hotbits
# apikey found off Github. Thank you Internet.
results=$(curl -so - 'http://www.fourmilab.ch/cgi-bin/Hotbits?nbytes=64&apikey=HB1RNFWeh9e8HTTZm06b5sRSUPU')
echo -n "$results" | grep -Eo '[[:xdigit:]]{64}' | paste -sd '' | tr A-F a-f
