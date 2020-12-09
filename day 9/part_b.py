from dotenv import load_dotenv; load_dotenv()

import aocd
import pytest
import sys

from parse import parse
from pathlib import Path

import more_itertools as mit
import itertools as it

def first_invalid(data, preamblesize):
    for *pres, curr in mit.windowed(data, preamblesize+1):
        if not any(x+y == curr for x,y in it.combinations(pres, 2)):
            return curr

def solve(data, preamblesize=25):
    data = [int(l) for l in data.splitlines()]
    target = first_invalid(data, preamblesize)

    start = 0
    end = 1
    while True:
        test = data[start:end+1]
        res = sum(test)

        if res == target:
            return min(test) + max(test)

        if end > len(data):
            start += 1
            end = start+1
        else:
            end += 1

@pytest.mark.parametrize('data,expect',
    # INSERT TEST CASES HERE
    [('''35
20
15
25
47
40
62
55
65
95
102
117
150
182
127
219
299
277
309
576''', 62)
    ])
def test_solve(data, expect):
    assert solve(data, 5) == expect

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

