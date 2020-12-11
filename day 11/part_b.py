from dotenv import load_dotenv; load_dotenv()

import aocd
import pytest
import sys

from parse import parse
from pathlib import Path

import more_itertools as mit
import itertools as it

from copy import deepcopy

def next_state(state):
    new_state = deepcopy(state)

    height, width = len(state),len(state[0])

    for y, row in enumerate(state):
        for x, spot in enumerate(row):
            if spot == '.': # Spots without a seat can never change
                continue

            seen = []
            directions = [ (-1, 0), (1,0), (0,1), (0,-1), (1,1), (1,-1), (-1,1), (-1,-1)]

            for dx, dy in directions:
                cand_x, cand_y = x, y
                 
                while True:
                    cand_x, cand_y = cand_x+dx, cand_y+dy

                    if not 0 <= cand_x < width or not 0 <= cand_y < height:
                        break

                    if state[cand_y][cand_x] == '.':
                        continue
                    
                    # Spot exists and we can see a seat in it
                    seen.append(state[cand_y][cand_x])
                    break

            if spot == 'L' and not any(s == '#' for s in seen):
                new_state[y][x] = '#'
            if spot == '#' and seen.count('#') >= 5:
                new_state[y][x] = 'L'

    return new_state


def print_state(state):
    print(*map(''.join, state), sep='\n')
    print()

def solve(data):
    current = [list(l) for l in data.splitlines()]

    while True:
        old, current = current, next_state(current)
        if old == current:
            return sum(row.count('#') for row in current)

@pytest.mark.parametrize('data,expect',
    # INSERT TEST CASES HERE
    [('''L.LL.LL.LL
LLLLLLL.LL
L.L.L..L..
LLLL.LL.LL
L.LL.LL.LL
L.LLLLL.LL
..L.L.....
LLLLLLLLLL
L.LLLLLL.L
L.LLLLL.LL''', 26) 
    ])
def test_solve(data, expect):
    assert solve(data) == expect

if __name__ == '__main__':
    if pytest.main([__file__]):
        # follows shell exit code conventions - nonzero = Failure
        sys.exit(1)

    # aocd's filename introspection doesn't fit my naming conventions
    f = Path(__file__).absolute()    
    year, day, part = parse("aoc-{:d}", f.parent.parent.name)[0], \
                      parse("day {:d}", f.parent.name)[0], \
                      parse("part_{}.py", f.name)[0]
    data = aocd.get_data(year=year, day=day)
    solution = solve(data)
    print("Solution: ", solution, sep="\n")
    aocd.submit(solution, year=year, day=day, part=part, reopen=False)

