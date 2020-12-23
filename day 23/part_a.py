from dotenv import load_dotenv; load_dotenv()

import aocd
import pytest
import sys

from parse import parse
from pathlib import Path

class Circle:
    def __init__(self, data):
        self._list = list(map(int,data))

    def index(self, label):
        return self._list.index(label)

    def next(self, label):
        return self._list[(self.index(label) + 1) % len(self._list)]

    def pop3(self, label):
        ret = []
        for _ in range(3):
            # Need to recalc each time because the length will change
            where = (self.index(label) + 1) % len(self._list)
            ret.append(self._list.pop(where))

        ret.reverse()
        return ret

    def insert(self, labels, destlabel):
        dest_ix = (self.index(destlabel) + 1) % len(self._list)
        for label in labels:
            self._list.insert(dest_ix, label)

    def __iter__(self):
        return iter(self._list)

    def __str__(self):
        # Start after label 1, gather everything wrapping around
        ix_one = self.index(1)
        order = self._list[ix_one+1:] + self._list[:ix_one]
        return ''.join(map(str, order))

def solve(data):
    circle = Circle(data)
    current = int(data[0])
    
    for _ in range(100):
        grab = circle.pop3(current)
        try:
            dest = max(label for label in circle if label < current)
        except ValueError:
            dest = max(circle)

        circle.insert(grab, dest)
        current = circle.next(current)
    
    return str(circle)

@pytest.mark.parametrize('data,expect',
    # INSERT TEST CASES HERE
    [('389125467', '67384529'),
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

