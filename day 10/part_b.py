from dotenv import load_dotenv; load_dotenv()

import aocd
import pytest
import sys

from parse import parse
from pathlib import Path

import functools

@functools.lru_cache()
def count_ways(all_available, target, i_most_recent):
    most_recent = all_available[i_most_recent]
    still_available = all_available[i_most_recent+1:]

    if not still_available:
        return 1

    next_candidates = [i for i,c in enumerate(still_available, start=i_most_recent+1) if c - most_recent <= 3]
    return sum(count_ways(all_available, target, i) for i in next_candidates)
    

def solve(data):
    available = [0] + [int(l) for l in data.splitlines()]
    available.sort()
    target = max(available)+3

    return count_ways(tuple(available), target, 0)

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

