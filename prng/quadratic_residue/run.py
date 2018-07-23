#!/usr/bin/python3
p = 5011 # our prime
n, i = 0, 5000
while n < p:
    if n <= p/2:
        print((n**2 % p)/i)
    else:
        print((p - n**2 % p)/i)
    n+=1
