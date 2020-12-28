def seat_id(directions):
    '''
    >>> seat_id("BFFFBBFRRR")
    567
    >>> seat_id("FFFBBBFRRR")
    119
    >>> seat_id("BBFFBBFRLL")
    820

    '''
    row_dir, column_dir = directions[:7],directions[7:]

    row = int(row_dir.replace('F', '0').replace('B', '1'), 2)
    col = int(column_dir.replace('L', '0').replace('R', '1'), 2)
    
    return row*8 + col

def part_1(data):
    return max(seat_id(line) for line in data.splitlines())


def part_2(data):
    seen_seats = set(seat_id(l) for l in data.splitlines())
    all_seats = set(row*8 + col for row in range(128) for col in range(8))

    missing_seats = all_seats - seen_seats
    possible_seats = {seat for seat in missing_seats if {seat-1, seat+1} <= seen_seats}
    
    assert len(possible_seats) == 1
    return possible_seats.pop()
