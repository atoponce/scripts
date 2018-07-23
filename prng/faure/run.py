#!/usr/bin/python3
import numpy as np
def faure_permutation(base):
    if base == 2: return np.array([0,1])
    if (base % 2 == 0):
        return np.concatenate((2*faure_permutation(base/2), 2*faure_permutation(base/2)+1))
    else:
        k = int((base-1)/2)
        faure = faure_permutation(base-1)
        faure += np.array(faure>=k)
        return np.concatenate((faure[:k],[k],faure[k:]))

a = faure_permutation(5000)
for n in a:
    print(n/5000)
