from dotenv import load_dotenv; load_dotenv()

import aocd
import pytest
import sys

from parse import parse
from pathlib import Path

from collections import deque
import more_itertools as mit


def parse_deck(string):
    return deque(int(l) for l in string.splitlines()[1:])

def solve(data):
    decks = [parse_deck(p) for p in data.split('\n\n')]

    round = 0
    while all(decks):
        round += 1
        cards = [d.popleft() for d in decks]
        winner = max(range(len(cards)), key=cards.__getitem__)
        decks[winner].extend(sorted(cards, reverse=True))

    winning_deck = mit.first(deck for deck in decks if deck)
    #breakpoint()
    return sum(i*c for i,c in enumerate(reversed(winning_deck), start=1))


@pytest.mark.parametrize('data,expect',
    # INSERT TEST CASES HERE
    [('''Player 1:
9
2
6
3
1

Player 2:
5
8
4
7
10''', 306)
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

