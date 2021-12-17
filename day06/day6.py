from aocd import data, lines, submit
try:
    from aocd import numbers
except ValueError:
    numbers = []

import os
from collections import defaultdict
import copy


if not os.path.exists("input"):
    with open("input","w") as f:
        f.write(data)
        
numbers = list(map(int, data.split(",")))

def part1(numbers=numbers, days=80):
    my_numbers = numbers[:]
    
    for _ in range(days):
        n_new_fish = my_numbers.count(0)
        for idx, n in enumerate(my_numbers):
            if n>7: m = n//7
            else: m = 0
            new_n = (n-1) % 7 + m*7
            my_numbers[idx] = new_n
        my_numbers += [8]*n_new_fish

    return len(my_numbers)


counter = defaultdict(int)
for i in numbers:
    counter[i] += 1

def part2(counter=counter, days=256):
    my_counter = copy.deepcopy(counter)
    for _ in range(days):
        n_new_fish = my_counter[0]
        for spawn_n in range(1, 9):
            my_counter[spawn_n-1] = my_counter[spawn_n]
        my_counter[6] += n_new_fish
        my_counter[8] = n_new_fish
    # print([my_counter[i] for i in range(9)])
    return sum(my_counter.values())

# submit(part1(), part="a")
# submit(part2(), part="b")



