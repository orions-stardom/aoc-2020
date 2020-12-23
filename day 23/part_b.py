from dotenv import load_dotenv; load_dotenv()

import aocd
import pytest
import sys

from parse import parse
from pathlib import Path

from dataclasses import dataclass
from dataslots import dataslots
import more_itertools as mit

@dataslots
@dataclass
class Node:
    value: int
    next: 'Node' = None
    previous: 'Node' = None

class Circle:
    def __init__(self, data, end=1_000_000):
        self.end = end
        initial = [int(x) for x in data]

        self.lookup = tuple(Node(i) for i in range(1, end+1))
        for x,y in mit.pairwise(initial):
            self[x].next = self[y]
            self[y].previous = self[x]
        
        if end > max(initial):
            high = max(initial)+1
            self[initial[-1]].next = self[high]
            self[high].previous = self[initial[-1]]

            for label in range(high, end):
                self[label].next = self[label+1]
                self[label+1].previous = self[label]

            self[initial[0]].previous = self[end]
            self[end].next = self[initial[0]]
        else:
            self[initial[-1]].next = self[initial[0]]
            self[initial[0]].previous = self[initial[-1]]

        self.current = self[initial[0]]

    def __getitem__(self, label):
        return self.lookup[label - 1]

    def next(self, label):
        return self[current].next


    def do_move(self):
        pickup = [self.current.next, self.current.next.next, self.current.next.next.next]
        current= self.current
        
        dest_label = self.current.value - 1 or self.end
        while self[dest_label] in pickup:
            dest_label = dest_label - 1 or self.end

        ins_after =  self[dest_label]
        ins_before = ins_after.next
        next = pickup[-1].next

        self.current.next, next.previous, pickup[0].previous, pickup[-1].next, ins_after.next, ins_before.previous =\
            pickup[-1].next, pickup[0].previous, ins_before.previous, ins_after.next, self.current.next, next.previous

        self.current = self.current.next

    def __iter__(self):
        yield self.current
        next = self.current.next
        while next != self.current:
            yield next
            next = next.next

    def __str__(self):
        # Start after label 1, gather everything wrapping around
        vals = []
        curr = self[1].next
        while curr.value != 1:
            vals.append(curr.value)
            curr = curr.next

        return ''.join(map(str,vals))
        


def solve(data):
    circle = Circle(data)

    for _ in range(10_000_000):
        circle.do_move()
  
    return circle[1].next.value * circle[1].next.next.value

@pytest.mark.parametrize('data,expect',
    # INSERT TEST CASES HERE
    [('389125467', 149245887792),
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

