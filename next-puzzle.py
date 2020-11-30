from pathlib import Path
from parse import parse
from shutil import copyfile
import os

cwd = Path.cwd()

try:
    # Blithely assume there are no gaps to fill in
    newest_day, newest_dir = max((parse("day {:n}", d.name)[0], d) 
                                 for d in cwd.iterdir() if d.is_dir()
                                        and not d.name.startswith('.'))
except ValueError:
    day = 1
    part = "a"
else:
    # align to part a+b used by advent-of-code-data rather than
    # part 1 and 2 used by aoc itself
    if (newest_dir / "part_b.py").exists():
        day = newest_day + 1
        part = "a"
    else:
        day = newest_day
        part = "b"

target = cwd / f"day {day}" / f"part_{part}.py"
target.parent.mkdir(exist_ok=True)

copyfile(cwd / "template.py", target)
os.execlp(os.environ["EDITOR"], os.environ["EDITOR"], str(target))

