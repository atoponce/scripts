#!/bin/sh
#
# Author: Troy Johnson <http://troy.jdmz.net/rsync/index.html>
# Modified: Aaron Toponce
# Date: July 22, 2011
# License: Public Domain
#
# Script to put into your ~/.ssh/authorized_keys file on a remote host that
# contains backups (a backup server for nightly cron jobs).
#
# You may need to do nightly backups over SSH, where the private key is not
# protected by a passphrase. As such, this script can make sure that the
# key is _only_ used for your rsync(1) backup command (can be modified for
# a "zfs receive", or other commands that rely on SSH keys.
#
# Change your ~/.ssh/authorized_keys file. If your public key line looks
# like this:
#
#   ssh-rsa   AAAAB3NzaC1yc2EAAAABIwAAAQEAzoblHIUARNP5Kq12QwUqxB6T7m8TWti4L...
#
# Then change it to look like this:
#
#   from="10.19.84.10",command="/home/user/bin/validate.sh" ssh-rsa   AAAAB...
#
# This would restrict use of the key from the 10.19.84.10 host only, and
# would execute this script upon connection. It is recommended to change:
#
#   PermitRootLogin no
#
# to:
#
#   PermitRootLogin forced-commands-only
#
# in your /etc/ssh/sshd_config on the remote host (where this script is
# installed). You may also want to consider using AllowUsers, AllowGroups,
# DenyUsers, and DenyGroups in your /etc/ssh/sshd_config.

case "$SSH_ORIGINAL_COMMAND" in
    *\&*)
        echo "Rejected"
    ;;
    *\(*)
        echo "Rejected"
    ;;
    *\{*)
        echo "Rejected"
    ;;
    *\;*)
        echo "Rejected"
    ;;
    *\<*)
        echo "Rejected"
    ;;
    *\`*)
        echo "Rejected"
    ;;
    *\|*)
        echo "Rejected"
    ;;
    rsync\ --server*)
        $SSH_ORIGINAL_COMMAND
    ;;
    # *zfs\ recv*)    # If using ZFS
    #   $SSH_ORIGINAL_COMMAND
    #;;
    # *zfs\ receive*) # If using ZFS
    #   $SSH_ORIGINAL_COMMAND
    #;;
    *)
        echo "Rejected"
    ;;
esac
