#!/usr/bin/env zsh
for f in /sys/block/zram*; do
    orig=$(< $f/orig_data_size)
    compr=$(< $f/compr_data_size)
    printf '%s: %6.2f%% (%.2f MiB -> %.2f MiB)\n' \
        ${f:t} \
        $((100 * ${compr}.0 / ${orig})) \
        $((${orig} / 1048576.0)) \
        $((${compr} / 1048576.0))
done
