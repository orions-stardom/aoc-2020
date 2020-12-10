from dotenv import load_dotenv; load_dotenv()

import aocd
import pytest
import sys

from parse import parse
from pathlib import Path

import functools
import itertools as it

@functools.lru_cache()
def count_ways(available, most_recent):
    # Recursively build up 'where can we go from here with what we have left'
    # Since the target is always biggest adapter we have + 3, we always have to use the biggest adapter
    # and our only end condition is when we've reached it
    if not available:
        return 1

    return sum(count_ways(available[i+1:], c) for i,c in enumerate(it.takewhile((lambda c: c - most_recent <= 3), available)))
    

def solve(data):
    available = sorted(int(l) for l in data.splitlines())
    return count_ways(tuple(available), 0)

@pytest.mark.parametrize('data,expect',
    # INSERT TEST CASES HERE
    [('''16
10
15
5
1
11
7
19
6
12
4''', 8),
('''28
33
18
42
31
14
46
20
48
47
24
23
49
45
19
38
39
11
1
32
25
35
8
17
7
9
4
2
34
10
3''', 19208)
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

