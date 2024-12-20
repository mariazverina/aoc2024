

with open('day11.in', 'r') as f:
    lines = [line.strip() for line in f.readlines()]

def xform(stone):
    if stone == 0:
        return [1]
    strstone = str(stone)
    l = len(strstone)
    if l % 2 == 0:
        return [int(strstone[:l//2]), int(strstone[l//2:])]
    return [stone * 2024]

xcache = {}
def xform2(stone):
    try:
        return xcache[stone]
    except KeyError:
        xcache[stone] = xform(stone)
        return xcache[stone]


def evolve(stones):
    # nl = []
    # for stone in stones:
    #     nl.append(xform(stone))
    return sum([xform2(stone) for stone in stones], [])

cache5 = {}
def evolve5(stones):
    key = ",".join(map(str,stones))
    if key in cache5:
        return cache5[key]
    for i in range(5):
        stones = evolve(stones)
    cache5[key] = stones
    return stones

evcache = {}

def cev (stone, n):
    try:
        return evcache[(stone, n)]
    except KeyError:
        evcache[(stone, n)] = ev(stone, n)
        return evcache[(stone, n)]

def ev(stone, n):
    if n == 0:
        return 1

    if stone == 0:
        return cev(1, n-1)

    strstone = str(stone)
    l = len(strstone)
    if l % 2 == 0:
        return cev(int(strstone[:l // 2]), n-1) + cev(int( strstone[l // 2:]), n-1)
    return cev(stone * 2024, n-1)

stones = list(map(int, lines[0].split(' ')))
print(stones)

# print(sum([len(cev(s, 25)) for s in stones]))

print(sum([cev(s, 75) for s in stones]))


# print(len(stones))