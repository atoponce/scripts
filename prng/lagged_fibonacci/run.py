#!/usr/bin/python3
lfg = [n*41 for n in range(128)]
j, k, m = 97, 127, 5000
for i in range(m+1):
    x = (lfg[j] + lfg[k]) % m
    lfg.insert(0, x)
    lfg.pop()
    print(x/5000)
