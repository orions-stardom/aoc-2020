from dotenv import load_dotenv; load_dotenv()

import aocd
import pytest
import sys

from parse import parse
from pathlib import Path

import itertools as it

def brute_force(key, subject_no):
    # This looks like it should just be 
    #return pow(subject_no, -1, key)
    # but that didn't work so I guess i have to actually brute force :(

    for loop_size in it.count(1):
        if pow(subject_no, loop_size, 20201227) == key:
            return loop_size

        
def solve(data):
    card_key, door_key = map(int, data.splitlines())
    card_loop_size, door_loop_size = brute_force(card_key, 7), brute_force(door_key, 7)
    encryption_key = pow(card_key, door_loop_size, 20201227)
    return encryption_key

@pytest.mark.parametrize('data,expect',
    # INSERT TEST CASES HERE
    [('5764801\n17807724', 14897079)
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

