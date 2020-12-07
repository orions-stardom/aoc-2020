from dotenv import load_dotenv; load_dotenv()

import aocd
import pytest
import sys

from parse import parse
from pathlib import Path

from collections import defaultdict 

def parse_rules(data):
    rules = defaultdict(lambda: defaultdict(int))
    for rule in data.splitlines():
        outer_name, content = rule.split(' contain ')
        outer_name = outer_name.rsplit(' ', 1)[0]
        if content == "no other bags":
            continue

        
        for c in content.split(', '):
            c = c.rsplit(' ', 1)[0]
            n, inner_name = c.split(' ', 1)
            if not n.isdigit():
                # bag type contains no other bags
                continue
    
            rules[outer_name][inner_name] = int(n)

    return rules

def containments(rules, target, current):
    possibilities = [bag for bag in rules if target in rules[bag]]
    
    for possibility in possibilities:
        yield current+[possibility]
        yield from containments(rules, possibility, current+[possibility])

def solve(data):
    rules = parse_rules(data)
    ways = list(containments(rules, 'shiny gold', []))
    from pprint import pprint; pprint(ways)
    return len(set(way[-1] for way in ways)) # Only count unique outermost bags

@pytest.mark.parametrize('data,expect',
    # INSERT TEST CASES HERE
    [('''light red bags contain 1 bright white bag, 2 muted yellow bags.
dark orange bags contain 3 bright white bags, 4 muted yellow bags.
bright white bags contain 1 shiny gold bag.
muted yellow bags contain 2 shiny gold bags, 9 faded blue bags.
shiny gold bags contain 1 dark olive bag, 2 vibrant plum bags.
dark olive bags contain 3 faded blue bags, 4 dotted black bags.
vibrant plum bags contain 5 faded blue bags, 6 dotted black bags.
faded blue bags contain no other bags.
dotted black bags contain no other bags.''', 4)
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

