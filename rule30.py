#!/usr/bin/python

# 8-bit 1D elementary cellular automata Rule 30 PRNG
# Released to the public domain

# seed
s = 180

s = bin(s)[2:].zfill(8)
t = ''

for i in xrange(8):
    print int(s, 2)
    for i, b in enumerate(xrange(8)):
        t = "{0}{1}".format(t, int(s[i-1]) ^ (int(s[i]) | int(s[(i+1)%8])))
    s = t
    t = ''
