from dotenv import load_dotenv; load_dotenv()

import aocd
import pytest
import sys

from parse import parse
from pathlib import Path

import more_itertools as mit

import collections

def solve(data):
    appearances = collections.Counter()
    possible = {} # allergen -> ingredients it could possibly be in

    for line in data.splitlines():
        ingredients, allergens = parse("{} (contains {})", line)
        ingredients = ingredients.split()
        allergens = allergens.split(", ")

        appearances.update(ingredients)
        for allergen in allergens: 
            possible.setdefault(allergen, set(ingredients)).intersection_update(ingredients)

    result = {}
    while len(result) < len(possible):
        allergen = mit.first(allergen for allergen,where in possible.items() if len(where) == 1)
        food = possible[allergen].pop()
        result[food] = allergen

        for allergen in possible:
            possible[allergen].discard(food)

    return ','.join(sorted(result,key=result.get))



@pytest.mark.parametrize('data,expect',
    # INSERT TEST CASES HERE
    [('''mxmxvkd kfcds sqjhc nhms (contains dairy, fish)
trh fvjkl sbzzf mxmxvkd (contains dairy)
sqjhc fvjkl (contains soy)
sqjhc mxmxvkd sbzzf (contains fish)''', 'mxmxvkd,sqjhc,fvjkl')
    ])
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

