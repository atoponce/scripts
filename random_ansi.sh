#!/bin/sh

while sleep .01; do printf "\e[48;5;$(($(od -d -N 2 -A n /dev/urandom)%$(tput colors)))m \e[0m" done
