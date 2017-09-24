#!/bin/bash
# apt-get install imagemagick i3lock
ps -ef | grep -q '[k]eybase -d'
if [ $? -ne 0 ]; then
    run_keybase
fi
TS=$(date +%Y%m%d%H%M%S%N)
cd ~/Private/screenshots/
import -window root ${TS}.png
# ~ 512-bits entropy appended to end of PNG
#tr -cd '[:print:][:cntrl:]' < /dev/urandom | head -c 74 >> ${TS}.png
sha512sum /keybase/public/atoponce/SHA256SUMS | awk '{print $1}' >> ${TS}.png
sha256sum ${TS}.png >> /keybase/public/atoponce/SHA256SUMS
convert -scale 10% -scale 1000% ${TS}.png ${TS}-sm.png
# ~ 512-bits entropy appended to end of PNG
#tr -cd '[:print:][:cntrl:]' < /dev/urandom | head -c 74 >> ${TS}-sm.png
sha512sum /keybase/public/atoponce/SHA256SUMS | awk '{print $1}' >> ${TS}-sm.png
sha256sum ${TS}-sm.png >> /keybase/public/atoponce/SHA256SUMS
sha512sum /keybase/public/atoponce/SHA256SUMS > /dev/urandom
tac /keybase/public/atoponce/SHA256SUMS | sha512sum /dev/stdin > /dev/urandom
shred ${TS}.png
rm ${TS}.png
i3lock -i ${TS}-sm.png
shred ${TS}-sm.png
rm ${TS}-sm.png
