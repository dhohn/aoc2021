from aocd import data, lines, submit
try:
    from aocd import numbers
except ValueError:
    numbers = []

import os
import numpy as np
import scipy.special
    
numbers = list(map(int, data.split(",")))

if not os.path.exists("input"):
    with open("input","w") as f:
        f.write(data)
        
def get_key(d, val):
    for key, value in d.items():
         if val == value:
             return key

def fuel_a(depth, numbers=numbers):
    return sum(abs(n-depth) for n in numbers)

def fuel_b(depth, numbers=numbers):
    return sum(scipy.special.comb(abs(n-depth)+1, 2, exact=True) for n in numbers)

def find(numbers=numbers, fuel=fuel_b):
    fuel_d = {}
    for i in range(min(numbers), max(numbers)+1):
        fuel_d[i] = fuel(i)
    return fuel_d
        

def part1(numbers=numbers):
    return fuel_a(int(np.median(numbers)))

def part2(lines=lines):
    return min(find(numbers, fuel_b).values())

# submit(part1(), part="a")
# submit(part2(), part="b")


