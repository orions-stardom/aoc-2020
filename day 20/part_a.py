from dotenv import load_dotenv; load_dotenv()

import aocd
import pytest
import sys

from parse import parse
from pathlib import Path

import itertools as it
import numpy as np

import math

def parse_all(pattern, it):
    return (parse(pattern, thing) for thing in it)

def all_edges(tile):
    yield tile[:,0]
    yield tile[:,-1]
    yield tile[0,:]
    yield tile[-1,:]

def edges_in_common(tile, other):
    return sum((edge == other_edge).all() or (edge[::-1] == other_edge).all()
               for edge, other_edge in it.product(all_edges(tile), all_edges(other)))

def count_edge_matches(tile, all_tiles):
    return sum(edges_in_common(tile, other) for other in all_tiles if tile is not other)

def solve(data):
    parsed=list(parse_all('Tile: {:n}:\n{}', data.split('\n\n')))
    tiles = {int(num): np.array(list(tile.replace('\n',''))).reshape(10,10) 
             for num, tile in parse_all('Tile {:d}:\n{}', data.split('\n\n'))}
    corners = [tile for tile in tiles if count_edge_matches(tiles[tile], tiles.values()) == 2]
    return math.prod(corners)

@pytest.mark.parametrize('data,expect',
    # INSERT TEST CASES HERE
    [('''Tile 2311:
..##.#..#.
##..#.....
#...##..#.
####.#...#
##.##.###.
##...#.###
.#.#.#..##
..#....#..
###...#.#.
..###..###

Tile 1951:
#.##...##.
#.####...#
.....#..##
#...######
.##.#....#
.###.#####
###.##.##.
.###....#.
..#.#..#.#
#...##.#..

Tile 1171:
####...##.
#..##.#..#
##.#..#.#.
.###.####.
..###.####
.##....##.
.#...####.
#.##.####.
####..#...
.....##...

Tile 1427:
###.##.#..
.#..#.##..
.#.##.#..#
#.#.#.##.#
....#...##
...##..##.
...#.#####
.#.####.#.
..#..###.#
..##.#..#.

Tile 1489:
##.#.#....
..##...#..
.##..##...
..#...#...
#####...#.
#..#.#.#.#
...#.#.#..
##.#...##.
..##.##.##
###.##.#..

Tile 2473:
#....####.
#..#.##...
#.##..#...
######.#.#
.#...#.#.#
.#########
.###.#..#.
########.#
##...##.#.
..###.#.#.

Tile 2971:
..#.#....#
#...###...
#.#.###...
##.##..#..
.#####..##
.#..####.#
#..#.#..#.
..####.###
..#.#.###.
...#.#.#.#

Tile 2729:
...#.#.#.#
####.#....
..#.#.....
....#..#.#
.##..##.#.
.#.####...
####.#.#..
##.####...
##..#.##..
#.##...##.

Tile 3079:
#.#.#####.
.#..######
..#.......
######....
####.#..#.
.#...#.##.
#.#####.##
..#.###...
..#.......
..#.###...''', 20899048083289)
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

