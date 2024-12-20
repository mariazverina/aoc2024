from utils import *
import re

def parse_games(lines):
    games = []
    while lines:
        a, b, r, _, *lines = lines
        m = re.match(r'Button A: X.(\d*), Y.(\d*)', a)
        a = (tuple(int(n) for n in m.groups()))
        m = re.match(r'Button B: X.(\d*), Y.(\d*)', b)
        b = (tuple(int(n) for n in m.groups()))
        m = re.match(r'Prize: X.(\d*), Y.(\d*)', r)
        r = (tuple(int(n) for n in m.groups()))
        games.append((a, b, r))
    return games




def mincost2(g, offset):
    a, b, r = g
    ax, ay = a
    bx, by = b
    rx, ry = r
    rx += offset
    ry += offset

    if ax * by == ay * bx:
        print("Underspecified equation")
        return 0

    j = (ay * rx - ry * ax) // (bx * ay - by * ax)
    i = (rx - bx * j) // ax

    if ax * i + bx * j == rx and ay * i + by * j == ry:
        return i * 3 + j
    return 0


with open('day13.in', 'r') as f:
    _lines = [line.strip() for line in f.readlines()]

games = parse_games(_lines)
print(sum([mincost2(g, 0) for g in games]))
print(sum([mincost2(g, 10000000000000) for g in games]))