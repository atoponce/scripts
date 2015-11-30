#!/usr/bin/python

# 8-bit xorshift prng
# released to the public domain

x = 21
y = 229
z = 181
w = 51

for i in xrange(10):
    t = x ^ (x << 3) & 0xff
    x = y
    y = z
    z = w
    w = w ^ (w >> 5) ^ t ^ (t >> 2)
    print w
