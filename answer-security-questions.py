#!/usr/bin/python

# Released to the public domain.

# Designed for answering security questions deterministically, while
# guaranteeing a minimum security margin to prevent anyone who knows the actual
# answer from compromising an account.

# SHA-3 is based on Keccak which uses the sponge construction
# bcrypt is based on Blowfish which uses the feistel construction
# BLAKE2 is based on ChaCha and uses the HAIFA construction

from Cryptodome.Hash import BLAKE2b
from Cryptodome.Hash import SHAKE256
from Cryptodome.Protocol.KDF import scrypt

print("Answers are case-sensitive.")
site = raw_input("What site is this for? Root domain and TLD only (E.G.: example.com) ")
key = raw_input("What is a secret key with at least 128-bits entropy only you know? ")
answer = raw_input("What is the answer to the security question? ")

shake = SHAKE256.new()
secret = shake.update(bytes(key)).read(32)
salt = BLAKE2b.new(digest_bits=256, key=(secret))
salt.update(bytes(site))

# A cost of 32 MiB of RAM and 5+ seconds computation
crypt = scrypt(bytes(answer), salt.digest(), 16, 2**15, 8, 1)

print("")
print("Enter this into your security question form: {}".format(crypt.encode('hex')))
