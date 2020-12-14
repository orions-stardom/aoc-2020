from dotenv import load_dotenv; load_dotenv()

import aocd
import pytest
import sys

from parse import parse
from pathlib import Path

from collections import defaultdict

def solve(data):
    mem = defaultdict(int)
    for line in data.splitlines():
        where, val = line.split(' = ')
        if where == 'mask':
            zeroes = int(val.replace('X', '1'), 2)
            ones = int(val.replace('X', '0'), 2)
        else:
            n = parse('mem[{:d}]', where)[0]
            mem[n] = (int(val) & zeroes) | ones

    return sum(mem.values())

@pytest.mark.parametrize('data,expect',
    # INSERT TEST CASES HERE
    [('''mask = XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X
mem[8] = 11
mem[7] = 101
mem[8] = 0''', 165)])
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

