import os
from collections import defaultdict
import copy
import numpy as np


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

def to_tuple(string):
    # turn "x=a..b" into (a, b)
    return tuple(map(int, string[2:].split("..")))
        
class Conway3D:
    def __init__(self, lines):
        self.state = defaultdict(int)
        for y, linex in enumerate(lines):
            for x, state in enumerate(linex):
                self.state[(x, y, 0)] = state
        self.state = {}

    def compress_coordinates(self, lines):
        self.x_coords = []
        self.y_coords = []
        self.z_coords = []
        
        for line in lines:
            onoff = {"on":1, "off":0}
            turn_on, coords = line.split(" ")
            x, y, z = tuple(map(to_tuple, coords.split(",")))
            self.x_coords += x
            self.x_coords[-1] += 1
            self.y_coords += y
            self.y_coords[-1] += 1
            self.z_coords += z
            self.z_coords[-1] += 1


        self.x_coords = list(set(self.x_coords))
        self.y_coords = list(set(self.y_coords))
        self.z_coords = list(set(self.z_coords))
        
        self.x_coords.sort()
        self.y_coords.sort()
        self.z_coords.sort()

        self.state = np.zeros((len(self.x_coords), len(self.y_coords), len(self.z_coords)), dtype=np.short)
           
    def count(self):
        return list(self.state.values()).count(1)

    def count_compressed(self):
        sum = 0
        it = np.nditer(self.state, flags=['multi_index'])
        for val in it:
            # print("%d <%s>" % (val, it.multi_index), end=' ')
        # for key, val in self.state.items():
            # print(key, val)
            # print(self.x_coords[key[0]], self.y_coords[key[1]], self.z_coords[key[2]])
            # print(self.x_coords[key[0]+1], self.y_coords[key[1]+1], self.z_coords[key[2]+1])
            if val:
                key = it.multi_index
                volume = (self.x_coords[key[0]+1]-self.x_coords[key[0]])*\
                         (self.y_coords[key[1]+1]-self.y_coords[key[1]])*\
                         (self.z_coords[key[2]+1]-self.z_coords[key[2]])
                # print(f"{volume=}")
                sum += volume
        return sum

    def step(self, instruction):
        onoff = {"on":1, "off":0}
        turn_on, coords = instruction.split(" ")
        turn_on = onoff[turn_on]
        x, y, z = tuple(map(to_tuple, coords.split(",")))
        # print(x,y,z)

        for xx in range(max(-50, x[0]), min(50, x[1]+1)):
            for yy in range(max(-50, y[0]), min(50, y[1]+1)):
                for zz in range(max(-50, z[0]), min(50, z[1]+1)):
                    self.state[xx,yy,zz] = turn_on

    def step_compressed(self, instruction):
        onoff = {"on":1, "off":0}
        turn_on, coords = instruction.split(" ")
        turn_on = onoff[turn_on]
        x, y, z = tuple(map(to_tuple, coords.split(",")))
        # print(x,y,z)
        # x = tuple(map(lambda x: x_coords.index(x), x))
        x = self.x_coords.index(x[0]), self.x_coords.index(x[1]+1)
        y = self.y_coords.index(y[0]), self.y_coords.index(y[1]+1)
        z = self.z_coords.index(z[0]), self.z_coords.index(z[1]+1)
        # print(x,y,z, turn_on)

        for xx in range(x[0], x[1]):
            for yy in range(y[0], y[1]):
                for zz in range(z[0], z[1]):
                    self.state[xx,yy,zz] = turn_on
                    
def part1(lines=lines):
    cw = Conway3D([])
    for line in lines:
        cw.step(line)

    print(f"{cw.count()= }")
        
    return cw.count()

def part2(lines=lines):
    cw = Conway3D([])
    cw.compress_coordinates(lines)
    for line in lines:
        cw.step_compressed(line)

    print(f"{cw.count_compressed()= }")

    return cw.count_compressed()

# submit(part1(), part="a")
# submit(part2(), part="b")

if __name__=="__main__":
    part1(lines)
    part2(lines)



