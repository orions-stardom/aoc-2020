import itertools as it

def brute_force(key, subject_no):
    # This looks like it should just be 
    #return pow(subject_no, -1, key)
    # but that didn't work so I guess i have to actually brute force :(

    for loop_size in it.count(1):
        if pow(subject_no, loop_size, 20201227) == key:
            return loop_size
        
def part_1(data):
    r'''
    >>> part_1("""\
    ... 5764801
    ... 17807724""")
    14897079

    '''
    card_key, door_key = map(int, data.splitlines())
    card_loop_size, door_loop_size = brute_force(card_key, 7), brute_force(door_key, 7)
    encryption_key = pow(card_key, door_loop_size, 20201227)
    return encryption_key
