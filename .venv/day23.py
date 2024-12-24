from utils import *
from collections import defaultdict

filename = __file__.split("/")[-1].split('.')[0]
with open(filename+'.in', 'r') as f:
    lines = [line.strip().split('-') for line in f.readlines()]

connections = defaultdict(set)

for n1, n2 in lines:
    connections[n1].add(n2)
    connections[n2].add(n1)

# part 1
triples = set()
for n1 in connections.keys():
    for n2 in connections[n1]:
        for n3 in connections[n1] | connections[n2]:
            triple = set([n1, n2, n3])
            if len(triple) < 3:
                continue
            if n2 not in connections[n1] or n3 not in connections[n1] or n3 not in connections[n2]:
                continue
            if 't' not in n1[0]+n2[0]+n3[0]:
                continue
            triples.add(tuple(sorted(triple)))

print("Part 1:", len(triples))

maxnetwork = set()
# part 2
for n1 in connections.keys():
    for n2 in connections[n1]:
        network = set([n1, n2])
        for n3 in connections[n1] | connections[n2]:
            if n3 in network:
                continue
            allconnected = True
            for n in network:
                if n3 not in connections[n]:
                    allconnected = False
                    break
            if allconnected:
                network.add(n3)
        if len(network) > len(maxnetwork):
            maxnetwork = network

print("Part 2:",','.join(sorted(maxnetwork)))



