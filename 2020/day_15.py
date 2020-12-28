from collections import defaultdict, deque

def part_1(data):
    '''
    >>> part_1("0,3,6")
    436

    '''
    start = [int(x) for x in data.split(',')]
    memory = defaultdict(list)
    
    for i, n in enumerate(start):
        memory[n].append(i+1)
    
    last = start[-1]
    for i in range(len(start), 2020):
        if len(memory[last]) > 1:
            x,y = memory[last][-2:]
            last = y-x
        else:
            last = 0

        memory[last].append(i+1)

    return last

def part_2(data):
    '''
    >>> part_2("0,3,6")
    175594
    >>> part_2("1,3,2")
    2578

    '''
    start = [int(x) for x in data.split(',')]
    memory = defaultdict(lambda: deque([], 2))
    
    for i, n in enumerate(start):
        memory[n].append(i+1)
    
    last = start[-1]
    for i in range(len(start), 30000000):
        if len(memory[last]) > 1:
            x,y = memory[last]
            last = y-x
        else:
            last = 0

        memory[last].append(i+1)

    return last

