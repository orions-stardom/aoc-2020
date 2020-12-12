from dotenv import load_dotenv; load_dotenv()

import aocd
import pytest
import sys

from parse import parse
from pathlib import Path

compass = {'N': (0,1), 'S': (0, -1), 'E': (1,0), 'W': (-1, 0)}
turns = [(0,1), (1,0), (0,-1), (-1, 0)]

def turn(bearing, degrees):
    return turns[(turns.index(bearing) + degrees//90) % len(turns)]


def solve(data):
    bearing = (1, 0) 
    position = (0, 0)

    for line in data.splitlines():
        move, amount = line[0], int(line[1:])

        if move in compass:
            dx, dy = compass[move]
            dx *= amount; dy *= amount
        elif move == 'F':
            dx = bearing[0] * amount
            dy = bearing[1] * amount
        elif move == 'L':
            dx = dy = 0
            bearing = turn(bearing, -amount)
        elif move == 'R':
            dx = dy = 0
            bearing = turn(bearing, amount)

        position = (position[0]+dx, position[1]+dy)

    return abs(position[0]) + abs(position[1])
            


@pytest.mark.parametrize('data,expect',
[('''F10
N3
F7
R90
F11''', 25)
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

