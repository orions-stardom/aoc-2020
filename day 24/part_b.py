from dotenv import load_dotenv; load_dotenv()

import aocd
import pytest
import sys

from parse import parse
from pathlib import Path

import re
import more_itertools as mit
from collections import Counter

directions = {
    'e':  (+1, 0, -1),
    'w':  (-1, 0, +1),
    'se': (0, +1, -1),
    'sw': (-1, +1, 0),
    'ne': (+1, -1, 0),
    'nw': (0, -1, +1)
}


def initial(data):
    tiles = set()
    instructions = re.compile('|'.join(directions))
    for line in data.splitlines():
        tile = (0, 0, 0)
        for d in instructions.findall(line):
            tile = tuple(c1+c2 for c1,c2 in zip(tile, directions[d]))

        if tile in tiles:
            tiles.discard(tile)
        else:
            tiles.add(tile)

    return tiles

def neighbours(tile):
    return (tuple(c1+c2 for c1,c2 in zip(tile,d)) for d in directions.values())

def evolve(tiles):
    new_tiles = set()
    white_tiles = Counter()

    for tile in tiles:
        white_neighbours, black_neighbours = mit.partition(tiles.__contains__, neighbours(tile))
        white_tiles.update(white_neighbours)

        if 0 < mit.ilen(black_neighbours) <= 2:
            new_tiles.add(tile)

    new_tiles.update(t for t in white_tiles if white_tiles[t] == 2)
    return new_tiles

def solve(data):
    black_tiles = initial(data)
    for _ in range(100):
        black_tiles = evolve(black_tiles)

    return len(black_tiles)

@pytest.mark.parametrize('data,expect',
    # INSERT TEST CASES HERE
    [('''sesenwnenenewseeswwswswwnenewsewsw
neeenesenwnwwswnenewnwwsewnenwseswesw
seswneswswsenwwnwse
nwnwneseeswswnenewneswwnewseswneseene
swweswneswnenwsewnwneneseenw
eesenwseswswnenwswnwnwsewwnwsene
sewnenenenesenwsewnenwwwse
wenwwweseeeweswwwnwwe
wsweesenenewnwwnwsenewsenwwsesesenwne
neeswseenwwswnwswswnw
nenwswwsewswnenenewsenwsenwnesesenew
enewnwewneswsewnwswenweswnenwsenwsw
sweneswneswneneenwnewenewwneswswnese
swwesenesewenwneswnwwneseswwne
enesenwswwswneneswsenwnewswseenwsese
wnwnesenesenenwwnenwsewesewsesesew
nenewswnwewswnenesenwnesewesw
eneswnwswnwsenenwnwnwwseeswneewsenese
neswnwewnwnwseenwseesewsenwsweewe
wseweeenwnesenwwwswnew''', 2208)  
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

