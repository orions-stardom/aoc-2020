def closest_multiple(n, x):
    ''' Multiple of x closest to and above n
    adapted from https://www.geeksforgeeks.org/multiple-of-x-closest-to-n/
    '''
    z = x//2
    nn = n+z
    nn -= nn%x

    if nn <= n:
        nn += x

    return nn

def part_1(data):
    '''
    >>> part_1("""939
    ... 7,13,x,x,59,x,31,19""")
    295

    '''
    data = data.splitlines()
    arrive = int(data[0])
    busses = [int(x) for x in data[1].split(',') if x != 'x']
    catch_at, bus = min((closest_multiple(arrive, bus), bus) for bus in busses)
    return bus * (catch_at - arrive)

# chinese_remainder and mul_inv from https://rosettacode.org/wiki/Chinese_remainder_theorem#Python_3.6
from functools import reduce
def chinese_remainder(n, a):
    sum = 0
    prod = reduce(lambda a, b: a*b, n)
    for n_i, a_i in zip(n, a):
        p = prod // n_i
        sum += a_i * mul_inv(p, n_i) * p
    return sum % prod
 
def mul_inv(a, b):
    b0 = b
    x0, x1 = 0, 1
    if b == 1: return 1
    while a > 1:
        q = a // b
        a, b = b, a%b
        x0, x1 = x1 - q * x0, x0
    if x1 < 0: x1 += b0
    return x1

def part_2(data):
    '''
    >>> part_2("7,13,x,x,59,x,31,19")
    1068781
    >>> part_2("67,7,59,61")
    754018
    >>> part_2("67,x,7,59,61")
    779210
    >>> part_2("67,7,x,59,61")
    1261476
    >>> part_2("1789,37,47,1889")
    1202161486

    '''
    data = data.splitlines()[-1]

    busses = [int(x) if x != 'x' else x for x in data.split(',')]
    require = [(bus, bus-i) for i, bus in enumerate(busses) if bus != 'x']
    return chinese_remainder(*zip(*require))
 
