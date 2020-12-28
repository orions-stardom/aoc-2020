import itertools as it
import more_itertools as mit

class GridPart1:
    @staticmethod
    def neighbours(coord):
        x,y,z = coord
        for i in it.product((x-1,x,x+1),(y-1,y,y+1),(z-1,z,z+1)):
            if i == coord: continue
            yield i

    @classmethod
    def parse(cls, initial):
        new = GridPart1()
        for y,row in enumerate(initial.splitlines()):
            for x,node in enumerate(row):
                if node == '#':
                    new.active.add((x,y,0))

        return new

    def __init__(self):
        self.active = set()

    def __len__(self):
        return len(self.active)

    def next(self):
        new = GridPart1()
        inactive_seen = set()
        for node in self.active:
            inactive, active = mit.partition(self.active.__contains__,GridPart1.neighbours(node))
            if mit.ilen(active) in (2,3):
                new.active.add(node)
            for neighbour in set(inactive) - self.active - inactive_seen:
                inactive_seen.add(neighbour)
                if len(set(GridPart1.neighbours(neighbour)) & self.active) == 3:
                    new.active.add(neighbour)
        return new

    def __str__(self):
        lines = []
        for z in range(min(c[2] for c in self.active), max(c[2] for c in self.active)+1):
            plane = {c for c in self.active if c[2] == z}
            lines.append(f'z={z}')
            for y in range(min(c[1] for c in plane), max(c[1] for c in plane)+1):
                line = []
                for x in range(min(c[0] for c in plane), max(c[0] for c in plane)+1):
                    line.append('#' if (x,y,z) in self.active else '.')
                lines.append(''.join(line))
            lines.append('')
        return '\n'.join(lines)

def part_1(data):
    r'''
    >>> part_1("""\
    ... .#.
    ... ..#
    ... ###""")
    112

    '''
    grid = GridPart1.parse(data)
    final = mit.nth(mit.iterate(GridPart1.next, grid), 6)
    return len(final)


class GridPart2:
    @staticmethod
    def neighbours(coord):
        x,y,z,w = coord
        for i in it.product((x-1,x,x+1),(y-1,y,y+1),(z-1,z,z+1),(w-1,w,w+1)):
            if i == coord: continue
            yield i

    @classmethod
    def parse(cls, initial):
        new = GridPart2()
        for y,row in enumerate(initial.splitlines()):
            for x,node in enumerate(row):
                if node == '#':
                    new.active.add((x,y,0,0))

        return new

    def __init__(self):
        self.active = set()

    def __len__(self):
        return len(self.active)

    def next(self):
        new = GridPart2()
        inactive_seen = set()
        for node in self.active:
            inactive, active = mit.partition(self.active.__contains__,GridPart2.neighbours(node))
            if mit.ilen(active) in (2,3):
                new.active.add(node)
            for neighbour in set(inactive) - self.active - inactive_seen:
                inactive_seen.add(neighbour)
                if len(set(GridPart2.neighbours(neighbour)) & self.active) == 3:
                    new.active.add(neighbour)
        return new

    def __str__(self):
        lines = []
        for z in range(min(c[2] for c in self.active), max(c[2] for c in self.active)+1):
            plane = {c for c in self.active if c[2] == z}
            lines.append(f'z={z}')
            for y in range(min(c[1] for c in plane), max(c[1] for c in plane)+1):
                line = []
                for x in range(min(c[0] for c in plane), max(c[0] for c in plane)+1):
                    line.append('#' if (x,y,z) in self.active else '.')
                lines.append(''.join(line))
            lines.append('')
        return '\n'.join(lines)

def part_2(data):
    r'''
    >>> part_2("""\
    ... .#.
    ... ..#
    ... ###""")
    848

    '''
    grid = GridPart2.parse(data)
    final = mit.nth(mit.iterate(GridPart2.next, grid), 6)
    return len(final)
