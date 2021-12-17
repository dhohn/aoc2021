from aocd import data, lines, submit
try:
    from aocd import numbers
except ValueError:
    numbers = []

import os
if not os.path.exists("input"):
    with open("input","w") as f:
        f.write(data)
    
from collections import defaultdict

def flatten(t):
    return set([item for sublist in t for item in sublist])

class Conway2D:
    def __init__(self, lines):
        self.state = defaultdict(lambda:10)
        for y, linex in enumerate(lines):
            for x, state in enumerate(linex):
                self.state[(x, y)] = int(state)
        self.size = len(lines)
        neighbours = [self.neighbours(*n) for n in self]

    def __iter__(self):
        for x in range(self.size):
            for y in range(self.size):
                yield (x, y)
                            
    def neighbours(self, x, y):
        return [(xx,y) for xx in (x-1, x+1)] +\
            [(x,yy) for yy in (y-1, y+1)]

    def local_min(self, x, y):
        return all(self.state[(x, y)] < self.state[neighbour] for neighbour in self.neighbours(x, y))

    def basin(self, x, y):
        my_basin = set([(x, y)])
        my_basin |= set([n for n in self.neighbours(x, y) if self.state[n] > self.state[(x, y)] and self.state[n] < 9])
        # print(x, y)
        # print(my_basin)
        return my_basin | flatten([self.basin(*n) for n in my_basin if n != (x, y)])


def part1(lines=lines):
    cw = Conway2D(lines)

    minima = [neigh for neigh in cw if cw.local_min(*neigh)]
    res = 0
    for n in minima:
        res += state[n] + 1
    return res

def part2(lines=lines):
    cw = Conway2D(lines)

    minima = [neigh for neigh in cw if cw.local_min(*neigh)]
    basins = [cw.basin(*n) for n in minima]
    size_basins = list(map(len, basins))
    
    import numpy as np
    res = np.prod(sorted(size_basins)[-3:])

    return res

# submit(part1(), part="a")
# submit(part2(), part="b")
