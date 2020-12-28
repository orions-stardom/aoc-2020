import itertools as it

def part_1(data):
    r'''
    >>> part_1("""\
    ... 1721
    ... 979
    ... 366
    ... 299
    ... 675
    ... 1456""")
    514579

    '''
    data = [int(x) for x in data.splitlines()]
    for i,j in it.combinations(data, 2):
        if i+j == 2020:
            return i*j

def part_2(data):
    r'''
    >>> part_2("""\
    ... 1721
    ... 979
    ... 366
    ... 299
    ... 675
    ... 1456""")
    241861950

    '''
    data = [int(x) for x in data.splitlines()]
    for i,j,k in it.combinations(data, 3):
        if i+j+k == 2020:
            return i*j*k
