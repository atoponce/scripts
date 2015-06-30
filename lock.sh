#!/bin/bash
# apt-get install scrot imagemagick i3lock
cd ~/Private/screenshots/
scrot screenshot.png
sha256sum screenshot.png >> SHA256SUMS
convert -scale 10% -scale 1000% screenshot.png blur.png
sha256sum blur.png >> SHA256SUMS
sha512sum SHA256SUMS > /dev/urandom
tac SHA256SUMS | sha512sum /dev/stdin > /dev/urandom
shred screenshot.png
rm screenshot.png
i3lock -i blur.png
shred blur.png
rm blur.png
