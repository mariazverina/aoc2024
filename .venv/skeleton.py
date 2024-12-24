from utils import *

filename = __file__.split("/")[-1].split('.')[0]
with open(filename+'x.in', 'r') as f:
    lines = [line.strip() for line in f.readlines()]

print(lines)


