from utils import *

with open('day19.in', 'r') as f:
    lines = [line.strip() for line in f.readlines()]

colours = lines.pop(0).split(", ")
lines.pop(0)

def arrangable(pattern, towels):
    if pattern == "":
        return True
    for t in towels:
        lt = len(t)
        if pattern[:lt] == t and arrangable(pattern[lt:], towels):
            return True
    return False

cache = {}
def permutations(pattern, towels):
    if pattern in cache:
        return cache[pattern]
    if pattern == "":
        return 1
    perms = 0
    for t in towels:
        lt = len(t)
        if pattern[:lt] == t:
            perms += permutations(pattern[lt:], towels)
    cache[pattern] = perms
    return perms

print(lines)
print(colours)

permutations('gbbr', colours)
# print(arrangable("bwurrg", colours))
# for line in lines:
#     if(arrangable(line, colours)):
#         print(line)

print(sum([1 for line in lines if arrangable(line, colours)]))
for line in lines:
    print(line)
    print(line, permutations(line, colours))

print(sum([permutations(line, colours) for line in lines]))
