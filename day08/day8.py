from aocd import data, lines, submit
try:
    from aocd import numbers
except ValueError:
    numbers = []

import os
if not os.path.exists("input"):
    with open("input","w") as f:
        f.write(data)

def loop(lines=lines):
    for l in lines:
        patterns, digits = l.split("|")
        yield list(map("".join, list(map(sorted, patterns.split())))), list(map("".join, list(map(sorted, digits.split()))))
        
def part1(lines=lines):
    counter = 0
    for p, d in loop(lines):
        for dd in d:
            if len(dd) in (2, 3, 4, 7):
                counter+=1
    return counter

def unique(patterns, length):
    return [p for p in patterns if len(p) == length][0]

def one(patterns):
    return unique(patterns, 2)

def four(patterns):
    return unique(patterns, 4)

def seven(patterns):
    return unique(patterns, 3)

def eight(patterns):
    return unique(patterns, 7)

def six(patterns):
    six = set(eight(patterns)) - set(seven(patterns))
    patterns = patterns[:]
    patterns.remove(eight(patterns))
    return [p for p in patterns if match(six, p)][0]

def five(patterns):
    topright = set(eight(patterns)) - set(six(patterns))
    patterns = patterns[:]
    patterns.remove(six(patterns))
    return [p for p in patterns if "".join(topright) not in p][0]

def nine(patterns):
    lowleft = set(six(patterns)) - set(five(patterns))
    return [p for p in patterns if "".join(lowleft) not in p and len(p) == 6][0]

def zero(patterns):
    return [p for p in patterns if p not in (six(patterns), nine(patterns)) and len(p) == 6][0]

def two(patterns, seg):
    sixminusfour = set(six(patterns)) - set(four(patterns))
    return [p for p in patterns if p not in seg and match(sixminusfour, p)][0]

def three(patterns, seg):
    return [p for p in patterns if p not in seg][0]

def match(test, ref):
    # are all members of test in ref
    return all((t in ref) for t in test)

def decode(lines):
    res = []
    for patterns, digits in loop(lines):
        seg = {}
        seg[one(patterns)]   = 1
        seg[four(patterns)]  = 4
        seg[seven(patterns)] = 7
        seg[eight(patterns)] = 8
        seg[six(patterns)]   = 6
        seg[five(patterns)]  = 5
        seg[nine(patterns)]  = 9
        seg[zero(patterns)]  = 0
        seg[two(patterns, seg)] = 2
        seg[three(patterns, seg)] = 3
        decoded_digits = [seg[d] for d in digits]
        res += ["".join(list(map(str, decoded_digits)))]
    return res

def part2(lines=lines):
    return sum(map(int, decode(lines)))

# submit(part1(), part="a")
# submit(part2(), part="b")



