from functools import lru_cache

from utils import *

filename = __file__.split("/")[-1].split('.')[0]
with open(filename+'.in', 'r') as f:
    lines = [line.strip() for line in f.readlines()]

print(lines)

class Keypad:
    OFFSET = dict(zip("<>^v", [(-1, 0), (1, 0), (0, -1), (0, 1)]))
    def __init__(self, layout):
        layout = layout.split(",")
        self.keymap = {}
        self.invmap = {}
        self.nextkeypad = None
        self.prevkeypad = None
        self.cache = {}
        self.apos = None
        for y in range(len(layout)):
            for x in range(len(layout[y])):
                c = layout[y][x]
                self.keymap[(x, y)] = c
                self.invmap[c] = (x, y)
                if c == 'A':
                    self.apos = (x, y)
                    self.x = x
                    self.y = y
        # print("init", self.x, self.y, self.keymap, )

    # Move:  v<<A>>^A<A>AvA<^AA>A<vAAA>^A
    # Move:  <A^A>^^AvvvA
    # Move:  083A
    def move(self, codes, abort=True):
        outbuf = ''
        for c in codes:
            if c == 'A':
                outbuf += self.keymap[(self.x, self.y)]
            else:
                ox, oy = Keypad.OFFSET[c]
                self.x += ox
                self.y += oy
                if self.keymap[(self.x, self.y)] == " " and abort:
                    print("codes", codes)
                    print("outbuf", outbuf)
                    fail("movement over space")

        print("Move: ", outbuf)
        if self.nextkeypad:
            return self.nextkeypad.move(outbuf)
        return outbuf

    def coded(self, output):
        # print("coded:", output)
        x, y = self.x, self.y
        if (x,y) != self.apos:
            fail("unexpected start")
        if output in self.cache:
            return self.cache[output]
        out = ""
        for c in output:
            tx, ty = self.invmap[c]
            vout, hout = "", ""
            if ty < y:
                vout = "^" * (y - ty)
            if ty > y:
                vout = "v" * (ty - y)
            if tx < x:
                hout = "<" * (x - tx)
            if tx > x:
                hout = ">" * (tx - x)

            if self.prevkeypad:
                vfirst = self.prevkeypad.coded(vout + hout + 'A')
                hfirst = self.prevkeypad.coded(hout + vout + 'A')
                if len(vfirst) <  len(hfirst):
                    outline = vfirst
                else:
                    outline = hfirst
                if  self.keymap[(tx, y)] == " ":
                    outline = vfirst
                if self.keymap[(x, ty)] == " ":
                    outline = hfirst
                out += outline
            else:
                if self.keymap[(tx, y)] == " " or len(self.keymap) > 6:
                    out += vout + hout + 'A'
                else:
                    out += hout + vout + 'A'
            x = tx
            y = ty

        # print("code", out)
        self.cache[output] = out
        return out

    def coded2(self, output, evalfun=None):
        # print("coded:", output)
        x, y = self.x, self.y
        if (x,y) != self.apos:
            fail("unexpected start")
        out = ""
        tlen = 0
        for c in output:
            tx, ty = self.invmap[c]
            vout, hout = "", ""
            if ty < y:
                vout = "^" * (y - ty)
            if ty > y:
                vout = "v" * (ty - y)
            if tx < x:
                hout = "<" * (x - tx)
            if tx > x:
                hout = ">" * (tx - x)

            vfirst = vout + hout + 'A'
            hfirst = hout + vout + 'A'
            vlen = evalfun(vfirst)
            hlen = evalfun(hfirst)
            if vlen < hlen:
                outline = vfirst
                addlen = vlen
            else:
                outline = hfirst
                addlen = hlen
            if  self.keymap[(tx, y)] == " ":
                outline = vfirst
                addlen = vlen
            if self.keymap[(x, ty)] == " ":
                outline = hfirst
                addlen = hlen
            out += outline
            tlen += addlen
            x = tx
            y = ty

        # print("code", out)
        return out, tlen

    def curves(self, c, previous, evalfun=None):
        # print("coded:", output)

        x, y = self.invmap[previous]
        tx, ty = self.invmap[c]
        vout, hout = "", ""
        if ty < y:
            vout = "^" * (y - ty)
        if ty > y:
            vout = "v" * (ty - y)
        if tx < x:
            hout = "<" * (x - tx)
        if tx > x:
            hout = ">" * (tx - x)

        vfirst = vout + hout + 'A'
        hfirst = hout + vout + 'A'

        if self.keymap[(tx, y)] == " ":
            return [vfirst]
        if self.keymap[(x, ty)] == " ":
            return [hfirst]
        if len(vout) == 0 or len(hout) == 0:
            return [hfirst]

        return [vfirst, hfirst]

    def ncoded(self, s, n):
        for i in range(n):
            s = self.coded(s)
        return s

    def chain(self, nextkeypad):
        self.nextkeypad = nextkeypad
        self.nextkeypad.prevkeypad = self

KEYNUM = Keypad("789,456,123, 0A")
KEYARR = Keypad(" ^A,<v>")

def genarrcurve(c, p):
    return KEYARR.curves(c, p)

def gennumcurve(c, p):
    return KEYNUM.curves(c, p)

@lru_cache(maxsize=None)
def curvelen(s, n, curvgen=genarrcurve):
    if n == 0:
        return len(s)
    s = 'A'+s
    minlen = 0
    for i in range(1, len(s)):
        curves = curvgen(s[i], s[i-1])
        minlen += min([curvelen(c, n-1) for c in curves])

    return minlen


s1 = "<vA<AA>>^AvAA<^A>A<v<A>>^AvA^A<vA>^A<v<A>^A>AAvA^A<v<A>A>^AAAvA<^A>A"

k1 = Keypad(" ^A,<v>")
k2 = Keypad(" ^A,<v>")
k3 = Keypad("789,456,123, 0A")



k1.chain(k2)
k2.chain(k3)
# k1.move(s1)

# kx = Keypad("789,456,123, 0A")
# print(kx.coded('341A'))
# ss = k3.coded('1A')
# print(ss)
# print(k1.move(ss))


s = 0
for line in lines:
    out = k3.coded(line)
    print(len(out), line, out)
    s += int(line[:3]) * len(out)
    # print(k1.move(out))
    # print(out)
print("S = ", s)



kk = Keypad(" ^A,<v>")

kk1 = Keypad(" ^A,<v>")
kk2 = Keypad(" ^A,<v>")
kk1.chain(kk2)

s = 0
for line in lines:
    ll = curvelen(line, 26, gennumcurve)
    print(line, ll)
    s += int(line[:3]) * ll

print("Part 2: S =", s)

