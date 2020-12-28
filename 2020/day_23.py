import more_itertools as mit
import itertools as it

def part_1(data):
    '''
    >>> part_1('389125467')
    '67384529'

    '''
    class Circle:
        def __init__(self, data):
            self._list = list(map(int,data))

        def index(self, label):
            return self._list.index(label)

        def next(self, label):
            return self._list[(self.index(label) + 1) % len(self._list)]

        def pop3(self, label):
            ret = []
            for _ in range(3):
                # Need to recalc each time because the length will change
                where = (self.index(label) + 1) % len(self._list)
                ret.append(self._list.pop(where))

            ret.reverse()
            return ret

        def insert(self, labels, destlabel):
            dest_ix = (self.index(destlabel) + 1) % len(self._list)
            for label in labels:
                self._list.insert(dest_ix, label)

        def __iter__(self):
            return iter(self._list)

        def __str__(self):
            # Start after label 1, gather everything wrapping around
            ix_one = self.index(1)
            order = self._list[ix_one+1:] + self._list[:ix_one]
            return ''.join(map(str, order))

    circle = Circle(data)
    current = int(data[0])

    for _ in range(100):
        grab = circle.pop3(current)
        try:
            dest = max(label for label in circle if label < current)
        except ValueError:
            dest = max(circle)

        circle.insert(grab, dest)
        current = circle.next(current)
    
    return str(circle)



def make_circle(data, size=None):
    if size is None:
        size = len(data)
    data = [int(d) for d in data]
    
    # Waste spot 0 to have the indices line up nicely
    circle = [None] * (size + 1)
    for x, y in mit.pairwise(it.chain(data, range(max(data)+1, size+1))):
        circle[x] = y
    
    # spot 0 is useless so we might as well use it for the first 'current' value
    circle[y] = circle[0] = data[0]
    return circle
    

def do_move(circle, current):
    get = [circle[current], circle[circle[current]], circle[circle[circle[current]]]]
    dest = current - 1 or len(circle) - 1
    while dest in get:
        dest = dest - 1 or len(circle) - 1

    circle[current], circle[dest], circle[get[-1]] = circle[get[-1]], circle[current], circle[dest]
    return circle[current]


def part_2(data):
    '''
    >>> part_2('389125467')
    149245887792

    '''
    circle = make_circle(data, 1000000)

    current = circle[0]
    for _ in range(10000000):
        current = do_move(circle, current)
  
    return circle[1] * circle[circle[1]]
