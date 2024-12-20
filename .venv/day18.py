from utils import *
import sys

with open('day18.in', 'r') as f:
    lines = [tuple(map(int, line.strip().split(","))) for line in f.readlines()]

OFFSETS = [(1,0), (-1,0), (0,1), (0,-1)]
def neighbours(p):
    px, py = p
    ns = [(px + ox, py + oy) for ox, oy in OFFSETS]
    ns = [(x, y) for x,y in ns if x >= 0 and x < SIZE and y >= 0 and y < SIZE]
    return ns


def solve(grid):
    cost = {}
    contour_cost = 0
    contour = [(70,70)]
    while len(contour) > 0:
        nn = set()
        for p in contour:
            if p == (0,0):
                return contour_cost
            px, py = p
            if p not in cost:
                if grid[py][px] != '#':
                    cost[p] = contour_cost
                    nn |= set(neighbours(p))
                else:
                    cost[p] = 9999
        contour = nn
        contour_cost += 1
    return 9999

SIZE = 71

def mkgrid(time):
    grid = [['.' for x in range(SIZE)] for y in range(SIZE)]
    for i in range(time):
        x, y = lines[i]
        grid[y][x] = '#'
    return grid

grid = mkgrid(1024)
print("cost =", solve(grid))

for i in range(1024):
    x, y = lines[i]
    grid[y][x] = '#'

lo = 1024
hi = SIZE ** 2

while hi - lo > 1:
    mid = (lo + hi + 1) // 2
    grid = mkgrid(mid)
    c = solve(grid)
    if c == 9999:
        hi = mid
    else:
        lo = mid

i = lo
x, y = lines[i]

print("{0}: {1},{2}".format(i, x, y))

