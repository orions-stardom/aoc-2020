from dotenv import load_dotenv; load_dotenv()

import aocd
import pytest
import sys

from parse import parse
from pathlib import Path

import cmath
import math

def turn(waypoint, degrees):
    rads = math.radians(degrees)    
    r,phi = cmath.polar(waypoint)
    return cmath.rect(r, phi+rads)

def solve(data):
    position = 0+0j
    waypoint = 10+1j # Relative to ship

    compass = {'N': 0+1j, 'S': 0-1j, 'E': 1+0j, 'W': -1+0j}

    for line in data.splitlines():
        move, amount = line[0], int(line[1:])

        if move in compass:
            waypoint += compass[move] * amount
        elif move == 'F':
            position += waypoint * amount
        elif move == 'L':
            waypoint = turn(waypoint, amount)
        elif move == 'R':
            waypoint = turn(waypoint, -amount)

    return abs(position.real) + abs(position.imag)
            
@pytest.mark.parametrize('data,expect',
[('''F10
N3
F7
R90
F11''', 286)
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

