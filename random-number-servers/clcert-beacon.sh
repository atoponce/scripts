#!/bin/sh
# 512-bits randm data from the CLCERT Randomness Beacon
results=$(curl -so - https://beacon.clcert.cl/beacon/1.0/pulse/last)
echo -n "$results" | grep -Eo 'outputValue":"[[:xdigit:]]{128}' | cut -d '"' -f 3
