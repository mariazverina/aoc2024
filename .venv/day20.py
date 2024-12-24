from numpy.f2py.crackfortran import endifs
from utils import *

filename = __file__.split("/")[-1].split('.')[0]
with open(filename+'.in', 'r') as f:
    lines = [line.strip() for line in f.readlines()]

print(lines)

distance = {}
XX = len(lines[0])
YY = len(lines)
for y in range(YY):
    for x in range(XX):
        if lines[y][x] == 'S':
            start = (x, y)
        if lines[y][x] == 'E':
            end = (x, y)
        if lines[y][x] != '#':
            distance[(x, y)] = -1

OFFSET = [(1,0), (-1,0), (0,1), (0,-1)]

pos = end
dist = 0
distance[end] = 0
while pos != start and dist < 10000:
    dist += 1
    px, py = pos
    neighbours = [(px+ox, py+oy) for ox,oy in OFFSET]
    for n in neighbours:
        if n in distance and distance[n] == -1:
            distance[n] = dist
            pos = n

# print(distance[(1,3)])

cheats = {}
npowerful = 0
for k in distance.keys():
    px, py = k
    for n in [(px+ox*2, py+oy*2) for ox,oy in OFFSET]:
        if n in distance and distance[n] < distance[k]:
            d = distance[k] - distance[n] - 2
            if d >= 100:
                print(k, n)
                npowerful += 1
            cheats[(k, n)] = d

print("np", npowerful)

cheats = {}
npowerful = 0
# print("d",distance[(7,1)],distance[(5,7)])

for p in distance.keys():
    px, py = p
    for n in distance.keys():
        nx, ny = n
        cdist = abs(nx - px) + abs(ny - py)
        if cdist > 20:
            continue
        if n in distance and distance[n] < distance[p]:
            d = distance[p] - distance[n] - cdist
            if d >= 100:
                npowerful += 1
            cheats[(k, n)] = d
            if npowerful % 10000 == 1:
                print(npowerful)

# print(cheats)
# print("d",distance[(7,1)],distance[(9,1)])
# print(cheats[((7,1),(5,7))])
print(len(distance))
print("np", npowerful)







