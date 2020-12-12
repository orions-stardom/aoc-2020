from dotenv import load_dotenv; load_dotenv()

import aocd
import pytest 
from parse import parse
from pathlib import Path
import sys

import itertools as it

def solve(data):
    for i,j in it.combinations(data, 2):
        if i+j == 2020:
            return i*j

@pytest.mark.parametrize('data,expect',
    # INSERT TEST CASES HERE
    [([1721,979,366,299,675,1456], 514579)])
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
    data = [int(d) for d in data.splitlines()]
    solution = solve(data)
    print("Solution: ", solution, sep="\n")
    aocd.submit(solution, year=year, day=day, part=part)

