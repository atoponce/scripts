#!/bin/zsh

cd /sys/block
echo -e "dev\torig\tcomp\tratio"

for FILE in zram?; do
    ORIG="$(cat $FILE/orig_data_size)"
    COMP="$(cat $FILE/compr_data_size)"
    RATIO="$(echo "scale=2; ${ORIG}/${COMP}" | bc -l)"
    echo -e "${FILE}\t${ORIG}\t${COMP}\t${RATIO}"
done 
