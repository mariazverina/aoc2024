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

    def ncoded(self, s, n):
        for i in range(n):
            s = self.coded(s)
        return s

    def chain(self, nextkeypad):
        self.nextkeypad = nextkeypad
        self.nextkeypad.prevkeypad = self

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


# s = 0
# for line in lines:
#     out = kfinal.coded(line)
#     print(len(out), line)
#     s += int(line[:3]) * len(out)
# print("S = ", s)
# too low 183354
# too high 185176

# 980A: <v<A>>^AAAvA^A<vA<AA>>^AvAA<^A>A<v<A>A>^AAAvA<^A>A<vA>^A<A>A
# 179A: <v<A>>^A<vA<A>>^AAvAA<^A>A<v<A>>^AAvA^A<vA>^AA<A>A<v<A>A>^AAAvA<^A>A
# 456A: <v<A>>^AA<vA<A>>^AAvAA<^A>A<vA>^A<A>A<vA>^A<A>A<v<A>A>^AAvA<^A>A
# 379A: <v<A>>^AvA^A<vA<AA>>^AAvA<^A>AAvA^A<vA>^AA<A>A<v<A>A>^AAAvA<^A>A""".split('\n')
#
# for q in qq:
#     q = q.split(": ")
#     print(q[0], " => ", k1.move(q[1]))
#

kk = Keypad(" ^A,<v>")

kk1 = Keypad(" ^A,<v>")
kk2 = Keypad(" ^A,<v>")
kk1.chain(kk2)

# v<<A>^AAA>A<vAAA>^AvA<^A>A<vA>^A
D1 = {'^': '<A', 'A': 'A', '<': 'v<<A', 'v': '<vA', '>': 'vA'}
D2 = {'^^': 'A', '^A': '>A', '^<': 'v<A', '^v': 'vA', '^>': '>vA', 'A^': '<A', 'AA': 'A', 'A<': 'v<<A', 'Av': '<vA',
      'A>': 'vA', '<^': '>^A', '<A': '>>^A', '<<': 'A', '<v': '>A', '<>': '>>A', 'v^': '^A', 'vA': '>^A', 'v<': '<A',
      'vv': 'A', 'v>': '>A', '>^': '<^A', '>A': '^A', '><': '<<A', '>v': '<A', '>>': 'A'}

def v2code(q):
    global D1, D2
    out = D1[q[0]]
    for i in range(0, len(q) - 1):
        out += D2[q[i:i + 2]]
    return out

def n2code(q, n):
    for _ in range(n):
        q = v2code(q)
    return q

print("LONG")
k1.move('<vA<AA>>^AvA<^A>AAvA^Av<<A>>^AvA^A<vA>^Av<<A>>^AvA<^A>Av<<A>A>^AAvA<^A>A')
print("Short")
k1.move('<vA<AA>>^AvA<^A>AAvA^Av<<A>>^AvA^Av<<A>A>^AvA^A<A>Av<<A>A>^AAvA<^A>A')


fastcache = {}
def fastcode(s):
    out = ""
    s = s.split("A")
    s.pop() # s is A terminated .. final chunk is a split artefact
    for chunk in s:
        chunk += 'A'
        if chunk not in fastcache:
            fastcache[chunk] = v2code(chunk)
        out += fastcache[chunk]
    return out

cache = {}
def n5code(s):
    if s not in cache:
        cache[s] = n2code(s, 5)
    return cache[s]

lencache = {}
def len5code(q, n):
    q = n5code(q)
    if n == 5:
        return len(q)
    s = 0
    qs = q.split('A')
    qs.pop() # q is A terminated .. final chunk is a split artefact
    for c in qs:
        c += 'A'
        if (c, n) not in lencache:
            lencache[(c, n)] = len5code(c, n-5)
        s += lencache[(c, n)]

    return s

qlencache = {}
def qlencode(q, n):
    q = fastcode(q)
    if n == 1:
        return len(q)
    s = 0
    qs = q.split('A')
    qs.pop() # q is A terminated .. final chunk is a split artefact
    for c in qs:
        c += 'A'
        if (c, n) not in qlencache:
            qlencache[(c, n)] =  qlencode(c, n-1)
        s += qlencache[(c, n)]
    return s

# print("N = ",qlencode('<^^A^Av>AvvA', 15))

def eval_lines(niter):
    knum = Keypad("789,456,123, 0A")
    s = 0
    outcomes = []
    for line in lines:
        out = knum.coded2(line, lambda x: qlencode(x, niter))
        outcomes.append(out)
        print(line, out)
        s += int(line[:3]) * out[1]
        # print(k1.move(out))
        # print(out)
    print("S = ", s)
    return outcomes

def eval5_lines(niter):
    knum = Keypad("789,456,123, 0A")
    s = 0
    outcomes = []
    for line in lines:
        out = knum.coded2(line, lambda x: len5code(x, niter))
        outcomes.append(out)
        print(line, out)
        s += int(line[:3]) * out[1]
        # print(k1.move(out))
        # print(out)
    print("S = ", s)
    return outcomes

qq = eval_lines(2)
qq = eval5_lines(25)
# 262412889851360 too high
# 228800606998554
print("part 2",qq)

print("QQ:", len5code('<^^^AvvvA>^AvA', 25))

print("N = ",len5code('<^^A^Av>AvvA', 20))

print("sanity check")
# qq = eval_lines(5)
# qq = eval5_lines(25)

qq = eval_lines(25)
print(qq)
# qq = eval5_lines(3)
# print(qq)
