from utils import *
from collections import *
import re

with open('day14.in', 'r') as f:
    lines = [line.strip() for line in f.readlines()]

GH = 103
GW = 101

print(lines)

def forward(n):
    newpos = []
    for line in lines:
        m = list(map(int, re.match(r'p=(\d+),(\d+) v=(-?\d+),(-?\d+)', line).groups()))
        x, y, vx, vy = m
        np = (x + n * vx) % GW, (y + n * vy) % GH
        newpos.append(np)
    return newpos

def quadrant(x,y):
    q = 0
    if y == GH // 2 or x == GW // 2:
        return None
    if y > GH // 2:
        q += 2
    if x > GW // 2:
        q += 1
    return q

def safety_factor(newpos):
    p = 1
    c = Counter(newpos)
    qs = defaultdict(int)
    for k, v in c.items():
        qs[quadrant(*k)] += v
    # print(c)
    for i in range(4):
        p *= qs[i]
    # print(qs)
    return p

def uniq(newpos):
    c = Counter(newpos)
    for n in c.values():
        if n > 1:
            return False
    return True

newpos = forward(100)
p = safety_factor(newpos)

def render(newpos):
    lls = [[" " for _ in range(GW)] for _ in range(GH)]
    for x, y in newpos:
        lls[y][x] = 'X'

    [print(''.join(l)) for l in lls]

magic = []
for i in range(10403):
    newpos = forward(i)
    if(uniq(newpos)):
        print(i)
        magic.append(i)

for i in magic:
    newpos = forward(i)
    render(newpos)
    print(i)