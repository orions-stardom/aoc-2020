import re
from collections import Counter

import more_itertools as mit

directions = {
    'e':  (+1, 0, -1),
    'w':  (-1, 0, +1),
    'se': (0, +1, -1),
    'sw': (-1, +1, 0),
    'ne': (+1, -1, 0),
    'nw': (0, -1, +1)
}

def part_1(data):
    r'''
    >>> part_1("""\
    ... sesenwnenenewseeswwswswwnenewsewsw
    ... neeenesenwnwwswnenewnwwsewnenwseswesw
    ... seswneswswsenwwnwse
    ... nwnwneseeswswnenewneswwnewseswneseene
    ... swweswneswnenwsewnwneneseenw
    ... eesenwseswswnenwswnwnwsewwnwsene
    ... sewnenenenesenwsewnenwwwse
    ... wenwwweseeeweswwwnwwe
    ... wsweesenenewnwwnwsenewsenwwsesesenwne
    ... neeswseenwwswnwswswnw
    ... nenwswwsewswnenenewsenwsenwnesesenew
    ... enewnwewneswsewnwswenweswnenwsenwsw
    ... sweneswneswneneenwnewenewwneswswnese
    ... swwesenesewenwneswnwwneseswwne
    ... enesenwswwswneneswsenwnewswseenwsese
    ... wnwnesenesenenwwnenwsewesewsesesew
    ... nenewswnwewswnenesenwnesewesw
    ... eneswnwswnwsenenwnwnwwseeswneewsenese
    ... neswnwewnwnwseenwseesewsenwsweewe
    ... wseweeenwnesenwwwswnew""")
    10

    '''
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

    return len(tiles)

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

def part_2(data):
    '''
    >>> part_2("""\
    ... sesenwnenenewseeswwswswwnenewsewsw
    ... neeenesenwnwwswnenewnwwsewnenwseswesw
    ... seswneswswsenwwnwse
    ... nwnwneseeswswnenewneswwnewseswneseene
    ... swweswneswnenwsewnwneneseenw
    ... eesenwseswswnenwswnwnwsewwnwsene
    ... sewnenenenesenwsewnenwwwse
    ... wenwwweseeeweswwwnwwe
    ... wsweesenenewnwwnwsenewsenwwsesesenwne
    ... neeswseenwwswnwswswnw
    ... nenwswwsewswnenenewsenwsenwnesesenew
    ... enewnwewneswsewnwswenweswnenwsenwsw
    ... sweneswneswneneenwnewenewwneswswnese
    ... swwesenesewenwneswnwwneseswwne
    ... enesenwswwswneneswsenwnewswseenwsese
    ... wnwnesenesenenwwnenwsewesewsesesew
    ... nenewswnwewswnenesenwnesewesw
    ... eneswnwswnwsenenwnwnwwseeswneewsenese
    ... neswnwewnwnwseenwseesewsenwsweewe
    ... wseweeenwnesenwwwswnew""")
    2208

    '''
    black_tiles = initial(data)
    for _ in range(100):
        black_tiles = evolve(black_tiles)

    return len(black_tiles)

