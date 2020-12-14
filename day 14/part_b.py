from dotenv import load_dotenv; load_dotenv()

import aocd
import pytest
import sys

from parse import parse
from pathlib import Path

from collections import defaultdict

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
                
def solve(data):
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

@pytest.mark.parametrize('data,expect',
    # INSERT TEST CASES HERE
    [('''mask = 000000000000000000000000000000X1001X
mem[42] = 100
mask = 00000000000000000000000000000000X0XX
mem[26] = 1''', 208)])
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

