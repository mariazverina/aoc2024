import numpy as np
from collections import Counter

with open('day1a.in', 'r') as f:
    lines = [line.strip().split() for line in f.readlines()]

a1 = np.array(sorted([int(a) for a,b in lines]))
a2 = np.array(sorted([int(b) for a,b in lines]))
d = np.abs(a1 - a2)

# part 1
n = np.sum(d)
print(n)

# part 2
f = Counter(a2)
n = np.sum([x * f[x] for x in a1])
print(n)
