#!/usr/bin/python
#
# Author: Aaron Toponce
# Date: Mar 25, 2013
# License: Public domain
#
# Blum Blum Shub in Python
#
# Very, very, very slow Python implementation of Blum Blum Shub in Python.
# Just wanted to see how slow it truly was (doesn't help that my primes
# have hundreds of thousands of digits- heh).

m=(2**13466917-1)*(2**20996011-1) # large known merseene primes
xi=2**24036583-1

def rng():
    global xi
    xi = (xi * xi) % m
    return xi

for i in xrange(10):
    print rng()
