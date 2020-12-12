from dotenv import load_dotenv; load_dotenv()

import aocd
import pytest
import sys

from parse import parse
from pathlib import Path

compass = {'N': (0,1), 'S': (0, -1), 'E': (1,0), 'W': (-1, 0)}
turns = [(0,1), (1,0), (0,-1), (-1, 0)]

def sign(n):
    # Integer sign
    if n == 0:
        return 0
    if n < 0:
        return -1
    if n > 0:
        return 1

def turn(waypoint, degrees):
    # Turn waypoint about ship by degrees
    nturns = degrees // 90
    if nturns > 0:
        for _ in range(nturns):
            waypoint = (-waypoint[1], waypoint[0])
    else:
        for _ in range(-nturns):
            waypoint = (waypoint[1], -waypoint[0])

    return waypoint

def solve(data):
    position = (0, 0)
    waypoint = (10, 1) # Relative to ship

    for line in data.splitlines():
        move, amount = line[0], int(line[1:])

        if move in compass:
            dx, dy = compass[move]
            dx *= amount; dy *= amount
            waypoint = (waypoint[0]+dx, waypoint[1]+dy)
        elif move == 'F':
            # Ship moves to waypoint amount times
            dx = waypoint[0] * amount
            dy = waypoint[1] * amount
            position = (position[0] + dx, position[1] + dy)
        elif move == 'L':
            waypoint = turn(waypoint, amount)
        elif move == 'R':
            waypoint = turn(waypoint, -amount)

    return abs(position[0]) + abs(position[1])
            
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

