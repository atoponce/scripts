#!/usr/bin/perl

# Author: Aaron Toponce
# Date: Mar 09, 2013
# License: Public Domain
#
# Script for parsing Nagios alerts from an IRC bot called "shazbot" in
# #xminfo in irc.xmission.com. I use ii(1) to connect to the irc server,
# then use:
#
#    tail -f ~/irc/irc.xmission.com/\#xminfo/out | shazbot.pl
#
# Produces color output based on the type of alert. Not perfect and
# bug-free, but "good enough".

use strict;
use Text::Wrap;
use Term::ReadKey;

while (my $line = <STDIN>) {
    my ($cols, $rows) = GetTerminalSize();
    $Text::Wrap::columns=$cols;

    ## Begin cleaning up the output
    $line =~ s/^.{5}//; # Strip year

    ## Remove joins/parts and other unnecessary cruft from output
    $line =~ s/^.*(joined|left).*\n//; # people joining and quitting the channel
    $line =~ s/^.*changed mode.*\n//; # mode changes in the channel
    $line =~ s/^.*911-MSG-VERY-OLD.*\n//;
    $line =~ s/^.*(Today:|Tonight:|Salt Lake City, UT conditions).*\n//; # remove weather
    $line =~ s/^.*(NOTICE|ONCALL).*\n//; # remove datacenter checks and oncall changes

    ## Cleaning up some of the output
    $line =~ s/\)$//g; # strip trailing parens
    $line =~ s/[\cC\d?\d?]+(N3?|I)//g; # strip mIRC color codes
    $line =~ s/(-!-| - )/ /g; # remove '-!-' and ' - ' from shazbot
    $line =~ tr/"//d; # remove all double quotes

    ## Color matching the whole line
    $line =~ s/.*(ACKNOWLEDGEMENT).*/\e[1;36m$&\e[0m/; # Bright cyan
    $line =~ s/.*(DOWN|RED|CRITICAL|UNKNOWN|withdrawn).*/\e[1;31m$&\e[0m/; # Bright red
    $line =~ s/.*(GREEN|RECOVERY).*/\e[1;32m$&\e[0m/; # Bright green
    $line =~ s/.*(YELLOW|WARNING).*/\e[1;33m$&\e[0m/; # Bright yellow

    $line =~ s/.?\d?(ACKNOWLEDGEMENT|PROBLEM|RECOVERY|CUSTOM|GREEN|RED|YELLOW|ONCALL|HOST:|is (OK|CRITICAL|DOWN|WARNING):)//g; # remove unnecessary text
    $line =~ s/\s{2,}/ /g; # remove all double spaces

    ## Underline the hostname
    $line =~ s/(\d+-\d+ \d+:\d+) ([.[:alnum:]\-]+) (.*)/$1 \e[4m$2\e[24m $3/;

    print $line;
}
