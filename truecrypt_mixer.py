#!/usr/bin/python

from Cryptodome.Hash import SHAKE256

ans = True
shake = SHAKE256.new()

def _get_passphrase():
    while True:
        passphrase = raw_input("Enter 320 random characters:\n")
        if len(passphrase) > 320:
            break
        else:
            print("Enter at least 320 random characters.")
    return passphrase[:320]

while ans:
    print ("""
    1. 128-bit
    2. 160-bit
    3. 256-bit
    4. 320-bit
    5. 512-bit
    """)

    ans = raw_input("How many bits should mix your input? ") 
    if ans == "1": 
        shake.update(_get_passphrase())
        shake.read(16)
    elif ans == "2":
        shake.update(_get_passphrase())
        shake.read(20)
    elif ans == "3":
        shake.update(_get_passphrase())
        shake.read(32)
    elif ans == "4":
        shake.update(_get_passphrase())
        shake.read(40)
    elif ans == "5":
        shake.update(_get_passphrase())
        shake.read(64)
    else:
        print("Not a valid input. Try again.")
