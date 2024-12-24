from functools import lru_cache

from utils import *

filename = __file__.split("/")[-1].split('.')[0]
with open(filename+'.in', 'r') as f:
    lines = [line.strip() for line in f.readlines()]

class Keypad:
    def __init__(self, layout):
        layout = layout.split("|")
        self.keymap = {(x, y) : layout[y][x] for y in range(len(layout)) for x in range(len(layout[y]))}
        self.invmap = {layout[y][x] : (x, y) for y in range(len(layout)) for x in range(len(layout[y]))}

    def curves(self, c, previous, evalfun=None):
        x, y = self.invmap[previous]
        tx, ty = self.invmap[c]
        vout = "^" * (y - ty) + "v" * (ty - y)
        hout = "<" * (x - tx) + ">" * (tx - x)
        vfirst = vout + hout + 'A'
        hfirst = hout + vout + 'A'

        if self.keymap[(tx, y)] == " ":
            return [vfirst]
        if self.keymap[(x, ty)] == " ":
            return [hfirst]
        return [vfirst, hfirst]

KEYNUM = Keypad("789|456|123| 0A")
KEYARR = Keypad(" ^A|<v>")

@lru_cache(maxsize=None)
def curvelen(s, n, keypad=KEYARR):
    if n == 0:
        return len(s)
    s = 'A'+s
    minlen = 0
    for i in range(1, len(s)):
        curves = keypad.curves(s[i], s[i-1])
        minlen += min([curvelen(c, n-1) for c in curves])
    return minlen

def solve(xform):
    global s, line
    s = 0
    for line in lines:
        ll = xform(line)
        # print(line, ll)
        s += int(line[:3]) * ll
    print("> S =", s)

print("Part 1")
solve(lambda line:curvelen(line, 3, KEYNUM))
print("Part 2")
solve(lambda line:curvelen(line, 26, KEYNUM))




