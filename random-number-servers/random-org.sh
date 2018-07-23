#!/bin/sh
# Reseed the Linux kernel CSPRING with data from random.org
results=$(curl -so - 'https://www.random.org/cgi-bin/randbyte?nbytes=64&format=h')
echo -n "$results" | sed 's/ //g' | paste -sd ''
