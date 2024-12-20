

with open('day4.in', 'r') as f:
    lines = [line.strip() for line in f.readlines()]


def transpose(m):
    return [''.join(l) for l in zip(*m)]

def diag(m):
    l = len(m)
    d = []
    for i in range(l):
        d.append(" " * i + m[i] + " " * (l - i))
    return d

def cxmas(m, sub):
    return sum([s.count(sub) for s in m])

# part 1
horizontal = lines
vertical = transpose(lines)
negdiag = transpose(diag(lines))
posdiag = transpose(list(reversed(diag(list(reversed(lines))))))

ms = [horizontal, vertical, negdiag, posdiag]
print(sum([cxmas(m, 'XMAS') + cxmas(m, 'SAMX') for m in ms]))

# part 2
c = 0
for y in range(1,len(lines) - 1):
    for x in range(1, len(lines[y]) - 1):
        if lines[y][x] != "A":
            continue
        d1 = ''.join(sorted(lines[y-1][x-1] + lines[y+1][x+1]))
        d2 = ''.join(sorted(lines[y+1][x-1] + lines[y-1][x+1]))
        if d1 == "MS" and d2 == "MS":
            c += 1

print(c)


