from aocd import data, lines, submit
try:
    from aocd import numbers
except ValueError:
    numbers = []

import os
if not os.path.exists("input"):
    with open("input","w") as f:
        f.write(data)

def count_bits_in_position(lines):
    length = len(lines[0])
    position = [0]*length
    for p in range(length):
        for l in lines:
            # l = int(l)
            position[p] += int(l[p])
    return position        

def unsigned_bit_inverse(n: int, bit_length: int = 0) -> int:
    if not bit_length:
        bit_length = n.bit_length()
    return ~n & (2**bit_length)-1

def part1(lines=lines):
    position = count_bits_in_position(lines)
    gamma = [1 if p>len(lines)/2 else 0 for p in position]
    epsilon = [1 if g==0 else 0 for g in gamma]
    # or 1 - g

    gamma = int("".join(map(str,gamma)), 2)
    epsilon = int("".join(map(str,epsilon)), 2)

    print(f"a: {gamma*epsilon}")
    return gamma*epsilon

def part2(lines=lines):
    #most common
    my_lines = lines[:]
    pos = 0
    while len(my_lines)>1:
        bits = count_bits_in_position(my_lines)
        onezero = "1" if bits[pos]>=len(my_lines)/2 else "0"
        my_lines = [l for l in my_lines if l[pos] == onezero]
        pos += 1

        ox = int("".join(map(str,my_lines)), 2)

    #least common
    my_lines = lines[:]
    pos = 0
    while len(my_lines)>1:
        bits = count_bits_in_position(my_lines)
        onezero = "0" if bits[pos]>=len(my_lines)/2 else "1"
        my_lines = [l for l in my_lines if l[pos] == onezero]
        pos += 1

        co2 = int("".join(map(str,my_lines)), 2)

    print(f"b: {ox*co2}")
    return ox*co2

part1()
# submit(part1(), part="a")
part2()
# submit(part2(), part="b")



# list[str(bin)] to dec
# list[int(bin)] to dec

# numpy
a = np.array(list(map(list, lines)))
position = [list(a[:,p]).count("1") for p in range(len(a[0]))]
