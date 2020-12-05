from dotenv import load_dotenv; load_dotenv()

import aocd
import pytest
import sys

from parse import parse
from pathlib import Path

def seat_id(directions):
    row_dir, column_dir = directions[:7],directions[7:]

    row = int(row_dir.replace('F', '0').replace('B', '1'), 2)
    col = int(column_dir.replace('L', '0').replace('R', '1'), 2)
    
    return row*8 + col

def solve(data):
    return max(seat_id(line) for line in data.splitlines())

@pytest.mark.parametrize('data,expect',
    # INSERT TEST CASES HERE
    [('BFFFBBFRRR', 567),
     ('FFFBBBFRRR', 119),
     ('BBFFBBFRLL', 820)
    ])
def test_solve(data, expect):
    assert seat_id(data) == expect

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

