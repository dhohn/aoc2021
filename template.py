import os

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

    
def part1(lines=lines):
    return

def part2(lines=lines):
    return

# submit(part1(), part="a")
# submit(part2(), part="b")



