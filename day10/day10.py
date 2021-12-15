from aocd import data, lines, submit
try:
    from aocd import numbers
except ValueError:
    numbers = []

import os
if not os.path.exists("input"):
    with open("input","w") as f:
        f.write(data)

opposites = {}
opposites[")"] = "("
opposites["("] = ")"
opposites["]"] = "["
opposites["["] = "]"
opposites["}"] = "{"
opposites["{"] = "}"
opposites[">"] = "<"
opposites["<"] = ">"

opening = ("(", "[", "{", "<")
closing = (")", "]", "}", ">")

def invalid(line):
    points = {}
    points[")"] = 3
    points["]"] = 57
    points["}"] = 1197
    points[">"] = 25137

    bracs = []
    for char in line:
        if char in opening:
            bracs += [char]
        if char in closing:
            last = bracs.pop()
            if last != opposites[char]:
                return points[char]
    return 0

def incomplete(line):
    bracs = []
    for char in line:
        if char in opening:
            bracs += [char]
        if char in closing:
            last = bracs.pop()
    bracs.reverse()
    return [opposites[brac] for brac in bracs]

def score(chars):
    points = {}
    points[")"] = 1
    points["]"] = 2
    points["}"] = 3
    points[">"] = 4

    my_score = 0
    for char in chars:
        my_score *= 5
        my_score += points[char]
    return my_score

def part1(lines=lines):
    my_sum = 0
    for l in lines:
        my_sum += invalid(l)

    return my_sum

def part2(lines=lines):
    scores = []
    for l in lines:
        if not invalid(l):
            missing = incomplete(l)
            scores += [score(missing)]
    return sorted(scores)[len(scores)//2]

# submit(part1(), part="a")
# submit(part2(), part="b")



