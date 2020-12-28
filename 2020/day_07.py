
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

def part_1(data):
    r'''
    >>> part_1("""\
    ... light red bags contain 1 bright white bag, 2 muted yellow bags.
    ... dark orange bags contain 3 bright white bags, 4 muted yellow bags.
    ... bright white bags contain 1 shiny gold bag.
    ... muted yellow bags contain 2 shiny gold bags, 9 faded blue bags.
    ... shiny gold bags contain 1 dark olive bag, 2 vibrant plum bags.
    ... dark olive bags contain 3 faded blue bags, 4 dotted black bags.
    ... vibrant plum bags contain 5 faded blue bags, 6 dotted black bags.
    ... faded blue bags contain no other bags.
    ... dotted black bags contain no other bags.""")
    4
    '''
    rules = parse_rules(data)
    ways = list(containments(rules, 'shiny gold', []))
    return len(set(way[-1] for way in ways)) # Only count unique outermost bags

def n_contained(rules, start):
    direct = rules[start]
    total = sum(direct.values())+ sum(rules[start][bag] * n_contained(rules, bag) for bag in direct)
    return total

def part_2(data):
    r'''
    >>> part_2("""\
    ... light red bags contain 1 bright white bag, 2 muted yellow bags.
    ... dark orange bags contain 3 bright white bags, 4 muted yellow bags.
    ... bright white bags contain 1 shiny gold bag.
    ... muted yellow bags contain 2 shiny gold bags, 9 faded blue bags.
    ... shiny gold bags contain 1 dark olive bag, 2 vibrant plum bags.
    ... dark olive bags contain 3 faded blue bags, 4 dotted black bags.
    ... vibrant plum bags contain 5 faded blue bags, 6 dotted black bags.
    ... faded blue bags contain no other bags.
    ... dotted black bags contain no other bags.""")
    32

    >>> part_2("""\
    ... shiny gold bags contain 2 dark red bags.
    ... dark red bags contain 2 dark orange bags.
    ... dark orange bags contain 2 dark yellow bags.
    ... dark yellow bags contain 2 dark green bags.
    ... dark green bags contain 2 dark blue bags.
    ... dark blue bags contain 2 dark violet bags.
    ... dark violet bags contain no other bags.""")
    126
    '''
    rules = parse_rules(data)
    return n_contained(rules, 'shiny gold')
