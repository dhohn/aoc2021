import os
import networkx as nx
import matplotlib.pyplot as plt

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

class Node:
    def __init__(self, name):
        self.name = name
        self.small = (name == name.lower())
        self.big = not self.small

class Graph:
    def __init__(self):
        self.edges = []
        self.nodes = []

    def add_edge(a, b):
        pass

G = nx.Graph()

for l in lines:
    G.add_edge(*l.split("-"))

def dfs(current, end, visited):
    if current == end:
        return 1
    return sum( dfs(nb, end, visited | {nb}) for nb in G.adj[current] if not nb.islower() or nb not in visited)


def dfs2(current, end, visited, visit_twice):
    if current == end:
        return 1
    count = 0
    for nb in G.adj[current]:
        if not nb.islower() or nb not in visited:
            count += dfs2(nb, end, visited | {nb}, visit_twice)
        elif visit_twice and nb not in {"start", "end"}:
            count += dfs2(nb, end, visited | {nb}, visit_twice=False)
    return count
    
def part1(lines=lines):
    return dfs("start", "end", {"start"})

def part2(lines=lines):
    return dfs2("start", "end", {"start"}, visit_twice=True)


# submit(part1(), part="a")
# submit(part2(), part="b")



