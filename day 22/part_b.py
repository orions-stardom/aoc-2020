from dotenv import load_dotenv; load_dotenv()

import aocd
import pytest
import sys

from parse import parse
from pathlib import Path

from collections import deque
import more_itertools as mit

import copy

def parse_deck(string):
    return deque(int(l) for l in string.splitlines()[1:])

def score(deck):
    return sum(i*c for i,c in enumerate(reversed(deck), start=1))

def solve(data):
    if isinstance(data, str):
        decks = [parse_deck(p) for p in data.split('\n\n')]
        calc_score = True
    else:
        decks = data
        calc_score = False

    seen_states = set()

    while all(decks):
        state = tuple(score(deck) for deck in decks)
        if state in seen_states:
            winning_deck = 0
            break
        
        seen_states.add(state)
        
        cards = [d.popleft() for d in decks]

        if all(len(deck) >= card for card,deck in zip(cards,decks)):
            # Play a recursive game
            winner = solve([deque(list(deck)[:val]) for deck, val in zip(decks,cards)])
        else:
            winner = max(range(len(cards)), key=cards.__getitem__)

        decks[winner].extend(cards if winner == 0 else reversed(cards))
    else:
        winning_deck = mit.first(ideck for ideck in range(len(decks)) if decks[ideck])
    
    if calc_score:
        #breakpoint()
        return score(decks[winning_deck])
    else:
        return winning_deck


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
10''', 291),
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

