from collections import Counter

with open('day6.in', 'r') as f:
    lines = [line.strip() for line in f.readlines()]

# print(lines)
def print_grid():
    global lines
    list(map(lambda x:print(''.join(x)), lines))
    print('---')

X = len(lines[0])
Y = len(lines)

lines = list(map(list, lines))

start = (0, 0)
for y in range(Y):
    for x in range(X):
        if lines[y][x] == '^':
            start = (x, y)
            break

DIRECTIONS = [(0, -1), (1, 0), (0, 1), (-1, 0)]
dir = 0

def move(pos, dir):
    global DIRECTIONS
    global lines
    x, y = pos
    x = x + DIRECTIONS[dir][0]
    y = y + DIRECTIONS[dir][1]
    newpos = (x, y)
    if x < 0 or y < 0 or x == X or y == Y:
        return newpos, -1
    if lines[y][x] != '#':
        return newpos, dir
    dir = (dir + 1) % 4
    return move(pos, dir)

pos = start
x, y = pos
lines[y][x] = 'X'

while True:
    pos, dir = move(pos, dir)
    x, y = pos
    if dir == -1:
        break
    lines[y][x] = 'X'

# part 1
c = Counter(sum(lines, []))
print(c['X'])

# part 2

loops = 0

for y in range(Y):
    for x in range(X):
        if (x, y) == start or lines[y][x] == '#':
            continue
        lines[y][x] = '#'
        pos = start
        dir = 0
        visited = set()
        while True:
            pos, dir = move(pos, dir)
            if dir == -1:
                break
            if (pos, dir) in visited:
                loops += 1
                break
            else:
                visited.add((pos, dir))
        lines[y][x] = '.'
    print(y)

print(loops)