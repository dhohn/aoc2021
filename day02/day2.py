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
    depth, x = 0, 0
    for l in lines:
        direction, n = l.split()
        n = int(n)
        if direction == "forward":
            x += n
        if direction == "down":
            depth += n
        if direction == "up":
            depth -= n
    print(f"a: {depth*x}")
    return depth*x

def part2(lines=lines):
    depth, x, aim = 0, 0, 0
    for l in lines:
        direction, n = l.split()
        n = int(n)
        if direction == "aim":
            aim += n
        if direction == "forward":
            x += n
            depth += n*aim
        if direction == "down":
            aim += n
        if direction == "up":
            aim -= n
    print(f"b: {depth*x}")
    return depth*x

part1()
# submit(part1(), part="a")
part2()
# submit(part2(), part="b")



