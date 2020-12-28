from parse import parse

def parse_data(data):
    # records are k:v pairs possibly split across many lines
    # separated by blank lines
    current_record = {}
    for line in data.splitlines():
        if not line.strip():
            yield current_record
            current_record = {}
            continue

        try:
            current_record.update(dict(field.split(':') for field in line.split()))
        except: breakpoint()

    yield current_record
        

def part_1(data):
    r'''
    >>> part_1("""\
    ... ecl:gry pid:860033327 eyr:2020 hcl:#fffffd
    ... byr:1937 iyr:2017 cid:147 hgt:183cm
    ... 
    ... iyr:2013 ecl:amb cid:350 eyr:2023 pid:028048884
    ... hcl:#cfa07d byr:1929
    ... 
    ... hcl:#ae17e1 iyr:2013
    ... eyr:2024
    ... ecl:brn pid:760753108 byr:1931
    ... hgt:179cm
    ... 
    ... hcl:#cfa07d eyr:2025 pid:166559648
    ... iyr:2011 ecl:brn hgt:59in""")
    2

    '''
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

    #data = [dict(field.split(':') for field in line.split()) for line in data.splitlines()]
    data = list(parse_data(data))
    return sum(is_valid(r) for r in data)


def part_2(data):
    r'''
    >>> part_2("""\
    ... eyr:1972 cid:100
    ... hcl:#18171d ecl:amb hgt:170 pid:186cm iyr:2018 byr:1926
    ... 
    ... iyr:2019
    ... hcl:#602927 eyr:1967 hgt:170cm
    ... ecl:grn pid:012533040 byr:1946
    ... 
    ... hcl:dab227 iyr:2012
    ... ecl:brn hgt:182cm pid:021572410 eyr:2020 byr:1992 cid:277
    ... 
    ... hgt:59cm ecl:zzz
    ... eyr:2038 hcl:74454a iyr:2023
    ... pid:3556412378 byr:2007""")
    0

    >>> part_2("""\
    ... pid:087499704 hgt:74in ecl:grn iyr:2012 eyr:2030 byr:1980
    ... hcl:#623a2f
    ... 
    ... eyr:2029 ecl:blu cid:129 byr:1989
    ... iyr:2014 pid:896056539 hcl:#a97842 hgt:165cm
    ... 
    ... hcl:#888785
    ... hgt:164cm byr:2001 iyr:2015 cid:88
    ... pid:545766238 ecl:hzl
    ... eyr:2022
    ... 
    ... iyr:2010 hgt:158cm hcl:#b6652a ecl:blu byr:1944 eyr:2021 pid:093154719""")
    4

    '''
    #data = [dict(field.split(':') for field in line.split()) for line in data.splitlines()]
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
    
    data = list(parse_data(data))
    return sum(is_valid(r) for r in data)

