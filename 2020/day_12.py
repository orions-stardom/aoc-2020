import math
import cmath

compass = {'N': 0+1j, 'S': 0-1j, 'E': 1+0j, 'W': -1+0j}

def part_1(data):
    r'''
    >>> int(part_1("""\
    ... F10
    ... N3
    ... F7
    ... R90
    ... F11"""))
    25

    '''
    def turn(bearing, degrees):
        r, phi = cmath.polar(bearing)
        rads = math.radians(degrees)
        return cmath.rect(r, phi+rads)


    bearing = 1+0j
    position = 0+0j

    for line in data.splitlines():
        move, amount = line[0], int(line[1:])

        if move in compass:
            position += compass[move] * amount
        elif move == 'F':
            position += bearing * amount
        elif move == 'L':
            bearing = turn(bearing, amount)
        elif move == 'R':
            bearing = turn(bearing, -amount)

    return abs(position.real) + abs(position.imag)


def part_2(data):
    r'''
    >>> int(part_2("""\
    ... F10
    ... N3
    ... F7
    ... R90
    ... F11"""))
    286

    '''
    def turn(waypoint, degrees):
        rads = math.radians(degrees)    
        r,phi = cmath.polar(waypoint)
        return cmath.rect(r, phi+rads)


    position = 0+0j
    waypoint = 10+1j # Relative to ship


    for line in data.splitlines():
        move, amount = line[0], int(line[1:])

        if move in compass:
            waypoint += compass[move] * amount
        elif move == 'F':
            position += waypoint * amount
        elif move == 'L':
            waypoint = turn(waypoint, amount)
        elif move == 'R':
            waypoint = turn(waypoint, -amount)

    return abs(position.real) + abs(position.imag)
 
