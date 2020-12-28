import itertools as it
import more_itertools as mit

from parse import parse


def part_1(data):
    r'''
    >>> part_1("""\
    ... class: 1-3 or 5-7
    ... row: 6-11 or 33-44
    ... seat: 13-40 or 45-50
    ... 
    ... your ticket:
    ... 7,1,14
    ... 
    ... nearby tickets:
    ... 7,3,47
    ... 40,4,50
    ... 55,2,20
    ... 38,6,12""")
    71

    '''
    rules, mine, nearby = data.split('\n\n')

    rules = {cname: (range(l1, h1+1), range(l2,h2+1)) 
                     for cname, l1,h1,l2,h2 in 
                     (parse('{}: {:d}-{:d} or {:d}-{:d}', line) for line in rules.splitlines())}

    nearby = [[int(x) for x in line.split(',')] for line in nearby.splitlines()[1:]]

    return sum(val for ticket in nearby for val in ticket if not any(val in r for r in it.chain.from_iterable(rules.values())))


def part_2(data):
    rules, mine, nearby = data.split('\n\n')

    rules = {cname: (range(l1, h1+1), range(l2,h2+1)) 
                     for cname, l1,h1,l2,h2 in 
             (parse('{}: {:d}-{:d} or {:d}-{:d}', line) for line in rules.splitlines())}

    mine = [int(x) for x in mine.splitlines()[1].split(',')]
    nearby = [[int(x) for x in line.split(',')] for line in nearby.splitlines()[1:]]

    mine = parse_my_ticket(rules, mine, nearby)

    return math.prod(v for k,v in mine.items() if k.startswith('departure'))


def meets(val, constraint):
    return val in constraint[0] or val in constraint[1]

def solve_field_order(rules,valid):
    candidates = {fname : set(i for i in range(len(rules)) if all(meets(ticket[i], constraint) for ticket in valid))   
                    for fname, constraint in rules.items()}

    solved = [None] * len(rules)
    while None in solved:
        fname, possible = mit.first((fname, possible) for fname, possible in candidates.items() if len(possible) == 1) 
        i = possible.pop()
        solved[i] = fname
        del candidates[fname]
                
        for other in candidates:
            candidates[other] -= {i}

    return solved

def parse_my_ticket(rules, mine, nearby):
    '''
    >>> sorted(parse_my_ticket(
    ... {'class': (range(0,2), range(4,19)),
    ...     'row':  (range(0,6), range(8,20)),
    ...     'seat': (range(0, 13), range(16,20)) },
    ... [11,12,13],
    ... [[3,9,18],[15,1,5], [5,14,9]] ).items())
    [('class', 12), ('row', 11), ('seat', 13)]

    '''
    valid = [ticket for ticket in nearby if
             all(any(val in r for r in it.chain.from_iterable(rules.values())) for val in ticket)]

    field_map = solve_field_order(rules,valid)
    return {fname: mine[i] for i, fname in enumerate(field_map)}

