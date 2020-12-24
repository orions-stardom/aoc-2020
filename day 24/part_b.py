from dotenv import load_dotenv; load_dotenv()

import aocd
import pytest
import sys

from parse import parse
from pathlib import Path

import re

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
    return {tuple(c1+c2 for c1,c2 in zip(tile,d)) for d in directions.values()}

def all_neighbours(tiles):
    return tiles.union(*(neighbours(t) for t in tiles)) 

def evolve(black_tiles):
    new_tiles = black_tiles.copy()

    for tile in all_neighbours(black_tiles):
        black_neighbours = len(neighbours(tile) & black_tiles)

        if tile in black_tiles and (black_neighbours == 0 or black_neighbours > 2):
            new_tiles.remove(tile)

        if tile not in black_tiles and black_neighbours == 2:
            new_tiles.add(tile)
    
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

