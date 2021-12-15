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
        
class Conway2D:
    def __init__(self, lines):
        self.state = defaultdict(lambda:-1)
        for y, linex in enumerate(lines):
            for x, state in enumerate(linex):
                self.state[(x, y)] = int(state)
        self.size = len(lines)
        neighbours = [self.neighbours(*n) for n in self]
        self.n_flashes = 0
        self.n_steps = 0
        self.flashed = set()

    def __iter__(self):
        for x in range(self.size):
            for y in range(self.size):
                yield (x, y)

    def __getitem__(self, arg):
        return self.state[arg]

    def __setitem__(self, arg, val):
        self.state[arg] = val
                
    def neighbours(self, x, y, n=6):
        if n==4:
            return [(xx,y) for xx in (x-1, x+1)] +\
                [(x,yy) for yy in (y-1, y+1)]
        if n==6:
            return [(xx, yy)
                    for xx in (x-1, x, x+1)
                    for yy in (y-1, y, y+1)
                    if (x, y) != (xx, yy)]

    def step(self):
        self.n_steps += 1
        self.flashed = set()
        for cell in self:
            self.state[cell] += 1
        while any(self[cell] > 9 for cell in self):
            for cell in self:
                if self[cell] > 9 and cell not in self.flashed:
                    self.flash(*cell)
        for cell in self.flashed:
            self[cell] = 0


    def flash(self, x, y):
        self.flashed.add((x, y))
        self.n_flashes += 1
        for cell in self.neighbours(x, y):
            self.state[cell] += 1
        self.state[(x, y)] = 0


def part1(lines=lines):
    cw = Conway2D(lines)

    for _ in range(100):
        cw.step()
    print(cw.n_flashes)
    return cw.n_flashes

def part2(lines=lines):
    cw = Conway2D(lines)

    while not len(cw.flashed) == cw.size**2:
        cw.step()
    return cw.n_steps

# submit(part1(), part="a")
# submit(part2(), part="b")



