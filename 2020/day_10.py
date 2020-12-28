import functools
import itertools as it

def part_1(data):
    r'''
    >>> part_1("""\
    ... 16
    ... 10
    ... 15
    ... 5
    ... 1
    ... 11
    ... 7
    ... 19
    ... 6
    ... 12
    ... 4""") # 7 * 5
    35

    >>> part_1("""\
    ... 28
    ... 33
    ... 18
    ... 42
    ... 31
    ... 14
    ... 46
    ... 20
    ... 48
    ... 47
    ... 24
    ... 23
    ... 49
    ... 45
    ... 19
    ... 38
    ... 39
    ... 11
    ... 1
    ... 32
    ... 25
    ... 35
    ... 8
    ... 17
    ... 7
    ... 9
    ... 4
    ... 2
    ... 34
    ... 10
    ... 3""") # 22 * 10
    220

    '''
    available = [0] + [int(l) for l in data.splitlines()]
    available.sort()
    differences = [k-j for j,k in zip(available, available[1:])]
    return differences.count(1) * (differences.count(3)+1)

@functools.cache
def count_ways(available, most_recent):
    # Recursively build up 'where can we go from here with what we have left'
    # Since the target is always biggest adapter we have + 3, we always have to use the biggest adapter
    # and our only end condition is when we've reached it
    if not available:
        return 1

    return sum(count_ways(available[i+1:], c) for i,c in enumerate(it.takewhile((lambda c: c - most_recent <= 3), available)))
    

def part_2(data):
    r'''
    >>> part_2("""\
    ... 16
    ... 10
    ... 15
    ... 5
    ... 1
    ... 11
    ... 7
    ... 19
    ... 6
    ... 12
    ... 4""") 
    8

    >>> part_2("""\
    ... 28
    ... 33
    ... 18
    ... 42
    ... 31
    ... 14
    ... 46
    ... 20
    ... 48
    ... 47
    ... 24
    ... 23
    ... 49
    ... 45
    ... 19
    ... 38
    ... 39
    ... 11
    ... 1
    ... 32
    ... 25
    ... 35
    ... 8
    ... 17
    ... 7
    ... 9
    ... 4
    ... 2
    ... 34
    ... 10
    ... 3""")
    19208

    '''
    available = sorted(int(l) for l in data.splitlines())
    return count_ways(tuple(available), 0)
