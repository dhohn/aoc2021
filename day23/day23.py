import os
import heapq
from collections import defaultdict
import more_itertools

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

lvl1 = lines[2].replace("#","")
lvl2 = lines[3].replace("#","").strip()

corridor = int(11*"0")
room_A = int((lvl1[0]+lvl2[0]).replace("A","1").replace("B","2").replace("C","3").replace("D","4"))

corridor = 11*"."
room_A = lvl1[0]+lvl2[0]
room_B = lvl1[1]+lvl2[1]
room_C = lvl1[2]+lvl2[2]
room_D = lvl1[3]+lvl2[3]

class AmphipodState:
    def __init__(self, corridor, a, b, c, d):
        self.corridor = corridor
        self.rooms = {}
        self.rooms["A"] = a
        self.rooms["B"] = b
        self.rooms["C"] = c
        self.rooms["D"] = d

    @classmethod
    def from_state_string(cls, state_string):
        corridor = state_string[:11]
        a,b,c,d = list(map("".join, more_itertools.divide(4, state_string[11:])))
        return cls(corridor, a, b, c, d)

    def state_string(self):
        # cat all members
        # coordinates in this are 0-10 for the corridor
        # and so one for A, B...
        return self.corridor + "".join(self.rooms.values())
    
    def __repr__(self):
        out = "\n" + self.corridor + "\n"
        for i in range(len(self.rooms["A"])):
            out += 2*" "
            out += self.rooms["A"][i] + " " + self.rooms["B"][i] + " " + self.rooms["C"][i] + " " + self.rooms["D"][i] + "\n"
        return out

    def __eq__(self, other):
        return\
            self.corridor == other.corridor and\
            self.rooms == other.rooms

    @staticmethod
    def door(letter: str) -> int:
        # return the door in the corridor corresponding to the room "letter"
        assert letter in "ABCD", "coord i must be in a room."
        return {"A":2, "B":4, "C":6, "D":8}[letter]

    @staticmethod
    def move_cost(letter: str) -> int:
        return {"A":1, "B":10, "C":100, "D":1000}[letter]
    
    def distance(self, other) -> int:
        # distance with moving cost
        coords = []
        for i in range(len(self.state_string()[:11])):
            a, b = self.state_string()[i], other.state_string()[i]
            if a != b:
                if a == ".":
                    # corridor is destination
                    to_corridor = True
                    moved = b
                else:
                    to_corridor = False
                    moved = a
                coords += [i]
        # coords[0] is the corridor

        # which room changed?
        changed_room = ""
        for k, v in self.rooms.items():
            vv = other.rooms[k]
            if v != vv:
                changed_room = k

        # which position in the room changed?
        for i in range(len(self.rooms[changed_room])):
            a, b = self.rooms[changed_room][i], other.rooms[changed_room][i]
            if a != b:
                coords += [i]

        door = self.door(changed_room)
        traversed = sorted([coords[0], door])
        traversed[-1] += 1
        traversed = list(range(*traversed))
        if to_corridor == False:
            traversed.remove(coords[0])

        # traversed has coords -> convert to contents
        traversed = list(map(lambda x:self.corridor[x], traversed))
        
        # add rooms contents
        # print(f"{changed_room= }")
        # print(f"{coords= }")
        traversed += [ self.rooms[changed_room][:(coords[1] + int(not to_corridor))] ]
        traversed = "".join(traversed).strip()

        if not all(t == "." for t in traversed):
            return 0
        cost = len(traversed)*self.move_cost(moved)
        return cost

    def open_spaces_in_rooms(self):
        # return bottom most open spaces in all rooms
        cands = []
        for rk, rv in self.rooms.items():
            if rv[0] == ".":
                coord = 0
                for l in rv[1:]:
                    if l == ".":
                        coord += 1
                cands += [(rk, coord)]
        cands = sorted(cands, key=lambda x: x[0], reverse=True)
        return cands

    def movable_pods_in_rooms(self):
        cands = []
        for rk, rv in self.rooms.items():
            if all(letter == rk for letter in rv):
                continue
            for i, letter in enumerate(rv):
                if letter != ".":
                    cands += [(rk, i)]
                    break
        cands = sorted(cands, key=lambda x: x[0], reverse=True)
        return cands

    @staticmethod
    def str_item_assignment(string: str, idx: int, char: str) -> str:
        l = list(string)
        l[idx] = char
        return "".join(l)
    
    def neighbours(self):
        cand_aps = []

        # corridor to room
        for i, ap in enumerate(self.corridor):
            if ap != ".":
                for rk, rc in self.open_spaces_in_rooms():
                    if ap != rk:
                        # dont move into non home rooms
                        continue
                    if not self.rooms[rk].count(rk) + self.rooms[rk].count(".") == len(self.rooms[rk]):
                        # dont move into home room containing foreigners
                        continue
                    cand_ap = AmphipodState.from_state_string(self.state_string())
                    cand_ap.corridor = self.str_item_assignment(cand_ap.corridor, i, ".")
                    cand_ap.rooms[rk] = self.str_item_assignment(cand_ap.rooms[rk], rc,  ap)
                    if self.distance(cand_ap):
                        cand_aps += [cand_ap]

        # room to corridor
        for rk, rc in self.movable_pods_in_rooms():
            for i, ap in enumerate(self.corridor):
                if ap == "." and i not in (2,4,6,8):
                    cand_ap = AmphipodState.from_state_string(self.state_string())
                    cand_ap.corridor = self.str_item_assignment(cand_ap.corridor, i, self.rooms[rk][rc])
                    cand_ap.rooms[rk] = self.str_item_assignment(cand_ap.rooms[rk], rc,  ".")
                    if self.distance(cand_ap):
                        cand_aps += [cand_ap]
        return cand_aps

    def heuristic(self):
        total_cost = 0
        for i, ap in enumerate(self.corridor):
            if ap != ".":
                distance = abs(i - self.door(ap)) + 1
                total_cost += distance*self.move_cost(ap)

        for rk, rv in self.rooms.items():
            if all(letter == rk for letter in rv):
                continue
            for i, letter in enumerate(rv):
                if letter == rk:
                    continue
                if letter != ".":
                    distance = abs(self.door(letter) - self.door(rk)) + 1 + i + 1
                    total_cost += distance*self.move_cost(letter)
        return total_cost
    
def A_star(start: AmphipodState, goal=None):
    # see https://en.wikipedia.org/wiki/A*_search_algorithm
    if not goal:
        n = len(start.rooms["A"])
        goal = AmphipodState(11*".", "A"*n, "B"*n, "C"*n, "D"*n).state_string()

    open_set = [(0, start.state_string())]

    came_from = {}

    g_score = defaultdict(lambda:1e9)
    g_score[start.state_string()] = 0

    f_score = {}
    f_score[start.state_string()] = start.heuristic()
    while len(open_set):
        current = heapq.heappop(open_set)[1]
        if current == goal:
            print(g_score[current])
            return reconstruct_path(came_from=came_from, current=current)
        current_ap = AmphipodState.from_state_string(current)
        # print(f"{current_ap.heuristic() = }")
        # print(f"{current_ap}")
        for nb in current_ap.neighbours():
            tentative_g_score = g_score[current] + current_ap.distance(nb)
            if tentative_g_score < g_score[nb.state_string()]:
                came_from[nb.state_string()] = current
                g_score[nb.state_string()] = tentative_g_score
                f_score[nb.state_string()] = tentative_g_score + nb.heuristic()
                if nb.state_string() not in open_set:
                    heapq.heappush(open_set, (f_score[nb.state_string()], nb.state_string()))

    return []

    
def reconstruct_path(came_from, current):
    path = [current]
    while current in came_from:
        current = came_from[current]
        path += [current]
    path.reverse()
    return path


def print_path(path):
    distance = 0
    current = path[0]
    current = AmphipodState.from_state_string(current)
    path = path[1:]
    print(current)
    for p in path:
        ap = AmphipodState.from_state_string(p)
        print(f"{current.distance(ap)= }")
        distance += current.distance(ap)
        current = ap
        print(ap)
        print(f"{distance= }")
    return distance

ap = AmphipodState(corridor, room_A, room_B, room_C, room_D)


def part1(lines=lines):
    ap = AmphipodState(corridor, room_A, room_B, room_C, room_D)
    path = A_star(ap)
    return print_path(path)

def part2(lines=lines):
    ap2 = AmphipodState("."*11,
                    room_A[0]+"DD"+room_A[1],
                    room_B[0]+"CB"+room_B[1],
                    room_C[0]+"BA"+room_C[1],
                    room_D[0]+"AC"+room_D[1])
     
    path = A_star(ap2)
    return print_path(path)

# submit(part1(), part="a")
# submit(part2(), part="b")


if __name__ == "__main__":
    # part1()
    part2()
