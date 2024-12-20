
def sentinels(lines, chr):
    guarded_lines = [chr + l + chr for l in lines]
    guarded_lines.insert(0, chr * len(guarded_lines[0]))
    guarded_lines.append(chr * len(guarded_lines[0]))
    return guarded_lines

def fail(s):
    print(s)
    raise Exception(s)
