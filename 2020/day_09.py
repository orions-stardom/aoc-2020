import more_itertools as mit
import itertools as it

def part_1(data, preamblesize=25):
    r'''
    >>> part_1("""\
    ... 35
    ... 20
    ... 15
    ... 25
    ... 47
    ... 40
    ... 62
    ... 55
    ... 65
    ... 95
    ... 102
    ... 117
    ... 150
    ... 182
    ... 127
    ... 219
    ... 299
    ... 277
    ... 309
    ... 576""", 5)
    127

    '''
    data = [int(l) for l in data.splitlines()]
    for *pres, curr in mit.windowed(data, preamblesize+1):
        if not any(x+y == curr for x,y in it.combinations(pres, 2)):
            return curr

def first_invalid(data, preamblesize):
    for *pres, curr in mit.windowed(data, preamblesize+1):
        if not any(x+y == curr for x,y in it.combinations(pres, 2)):
            return curr


def part_2(data, preamblesize=25):
    r'''
    >>> part_2("""\
    ... 35
    ... 20
    ... 15
    ... 25
    ... 47
    ... 40
    ... 62
    ... 55
    ... 65
    ... 95
    ... 102
    ... 117
    ... 150
    ... 182
    ... 127
    ... 219
    ... 299
    ... 277
    ... 309
    ... 576""", 5)
    62

    '''
    data = [int(l) for l in data.splitlines()]
    target = first_invalid(data, preamblesize)

    start = 0
    end = 1
    while True:
        test = data[start:end+1]
        res = sum(test)

        if res == target:
            return min(test) + max(test)

        if end > len(data):
            start += 1
            end = start+1
        else:
            end += 1
