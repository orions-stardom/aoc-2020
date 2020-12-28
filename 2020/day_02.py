from parse import parse

def part_1(data):
    r'''
    >>> part_1("""\
    ... 1-3 a: abcde
    ... 1-3 b: cdefg
    ... 2-9 c: ccccccccc""")
    2

    '''
    return sum(least <= password.count(letter) <= most 
               for least,most,letter,password in [parse("{:d}-{:d} {}: {}", line) for line in data.splitlines()])


def part_2(data):
    r'''
    >>> part_2("""\
    ... 1-3 a: abcde
    ... 1-3 b: cdefg
    ... 2-9 c: ccccccccc""")
    1

    '''
    return sum( (password[pos_a-1] == letter) ^ (password[pos_b-1] == letter)
               for pos_a, pos_b,letter,password in [parse("{:d}-{:d} {}: {}", line) for line in data.splitlines()])
