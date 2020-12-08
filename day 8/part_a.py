from dotenv import load_dotenv; load_dotenv()

import aocd
import pytest
import sys

from parse import parse
from pathlib import Path

def solve(data):
    instructions = [line.split() for line in data.splitlines()]

    acc = 0
    pc = 0
    visited = set()
    while True:
        inst, val = instructions[pc]
        if inst == 'nop':
            pc += 1
        elif inst == 'acc':
            acc += int(val)
            pc += 1
        elif inst == 'jmp':
            pc += int(val)

        if pc in visited:
            return acc
        else:
            visited.add(pc)
            continue

@pytest.mark.parametrize('data,expect',
    # INSERT TEST CASES HERE
    [('''nop +0
acc +1
jmp +4
acc +3
jmp -3
acc -99
acc +1
jmp -4
acc +6''', 5),
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

