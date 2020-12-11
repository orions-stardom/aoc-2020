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
    for first_row, last_row, (i, row) in mit.mark_ends(enumerate(state)):
        for first_spot, last_spot, (j, spot) in mit.mark_ends(enumerate(row)):
            adjacent = []


            if not first_row:
                adjacent.append(state[i-1][j])
                
                if not first_spot:
                    adjacent.append(state[i-1][j-1])
                if not last_spot:
                    adjacent.append(state[i-1][j+1])

            if not last_row:
                adjacent.append(state[i+1][j])
                
                if not first_spot:
                    adjacent.append(state[i+1][j-1])
                if not last_spot:
                    adjacent.append( state[i+1][j+1])

            if not first_spot:
                adjacent.append(state[i][j - 1])
            if not last_spot:
                adjacent.append(state[i][j + 1])

            if spot == 'L' and not any(s == '#' for s in adjacent):
                new_state[i][j] = '#'
            if spot == '#' and adjacent.count('#') >= 4:
                new_state[i][j] = 'L'

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
L.LLLLL.LL''', 37)
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

