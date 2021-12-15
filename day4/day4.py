from aocd import data, lines, submit
try:
    from aocd import numbers
except ValueError:
    numbers = []

import os
if not os.path.exists("input"):
    with open("input","w") as f:
        f.write(data)

def flatten(t):
    return [item for sublist in t for item in sublist]

class BingoBoard:
    def __init__(self, lines):
        self.numbers = []
        for l in lines:
            self.numbers += [list(map(int, l.split()))]

    def rows(self):
        return self.numbers

    def columns(self):
        return list(map(list, zip(*self.numbers)))

    def bingo(self, drawn):
        return any(all(n in drawn for n in rows) for rows in self.rows()) or \
            any(all(n in drawn for n in rows) for rows in self.columns())

    def unmarked(self, drawn):
        return [n for n in flatten(self.numbers) if n not in drawn]

    def winning_number_idx(self, drawn):
        for i in range(1, len(drawn)):
            if self.bingo(drawn[:i]):
                return i-1

parsed = data.split("\n\n")
drawn = list(map(int, parsed[0].split(",")))

boards = []

for board in parsed[1:]:
    boards += [BingoBoard(board.split("\n"))]

            
def part1(lines=lines):
    for i in range(1, len(drawn)):
        for bb in boards:
            if bb.bingo(drawn[:i]):
                ans = sum(bb.unmarked(drawn[:i]))*drawn[i-1]
                print(f"a: {ans}")
                return ans

def part2(lines=lines):
    pass
    winning_board_indices = []
    for i in range(1, len(drawn)):
        for bbi, bb in enumerate(boards):
            if bb.bingo(drawn[:i]):
                # print(f"i: {i}, bbi: {bbi}")
                if bbi not in winning_board_indices:
                    winning_board_indices += [bbi]

    last_winner = boards[winning_board_indices[-1]]
    idx = last_winner.winning_number_idx(drawn)
    ans = sum(last_winner.unmarked(drawn[:idx+1]))*drawn[idx]
    print(f"b: {ans}")
    return ans

part1()
# submit(part1(), part="a")
part2()
# submit(part2(), part="b")
