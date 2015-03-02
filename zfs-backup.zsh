#!/bin/zsh
# Author: Aaron Toponce
# License: Public Domain
# Date: Mar 6, 2013
#
# Script to backup the snapshots of a ZFS filesystem to an offsite ZFS
# storage server using "zfs send" and "zfs receive". If put in crontab(5),
# it can execute after your "time sliding" snapshots, to make sure the
# latest snapshot is always offsite.
#
# This does require that your offsite ZFS pool is fully caught up with the
# exact snapshots as is on the source before this can be automated. After
# the offsite ZFS pool is a mirror of the src pool, then you can proceed
# with automating the script.

# Edit LIVE and BACKUP only
LIVE="tank"
BACKUP="backup"

# Do not edit after here
ZFS="/sbin/zfs"
DSETS=($($ZFS list -H -o name -t filesystem -r "$LIVE"))

for D in $DSETS; do
    POOL=$(echo "$D" | awk -F '@' '{split($1,a,"/"); print a[1]}')
    DSET=$(echo "$D" | awk -F '@' '{split($1,a,"/"); print a[2]}')
    if [ -z "$DSET" ]; then FS="$POOL" else FS="$POOL/$DSET" fi
    SNAPS=($($ZFS list -t snap -Ho name -S creation -r "$FS" | grep "$FS@"))
    SNAPS=(${(@)SNAPS:#*swap*}) # no need to worry about swap
    FREQ_SNAP=(${(M)SNAPS:#*frequent*})
    if [[ ! -z "$FREQ_SNAP" ]]; then
        $ZFS send -RI $FREQ_SNAP[2] $FREQ_SNAP[1] | $ZFS recv -Fduv $BACKUP
    fi
done
