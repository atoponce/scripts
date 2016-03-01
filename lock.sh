#!/bin/bash
# apt-get install imagemagick i3lock
TS=$(date +%Y%m%d%H%M%S%N)
cd ~/Private/screenshots/
import -window root ${TS}.png
sha256sum ${TS}.png >> SHA256SUMS
convert -scale 10% -scale 1000% ${TS}.png ${TS}-sm.png
sha256sum ${TS}-sm.png >> SHA256SUMS
sha512sum SHA256SUMS > /dev/urandom
tac SHA256SUMS | sha512sum /dev/stdin > /dev/urandom
shred ${TS}.png
rm ${TS}.png
i3lock -i ${TS}-sm.png
shred ${TS}-sm.png
rm ${TS}-sm.png
