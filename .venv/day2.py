import numpy as np

with open('day2.in', 'r') as f:
    lines = [np.array(list(map(int, line.strip().split(" ")))) for line in f.readlines()]

print(lines)

def safe(diffs):
    min_diff = min(diffs)
    max_diff = max(diffs)
    if min_diff >= -3 and max_diff <= -1:
        return True
    if max_diff <= 3 and min_diff >= 1:
        return True
    return False

SAFE = [-3, -2, -1, 1, 2, 3]

def safe2(diffs):
    if safe(diffs):
        return True
    for i in range(0, len(diffs) - 1):
        if safe(np.concatenate([diffs[:i], [diffs[i] + diffs[i+1]], diffs[i+2:]])):
            return True
    return safe(diffs[:-1]) or safe(diffs[1:])



delta  = [a[1:] - a[:-1] for a in lines]
print(delta)
print(sum(map(safe, delta)))
s1 = list(map(safe, delta))

s2 = list(map(safe2, delta))

for i in range(len(s1)):
    if s1[i] != s2[i]:
        print(i, lines[i], s1[i], s2[i])
print(sum(map(safe2, delta)))