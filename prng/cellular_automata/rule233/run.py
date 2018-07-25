#!/usr/bin/python3

seed = '00000000000000000100000000000000000' # textbook initial state
bits = len(seed)

for n in range(5000):
    state = ''
    p, q, r = -1, 0, 1
    for n in range(bits): # there must be a more efficient way to do this
        state += str(int(seed[p]) ^ (int(seed[q]) | int(seed[r]))) # rule 30
        p = (p + 1) % bits
        q = (q + 1) % bits
        r = (r + 1) % bits
    seed = state
    print(int(seed, 2)/2**bits)
