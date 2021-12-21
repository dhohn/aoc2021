import os
import itertools
from functools import cache

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

class DeterministicD100:
    def __init__(self):
        self.rolls = 0
        self.cycle = itertools.cycle(range(1,100+1))

    def roll(self):
        self.rolls += 3
        return sum(next(self.cycle) for _ in range(3))

@cache
def mod10p1(n):
    return ((n-1)%10)+1

@cache
def dirac(pos1, pos2, points1, points2):
    # player2 always wins first 
    if points2 >= 21:
        return 0, 1

    wins1 = wins2 = 0
    for roll in map(sum, itertools.product(range(1, 3+1), repeat=3)):
        new_pos1 = mod10p1(pos1+roll)
        new_points1 = points1 + new_pos1
        # swap positions of players
        w2, w1 = dirac(pos2, new_pos1, points2, new_points1)
        wins1 += w1
        wins2 += w2

    return wins1, wins2
        

def part1(lines=lines):
    die = DeterministicD100()
    
    positions = [int(line.split(": ")[1]) for line in lines]
    # positions = [4,8]
    points = [0, 0]
    current_player = 0    
    while max(points)<1000:
        round_points = mod10p1(positions[current_player] + die.roll())
        positions[current_player] = round_points
        points[current_player] += round_points
        current_player = (current_player+1)%2


    ans = min(points)*die.rolls
    print(ans)  
    return ans

def part2(lines=lines):
    positions = [int(line.split(": ")[1]) for line in lines]
    return max(dirac(*positions, 0, 0))



# submit(part1(), part="a")
# submit(part2(), part="b")
