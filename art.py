#!/usr/bin/env python

import os
import os.path
import subprocess
import sys

try:
    keyfile = sys.argv[1]
except IndexError:
    print "Usage: keyart /path/to/exported-key"
    sys.exit(1)

if not os.path.isfile(keyfile):
    print "No such file or directory: {0}".format(keyfile)
    sys.exit(2)
elif not os.access(keyfile, os.R_OK):
    print "{0} is not readable. Check permissions.".format(keyfile)
    sys.exit(3)

gpg = subprocess.Popen(
    ('gpg','--with-fingerprint','--with-colons', keyfile),
    stdout=subprocess.PIPE)
out = gpg.communicate()

key_size = [i.strip() for i in out[0].split(':')][2]
key_algo = [i.strip() for i in out[0].split(':')][3]
key_fpr = [i.strip() for i in out[0].split(':')][19]

coin = ''
f_bytes = []
pos = 104
walk = [pos]
visits = [0]*209
coins = [' ','.','^',':','l','i','?','{','f','x','X','Z','#','M','W','&','8','%','@']

zfill = str.zfill

for c in key_fpr:
    f_bytes.append(zfill(bin(int(c,16))[2:],4)[:2]) # last 2 bits
    f_bytes.append(zfill(bin(int(c,16))[2:],4)[2:]) # first 2 bits

# I break from the OpenSSH implementation here. Rather than reading the
# bytes in little endian, the code is simpler reading in big endian. I
# don't see the point in complicating the code for little endian reading,
# when the fingerprint is SHA1 output, and should provide random output.
for d in f_bytes:
    if (20 <= pos <=  36 or  39 <= pos <=  55 or  58 <= pos <=  74 or
        77 <= pos <=  93 or  96 <= pos <= 112 or 115 <= pos <= 131 or
       134 <= pos <= 150 or 153 <= pos <= 169 or 172 <= pos <= 188):
        if   d == '00': pos -= 20 # Square 'M'
        elif d == '01': pos -= 18
        elif d == '10': pos += 18
        else: pos += 20
    elif 1 <= pos <= 17: # Square 'T'
        if   d == '00': pos -= 1
        elif d == '01': pos += 1
        elif d == '10': pos += 18
        else: pos += 20
    elif 191 <= pos <= 207: # Square 'B'
        if   d == '00': pos -= 20
        elif d == '01': pos -= 18
        elif d == '10': pos -= 1
        else: pos += 1
    elif pos in [19, 38, 57, 76, 95, 114, 133, 152, 171]: # Square 'L'
        if   d == '00': pos -= 19
        elif d == '01': pos -= 18
        elif d == '10': pos += 19
        else: pos += 20
    elif pos in [37, 56, 75, 94, 113, 132, 151, 170, 189]: # Square 'R'
        if   d == '00': pos -= 20
        elif d == '01': pos -= 19
        elif d == '10': pos += 18
        else: pos += 19
    elif pos == 0: # Square 'a'
        if   d == '01': pos += 1
        elif d == '10': pos += 19
        elif d == '11': pos += 20
    elif pos == 18: # Square 'b'
        if   d == '00': pos -= 1
        elif d == '10': pos += 18
        elif d == '11': pos += 19
    elif pos == 190: # Square 'c'
        if   d == '00': pos -= 19
        elif d == '01': pos -= 18
        elif d == '11': pos += 1
    else: # Square 'd'
        if   d == '00': pos -= 20
        elif d == '01': pos -= 19
        elif d == '10': pos -= 1
    walk.append(pos)

for w in walk:
    visits[w] += 1
    if visits[w] > 18: visits[w] = 18

# See https://tools.ietf.org/html/rfc4880#section-9.1
# Also https://tools.ietf.org/html/rfc6637#section4
if key_algo == '17':
    key_algo = 'DSA'
elif key_algo == '1' or key_algo == '2' or key_algo == '3':
    key_algo = 'RSA'
elif key_algo == '16' or key_algo == '20':
    key_algo = 'Elg'
elif key_algo == '18':
    key_algo = 'ECDH'
elif key_algo == '19':
    key_algo = 'ECDSA'
elif key_algo == '21':
    key_algo = 'X9.42'
else: key_algo = 'N/A'

if len("["+key_algo+" "+key_size+"]") == 10:
    print '+----[{0} {1}]-----+'.format(key_algo, key_size)
elif len("["+key_algo+" "+key_size+"]") == 11:
    print '+----[{0} {1}]----+'.format(key_algo, key_size)
elif len("["+key_algo+" "+key_size+"]") == 9:
    print '+-----[{0} {1}]-----+'.format(key_algo, key_size)
elif len("["+key_algo+" "+key_size+"]") == 12:
    print '+---[{0} {1}]----+'.format(key_algo, key_size)
elif len("["+key_algo+" "+key_size+"]") == 13:
    print '+---[{0} {1}]---+'.format(key_algo, key_size)
elif len("["+key_algo+" "+key_size+"]") == 14:
    print '+--[{0} {1}]---+'.format(key_algo, key_size)
elif len("["+key_algo+" "+key_size+"]") == 15:
    print '+--[{0} {1}]--+'.format(key_algo, key_size)
elif len("["+key_algo+" "+key_size+"]") == 16:
    print '+-[{0} {1}]--+'.format(key_algo, key_size)
elif len("["+key_algo+" "+key_size+"]") == 17:
    print '+-[{0} {1}]-+'.format(key_algo, key_size)
else:
    print '+-------------------+'

for i, v in enumerate(visits):
    coin += coins[v]
    if i % 19 == 0:
        coin = "|%s" % coin
    if i == 104:
        coin = "%sS" % coin[:10]
    if i == walk[len(walk)-1]:
        coin = "%sE" % coin[:len(coin)-1]
    if i % 19 == 18:
        print "%s|" % coin
        coin = ''
print '+----[{0}]-----+'.format(key_fpr[-8:])
