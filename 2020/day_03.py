import itertools as it
from math import prod


def part_1(data):
    r'''
    >>> part_1("""\
    ... ..##.......
    ... #...#...#..
    ... .#....#..#.
    ... ..#.#...#.#
    ... .#...##..#.
    ... ..#.##.....
    ... .#.#.#....#
    ... .#........#
    ... #.##...#...
    ... #...##....#
    ... .#..#...#.#""")
    7
    '''
    grid = [line.strip() for line in data.splitlines()]
    width, height = len(grid[0]), len(grid)

    x_motion = it.islice(it.cycle(range(width)), None, None, 3)
    y_motion = range(height)
    return sum(grid[y][x] == '#' for x,y in zip(x_motion, y_motion))


def part_2(data):
    r'''
    >>> part_2("""\
    ... ..##.......
    ... #...#...#..
    ... .#....#..#.
    ... ..#.#...#.#
    ... .#...##..#.
    ... ..#.##.....
    ... .#.#.#....#
    ... .#........#
    ... #.##...#...
    ... #...##....#
    ... .#..#...#.#""")
    336
    '''
    def count_trees(grid, dx, dy):
        width, height = len(grid[0]), len(grid)
        x_motion = it.islice(it.cycle(range(width)), None, None, dx)
        y_motion = range(height)[::dy]
        return sum(grid[y][x] == '#' for x,y in zip(x_motion, y_motion))

    grid = [line.strip() for line in data.splitlines()]
    return prod(count_trees(grid, *grad) for grad in [(1,1),(3,1),(5,1),(7,1),(1,2)])
