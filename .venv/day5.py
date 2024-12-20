import functools

with open('day5.in', 'r') as f:
    lines = [line.strip() for line in f.readlines()]

n = lines.index('')

order = lines[:n]
pages = lines[n+1:]

order = [ (int(a), int(b)) for a, b in map(lambda x:x.split('|'), order)]
pages = [list(map(int, x.split(','))) for x in pages]

def valid(order, pages):
    pages = {p : n for n, p in enumerate(pages)}
    for a, b in order:
        try:
            if pages[a] > pages[b]:
                return False
        except KeyError:
            pass
    return True

print(sum([p[len(p) // 2] for p in pages if valid(order, p)]))

def correct(order, pages):
    order = set(order)
    c = lambda x, y: -1 if (x,y) in order else 1
    pages = sorted(pages, key=functools.cmp_to_key(c))
    return pages


invalid = [p for p in pages if not valid(order, p)]

print(invalid)
invalid = [correct(order, p) for p in invalid]

print(sum([p[len(p) // 2] for p in invalid]))
