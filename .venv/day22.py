from utils import *
from collections import defaultdict

filename = __file__.split("/")[-1].split('.')[0]
with open(filename+'.in', 'r') as f:
    lines = [int(line.strip()) for line in f.readlines()]

print(lines)

def rando(n):
    n = n ^ n << 6 & 0xFFFFFF
    n = n ^ n >> 5 & 0xFFFFFF
    n = n ^ n << 11 & 0xFFFFFF
    return n

def r2k(n):
    for i in range(2000):
        n = rando(n)
    return n

# part 1
print("part 1:", sum([r2k(n) for n in lines]))

# part 2
def genprices(secret):
    maxima = defaultdict(int)
    price = secret % 10
    window = [-99, -99, -99, -99]
    for i in range(2000):
        secret = rando(secret)
        newprice = secret % 10
        delta = newprice - price
        window.pop(0)
        window.append(delta)
        price = newprice
        if tuple(window) not in maxima:
            maxima[tuple(window)] = price
    return maxima

sums = defaultdict(int)

for n in lines:
    d = genprices(n)
    for k in d.keys():
        sums[k] += d[k]

maxbanana = max(sums.values())
print("part 2:", maxbanana)





