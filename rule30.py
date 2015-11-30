#!/usr/bin/python

# 8-bit 1D elementary cellular automata Rule 30 PRNG
# Period lengths:
#   * 8-bit: 56 (59, 103, 118, 157, 179, 206, 217, 236)
#   * 9-bit: 67 (115)
#   * 10-bit: 186 (357)
#   * 11-bit: 296 (1245)
#   * 12-bit: 255 (1480)
#   * 13-bit: 394 (894)
# Released to the public domain

import argparse

parser = argparse.ArgumentParser(description='Rule 30 PRNG')
parser.add_argument('-s','--seed',help='Initial seed')
args = parser.parse_args()

# seed
if args.seed:
    s = int(args.seed)


s = bin(s)[2:].zfill(13)
t = ''

for i in xrange(2**len(s)):
    print int(s, 2)
    for i, b in enumerate(xrange(len(s))):
        t = "{0}{1}".format(t, int(s[i-1]) ^ (int(s[i]) | int(s[(i+1)%8])))
    s = t
    t = ''
