from dotenv import load_dotenv; load_dotenv()

import aocd
import pytest
import sys

from parse import parse
from pathlib import Path

import itertools as it
import re

def parse_rules(rules):
    rules = dict(line.replace("'",'').split(": ") for line in rules.splitlines())
    # No rule munging here - matches_rule_0 below hard codes the logic instead
    
    non_terminal = re.compile(r'(\d+)')

    def nt_fill(match):
        return f'({rules[match[0]]})'
    
    while any(non_terminal.search(rule) for rule in rules.values()):
        rules = {i:non_terminal.sub(nt_fill, rule) for i,rule in rules.items()}

    rules = {i: rule.replace(' ', '') for i,rule in rules.items()}

    return rules

def matches_rule_0(r42,r31, message):
    # Need some number of 42s followed by some smaller non-zero number of 31s
    for n_42s in it.count():
        m = r42.match(message)
        if m is None:
            break

        message = message[m.end():]

    for n_31s in it.count():
        m = r31.match(message)
        if m is None:
            break
        message = message[m.end():]

    return not message and n_42s > n_31s > 0
    

def solve(data):
    rules, messages = data.split('\n\n')
    rules = parse_rules(rules)

    r42 = re.compile(rules['42'])
    r31 = re.compile(rules['31'])

    return sum(matches_rule_0(r42, r31, message) for message in messages.splitlines())

@pytest.mark.parametrize('data,expect',
    # INSERT TEST CASES HERE
    [('''42: 9 14 | 10 1
9: 14 27 | 1 26
10: 23 14 | 28 1
1: "a"
11: 42 31
5: 1 14 | 15 1
19: 14 1 | 14 14
12: 24 14 | 19 1
16: 15 1 | 14 14
31: 14 17 | 1 13
6: 14 14 | 1 14
2: 1 24 | 14 4
0: 8 11
13: 14 3 | 1 12
15: 1 | 14
17: 14 2 | 1 7
23: 25 1 | 22 14
28: 16 1
4: 1 1
20: 14 14 | 1 15
3: 5 14 | 16 1
27: 1 6 | 14 18
14: "b"
21: 14 1 | 1 14
25: 1 1 | 1 14
22: 14 14
8: 42
26: 14 22 | 1 20
18: 15 15
7: 14 5 | 1 21
24: 14 1

abbbbbabbbaaaababbaabbbbabababbbabbbbbbabaaaa
bbabbbbaabaabba
babbbbaabbbbbabbbbbbaabaaabaaa
aaabbbbbbaaaabaababaabababbabaaabbababababaaa
bbbbbbbaaaabbbbaaabbabaaa
bbbababbbbaaaaaaaabbababaaababaabab
ababaaaaaabaaab
ababaaaaabbbaba
baabbaaaabbaaaababbaababb
abbbbabbbbaaaababbbbbbaaaababb
aaaaabbaabaaaaababaa
aaaabbaaaabbaaa
aaaabbaabbaaaaaaabbbabbbaaabbaabaaa
babaaabbbaaabaababbaabababaaab
aabbbbbaabbbaaaaaabbbbbababaaaaabbaaabba''', 12)

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

