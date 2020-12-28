import more_itertools as mit
import operator

from math import prod

ops = {'+': operator.add, '*': operator.mul}
def part_1(data):
    '''
    >>> part_1("1 + 2 * 3 + 4 * 5 + 6")
    71
    >>> part_1("1 + (2 * 3) + (4 * (5 + 6))")
    51
    >>> part_1("2 * 3 + (4 * 5)")
    26
    >>> part_1("5 + (8 * 3 + 9 + 3 * 4 * 3)")
    437
    >>> part_1("5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))")
    12240
    >>> part_1("((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2")
    13632

    '''
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


    return sum(math(mit.peekable(f'({line})'))[0] for line in data.splitlines())


def part_2(data):
    '''
    >>> part_2("1 + 2 * 3 + 4 * 5 + 6")
    231
    >>> part_2("1 + (2 * 3) + (4 * (5 + 6))")
    51
    >>> part_2("2 * 3 + (4 * 5)")
    46
    >>> part_2("5 + (8 * 3 + 9 + 3 * 4 * 3)")
    1445
    >>> part_2("5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))")
    669060
    >>> part_2("((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2")
    23340

    '''
    def math(eqn):
        '''
        Do math on the first bracketed portion of eqn, returning
        the result and the remainder of the equation

        '''
        assert next(eqn) == '('
        # Set initial state so that result will be exactly the first
        # digit or sub-expression by the time we hit the first operator
        current_op = '+'
        result = 0
        multiply_later = []
        while eqn:
            if eqn.peek() == '(':
                partial, eqn = math(eqn)
                if current_op == '+':
                    result += partial
                elif current_op == '*':
                    multiply_later.append(result)
                    result = partial
            else:
                symbol = next(eqn)
                if symbol == ')':
                    if multiply_later:
                        result *= prod(multiply_later)
                    return result,eqn
                elif symbol.isdigit():
                    num = int(symbol)
                    if current_op == '+':
                        result += num
                    elif current_op == '*':
                        multiply_later.append(result)
                        result = num
                elif symbol in ops:
                    current_op = symbol
                else:
                    # Whitespace
                    pass
        else:
            raise ValueError(f'Equation too short; result so far: {result}, last operator: {current_op}')


    return sum(math(mit.peekable(f'({line})'))[0] for line in data.splitlines())


