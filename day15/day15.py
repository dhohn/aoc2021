# see https://adventofcode.com/2021/day/15
import os
import heapq
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
    def __init__(self, lines):
        # nothing works with with lambda having default value of 100ish or larger
        # with the bug fixed this can be whatever as expected :)
        self.state = defaultdict(lambda:10000)
        for y, linex in enumerate(lines):
            for x, state in enumerate(linex):
                self.state[(x, y)] = int(state)
        self.size = len(lines)

    def extend(self, n=5):
        #right and down
        for newx in range(n):
            for newy in range(n):
                for x in range(self.size):
                    for y in range(self.size):
                        wrap = (self[(x, y)] + newx + newy) // 10
                        self[(x + newx*self.size, y + newy*self.size)] = ((self[(x, y)] + newx + newy) % 10) + wrap
        self.size *= n
        
    def __iter__(self):
        for x in range(self.size):
            for y in range(self.size):
                yield (x, y)

    def __getitem__(self, arg):
        return self.state[arg]

    def __setitem__(self, arg, val):
        self.state[arg] = val
        
    def __repr__(self):
        out = []
        for y in range(self.size):
            for x in range(self.size):
                out += [str(self[(x, y)])]
            out += ["\n"]
        return "".join(out)

    def neighbours(self, x, y, n=4):
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
        if n==6:
            return [(xx, yy)
                    for xx in (x-1, x, x+1)
                    for yy in (y-1, y, y+1)
                    if (x, y) != (xx, yy)]

    def distance(self, start, end, metric="manhattan"):
        return abs(start[0]-end[0]) + abs(start[1]-end[1])
        
    def path_risk(self, path):
        return sum([self[cell] for cell in path]) - self[(0, 0)]

    def best_case_risk(self, start, end=None):
        if not end:
            end = (self.size-1, self.size-1)
        return 1*self.distance(start=start, end=end)

    def reconstruct_path(self, came_from, current):
        path = [current]
        while current in came_from:
            current = came_from[current]
            path += [current]
        path.reverse()
        return path
    
    def A_star(self, goal=None):
        # see https://en.wikipedia.org/wiki/A*_search_algorithm
        start = (0, 0)
        if not goal:
            goal = (self.size-1, self.size-1)

        open_set = [(0, start)]
        
        came_from = {}

        g_score = defaultdict(lambda:1e9)
        g_score[start] = 0

        h = self.best_case_risk
        f_score = {}
        f_score[start] = h(start=start)
        while len(open_set):
            current = heapq.heappop(open_set)[1]
            if current == goal:
                print(g_score[current])
                return self.reconstruct_path(came_from=came_from, current=current)

            for nb in self.neighbours(*current, n=4):
                tentative_g_score = g_score[current] + self[nb]
                if tentative_g_score < g_score[nb]:
                    came_from[nb] = current
                    g_score[nb] = tentative_g_score
                    f_score[nb] = tentative_g_score + h(nb)
                    if nb not in open_set:
                        heapq.heappush(open_set, (f_score[nb], nb))

        return []
            
# correct answer is 390
def part1(lines=lines):
    cw = Conway2D(lines)
    return cw.path_risk(cw.A_star())

cw = Conway2D(lines)
# cw.extend(5)

# correct answer is 2814
def part2(lines=lines):
    cw = Conway2D(lines)
    cw.extend(5)
    return cw.path_risk(cw.A_star())

# submit(part1(), part="a")
# submit(part2(), part="b")



