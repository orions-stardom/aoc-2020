from dotenv import load_dotenv; load_dotenv()

import aocd
import pytest
import sys

from parse import parse
from pathlib import Path

import itertools as it

import math

def solve(data):
    rules, mine, nearby = data.split('\n\n')

    rules = {cname: (range(l1, h1+1), range(l2,h2+1)) 
                     for cname, l1,h1,l2,h2 in 
             (parse('{}: {:d}-{:d} or {:d}-{:d}', line) for line in rules.splitlines())}

    mine = [int(x) for x in mine.splitlines()[1].split(',')]
    nearby = [[int(x) for x in line.split(',')] for line in nearby.splitlines()[1:]]

    mine = parse_my_ticket(rules, mine, nearby)

    return math.prod(v for k,v in mine if k.startswith('departure'))


def parse_my_ticket(rules, mine, nearby):
    valid = [ticket for ticket in nearby if
             all(any(val in r for r in it.chain.from_iterable(rules.values())) for val in ticket)]

    for candidate_field_map in it.permutations(rules):
        if all(ticket[i] in rules[fname][0] or ticket[i] in rules[fname][1] 
               for ticket in valid
               for i, fname in enumerate(candidate_field_map)):

            field_map = candidate_field_map
            break

    else:
        assert False, 'no possible orderings work'

    return {fname: mine[i] for i, fname in enumerate(field_map)}


@pytest.mark.parametrize('rules,mine,nearby,expect',
    # INSERT TEST CASES HERE
    [({'class': (range(0,2), range(4,19)),
        'row':  (range(0,6), range(8,20)),
        'seat': (range(0, 13), range(16,20)) },
    [11,12,13],
    [[3,9,18],[15,1,5], [5,14,9]], 
    {'class': 12, 'row': 11, 'seat': 13} )
    ])
def test_parse(rules, mine, nearby, expect):
    assert parse_my_ticket(rules, mine, nearby) == expect

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
    aocd.submit(solution, year=year, day=day, part='b', reopen=False)

