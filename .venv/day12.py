from utils import *
from collections import defaultdict

with open('day12.in', 'r') as f:
    lines = [line.strip() for line in f.readlines()]

print(lines)
lines = sentinels(lines, '.')

def neighbours(x, y):
    ix = [(x+1, y), (x-1, y), (x, y-1), (x, y+1)]
    return [lines[y][x] for x, y in ix]

X = len(lines[0])
Y = len(lines)

visited = set()

def crawl(c, x, y):
    if (x, y) in visited:
        return (c, 0, 0)
    visited.add((x, y))
    ix = [(x+1, y), (x-1, y), (x, y-1), (x, y+1)]
    c = lines[y][x]
    p = 0
    a = 1
    for xx, yy in ix:
        if lines[yy][xx] == c:
            _, aa, pp = crawl(c, xx, yy)
            p += pp
            a += aa
        else:
            p += 1

    ns = neighbours(x, y)
    n = sum([1 if n != c else 0 for n in ns])
    return (c, a, p)

def crawl2(c, x, y):
    if (x, y) in visited:
        return (c, 0, 0)
    visited.add((x, y))
    ix = [(x+1, y), (x-1, y), (x, y-1), (x, y+1)]
    c = lines[y][x]
    p = 0
    a = 1
    for xx, yy in ix:
        if lines[yy][xx] == c:
            _, aa, pp = crawl2(c, xx, yy)
            p += pp
            a += aa
        else:
            p += 1

    if lines[y][x] == c and lines[y][x-1] == c and lines[y-1][x] != c and lines[y-1][x-1] != c:
        p -= 1
    if lines[y][x] == c and lines[y][x-1] == c and lines[y+1][x] != c and lines[y+1][x-1] != c:
        p -= 1
    if lines[y][x] == c and lines[y-1][x] == c and lines[y][x-1] != c and lines[y-1][x-1] != c:
        p -= 1
    if lines[y][x] == c and lines[y-1][x] == c and lines[y][x+1] != c and lines[y-1][x+1] != c:
        p -= 1

    return (c, a, p)

regions = []

for x in range(1, X-1):
    for y in range(1, Y-1):
        if (x, y) in visited:
            continue
        c = lines[y][x]
        regions.append(crawl(c, x, y))



print(regions)
print(sum([a * b for _, a, b in regions]))

visited = set()
regions = []
for x in range(1, X-1):
    for y in range(1, Y-1):
        if (x, y) in visited:
            continue
        c = lines[y][x]
        regions.append(crawl2(c, x, y))

print(regions)
print(sum([a * b for _, a, b in regions]))
