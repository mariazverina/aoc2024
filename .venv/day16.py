from utils import *
import sys

sys.setrecursionlimit(800)

with open('day16.in', 'r') as f:
    lines = [line.strip() for line in f.readlines()]

grid = list(map(list, lines))

MAXPATHSEARCH = 115500   # heuristic based on part 1

for y in range(len(grid)):
    for x in range(len(grid[0])):
        if grid[y][x] == 'S':
            _start = (x, y)

visited = {}
heading = 1
OFFSET = [(0, -1), (1, 0), (0, 1), (-1, 0)]

def mincost(start, heading, cost):
    if (start, heading) in visited and visited[(start, heading)] < cost :
        return None, None
    if cost > MAXPATHSEARCH:
        return None, None
    visited[(start, heading)] = cost
    sx, sy = start
    if grid[sy][sx] == '#':
        return None, None
    if grid[sy][sx] == 'E':
        return cost, set([start])
    minimum = 9999999

    paths = set()
    for i in range(4):
        if i == 2:
            continue
        h = (heading + i) % 4
        dx, dy = OFFSET[h]
        c, p = mincost((sx + dx, sy + dy), h, cost + (1 if i == 0 else 1001))
        if c is not None and c == minimum:
            paths |= p
        if c is not None and c < minimum:
            minimum = c
            paths = p

    paths.add(start)
    return minimum, paths

c, allcells = mincost(_start, 1, 0)

print(c)
print(len(allcells))


