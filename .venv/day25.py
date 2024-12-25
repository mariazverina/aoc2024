from utils import *

filename = __file__.split("/")[-1].split('.')[0]
with open(filename+'.in', 'r') as f:
    lines = [line.strip() for line in f.readlines() if len(line)>1]

keylocks = list(zip(*([iter(lines)] * 7))) # groups into groups of 7

keys, locks = [], []
for key in keylocks:
    key = list(zip(*key)) # transpose
    combo = [len(''.join(line).strip('.'))-1 for line in key] # flip into num vector
    (locks if key[0][0] == '#' else keys).append(combo)

n = sum([max([x + y for x, y in zip(k, l)]) <= 5 for l in locks for k in keys])
print(n)



