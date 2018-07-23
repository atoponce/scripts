#!/usr/bin/python3
import math
def halton(n, base=2):
    f, r = 1, 0
    while n:
        f /= base
        r += f * (n % base)
        n = math.floor(n/base)
    return r

for n in [halton(i, 3) for i in range(1001)]:
    print(n,)
