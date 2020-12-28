import more_itertools as mit
import itertools as it

from copy import deepcopy

def print_state(state):
    print(*map(''.join, state), sep='\n')
    print()

def part_1(data):
    r'''
    >>> part_1("""\
    ... L.LL.LL.LL
    ... LLLLLLL.LL
    ... L.L.L..L..
    ... LLLL.LL.LL
    ... L.LL.LL.LL
    ... L.LLLLL.LL
    ... ..L.L.....
    ... LLLLLLLLLL
    ... L.LLLLLL.L
    ... L.LLLLL.LL""")
    37

    '''
    def next_state(state):
        new_state = deepcopy(state)
        for first_row, last_row, (i, row) in mit.mark_ends(enumerate(state)):
            for first_spot, last_spot, (j, spot) in mit.mark_ends(enumerate(row)):
                adjacent = []


                if not first_row:
                    adjacent.append(state[i-1][j])
                    
                    if not first_spot:
                        adjacent.append(state[i-1][j-1])
                    if not last_spot:
                        adjacent.append(state[i-1][j+1])

                if not last_row:
                    adjacent.append(state[i+1][j])
                    
                    if not first_spot:
                        adjacent.append(state[i+1][j-1])
                    if not last_spot:
                        adjacent.append( state[i+1][j+1])

                if not first_spot:
                    adjacent.append(state[i][j - 1])
                if not last_spot:
                    adjacent.append(state[i][j + 1])

                if spot == 'L' and not any(s == '#' for s in adjacent):
                    new_state[i][j] = '#'
                if spot == '#' and adjacent.count('#') >= 4:
                    new_state[i][j] = 'L'

        return new_state



    current = [list(l) for l in data.splitlines()]

    while True:
        old, current = current, next_state(current)
        if old == current:
            return sum(row.count('#') for row in current)


def part_2(data):
    r'''
    >>> part_2("""\
    ... L.LL.LL.LL
    ... LLLLLLL.LL
    ... L.L.L..L..
    ... LLLL.LL.LL
    ... L.LL.LL.LL
    ... L.LLLLL.LL
    ... ..L.L.....
    ... LLLLLLLLLL
    ... L.LLLLLL.L
    ... L.LLLLL.LL""")
    26
    
    '''
    
    def next_state(state):
        new_state = deepcopy(state)

        height, width = len(state),len(state[0])

        for y, row in enumerate(state):
            for x, spot in enumerate(row):
                if spot == '.': # Spots without a seat can never change
                    continue

                seen = []
                directions = [ (-1, 0), (1,0), (0,1), (0,-1), (1,1), (1,-1), (-1,1), (-1,-1)]

                for dx, dy in directions:
                    cand_x, cand_y = x, y
                     
                    while True:
                        cand_x, cand_y = cand_x+dx, cand_y+dy

                        if not 0 <= cand_x < width or not 0 <= cand_y < height:
                            break

                        if state[cand_y][cand_x] == '.':
                            continue
                        
                        # Spot exists and we can see a seat in it
                        seen.append(state[cand_y][cand_x])
                        break

                if spot == 'L' and not any(s == '#' for s in seen):
                    new_state[y][x] = '#'
                if spot == '#' and seen.count('#') >= 5:
                    new_state[y][x] = 'L'

        return new_state


    current = [list(l) for l in data.splitlines()]

    while True:
        old, current = current, next_state(current)
        if old == current:
            return sum(row.count('#') for row in current)


