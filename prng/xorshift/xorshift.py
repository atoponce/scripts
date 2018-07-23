#!/usr/bin/python

# 128-bit xorshift prng
# released to the public domain

x = 123456789
y = 362436069
z = 521288629
w = 88675123

for i in xrange(10):
    t = x ^ (x << 11) & 0xff
    x = y
    y = z
    z = w
    w = w ^ (w >> 19) ^ t ^ (t >> 8)
    print w
