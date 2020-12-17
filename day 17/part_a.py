from dotenv import load_dotenv; load_dotenv()

import aocd
import pytest
import sys

from parse import parse
from pathlib import Path

import itertools as it
import more_itertools as mit

class Grid:
    @staticmethod
    def neighbours(coord):
        x,y,z = coord
        for i in it.product((x-1,x,x+1),(y-1,y,y+1),(z-1,z,z+1)):
            if i == coord: continue
            yield i

    @classmethod
    def parse(cls, initial):
        new = Grid()
        for y,row in enumerate(initial.splitlines()):
            for x,node in enumerate(row):
                if node == '#':
                    new.active.add((x,y,0))

        return new

    def __init__(self):
        self.active = set()

    def __len__(self):
        return len(self.active)

    def next(self):
        new = Grid()
        inactive_seen = set()
        for node in self.active:
            inactive, active = mit.partition(self.active.__contains__,Grid.neighbours(node))
            if mit.ilen(active) in (2,3):
                new.active.add(node)
            for neighbour in set(inactive) - self.active - inactive_seen:
                inactive_seen.add(neighbour)
                if len(set(Grid.neighbours(neighbour)) & self.active) == 3:
                    new.active.add(neighbour)
        return new

    def __str__(self):
        lines = []
        for z in range(min(c[2] for c in self.active), max(c[2] for c in self.active)+1):
            plane = {c for c in self.active if c[2] == z}
            lines.append(f'z={z}')
            for y in range(min(c[1] for c in plane), max(c[1] for c in plane)+1):
                line = []
                for x in range(min(c[0] for c in plane), max(c[0] for c in plane)+1):
                    line.append('#' if (x,y,z) in self.active else '.')
                lines.append(''.join(line))
            lines.append('')
        return '\n'.join(lines)

def solve(data):
    grid = Grid.parse(data)
    final = mit.nth(mit.iterate(Grid.next, grid), 6)
    return len(final)

@pytest.mark.parametrize('data,expect',
    # INSERT TEST CASES HERE
    [('''.#.
..#
###''', 112)
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

