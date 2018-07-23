#!/usr/bin/python3
lfg = [n**2 % 5011 for n in range(128)]
j, k, m = 97, 127, 5000
for i in range(m):
    x = (lfg[j] + lfg[k]) % m
    lfg[k] = x
    j -= 1
    k -= 1
    if j == -1:
        j = 127
    if k == -1:
        k = 127
    print(x/5000)
