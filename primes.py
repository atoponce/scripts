#!/usr/bin/python

import random
import sys
 
# how many bits?
k = 2048

# create an odd candidate securely
r = random.SystemRandom()
n = r.randrange(2**(k-1), 2**k)
if n % 2 == 0:
    n += 1

def sum_digits(n):
    s = 0
    while n:
        s += n % 10
        n /= 10
    return s
 
def miller_rabin(n):
    s = 0
    d = n-1
    while True:
        q, r = divmod(d, 2)
        if r == 1:
            break
        s += 1
        d = q
    assert(2**s * d == n-1)
 
    def is_composite(a):
        if pow(a, d, n) == 1:
            return False
        for i in range(s):
            if pow(a, 2**i * d, n) == n-1:
                return False
        return True
 
    for i in range(5):
        a = random.randrange(2, n)
        if is_composite(a):
            return False
 
    return True

count = 0
while True:
    count += 1
    sys.stdout.write('{0}\r'.format(count))
    sys.stdout.flush()

    if n % 5 == 0:
        n += 2
    if sum_digits(n) % 3 == 0:
        n += 2

    if miller_rabin(n):
        break

    n += 2

print
print n
