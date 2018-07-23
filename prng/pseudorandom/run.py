#!/usr/bin/python3
import random, math

random.seed(2)
with open("seed2-sequence.txt", "w") as f:
    a = [random.random() for i in range(5001)]
    for n in a:
        f.write("{}\n".format(n))

random.seed(3)
with open("seed3-sequence.txt", "w") as f:
    a = [random.random() for i in range(5001)]
    for n in a:
        f.write("{}\n".format(n))
