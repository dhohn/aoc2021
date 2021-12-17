import os
import itertools

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


x = data[data.index("x="):data.index(",")]
y = data[data.index("y="):]
x = list(map(int, x.strip("xy=").split("..")))
y = list(map(int, y.strip("xy=").split("..")))

class Probe:
    def __init__(self, vx, vy, target_x=x, target_y=y):
        self.pos = (0, 0)
        self.vx = vx
        self.vy = vy
        self.t = 0
        self.target_x = x
        self.target_y = y
        self.max_y = 0

    def step(self):
        self.t += 1
        self.pos = (self.pos[0]+self.vx, self.pos[1]+self.vy)
        self.max_y = max(self.max_y, self.pos[1])
        if self.vx:
            self.vx += 1*(-1 if self.vx > 0 else 1)
        self.vy -= 1
        # print(self.pos, self.vx, self.vy)
        # if self.target_x[0] <= self.pos[0] <= self.target_x[1]:
        #     print("x")
        # if self.target_y[0] <= self.pos[1] <= self.target_y[1]:
        #     print("y")

    def shoot_y(self):
        while self.pos[1] > min(self.target_y) or (self.pos[1] < max(self.target_y) and self.vy > 0):
            self.step()
            if self.target_y[0] <= self.pos[1] <= self.target_y[1]:
                # print("hit")
                return True
        return False

    def shoot_x(self):
        while (self.pos[0] > min(self.target_x) or self.pos[0] < max(self.target_x)) and self.vx:
            self.step()
            if self.target_x[0] <= self.pos[0] <= self.target_x[1]:
                # print("hit")
                return True
        return False

    def shoot(self):
        while ((self.pos[0] > min(self.target_x) or self.pos[0] < max(self.target_x)) and self.vx) or\
              (self.pos[1] > min(self.target_y) or (self.pos[1] < max(self.target_y) and self.vy > 0)):
            self.step()
            if self.target_x[0] <= self.pos[0] <= self.target_x[1] and\
               self.target_y[0] <= self.pos[1] <= self.target_y[1]:
                # print("hit")
                return True
        return False

    
def part1(lines=lines):
    allowed_vy = [v for v in range(0,200) if Probe(0,v).shoot_y()]

    p = Probe(0, max(allowed_vy))
    p.shoot_y()
    return p.max_y

def part2(lines=lines):
    allowed_vy = [v for v in range(-200,200) if Probe(0,v).shoot_y()]
    allowed_vx = [v for v in range(0,200) if Probe(v,0).shoot_x()]
    allowed = [(vx, vy) for vx in allowed_vx for vy in allowed_vy if Probe(vx, vy).shoot()]
    return len(allowed)

# submit(part1(), part="a")
# submit(part2(), part="b")



