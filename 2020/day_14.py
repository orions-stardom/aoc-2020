from collections import defaultdict
from parse import parse


def part_1(data):
    r'''
    >>> part_1("""\
    ... mask = XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X
    ... mem[8] = 11
    ... mem[7] = 101
    ... mem[8] = 0""")
    165

    '''
    mem = defaultdict(int)
    for line in data.splitlines():
        where, val = line.split(' = ')
        if where == 'mask':
            zeroes = int(val.replace('X', '1'), 2)
            ones = int(val.replace('X', '0'), 2)
        else:
            n = parse('mem[{:d}]', where)[0]
            mem[n] = (int(val) & zeroes) | ones

    return sum(mem.values())

def addrs(n, mask):
    floating_bits = mask.count('X')
    for i in range(2**floating_bits):
        replacement_bits = format(i, f'0{floating_bits}b')
        replacement_index = 0
        finalbits = []
        for nbit, maskbit in zip(format(n, '036b'), mask):
            if maskbit == '0':
                finalbits.append(str(nbit))
            elif maskbit == '1':
                finalbits.append('1')
            elif maskbit == 'X':
                finalbits.append(replacement_bits[replacement_index])
                replacement_index += 1
            else:
                print('.. umm.. ?')
                1 / 0

        yield int(''.join(finalbits), 2)
                
def part_2(data):
    r'''
    >>> part_2("""\
    ... mask = 000000000000000000000000000000X1001X
    ... mem[42] = 100
    ... mask = 00000000000000000000000000000000X0XX
    ... mem[26] = 1""")
    208

    '''
    mem = defaultdict(int)
    for line in data.splitlines():
        where, val = line.split(' = ')
        if where == 'mask':
            mask = val
        else:
            n = parse('mem[{:d}]', where)[0]
            for addr in addrs(n, mask):
                mem[addr] = int(val)
    
    return sum(mem.values())

