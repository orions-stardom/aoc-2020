from dotenv import load_dotenv; load_dotenv()

import aocd
import pytest
import sys

from parse import parse
from pathlib import Path

import itertools as it

def closest_multiple(n, x):
    ''' Multiple of x closest to and above n
    adapted from https://www.geeksforgeeks.org/multiple-of-x-closest-to-n/
    '''
    z = x//2
    nn = n+z
    nn -= nn%x

    if nn <= n:
        nn += x

    return nn

def solve(data):
    data = data.splitlines()
    arrive = int(data[0])
    busses = [int(x) for x in data[1].split(',') if x != 'x']
    catch_at, bus = min((closest_multiple(arrive, bus), bus) for bus in busses)
    return bus * (catch_at - arrive)

@pytest.mark.parametrize('data,expect',
    [('''939
7,13,x,x,59,x,31,19''', 295)])
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

