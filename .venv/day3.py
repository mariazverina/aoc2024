import re

with open('day3.in', 'r') as f:
    lines = [line.strip() for line in f.readlines()]

line = ''.join(lines)
# part 1
m = re.findall(r"mul\((\d+),(\d+)\)", line)
print(sum([int(a) * int(b) for a, b in m]))

# part 2
line += 'do()'
line = re.sub(r"don\'t\(\).*?do\(\)", "", line)
m = re.findall(r"mul\((\d+),(\d+)\)", line)
print(sum([int(a) * int(b) for a, b in m]))
