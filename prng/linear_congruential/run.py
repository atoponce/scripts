#!/usr/bin/python3
x, a, c, m = 0, 4961, 4999, 5000
for i in range(m+1):
    x = (a*x + c) % m
    print(x/m)
