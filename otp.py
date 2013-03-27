#!/usr/bin/env python
#
# Author: Aaron Toponce
# Date Mar 25, 2013
# License: Public Domain
#
# One Time Pad implementation using 2 USB sticks.
#
# The idea of this OTP is to write /dev/random data to a full USB stick,
# then image that USB stick to another USB stick. Thus, you have 2 USB
# sticks with the same random data from start to finish, that can be
# verified with a cryptographic hashing algorithm, such as SHA1.
#
# This script takes your USB stick as an argument, and requires the 'root'
# user to run. It will read the size of the file you wish to encrypt, read
# that many bytes from the USB stick, and XOR the read data with the
# plaintext file, saving to an encrypted file. Afterwhich, the read data
# from the USB stick will be overwritten with new /dev/random data, to
# prevent from being used again. A counter file is created to keep track
# what the last read byte on the USB stick was.
#
# A recipient is given the other USB stick. When an encrypted note is
# created with this OTP, the sender's USB stick will be modified, with a
# counter file updated as necessary. When the recipient gets the encrypted
# file, the same process is used, with the same counter file created.
#
# IT'S CRITICAL THAT THE USB STICKS START OUT IDENTICAL!
# IT'S IMPORTANT TO KEEP THE TWO COUNTER FILES IN SYNC!
#
# If the two counter files are not kept in sync, then the encrypted data
# will not be decrypted correctly. If the two USB sticks do not start out
# with identica data, then the encrypted files will not be decrypted
# correctly.

import sys
import argparse

for arg in sys.argv[1:]:
    try:
        f = open(arg, "rw")
    except IOError:
        print arg, "is not available."
    else:
        parser = argparse.ArgumentParser()
        parser.add_argument("-e", "--encrypt", help="Encrypt a file")
        parser.add_argument("-d", "--decrypt", help="Decrypt a file")
        parser.add_argument("device", help="Device to read for the One Time Pad")
        args = parser.parse_args()
        f.close()

def encrypt():
    return True

def decrypt():
    return True
