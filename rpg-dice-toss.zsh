#!/usr/bin/zsh
# Usage: rpg-dice-toss.zsh 3d6
count="${1%%d*}"; die="${1#*d}"
for i in {1.."$count"}; do
    roll=999
    # lcm(4,6,8,10,12,20)=120. 120*8=960
    while [[ "$roll" -ge "960" ]]; do
        roll=$(tr -cd 0-9 < /dev/urandom | head -c 3)
    done
    printf "%d " "($roll % $die) + 1"
done
printf "\n"
