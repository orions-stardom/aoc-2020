from invoke import task
from datetime import date
from pathlib import Path
import doctest
import importlib

import aocd

import os

import dotenv; dotenv.load_dotenv()

def current_day():
    today = datetime.today()
    if today.month != 12 or not 1 <= today.day <= 25:
        raise ArgumentError("Can only guess the day during AOC season")
    
    return today.year, today.day

def resolve_args(year, day):
    if None in (year, day):
        return current_puzzle()

    return year, day

def solution_module(year, day):
    return importlib.import_module(f'{year}.day_{day:02}')

@task
def test(c, year=0, day=0):
    if 0 in (year,day):
        year, day = current_day()

    mod = solution_module(year, day)
    doctest.testmod(mod)

@task
def run(c, year=0, day=0, part=0, testing=True, submit=True):
    year, day = resolve_args(year, day)
    if testing:
        test(c, year, day)

    data = aocd.get_data(year=year, day=day)
    m = solution_module(year, day)

    if not part:
        part = 2 if hasattr(m, 'part_2') else 1

    solution = getattr(m, f'part_{part}')(data)
    print("Solution: ", solution, sep="\n")
    aocd.submit(solution, year=year, day=day, part='ab'[part-1], reopen=False)

@task
def edit(c, year=0, day=0):
    if 0 in (year,day):
        year, day = current_day()

    file = Path(str(year)) / f"day_{day:02}.py"
    # c.run(f'{os.environ["EDITOR"]} {file}') steals my keystrokes :(
    os.execlp(os.environ["EDITOR"], os.environ["EDITOR"], str(file))

    
