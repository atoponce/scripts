#!/usr/bin/python

import re
import hashlib

counter = 8701226685
pattern = re.compile(r'^0+e\d+$')

while True:
    hash_obj = hashlib.md5(str(counter))
    hash_hex = hash_obj.hexdigest()
    if pattern.search(hash_hex):
        print("|MD5|{}|{}|".format(counter, hash_hex))
    counter += 1
