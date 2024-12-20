

with open('day9.in', 'r') as f:
    lines = [line.strip() for line in f.readlines()]

print(lines, len(lines[0]))

diskmap = lines[0]
space = []

fid = 0
flen = {}
findex = {}

for i in range(0, len(diskmap)):
    blocksize = int(diskmap[i])
    if i % 2 == 0:
        flen[fid] = blocksize
        findex[fid] = len(space)
        space += [fid] * blocksize
        fid += 1
    else:
        space += [-1] * blocksize

max_fid = fid - 1
backup_space  = list(space)
start = 0
end = len(space) - 1
print(flen, findex)

# defrag 1
while start < end:
    while space[start] != -1:
        start += 1
    while space[end] == -1:
        end -= 1
    if start < end:
        space[start], space[end] = space[end], space[start]
    # print(start, end, space)


def checksum(space):
    s = 0
    for i in range(len(space)):
        if space[i] >= 0:
            s += space[i] * i
    return s


def findfree(size):
    b = [-1] * size
    a = space
    for i in range(0, len(a) - len(b) + 1):
        if a[i:i + len(b)] == b:
            return i
    return None

s = checksum(space)
print(s)

# defreg 2
space = backup_space
for i in range(max_fid, 0, -1):
    siz = flen[i]
    newloc = findfree(siz)
    fpos = findex[i]
    if newloc is not None and fpos > newloc:
        space[newloc:newloc + siz], space[fpos:fpos + siz] = space[fpos:fpos + siz], space[newloc:newloc + siz]
    print(newloc, findex[i])

print(checksum(space))
# 00992111777.44.333....5555.6666.....8888..

# print(''.join(map(str, space)))
