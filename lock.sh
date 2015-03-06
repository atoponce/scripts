#!/bin/bash
# apt-get install scrot imagemagick i3lock
cd ~/Private/screenshots/
scrot screenshot.png
convert -scale 10% -scale 1000% screenshot.png blur.png
shred screenshot.png
rm screenshot.png
i3lock -i blur.png
