import os
import math

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


def decode_hex_to_bin(hex_string: str) -> str:
    return "".join([f"{int(char, 16):04b}" for char in hex_string])

def next5(string: str):
    i = 0
    while True:
        yield string[i:i+5]
        i += 5

class Packet:
    def __init__(self, bit_string):
        self.bit_string = bit_string
        self.version()
        self.packets = []
        
        if self.type_id() == 4:
            self.literal_value()
        else:
            self.length_type()

    def __repr__(self):
        out = f"v{self.version} t{self.type_id}"
        if self.type_id == 4:
            out += f" val:{self.literal_value}"
        return out
            
    def version(self):
        self.version = int(self.bit_string[:3], 2)
        return self.version
    
    def type_id(self):
        self.type_id = int(self.bit_string[3:6], 2)
        return self.type_id

    def literal_value(self):
        value = ""
        for chunk in next5(self.bit_string[6:]):
            value += chunk[1:]
            if chunk[0] == "0":
                break
        self.literal_value = int(value, 2)
        self.length = 6 + len(value) + len(value)//4
        return self.literal_value

    def length_type(self):
        self.length_type_id = int(self.bit_string[6])
        if self.length_type_id == 0:
            self.length_bits = int(self.bit_string[7:7+15], 2)
            self.length = 6 + 1 + 15 + self.length_bits
            
            remainder = self.bit_string[6+1+15:]
            n_parsed = 0
            while n_parsed < self.length_bits - 7:
                self.packets += [Packet(remainder)]
                remainder = remainder[self.packets[-1].length:]
                n_parsed += self.packets[-1].length

        if self.length_type_id == 1:
            self.length_packets = int(self.bit_string[7:7+11], 2)
            
            remainder = self.bit_string[6+1+11:]
            n_parsed = 0
            while len(self.packets) < self.length_packets:
                self.packets += [Packet(remainder)]
                remainder = remainder[self.packets[-1].length:]
            self.length = 6 + 1 + 11 + sum([p.length for p in self.packets])
                            
    def cum_version(self):
        if not len(self.packets):
            return self.version
        return self.version + sum([p.cum_version() for p in self.packets])

    def op(self):
        if self.type_id == 0:
            # sum
            return sum([p.op() for p in self.packets])
        if self.type_id == 1:
            # product
            return math.prod([p.op() for p in self.packets])
        if self.type_id == 2:
            # min
            return min([p.op() for p in self.packets])
        if self.type_id == 3:
            # max
            return max([p.op() for p in self.packets])
        if self.type_id == 4:
            # id
            return self.literal_value
        if self.type_id == 5:
            # ge
            return int(self.packets[0].op() > self.packets[1].op())
        if self.type_id == 6:
            # lt
            return int(self.packets[0].op() < self.packets[1].op())
        if self.type_id == 7:
            # eq
            return int(self.packets[0].op() == self.packets[1].op())        

def part1(data=data):
    data = decode_hex_to_bin(data)
    p = Packet(data)
    print(f"{p.cum_version()}")

    return p.cum_version()

def part2(data=data):
    data = decode_hex_to_bin(data)
    p = Packet(data)
    print(f"{p.op()}")

    return p.op()

# submit(part1(), part="a")
# submit(part2(), part="b")



