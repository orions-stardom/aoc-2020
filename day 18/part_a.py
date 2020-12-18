from dotenv import load_dotenv; load_dotenv()

import aocd
import pytest
import sys

from parse import parse
from pathlib import Path

import more_itertools as mit
import operator

ops = {'+': operator.add, '*': operator.mul}
def math(eqn):
    '''
    Do math on the first bracketed portion of eqn, returning
    the result and the remainder of the equation

    '''
    assert next(eqn) == '('
    # Set initial state so that result will be exactly the first
    # digit or sub-expression by the time we hit the first operator
    result = 0
    current_op = '+'
    while eqn:
        if eqn.peek() == '(':
            partial, eqn = math(eqn)
            result = ops[current_op](result, partial)
        else:
            symbol = next(eqn)
            if symbol == ')':
                return result,eqn
            elif symbol.isdigit():
                result = ops[current_op](result,int(symbol))
            elif symbol in ops:
                current_op = symbol
            else:
                # Whitespace
                pass

    else:
        raise ValueError(f'Equation too short; result so far: {result}, last operator: {current_op}')

def solve(data):
    return sum(math(mit.peekable(f'({line})'))[0] for line in data.splitlines())


@pytest.mark.parametrize('data,expect',
    # INSERT TEST CASES HERE
    [('1 + 2 * 3 + 4 * 5 + 6', 71),
     ('1 + (2 * 3) + (4 * (5 + 6))', 51),
     ('2 * 3 + (4 * 5)', 26),
     ('5 + (8 * 3 + 9 + 3 * 4 * 3)', 437),
     ('5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))', 12240),
     ('((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2', 13632),
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

