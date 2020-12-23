from dotenv import load_dotenv; load_dotenv()

import aocd
import pytest
import sys

from parse import parse
from pathlib import Path

import more_itertools as mit
import itertools as it

def make_circle(data, size=None):
    if size is None:
        size = len(data)
    data = [int(d) for d in data]
    
    # Waste spot 0 to have the indices line up nicely
    circle = [None] * (size + 1)
    for x, y in mit.pairwise(it.chain(data, range(max(data)+1, size+1))):
        circle[x] = y
    
    # spot 0 is useless so we might as well use it for the first 'current' value
    circle[y] = circle[0] = data[0]
    return circle
    

def do_move(circle, current):
    get = [circle[current], circle[circle[current]], circle[circle[circle[current]]]]
    dest = current - 1 or len(circle) - 1
    while dest in get:
        dest = dest - 1 or len(circle) - 1

    circle[current], circle[dest], circle[get[-1]] = circle[get[-1]], circle[current], circle[dest]
    return circle[current]


def solve(data):
    circle = make_circle(data, 1000000)

    current = circle[0]
    for _ in range(10000000):
        current = do_move(circle, current)
  
    return circle[1] * circle[circle[1]]

@pytest.mark.parametrize('data,expect',
    # INSERT TEST CASES HERE
    [('389125467', 149245887792),
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
    print("Solution: \n", solution)
    #aocd.submit(solution, year=year, day=day, part=part, reopen=False)

