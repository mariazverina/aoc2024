

with open('day10.in', 'r') as f:
    lines = [line.strip() for line in f.readlines()]

X = len(lines[0])
Y = len(lines)

def crawl(x, y, upto):
    if x < 0 or y < 0 or x >= X or y >= Y or int(lines[y][x]) != upto:
        return set()
    if lines[y][x] == '9':
        return set([(x, y)])
    return set.union(*[crawl(x+xd, y+yd, upto+1) for xd, yd in [(-1, 0), (1, 0), (0, -1), (0, 1)]])

def crawl2(x, y, upto):
    if x < 0 or y < 0 or x >= X or y >= Y or int(lines[y][x]) != upto:
        return 0
    if lines[y][x] == '9':
        return 1
    return sum([crawl2(x+xd, y+yd, upto+1) for xd, yd in [(-1, 0), (1, 0), (0, -1), (0, 1)]])

print(sum([len(crawl(x, y, 0)) for y in range(Y) for x in range(X)]))
print(sum([crawl2(x, y, 0) for y in range(Y) for x in range(X)]))
