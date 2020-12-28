import regex
from parse import parse

def part_1(data):
    r'''
    >>> part_1("""\
    ... 0: 4 1 5
    ... 1: 2 3 | 3 2
    ... 2: 4 4 | 5 5
    ... 3: 4 5 | 5 4
    ... 4: "a"
    ... 5: "b"
    ... 
    ... ababbb
    ... bababa
    ... abbbab
    ... aaabbb
    ... aaaabbb""")
    2

    '''

    def parse_rules(rules_lines):
        rules = [None] * len(rules_lines)

        for line in rules_lines:
            num, rule = parse("{:d}: {}", line)
            rules[num] = rule

        non_terminal = regex.compile(r'(\d+)')

        def nt_fill(match):
            sym = int(match[0])
            return f'({rules[sym]})' if rules[sym] is not None else sym
        while non_terminal.search(rules[0]) is not None:
            rules = [non_terminal.sub(nt_fill, rule) for rule in rules]

        rule = ''.join(c for c in rules[0] if not c.isspace() and c != '"')
        return regex.compile(rule)

    rules_string, messages = data.split('\n\n')
    rule_0 = parse_rules(rules_string.splitlines())
    return sum(rule_0.fullmatch(message) is not None for message in messages.splitlines())

def part_2(data):
    r'''
    part_2("""\
    ... 42: 9 14 | 10 1
    ... 9: 14 27 | 1 26
    ... 10: 23 14 | 28 1
    ... 1: "a"
    ... 11: 42 31
    ... 5: 1 14 | 15 1
    ... 19: 14 1 | 14 14
    ... 12: 24 14 | 19 1
    ... 16: 15 1 | 14 14
    ... 31: 14 17 | 1 13
    ... 6: 14 14 | 1 14
    ... 2: 1 24 | 14 4
    ... 0: 8 11
    ... 13: 14 3 | 1 12
    ... 15: 1 | 14
    ... 17: 14 2 | 1 7
    ... 23: 25 1 | 22 14
    ... 28: 16 1
    ... 4: 1 1
    ... 20: 14 14 | 1 15
    ... 3: 5 14 | 16 1
    ... 27: 1 6 | 14 18
    ... 14: "b"
    ... 21: 14 1 | 1 14
    ... 25: 1 1 | 1 14
    ... 22: 14 14
    ... 8: 42
    ... 26: 14 22 | 1 20
    ... 18: 15 15
    ... 7: 14 5 | 1 21
    ... 24: 14 1
    ... 
    ... abbbbbabbbaaaababbaabbbbabababbbabbbbbbabaaaa
    ... bbabbbbaabaabba
    ... babbbbaabbbbbabbbbbbaabaaabaaa
    ... aaabbbbbbaaaabaababaabababbabaaabbababababaaa
    ... bbbbbbbaaaabbbbaaabbabaaa
    ... bbbababbbbaaaaaaaabbababaaababaabab
    ... ababaaaaaabaaab
    ... ababaaaaabbbaba
    ... baabbaaaabbaaaababbaababb
    ... abbbbabbbbaaaababbbbbbaaaababb
    ... aaaaabbaabaaaaababaa
    ... aaaabbaaaabbaaa
    ... aaaabbaabbaaaaaaabbbabbbaaabbaabaaa
    ... babaaabbbaaabaababbaabababaaab
    ... aabbbbbaabbbaaaaaabbbbbababaaaaabbaaabba""")
    12

    '''
    def parse_rules(rules):
        rules = dict(line.replace('"','').split(': ') for line in rules.splitlines())
        # No rule munging here - matches_rule_0 below hard codes the logic instead
        
        non_terminal = regex.compile(r'(\d+)')

        def nt_fill(match):
            return f'({rules[match[0]]})'
        
        while any(non_terminal.search(rule) for rule in rules.values()):
            rules = {i:non_terminal.sub(nt_fill, rule) for i,rule in rules.items()}

        rules = {i: rule.replace(' ', '') for i,rule in rules.items()}

        return rules

    def matches_rule_0(rules, message):
        # Need some number of 42s followed by some smaller non-zero number of 31s
        m = regex.fullmatch(f"(?P<fourtytwo>{rules['42']}){{2,}}(?P<thirtyone>{rules['31']})+", message)

        if m is None:
            return False
        
        matches = m.capturesdict()
        return len(matches['fourtytwo']) > len(matches['thirtyone'])

    rules, messages = data.split('\n\n')
    rules = parse_rules(rules)
    return sum(matches_rule_0(rules, message) for message in messages.splitlines())
