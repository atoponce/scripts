#!/bin/sh
#
# Author: Aaron Toponce
# Date May 28, 2008
# License: Public Domain
#
# Script to rotate passwords on servers. Sends a SHA1 of random data to
# every server as the password for the server. Requires ssh keys to be
# setup, mail(1), expect(1) and gpg(1). Recommended to use an SSH agent and
# GPG agent to prevent typing passwords a lot. Each server gets the same
# password. An encrypted version of the password is emailed.

KEYID="22EEE0488086060F" # replace long keyid with your own
EMAIL="user@example.com" # replace email with your own

if [[ -f newpass.gpg ]]; then
    mv -f newpass.gpg oldpass.gpg
    OLDPASSWD="$(gpg -d oldpass.gpg)"
fi

dd if=/dev/urandom count=100 2> /dev/null | sha1sum -b - |\
awk '{print $1}' | gpg -ar $KEYID -e - > newpass.gpg

cat newpass.gpg | mail -s "Password for servers" $EMAIL

NEWPASSWD="$(gpg -d newpass.gpg)"

# Change "server1 server2 sever3" to match the hostnames of the servers you'll loop over
# Change "domain.tld" to match the FQDN for your servers
# Could also put into a flat text file, and loop over that file with:
# while read host; do
# ... expect(1) code here
# done < servers.txt

for host in server1 server2 server3; do
    EXPECT=$(expect -c "
        spawn ssh $host.domain.tld
        send \"passwd\r\"
        expect \"(current) UNIX password: \"
        send \"$OLDPASSWD\r\"
        expect \"New UNIX password: \"
        send \"$NEWPASSWD\r\"
        expect \"Retype new password: \"
        send \"$NEWPASSWD\r\"
    ")
    echo $EXPECT
done
