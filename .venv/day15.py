from utils import *
from time import sleep


def read_inputs():
    with open('day15.in', 'r') as f:
        lines = [line.strip() for line in f.readlines()]
    grid = []
    while lines[0] != '':
        grid.append(list(lines.pop(0)))
    lines.pop(0)
    moves = ''.join(lines)
    return grid, moves


def print_grid(grid, tag=None, move=None):
    if tag is not None:
        print(tag)
    for row in grid:
        r = ''.join(row)
        if move is not None:
            r = r.replace('@', move)
        print(r)
    print()

def gps(grid, chr):
    s = 0
    for y in range(len(grid)):
        for x in range(len(grid[0])):
            if grid[y][x] == chr:
                s += 100 * y + x
    return s


def xform(grid):
    simple2extended = dict(zip("# O . @".split(" "), "## [] .. @.".split(" ")))
    ng = [sum([list(simple2extended[s]) for s in line], []) for line in grid]
    return ng


def canmove(pos, grid, dir):
    n = [axis + offset for (axis, offset) in zip(pos, dir)]
    nx, ny = n
    if grid[ny][nx] == '#':
        return False
    if grid[ny][nx] == '.':
        return True
    if grid[ny][nx] == ']' and dir[1] != 0:
        return canmove(n, grid, dir) and canmove((nx - 1, ny), grid, dir)
    if grid[ny][nx] == '[' and dir[1] != 0:
        return canmove(n, grid, dir) and canmove((nx + 1, ny), grid, dir)
    return canmove(n, grid, dir)

def domove(pos, grid, dir):
    x, y = pos
    dx, dy = dir
    n = (x + dx, y + dy)
    nx, ny = n
    if grid[ny][nx] != '.':
        if grid[ny][nx] == ']' and dy != 0:
            domove((nx - 1, ny), grid, dir)
        if grid[ny][nx] == '[' and dy != 0:
            domove((nx + 1, ny), grid, dir)
        domove(n, grid, dir)
    grid[ny][nx], grid[y][x] = grid[y][x], grid[ny][nx]
    return n


def solve(chr, grid, moves):
    # find starting pos
    position = None
    for y in range(len(grid)):
        try:
            pos = grid[y].index('@')
            position = (pos, y)
            break
        except ValueError:
            continue

    # update grid for the moves
    dir2vec = dict(zip(list("<>^v"), [(-1, 0), (1, 0), (0, -1), (0, 1)]))
    for m in moves:
        dir = dir2vec[m]
        if canmove(position, grid, dir):
            position = domove(position, grid, dir)

    print(gps(grid, chr))

# setup
_grid, _moves = read_inputs()
xgrid = xform(_grid)

# part 1
solve('O', _grid, _moves)

# part 2
solve('[', xgrid, _moves)
