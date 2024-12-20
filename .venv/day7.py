import operator

with open('day7.in', 'r') as f:
    lines = [line.strip().split(": ") for line in f.readlines()]

lines =[(int(s), list(map(int, f.split(" ")))) for s, f in lines]

def reachable(goal, partial, ns, fs):
    if ns == []:
        return goal == partial
    nss = ns[1:]
    return any([reachable(goal, f(partial, ns[0]), nss, fs) for f in fs])

def conc(a, b):
    return int(str(a) + str(b))

fs = [operator.add, operator.mul]
print(sum([s for s,ns in lines if reachable(s, ns[0], ns[1:], fs)]))

fs.append(conc)
print(sum([s for s,ns in lines if reachable(s, ns[0], ns[1:], fs)]))

