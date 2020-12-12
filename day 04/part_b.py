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
        
def valid_height(h):
    in_cm = parse("{:n}cm", h)
    if in_cm is not None:
        return 150 <= in_cm[0] <= 193
    
    in_in = parse("{:n}in", h)
    if in_in is not None:
        return 59 <= in_in[0] <= 76

    return False

def is_valid(record):
    require={'byr': lambda x: x.isdigit() and 1920 <= int(x) <= 2002,
             'iyr': lambda x: x.isdigit() and 2010 <= int(x) <= 2020, 
             'eyr': lambda x: x.isdigit() and 2020 <= int(x) <= 2030,
             'hgt': valid_height, 
             'hcl': lambda x: x.startswith('#') and len(x) == 7,
             'ecl': lambda x: x in 'amb blu brn gry grn hzl oth'.split(), 
             'pid': lambda x: x.isdigit() and len(x) == 9 } 
    # not cid

    return all(k in record and require[k](record[k]) for k in require)

def solve(data):
    #data = [dict(field.split(':') for field in line.split()) for line in data.splitlines()]
    data = list(parse_data(data))
    return sum(is_valid(r) for r in data)

@pytest.mark.parametrize('data,expect',
    # INSERT TEST CASES HERE
    [('''eyr:1972 cid:100
hcl:#18171d ecl:amb hgt:170 pid:186cm iyr:2018 byr:1926

iyr:2019
hcl:#602927 eyr:1967 hgt:170cm
ecl:grn pid:012533040 byr:1946

hcl:dab227 iyr:2012
ecl:brn hgt:182cm pid:021572410 eyr:2020 byr:1992 cid:277

hgt:59cm ecl:zzz
eyr:2038 hcl:74454a iyr:2023
pid:3556412378 byr:2007''', 0 ),
     ('''pid:087499704 hgt:74in ecl:grn iyr:2012 eyr:2030 byr:1980
hcl:#623a2f

eyr:2029 ecl:blu cid:129 byr:1989
iyr:2014 pid:896056539 hcl:#a97842 hgt:165cm

hcl:#888785
hgt:164cm byr:2001 iyr:2015 cid:88
pid:545766238 ecl:hzl
eyr:2022

iyr:2010 hgt:158cm hcl:#b6652a ecl:blu byr:1944 eyr:2021 pid:093154719''', 4)])
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

