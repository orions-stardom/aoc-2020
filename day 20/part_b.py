from dotenv import load_dotenv; load_dotenv()

import aocd
import pytest
import sys

from parse import parse
from pathlib import Path

import collections

import itertools as it
import more_itertools as mit
import numpy as np

from typing import NamedTuple

import math

class Tile:
    @classmethod
    def parse(cls, id, string):
        rows, cols = len(string.splitlines()), len(string.splitlines()[0])
        data = np.array(list(string.replace('\n',''))).reshape(rows, cols) 
        return cls(id, data)

    def __init__(self, id, data):
        self.id = id
        self.data = data

        self._neighbours = Neighbour(None,None,None,None)


    def __repr__(self):
        return f'Tile {self.id}'
    @property
    def neighbours(self):
        return sum(n is not None for n in self._neighbours)

    @property
    def bottom_neighbour(self):
        below = self.all_tiles.get(self._neighbours.down, None)
        if below == None or self.bottom == below.top:
            return below

        for cand in below.orientations:
            if self.bottom == cand.top:
                return cand

        assert False, 'impossible'

    @property
    def right_neighbour(self):
        right = self.all_tiles.get(self._neighbours.right, None)
        if right == None or self.right == right.left:
            return right

        for cand in right.orientations:
            if self.right == cand.left:
                return cand

        assert False, 'impossible'

    @property
    def top(self):
        return Edge(self.data[0,:])

    @property
    def bottom(self):
        return Edge(self.data[-1,:])

    @property
    def left(self):
        return Edge(self.data[:,0])

    @property
    def right(self):
        return Edge(self.data[:,-1])

    @property
    def orientations(self):
        data = self.data
        neighbours = self._neighbours
        for _ in range(4):
            data = np.rot90(data)
            neighbours = neighbours.rotate()

            new_tile = Tile(self.id, data)
            new_tile._neighbours = neighbours
            yield new_tile

            # At each rotation, we can flip left-to-right, top-to-bottom
            # or both at once
            for newdata, newneighbours in (np.flip(data),  neighbours.flip()),\
                                          (np.flipud(data),neighbours.flipud()),\
                                          (np.fliplr(data),neighbours.fliplr()):
                new_tile = Tile(self.id, newdata)
                new_tile._neighbours = newneighbours
                yield new_tile

    def __str__(self):
        return '\n'.join(''.join(row) for row in self.data)

class Edge:
    def __init__(self, data):
        self.data = data

    def __eq__(self, other):
        return np.array_equal(self.data, other.data)

class Neighbour(NamedTuple):
    up: Tile
    left: Tile
    down: Tile
    right: Tile

    def rotate(self):
        '''Rotate anticlockwise 90 degrees'''
        return self._replace(left=self.up,up=self.right,right=self.down,down=self.left)

    def fliplr(self):
        return self._replace(left=self.right, right=self.left)

    def flipud(self):
        return self._replace(up=self.down, down=self.up)

    def flip(self):
        return self._replace(up=self.down, down=self.up, left=self.right, right=self.left)



def parse_all(pattern, it):
     return (parse(pattern, thing) for thing in it)

def calculate_neighbours(tiles):
    # Each tile only carries the id of its neighbour, which is an index into this dict
    # This indirection is needed because when we identify the neighbour we don't necesarily
    # have all of the other neighbours, so a direct reference to the neighbour could go stale.
    # So the tiles need to know about the dict, and we edit the values in there to appropriately 
    # updates tiles.
    # Don't do this at home
    Tile.all_tiles = tiles

    for ida,idb in it.combinations(tiles, 2):
        for orienta, orientb in it.product(tiles[ida].orientations, tiles[idb].orientations):
            if orienta.right == orientb.left:
                orienta._neighbours = orienta._neighbours._replace(right=idb)
                orientb._neighbours = orientb._neighbours._replace(left=ida)
                tiles[ida] = orienta
                tiles[idb] = orientb

                break

sea_monster_string = \
'''                  # 
#    ##    ##    ###
 #  #  #  #  #  #   '''

def solve(data):
    parsed=list(parse_all('Tile: {:n}:\n{}', data.split('\n\n')))
    tiles = {int(num): Tile.parse(int(num),tile) for num, tile in parse_all('Tile {:d}:\n{}', data.split('\n\n'))}
    
    Tile.all_tiles = tiles
    calculate_neighbours(tiles)
    
    # We don't know the orientation of the picture yet, so just 
    # pick any corner piece and declare it to be the top left
    top_left = mit.first(tiles[c] for c in tiles if tiles[c].neighbours == 2)

    # and put it around the right way
    oriented_top_left = mit.first(o for o in top_left.orientations if None not in (o.bottom_neighbour, o.right_neighbour))
    
    side_length = int(math.sqrt(len(tiles)))

    rows = []
    start = oriented_top_left
    while len(rows) < side_length:
        row = [start]
        while len(row) < side_length:
            row.append(row[-1].right_neighbour)
        
        start = row[0].bottom_neighbour
        # Strip borders of placed tiles
        rows.append(np.hstack([r.data[1:-1,1:-1] for r in row]))
    
    picture = Tile('picture', np.vstack(rows))

    sea_monster = Tile.parse('AHHH!', sea_monster_string)
    n_seamonsters = sum(((sea_monster.data == ' ') | (sea_monster.data == window)).all() 
                        for opicture in picture.orientations
                        for window in np_windows(opicture.data, sea_monster.data.shape)
                        )

    # The above seems to reliably double count all the sea monsters and I don't really
    # know why..
    return (picture.data == '#').sum() - (sea_monster.data == '#').sum()*int(n_seamonsters / 2)
   
def np_windows(data, shape):
    # This is horrible and there's lots of vectorised solutions on the internet
    # but I didn't understand how to use them
    w_height, w_width = shape
    d_height, d_width = data.shape
    for y in range(d_height - w_height):
        for x in range(d_width - w_width):
            yield data[y:y+w_height,x:x+w_width]


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
..#.###...''', 273)
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

