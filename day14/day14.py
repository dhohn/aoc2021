import os
from collections import Counter, defaultdict

try:
    from aocd import data, lines, submit
    from aocd import numbers
except ValueError:
    numbers = []
except ImportError:
    numbers = []
    with open("input","r") as f:
        lines = list(map(str.strip, f.readlines()))

if not os.path.exists("input"):
    with open("input","w") as f:
        f.write(data)

try:
    from itertools import pairwise
except ImportError:
    from itertools import tee
    def pairwise(iterable, n=2):
        # pairwise('ABCDEFG') --> AB BC CD DE EF FG
        iterators = tee(iterable, n)
        for i in range(1, n):
            for _ in range(i):
                next(iterators[i], None)
        return zip(*iterators)

start = lines[0]
rules = lines[2:]

rules = {rule.split(" -> ")[0]:rule.split(" -> ")[1] for rule in rules}

def most_common_min_least_common(pairs):
    letters = defaultdict(int)
    for p in pairs:
        letters[p[0]] += pairs[p]
        # letters[p[1]] += pairs[p]
    letters[start[-1]] += 1
    c = Counter(letters)
    return max(c.values()) - min(c.values())

def part1(lines=lines):
    start = lines[0]
    rules = lines[2:]

    rules = {rule.split(" -> ")[0]:rule.split(" -> ")[1] for rule in rules}

    def step(string):
        new = [string[0]]
        for p in pairwise(string):
            out = p[1]
            p = "".join(p)
            if p in rules:
                out = f"{rules[p]}{p[1]}"
            new += [out]
        return "".join(new)

    for _ in range(10):
        start = step(start)

    c = Counter(start)
    answer = c.most_common()[0][1] - c.most_common()[-1][1]

    return answer

def part2(n=40):
    pairs = defaultdict(int)            

    for p in pairwise(start):
        pairs["".join(p)] += 1

    for _ in range(n):
        tmp = defaultdict(int)
        for p in pairs:
            if p in rules:
                # new pair p[0]+rules[p]
                # and rules[p]+p[1]
                # as often as p occurs
                tmp[p[0]+rules[p]] += pairs[p]
                tmp[rules[p]+p[1]] += pairs[p]
        pairs = tmp
        
    return most_common_min_least_common(pairs)

# submit(part1(), part="a")
# submit(part2(), part="b")



