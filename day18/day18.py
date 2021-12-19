import os
import math
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

class BinaryNode:
    def __init__(self, pairs):
        self.value = self.parent = self.left = self.right = None
        if isinstance(pairs, str):
            pairs = eval(pairs)
        if isinstance(pairs, int):
            self.value = pairs
        else:
            left, right = pairs
            self.left = type(self)(left)
            self.left.parent = self
            self.right = type(self)(right)
            self.right.parent = self

    def depth(self):
        if self.parent == None:
            return 0
        return 1 + self.parent.depth()
            

class SnailNumber(BinaryNode):    
    def magnitude(self):
        if self.value != None:
            return self.value
        return 3*self.left.magnitude() + 2*self.right.magnitude()

    def end_branch(self):
        return self.left.value != None and self.right.value != None

    def leaf(self):
        return self.value != None

    def split(self):
        assert self.leaf() and self.value >= 10
        left_value = math.floor(self.value / 2)
        right_value = math.ceil(self.value / 2)
        self.value = None
        self.left = SnailNumber(left_value)
        self.left.parent = self
        self.right = SnailNumber(right_value)
        self.right.parent = self

    def __repr__(self):
        if self.leaf():
            return str(self.value)
        else:
            return f"[{self.left.__repr__()},{self.right.__repr__()}]"

    def get_leftest_leaf(self):
        if self.leaf():
            return self
        return self.left.get_leftest_leaf()

    def get_rightest_leaf(self):
        if self.leaf():
            return self
        return self.right.get_rightest_leaf()
    
    def next_right(self):
        right_cand = self.parent
        while right_cand.get_rightest_leaf() == self and right_cand.parent:
            right_cand = right_cand.parent
        else:
            if right_cand.right:
                right_cand = right_cand.right
        if right_cand.get_rightest_leaf() == self:
            return None
        next_right = right_cand.get_leftest_leaf()
        return next_right
        
    def next_left(self):
        left_cand = self.parent
        while left_cand.get_leftest_leaf() == self and left_cand.parent:
            left_cand = left_cand.parent
        else:
            if left_cand.left:
                left_cand = left_cand.left
        if left_cand.get_leftest_leaf() == self:
            # means we came from left and there no next left
            return None
        next_left = left_cand.get_rightest_leaf()
        return next_left

    def go_right(self, source=None):
        # recursive version of next_right... might have been easier
        if not source:
            return self.parent.go_right(self)
        if self.leaf():
            return self
        if source == self.left:
            next = self.right
        if source == self.right:
            next = self.parent
        if source == self.parent:
            next = self.left
        if next:
            return next.go_right(self)
        else:
            return None
        
    def explode(self):
        assert self.end_branch()
        next_left = self.left.next_left()
        next_right = self.right.next_right()
        if next_left:
            next_left.value += self.left.value
        if next_right:
            next_right.value += self.right.value
        self.value = 0

        # clean up children
        del self.left
        del self.right
        self.left = None
        self.right = None
        
    def explode_pass(self):
        current = self.get_leftest_leaf()
        while current:
            # print(f"{current}: {current.depth()}")
            if current.depth()>=5:
                # print(f"explode{current.parent}")
                current.parent.explode()
                return True
            current = current.next_right()
        return False

    def split_pass(self):
        current = self.get_leftest_leaf()
        while current:
            if current.value >= 10:
                # print(f"split{current}")
                current.split()
                return True
            current = current.next_right()
        return False

    
    def reduce_pass(self):
        return self.explode_pass() or self.split_pass()

    def reduce(self):
        while self.reduce_pass():
            pass

    def __add__(self, other):
        self_list = eval(self.__repr__())
        other_list = eval(other.__repr__())
        self_list = [self_list, other_list]
        n = SnailNumber(str(self_list))
        n.reduce()
        return n

    def __iadd__(self, other):
        n = self + other
        self = n
        return self

test1 = """[1,1]
[2,2]
[3,3]
[4,4]""".splitlines()

test2 = """[1,1]
[2,2]
[3,3]
[4,4]
[5,5]""".splitlines()

test3 = """[1,1]
[2,2]
[3,3]
[4,4]
[5,5]
[6,6]""".splitlines()

test4 = """[[[0,[4,5]],[0,0]],[[[4,5],[2,6]],[9,5]]]
[7,[[[3,7],[4,3]],[[6,3],[8,8]]]]
[[2,[[0,8],[3,4]]],[[[6,7],1],[7,[1,6]]]]
[[[[2,4],7],[6,[0,5]]],[[[6,8],[2,8]],[[2,1],[4,5]]]]
[7,[5,[[3,8],[1,4]]]]
[[2,[2,2]],[8,[8,1]]]
[2,9]
[1,[[[9,3],9],[[9,0],[0,7]]]]
[[[5,[7,4]],7],1]
[[[[4,2],2],6],[8,7]]""".splitlines()

        
def part1(lines=lines):
    current = SnailNumber(lines[0])

    for line in lines[1:]:
        # print(current)
        current += SnailNumber(line)

    return current.magnitude()

def part2(lines=lines):
    mags = []
    for a, b in itertools.permutations(lines, 2):
        mags += [(SnailNumber(a)+SnailNumber(b)).magnitude()]
    return max(mags)

# submit(part1(), part="a")
# submit(part2(), part="b")



