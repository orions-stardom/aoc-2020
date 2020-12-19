from dotenv import load_dotenv; load_dotenv()

import aocd
import pytest
import sys

from parse import parse
from pathlib import Path

import re

def parse_rules(rules_lines):
    rules = [None] * len(rules_lines)

    for line in rules_lines:
        num, rule = parse("{:d}: {}", line)
        rules[num] = rule

    non_terminal = re.compile(r'(\d+)')

    def nt_fill(match):
        sym = int(match[0])
        return f'({rules[sym]})' if rules[sym] is not None else sym
    while non_terminal.search(rules[0]) is not None:
        rules = [non_terminal.sub(nt_fill, rule) for rule in rules]

    rule = ''.join(c for c in rules[0] if not c.isspace() and c != '"')
    return re.compile(rule)

def solve(data):
    rules_string, messages = data.split('\n\n')
    rule_0 = parse_rules(rules_string.splitlines())
    return sum(rule_0.fullmatch(message) is not None for message in messages.splitlines())

@pytest.mark.parametrize('data,expect',
    # INSERT TEST CASES HERE
    [('''0: 4 1 5
1: 2 3 | 3 2
2: 4 4 | 5 5
3: 4 5 | 5 4
4: "a"
5: "b"

ababbb
bababa
abbbab
aaabbb
aaaabbb''', 2)
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

