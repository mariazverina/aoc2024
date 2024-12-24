from utils import *

filename = __file__.split("/")[-1].split('.')[0]
with open(filename+'.in', 'r') as f:
    lines = [line.strip() for line in f.readlines()]

split = lines.index('')
lines, ops = lines[:split], lines[split+1:]

inputs = {}
for line in lines:
    label, val = line.split(": ")
    inputs[label] = int(val)

def AND (a, b):
    return (a&b)&1

def OR (a, b):
    return (a|b)&1

def XOR (a, b):
    return (a^b)&1

OPS = {"AND" : AND, "OR" : OR, "XOR" : XOR}

# part 1

def simulate(vars, corrections):
    gates = {}
    thispass = ops
    while len(thispass):
        nextpass = []
        for line in thispass:
            a, op, b, _, var = line.split(" ")
            var = corrections[var] if var in corrections else var
            gates[var] = (a, op, b) if a < b else (b, op, a)
            try:
                vars[var] = OPS[op](vars[a], vars[b])
            except(KeyError):
                nextpass.append(line)
        thispass = nextpass
    return vars, gates

def xval(vars, prefix):
    zvals = sorted([k for k in vars.keys() if k[0] == prefix], reverse=True)
    zvals = ''.join([str(vars[v]) for v in zvals])
    return int(zvals, 2)

vars, gates = simulate(inputs.copy(), [])

x = xval(vars, 'x')
y = xval(vars, 'y')
z = xval(vars, 'z')

print("Part 1: Z =", z)

# part 2


print("X     = {:046b}".format(x))
print("Y     = {:046b}".format(y))
print("X + Y = {:046b}".format(x+y))
print("Z     = {:046b}".format(z))

zexp = x + y
zact = z

mismatched = []
for i in range(46):
    if zact >> i & 1 != zexp >> i & 1:
        mismatched.append(i)

print("Mismatched bits: ", mismatched)


def dumpcircuit():
    for i in range(45):
        zval = "z{:02d}".format(i)
        yval = "y{:02d}".format(i)
        xval = "z{:02d}".format(i)
        gate = gates[zval]
        if gate[1] != 'XOR':
            print("Broken line:", zval)
        try:
            left = gates[gate[0]]
            right = gates[gate[2]]
            if ''.join(sorted([left[1], right[1]])) != 'ORXOR' and i > 1:
                print("Bad ops", gate)
            # if right != (xval, 'XOR', yval) and left != (xval, 'XOR', yval):
            #     print("Broken line:", gate[2], gate[0])
            left, right = (left, right) if left < right else (right, left)
            print(zval, left, gate[1], right)
        except:
            print("key error")
            print(zval, gate)
    #     print(zval, expanded[zval])


dumpcircuit()
print("z == x + y", z == x + y)


corrections = {}
patch = "z05=frn gmq=z21 wnf=vtj wtt=z39"
for p in patch.split(" "):
    a, b = p.split("=")
    corrections[a] = b
    corrections[b] = a

vars, gates = simulate(inputs.copy(), corrections)
# vars, gates = simulate(inputs.copy(), [])

dumpcircuit()
z = xval(vars, 'z')
print("z == x + y", z == x + y)
print(','.join(sorted(corrections.keys())))

