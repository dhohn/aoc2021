from aocd import data, lines, submit
try:
    from aocd import numbers
except ValueError:
    numbers = []

import os
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
    
def part1(lines=lines):
    my_count = 0
    for a, b in pairwise(numbers):
        if a<b:
            my_count += 1
    print(f"a: {my_count}")
    return my_count

def part2(lines=lines):
    triple_it = pairwise(numbers, 3)
    previous = sum(next(triple_it))
    
    my_count = 0
    for n in triple_it:
        current = sum(n)
        if current > previous:
            my_count += 1
        previous = current
    print(f"b: {my_count}")
    return my_count

# submit(part1(), part="a")
# submit(part2(), part="b")



