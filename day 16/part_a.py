from dotenv import load_dotenv; load_dotenv()

import aocd
import pytest
import sys

from parse import parse
from pathlib import Path

import itertools as it

def solve(data):
    rules, mine, nearby = data.split('\n\n')

    rules = {cname: (range(l1, h1+1), range(l2,h2+1)) 
                     for cname, l1,h1,l2,h2 in 
                     (parse('{}: {:d}-{:d} or {:d}-{:d}', line) for line in rules.splitlines())}

    nearby = [[int(x) for x in line.split(',')] for line in nearby.splitlines()[1:]]

    return sum(val for ticket in nearby for val in ticket if not any(val in r for r in it.chain.from_iterable(rules.values())))

@pytest.mark.parametrize('data,expect',
    # INSERT TEST CASES HERE
    [('''class: 1-3 or 5-7
row: 6-11 or 33-44
seat: 13-40 or 45-50

your ticket:
7,1,14

nearby tickets:
7,3,47
40,4,50
55,2,20
38,6,12''', 71)
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

