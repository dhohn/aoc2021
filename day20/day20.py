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
    def __init__(self, lines, alg):
        self.alg = alg
        if isinstance(lines, str):
            lines = lines.splitlines()
        self.state = defaultdict(lambda:".")
        for y, linex in enumerate(lines):
            for x, state in enumerate(linex):
                self.state[(x, y)] = state
        self.size = len(lines)
        self.range = (0, len(lines))
        
    def __iter__(self):
        for y in range(*self.range):
            for x in range(*self.range):
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
        for y in range(*self.range):
            for x in range(*self.range):
                out += [str(self[(x, y)])]
            out += ["\n"]
        return "".join(out)

    def neighbours(self, x, y, n=9):
        nbs = []
        if isinstance(n, str):
            if "r" in n:
                nbs += [(x+1, y)]
            if "d" in n:
                nbs += [(x, y+1)]
            if "u" in n:
                nbs += [(x, y-1)]
            if "l" in n:
                nbs += [(x-1, y)]
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
        
    def window(self, x, y):
        binary = "".join([str(int(self.active(*n))) for n in self.neighbours(x, y)])
        # return binary
        return int(binary, 2)
        
    def distance(self, start, end, metric="manhattan"):
        return abs(start[0]-end[0]) + abs(start[1]-end[1])

    def step(self, n=1):
        for _ in range(n):
            # visit all neighbours to create them
            for cell in list(self.state.keys()):
                [self.active(*n) for n in self.neighbours(*cell)]

            # save state
            newstate = copy.deepcopy(self.state)

            # make new state
            for cell in list(self.state.keys()):
                newstate[cell] = self.alg[self.window(*cell)]

            # overwrite
            del self.state
            self.state = newstate

            # new range
            self.range = (self.range[0]-1, self.range[1]+1)

            # new default
            if self.state.default_factory() == ".":
                self.state.default_factory = lambda:self.alg[0]
            else:
                self.state.default_factory = lambda:self.alg[int("1"*9, 2)]
        
def parse(data=data):
    alg, img = data.split("\n\n")
    alg = alg.replace("\n", "")
    return img.splitlines(), alg

def test():
    test1 = """..#.#..#####.#.#.#.###.##.....###.##.#..###.####..#####..#....#..#..##..##
#..######.###...####..#..#####..##..#.#####...##.#.#..#.##..#.#......#.###
.######.###.####...#.##.##..#..#..#####.....#.#....###..#.##......#.....#.
.#..#..##..#...##.######.####.####.#.#...#.......#..#.#.#...####.##.#.....
.#..#...##.#.##..#...##.#.##..###.#......#.#.......#.#.#.####.###.##...#..
...####.#..#..#.##.#....##..#.####....##...##..#...#......#.#.......#.....
..##..####..#...#.#.#...##..#.#..###..#####........#..####......#..#

#..#.
#....
##..#
..#..
..###"""

    test_cw = Conway2D(*parse(test1))
    test_cw.step(2)
    assert test_cw.count() == 35
    test_cw.step(48)
    assert test_cw.count() == 3351
    

def part1(data=data):
    cw = Conway2D(*parse())
    cw.step(2)
    return cw.count()

def part2(data=data):
    cw = Conway2D(*parse(data))
    cw.step(50)
    return cw.count()

# submit(part1(), part="a")
# submit(part2(), part="b")



