#!/usr/bin/env python3

# From a Twitter discussion: https://twitter.com/Sc00bzT/status/1225304929293815808
# bcrypt still reigns supreme, despite scrypt and Argon2 existing
#
# If you prehash to address the 72 byte limit, you should salt your prehash.
# This is the way.
#
# Note: While passlib provides bcrypt_sha256 to address this problem, it does
# not salt the prehash. As such, is vulnerable to breach correlation attacks.
# https://passlib.readthedocs.io/en/stable/lib/passlib.hash.bcrypt_sha256.html#algorithm

from passlib.hash import bcrypt
from passlib.crypto import digest
from passlib.utils import b64encode

# any password. this one exceeds the 72 character limit for bcrypt
password = b"rIjbam-pysxih-disbac-jagwa4-bodnuk-megfuw-mitnax-xyszyh-sespar-donres-muvreq"

# first, you need a "pepper". it can be anything, and it can be static.
pepper = b"bcrypt"

# hash the pepper with SHA-256, to create a deterministic salt
salt = digest.hashlib.sha256()
salt.update(pepper)

# now hash a salted password
hashed = digest.hashlib.sha256()
hashed.update(salt.digest())
hashed.update(password)

# now base64 the result
password = b64encode(hashed.digest())

# now process with bcrypt
crypt = bcrypt.using(rounds=12).hash(password)

print(crypt)
