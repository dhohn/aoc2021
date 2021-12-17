import os
from collections import defaultdict

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

class Conway2D:
    def __init__(self, lines=[]):
        self.state = defaultdict(lambda:".")
        for y, linex in enumerate(lines):
            for x, state in enumerate(linex):
                self.state[(x, y)] = int(state)
        self.size = len(lines)

    def fill_from_coords(self, coords: list[str]):
        for c in coords:
            self[tuple(map(int, c.split(",")))] = "#"
        x = [k[0] for k in self.state.keys()]
        y = [k[1] for k in self.state.keys()]
        self.range_x = (0, max(x)+1)
        self.range_y = (0, max(y)+1)        
            
    def __iter__(self):
        for x in range(*self.range_x):
            for y in range(*self.range_y):
                yield (x, y)

    def __getitem__(self, arg):
        return self.state[arg]

    def __setitem__(self, arg, val):
        self.state[arg] = val

    def __delitem__(self, arg):
        del self.state[arg]

    def __len__(self):
        return len(self.state)
        
    def __repr__(self):
        out = []
        for y in range(*self.range_y):
            for x in range(*self.range_x):
                out += [str(self[(x, y)])]
            out += ["\n"]
        return "".join(out)

    def count(self):
        return sum([self[cell] == "#" for cell in self])

    def fold(self, axis, coord):
        if axis == 0:
            # x
            for y in range(*self.range_y):
                for i, x in enumerate(range(coord+1, self.range_x[1])):
                    if self[coord-1-i, y] == ".":
                        self[coord-1-i, y] = self[x, y]
                    try:
                        del self[x, y]
                    except KeyError: pass
            self.range_x = (self.range_x[0], coord)
        if axis == 1:
            # y
            for x in range(*self.range_x):
                for i, y in enumerate(range(coord+1, self.range_y[1])):
                    if self[x, coord-1-i] == ".":
                        self[x, coord-1-i] = self[x, y]
                    try:
                        del self[x, y]
                    except KeyError: pass
            self.range_y = (self.range_y[0], coord)

coords, folds = data.split("\n\n")
coords = coords.split("\n")
folds = folds.split("\n")

def test():
    c = """6,10
    0,14
    9,10
    0,3
    10,4
    4,11
    6,0
    6,12
    4,1
    0,13
    10,12
    3,4
    3,0
    8,4
    1,10
    2,14
    8,10
    9,0""".split("\n")

    cw = Conway2D()
    cw.fill_from_coords(c)
    cw.fold(1,7)
    cw.fold(0,5)
    return cw


def part1(lines=lines):
    coords, folds = data.split("\n\n")
    coords = coords.split("\n")
    folds = folds.split("\n")
    
    cw = Conway2D()
    cw.fill_from_coords(coords)        

    fold = folds[0]
    axis = fold.count("y")
    along = int(fold.split("=")[-1])

    cw.fold(axis, along)
    
    return cw.count()

def part2(lines=lines):
    coords, folds = data.split("\n\n")
    coords = coords.split("\n")
    folds = folds.split("\n")
    
    cw = Conway2D()
    cw.fill_from_coords(coords)        

    for fold in folds:
        axis = fold.count("y")
        along = int(fold.split("=")[-1])
        cw.fold(axis, along)

    return cw

# submit(part1(), part="a")
# submit(part2(), part="b")



