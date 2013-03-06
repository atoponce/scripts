#! /bin/bash
#
# swap.sh: Shows the swap usage of each process
# Author: Robert Love
# Improved: Aaron Toponce <atoponce@xmission.com>

NAME=$(basename $0 2> /dev/null)
FILE=/tmp/swap-usage.txt
PIDFILE=/usr/local/var/run/backup_disks.pid
SWAP_TOTAL=0

if [ "$EUID" -ne 0 ]; then
    echo "Permission denied. This script must be run with root privileges."
    exit 1
fi

function usage {
    echo "Usage: $NAME [OPTION]"
    echo "Show the total swap usage by the system by individual PID and process name."
    echo "Default sort order is alphabetical order by process name."
    echo # blank line
    echo "-a, --ascending       Sort the swap usage in numerical ascending order."
    echo "-d, --descending      Sort the swap usage in numerical descending order."
    echo "-h, --help            Display this help and exit."
    echo # blank line
}

if [ ! -z "$1" ]; then
    case "$1" in
        -a|--ascending)
            SORTSW="-n"
            ;;
        -d|--descending)
            SORTSW="-rn"
            ;;
        -h|--help)
            usage
            exit 0
            ;;
    esac
fi

touch "$FILE"

for I in /proc/[0-9]*; do
    PID=$(echo "$I" | sed -e 's/\/proc\///g')
    SWAP_PID=$(awk 'BEGIN{total=0}/^Swap:/{total+=$2}END{print total}' /proc/$PID/smaps)
    if [ "$SWAP_PID" -gt 0 ]; then
        PNAME=$(awk '/^Name:/ {print $2}' /proc/$PID/status)
        echo "$PNAME ($PID) $SWAP_PID kB" >> $FILE
        let SWAP_TOTAL+="$SWAP_PID"
    fi
done

if [ ! -z "$SORTSW" ]; then
    sort "$SORTSW" -k 3 -o "$FILE" "$FILE"
else
    sort -o "$FILE" "$FILE"
fi

echo >> "$FILE" # blank line
echo "Total: "$SWAP_TOTAL" kB" >> "$FILE"
cat "$FILE"
rm "$FILE"
