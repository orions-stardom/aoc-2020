from dotenv import load_dotenv; load_dotenv()

import aocd
import pytest
import sys

from parse import parse
from pathlib import Path

from collections import defaultdict, deque

def solve(data):
    start = [int(x) for x in data.split(',')]
    memory = defaultdict(lambda: deque([], 2))
    
    for i, n in enumerate(start):
        memory[n].append(i+1)
    
    last = start[-1]
    for i in range(len(start), 30000000):
        if len(memory[last]) > 1:
            x,y = memory[last]
            last = y-x
        else:
            last = 0

        memory[last].append(i+1)

    return last

@pytest.mark.parametrize('data,expect',
    # INSERT TEST CASES HERE
    [('''0,3,6''', 175594),
     ('''1,3,2''', 2578)
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

