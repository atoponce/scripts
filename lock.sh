#!/bin/bash
# apt-get install scrot imagemagick i3lock
scrot /tmp/screenshot.png
convert /tmp/screenshot.png -blur 0x5 /tmp/blur.png
i3lock -i /tmp/blur.png
