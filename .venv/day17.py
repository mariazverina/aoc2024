from utils import *

with open('day17.in', 'r') as f:
    lines = [line.strip() for line in f.readlines()]


a = int(lines[0].split(': ')[1])
b = int(lines[1].split(': ')[1])
c = int(lines[2].split(': ')[1])
prog = lines[4].split(': ')[1]

buf = []
ip = 0

def adv(val):
    global a, b, c, ip
    a //= (2 ** val)

def bxl(val):
    global a, b, c, ip
    b ^= val

def bst(val):
    global a, b, c, ip
    b = val & 0x7

def jnz(val):
    global a, b, c, ip
    if a != 0:
        ip = val - 2

def bxc(val):
    global a, b, c, ip
    b ^= c

def bdv(val):
    global a, b, c, ip
    b = a // (2 ** val)

def cdv(val):
    global a, b, c, ip
    c = a // (2 ** val)

def out(val):
    global a, b, c, ip
    buf.append(val&0x7)

def cval(v):
    global a, b, c, ip
    if v < 4:
        return v
    if v == 4:
        return a
    if v == 5:
        return b
    if v == 6:
        return c
    sys.exit("unknown literal")

ops = [adv, bxl, bst, jnz, bxc, out, bdv, cdv]

prog = list(map(int, prog.split(',')))

def run(ia = None):
    global a, b, c, ip, buf
    if ia is not None:
        a = ia
    b = 0
    c = 0
    buf = []
    ip = 0
    while ip < len(prog):
        opcode = prog[ip]
        val = prog[ip + 1]
        if opcode != 1 and opcode != 3:
            xval = cval(val)
        else:
            xval = val

        ops[opcode](xval)
        ip += 2
    return buf


# run()
# print(','.join(map(str, buf)))
# part 1
print("Part 1: ",','.join(map(str, run())))

def fn(k):
    foo = (k & 7) ^ 5
    bar = (k >> foo) ^ 6
    v = (foo ^ bar) & 7
    k = k >> 3
    return k, v

pp = list(prog)

def unfuck(k, pp):
    if len(pp) == 0:
        return k
    target = pp[-1]
    k *= 8
    for i in range(8):
        _, val = fn( k + i )
        if val == target:
            r = unfuck( k + i, pp[:-1])
            if r is not None:
                return r

    return None

print("Part 2: ", unfuck(0, pp))
print(prog)
fail('fisk')
run(136904920099226)
print(buf)
