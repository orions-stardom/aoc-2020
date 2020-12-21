from dotenv import load_dotenv; load_dotenv()

import aocd
import pytest
import sys

from parse import parse
from pathlib import Path

import collections

def solve(data):
    appearances = collections.Counter()
    possible_allergens = {} # allergen -> ingredients it could possibly be in

    for line in data.splitlines():
        ingredients, allergens = parse("{} (contains {})", line)
        ingredients = ingredients.split()
        allergens = allergens.split(", ")

        appearances.update(ingredients)
        for allergen in allergens: 
            possible_allergens.setdefault(allergen, set(ingredients)).intersection_update(ingredients)

    #breakpoint()
    return sum(appearances[ingredient] for ingredient in appearances 
               if not any(ingredient in cands for cands in possible_allergens.values()))



@pytest.mark.parametrize('data,expect',
    # INSERT TEST CASES HERE
    [('''mxmxvkd kfcds sqjhc nhms (contains dairy, fish)
trh fvjkl sbzzf mxmxvkd (contains dairy)
sqjhc fvjkl (contains soy)
sqjhc mxmxvkd sbzzf (contains fish)''', 5)
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

