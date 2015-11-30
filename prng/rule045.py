#!/usr/bin/python

# 8-bit 1D elementary cellular automata Rule 45 PRNG
# Released to the public domain

import argparse

parser = argparse.ArgumentParser(description='Rule 45 PRNG')
parser.add_argument('seed', metavar='s', type=int, nargs=1, help='A seed to start the PRNG')
args = parser.parse_args()

s = int(args.seed[0])

bits = 8
s = bin(s)[2:].zfill(bits)
t = ''

for i in xrange(2**len(s)):
    print int(s, 2)
    for j, b in enumerate(xrange(len(s))):
        p, q, r = int(s[j-1]), int(s[j]), int(s[(j+1)%bits])
        rule = (1 + p + r + q * r) % 2
        t = "{0}{1}".format(t, rule)
    s = t
    t = ''
