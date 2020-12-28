def part_1(data):
    r'''\
    >>> part_1("""\
    ... abc
    ...
    ... a
    ... b
    ... c
    ...
    ... ab
    ... ac
    ...
    ... a
    ... a
    ... a
    ... a
    ...
    ... b""")
    11
    '''
    return sum(len(set(x) - set('\n')) for x in data.split('\n\n'))


def count_common(group):
    records = [set(r) for r in group.splitlines()]
    return len(set.intersection(*records))

def part_2(data):
    r'''
    >>> part_2("""\
    ... abc
    ...
    ... a
    ... b
    ... c
    ...
    ... ab
    ... ac
    ...
    ... a
    ... a
    ... a
    ... a
    ...
    ... b""")
    6
    '''
    return sum(count_common(x) for x in data.split('\n\n'))

