from dotenv import load_dotenv; load_dotenv()

import aocd
import pytest
import sys

from parse import parse
from pathlib import Path
import itertools as it

def prod(vals): # py < 3.8
    ret = 1
    for val in vals:
        ret *= val
    return ret

def solve(data):
    grid = [line.strip() for line in data.splitlines()]

    return prod(count_trees(grid, *grad) for grad in [(1,1),(3,1),(5,1),(7,1),(1,2)])


def count_trees(grid, dx, dy):
    width, height = len(grid[0]), len(grid)
    x_motion = it.islice(it.cycle(range(width)), None, None, dx)
    y_motion = range(height)[::dy]
    return sum(grid[y][x] == '#' for x,y in zip(x_motion, y_motion))

@pytest.mark.parametrize('data,expect',
    # INSERT TEST CASES HERE
    [('''..##.......
    #...#...#..
    .#....#..#.
    ..#.#...#.#
    .#...##..#.
    ..#.##.....
    .#.#.#....#
    .#........#
    #.##...#...
    #...##....#
    .#..#...#.#''', 336)
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

