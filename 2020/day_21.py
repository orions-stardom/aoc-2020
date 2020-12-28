import collections
import more_itertools as mit

from parse import parse

def part_1(data):
    r'''
    >>> part_1("""\
    ... mxmxvkd kfcds sqjhc nhms (contains dairy, fish)
    ... trh fvjkl sbzzf mxmxvkd (contains dairy)
    ... sqjhc fvjkl (contains soy)
    ... sqjhc mxmxvkd sbzzf (contains fish)""")
    5

    '''
    appearances = collections.Counter()
    possible_allergens = {} # allergen -> ingredients it could possibly be in

    for line in data.splitlines():
        ingredients, allergens = parse("{} (contains {})", line)
        ingredients = ingredients.split()
        allergens = allergens.split(", ")

        appearances.update(ingredients)
        for allergen in allergens: 
            possible_allergens.setdefault(allergen, set(ingredients)).intersection_update(ingredients)

    return sum(appearances[ingredient] for ingredient in appearances 
               if not any(ingredient in cands for cands in possible_allergens.values()))

def part_2(data):
    '''
    part_2("""\
    ... mxmxvkd kfcds sqjhc nhms (contains dairy, fish)
    ... trh fvjkl sbzzf mxmxvkd (contains dairy)
    ... sqjhc fvjkl (contains soy)
    ... sqjhc mxmxvkd sbzzf (contains fish)""")
    mxmxvkd,sqjhc,fvjkl   

    '''
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
