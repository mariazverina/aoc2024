from collections import defaultdict

with open('day8.in', 'r') as f:
    lines = [line.strip() for line in f.readlines()]

Y = len(lines)
X = len(lines[0])
def antinodes(nodes):
    antinodes = []
    for n1 in nodes:
        for n2 in nodes:
            if n1 == n2:
                continue
            x1, y1 = n1
            x2, y2 = n2
            x1 -= (x2 - x1)
            x2 -= (y2 - y1)
            f = 0
            if x1 >= 0 and y1 >= 0 and x1 < X and y1 < Y:
                antinodes.append((x1, y1))
    return antinodes

def antinodes2(nodes):
    antinodes = []
    for n1 in nodes:
        for n2 in nodes:
            if n1 == n2:
                continue
            x1, y1 = n1
            x2, y2 = n2
            dx = (x2 - x1)
            dy = (y2 - y1)
            f = 0
            while True:
                nx = x1 - f * dx
                ny = y1 - f * dy
                if nx >= 0 and ny >= 0 and nx < X and ny < Y:
                    antinodes.append((nx, ny))
                else:
                    break
                f += 1
    return antinodes

nodes = defaultdict(list)
for y in range(Y):
    for x in range(X):
        if lines[y][x] != '.':
            nodes[lines[y][x]].append((x, y))

antis = set()
for label, locs in nodes.items():
    antis |= set(antinodes(locs))
print(len(antis))

antis = set()
for label, locs in nodes.items():
    aa = antinodes2(locs)
    antis |= set(aa)
print(len(antis))

