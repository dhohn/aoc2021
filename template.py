from aocd import data, lines, submit
try:
    from aocd import numbers
except ValueError:
    numbers = []

import os
if not os.path.exists("input"):
    with open("input","w") as f:
        f.write(data)
    
def part1(lines=lines):
    return

def part2(lines=lines):
    return

# submit(part1(), part="a")
# submit(part2(), part="b")



