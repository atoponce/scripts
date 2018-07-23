#!/bin/sh
# 512-bits random data from ANU's QRNG
results=$(curl -so - 'https://qrng.anu.edu.au/API/jsonI.php?length=1&type=hex16&size=64')
echo "$results" | grep -Eo '[[:xdigit:]]{128}'
