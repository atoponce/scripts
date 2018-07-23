#!/usr/bin/python3
import math
n, x, i = 0, 0, 5000
while n < i:
    x += math.sqrt(i)
    if x > i:
        x -= i
    print(x/i)
    n += 1
