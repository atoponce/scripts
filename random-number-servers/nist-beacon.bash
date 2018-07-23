#!/bin/bash
# 512-bits random data from the NIST randomness beacon
read_xml () { local IFS=\>; read -d \< entity content; }

epoch=$(date --date="$(date +%H:%M:00)" +%s)
results=$(curl -so - https://beacon.nist.gov/rest/record/"$epoch")

while read_xml; do
    if [[ $entity = "outputValue" ]]; then
        echo "$content"
    fi
done <<< "$results" | tr A-F a-f
