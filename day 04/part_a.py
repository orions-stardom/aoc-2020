from dotenv import load_dotenv; load_dotenv()

import aocd
import pytest
import sys

from parse import parse
from pathlib import Path

def parse_data(data):
    # records are k:v pairs possibly split across many lines
    # separated by blank lines
    current_record = {}
    for line in data.splitlines():
        if not line.strip():
            yield current_record
            current_record = {}
            continue

        current_record.update(dict(field.split(':') for field in line.split()))

    yield current_record
        
def is_valid(record):
    require='''byr
    eyr 
    iyr 
    eyr
    hgt 
    hcl 
    ecl 
    pid '''.split()
    # not cid

    return all(k in record for k in require)

def solve(data):
    #data = [dict(field.split(':') for field in line.split()) for line in data.splitlines()]
    data = list(parse_data(data))
    return sum(is_valid(r) for r in data)

@pytest.mark.parametrize('data,expect',
    # INSERT TEST CASES HERE
    [('''ecl:gry pid:860033327 eyr:2020 hcl:#fffffd
byr:1937 iyr:2017 cid:147 hgt:183cm

iyr:2013 ecl:amb cid:350 eyr:2023 pid:028048884
hcl:#cfa07d byr:1929

hcl:#ae17e1 iyr:2013
eyr:2024
ecl:brn pid:760753108 byr:1931
hgt:179cm

hcl:#cfa07d eyr:2025 pid:166559648
iyr:2011 ecl:brn hgt:59in''', 2)
     
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

