from dotenv import load_dotenv; load_dotenv()

import aocd
import pytest 
from parse import parse
from pathlib import Path

import itertools as it

def solve(data):
    for i,j,k in it.combinations(data, 3):
        if i+j+k == 2020:
            return i*j*k

@pytest.mark.parametrize('data,expect',
    # INSERT TEST CASES HERE
    [([1721,979,366,299,675,1456], 241861950)])
def test_solve(data, expect):
    assert solve(data) == expect

if __name__ == '__main__':
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

