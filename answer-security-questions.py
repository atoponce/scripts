#!/usr/bin/python

# Released to the public domain.

# Designed for answering security questions deterministically, while
# guaranteeing a minimum security margin to prevent anyone who knows the actual
# answer from compromising an account.

# SHA-3 is based on Keccak which uses the sponge construction
# bcrypt is based on Blowfish which uses the feistel construction
# BLAKE2 is based on ChaCha and uses the HAIFA construction

import sha3
import bcrypt
import pyblake2

print("Answers are case-sensitive.")
site = raw_input("What site is this for? Root domain and TLD only (E.G.: example.com) ")
key = raw_input("What is a secret key with at least 128-bits entropy only you know? ")
answer = raw_input("What is the answer to the security question? ")

b2salt = sha3.sha3_256(key).digest()
bcrypt_salt = pyblake2.blake2s(data=site, key=b2salt, digest_size=16).digest()

# A cost of 16 for bcrypt takes a full 5+ seconds on my ThinkPad T61
result = bcrypt.hashpw(answer, "$2b$16${}".format(bcrypt_salt.encode('base64').strip()[:22]))

print("")
print("Enter this into your security question form: {}".format(result[30:]))
