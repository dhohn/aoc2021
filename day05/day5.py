from aocd import data, lines, submit
try:
    from aocd import numbers
except ValueError:
    numbers = []

import os
if not os.path.exists("input"):
    with open("input","w") as f:
        f.write(data)

import itertools
import numpy as np
from collections import defaultdict
        
class Line:
    def __init__(self, line):
        start, end = line.split(" -> ")
        self.start = tuple(map(int, start.split(",")))
        self.end = tuple(map(int, end.split(",")))

    def horizontal(self):
        return self.start[1] == self.end[1]

    def vertical(self):
        return self.start[0] == self.end[0]

    def slope(self):
        return (self.end[1]-self.start[1]) / (self.end[0]-self.start[0])

    def points(self):
        if self.vertical():
            x = self.start[0]
            size_y = abs(self.start[1] - self.end[1]) + 1
            return list(itertools.zip_longest( [x],
                                               np.linspace(self.start[1], self.end[1], size_y, dtype=int), fillvalue=x
                                              )
                        )
        elif self.horizontal():
            y = self.start[1]
            size_x = abs(self.start[0] - self.end[0]) + 1
            return list(itertools.zip_longest( np.linspace(self.start[0], self.end[0], size_x, dtype=int),
                                               [y], fillvalue=y
                                              )
                        )
        else:
            size_x = abs(self.start[0] - (self.end[0])) + 1
            size_y = abs(self.start[1] - (self.end[1])) + 1
            return list(itertools.zip_longest( np.linspace(self.start[0], self.end[0], size_x, dtype=int),
                                               np.linspace(self.start[1], self.end[1], size_y, dtype=int)
                                              )
                        )

    def __repr__(self):
        return f"{self.start} -> {self.end}"
    
vents = []
for l in lines:
    vents += [Line(l)]

def part1(lines=lines):
    points = defaultdict(int)
    for v in vents:
        if v.horizontal() or v.vertical():
            for p in v.points():
                points[p] += 1

    ans = sum(1 for p in points if points[p] >= 2)
    return ans

def part2(lines=lines):
    points = defaultdict(int)
    for v in vents:
        for p in v.points():
            points[p] += 1

    ans = sum(1 for p in points if points[p] >= 2)
    return ans

# submit(part1(), part="a")
# submit(part2(), part="b")



