import os
from collections import defaultdict
import copy

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
    def __init__(self, lines):
        if isinstance(lines, str):
            lines = lines.splitlines()
        self.state = defaultdict(lambda:".")
        for y, linex in enumerate(lines):
            self.size_x = len(linex)
            for x, state in enumerate(linex):
                self.state[(x, y)] = state
        self.size_y = len(lines)
        self.range_x = (0, self.size_x)
        self.range_y = (0, self.size_y)
        self.steps = 0

        
    def __iter__(self):
        for y in range(*self.range_y):
            for x in range(*self.range_x):
                yield (x, y)

    def active(self, *args):
        return self.state[args] == "#"
    def inactive(self, *args):
        return self.state[args] == "."

    def count(self, match="#"):
        return list(self.state.values()).count(match)
    
    def count_neighbours(self, *args, state="active"):
        return sum([self.__getattribute__(state)(*n) for n in self.neighbours(*args)])
                
    def __getitem__(self, arg):
        return self.state[arg]

    def __setitem__(self, arg, val):
        self.state[arg] = val
        
    def __repr__(self):
        out = []
        for y in range(*self.range_y):
            for x in range(*self.range_x):
                out += [str(self[(x, y)])]
            out += ["\n"]
        return "".join(out)

    def neighbours(self, x, y, n=9):
        nbs = []
        if isinstance(n, str):
            if n == "seacucumber":
                if self[x, y] == ">":
                    n = "r"
                if self[x, y] == "v":
                    n = "d"
                if self[x, y] == ".":
                    return [(x, y)]
            if "r" in n:
                nbs += [(x+1, y)]
            if "d" in n:
                nbs += [(x, y+1)]
            if "u" in n:
                nbs += [(x, y-1)]
            if "l" in n:
                nbs += [(x-1, y)]
            # nbs = [tuple(map( lambda x: x%self.size, t)) for t in nbs]
            nbs = [(t[0]%self.size_x, t[1]%self.size_y) for t in nbs]
            return nbs
        if n==4:
            nbs = [(xx,y) for xx in (x-1, x+1)] +\
                [(x,yy) for yy in (y-1, y+1)]
            # return [nb for nb in nbs if 0<=nb[0]<self.size and 0<=nb[1]<self.size]
            return [nb for nb in nbs if self[nb]<10]
        if n==8:
            return [(xx, yy)
                    for xx in (x-1, x, x+1)
                    for yy in (y-1, y, y+1)
                    if (x, y) != (xx, yy)]
        if n==9:
            return [(xx, yy)
                    for yy in (y-1, y, y+1)
                    for xx in (x-1, x, x+1)]

    def distance(self, start, end, metric="manhattan"):
        return abs(start[0]-end[0]) + abs(start[1]-end[1])

    def step(self, n=1):
        changed = False
        for _ in range(n):
            self.steps += 1
            # save state
            newstate = copy.deepcopy(self.state)

            # make new state. go right
            for cell in list(self.state.keys()):
                nb = self.neighbours(*cell, "seacucumber")[0]
                if self[cell] == ">" and self[nb] == ".":
                    newstate[nb] = newstate[cell]
                    newstate[cell] = "."
                    changed = True

            # overwrite
            del self.state
            self.state = newstate

            # save state
            newstate = copy.deepcopy(self.state)

            # make new state. go down
            for cell in list(self.state.keys()):
                nb = self.neighbours(*cell, "seacucumber")[0]
                if self[cell] == "v" and self[nb] == ".":
                    newstate[nb] = newstate[cell]
                    newstate[cell] = "."
                    changed = True

            # overwrite
            del self.state
            self.state = newstate
            
        return changed


test = Conway2D('''..........
.>v....v..
.......>..
..........''')
        
def part1(lines=lines):
    cw = Conway2D(lines)
    while cw.step():
        pass

    return cw.steps

def part2(lines=lines):
    return

# submit(part1(), part="a")
# submit(part2(), part="b")



