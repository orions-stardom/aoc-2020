from dotenv import load_dotenv; load_dotenv()

import aocd
import pytest 
from parse import parse
from pathlib import Path

def solve(data):
    return sum(least <= password.count(letter) <= most 
               for least,most,letter,password in [parse("{:d}-{:d} {}: {}", line) for line in data.splitlines()])


@pytest.mark.parametrize('data,expect',
    [('''1-3 a: abcde
1-3 b: cdefg
2-9 c: ccccccccc''', 2)] 
)
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

