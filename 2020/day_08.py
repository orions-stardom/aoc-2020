def part_1(data):
    r'''
    >>> part_1("""\
    ... nop +0
    ... acc +1
    ... jmp +4
    ... acc +3
    ... jmp -3
    ... acc -99
    ... acc +1
    ... jmp -4
    ... acc +6""")
    5
    '''
    instructions = [line.split() for line in data.splitlines()]

    acc = 0
    pc = 0
    visited = set()
    while True:
        inst, val = instructions[pc]
        if inst == 'nop':
            pc += 1
        elif inst == 'acc':
            acc += int(val)
            pc += 1
        elif inst == 'jmp':
            pc += int(val)

        if pc in visited:
            return acc
        else:
            visited.add(pc)
            continue

class InfiniteLoop(Exception): pass

def run(instructions):
    acc = 0
    pc = 0
    visited = set()
    while pc < len(instructions):
        inst, val = instructions[pc]
        if inst == 'nop':
            pc += 1
        elif inst == 'acc':
            acc += int(val)
            pc += 1
        elif inst == 'jmp':
            pc += int(val)

        if pc in visited:
            raise InfiniteLoop 
        else:
            visited.add(pc)
            continue

    return acc

def part_2(data):
    r'''
    >>> part_2("""\
    ... nop +0
    ... acc +1
    ... jmp +4
    ... acc +3
    ... jmp -3
    ... acc -99
    ... acc +1
    ... jmp -4
    ... acc +6""")
    8
    '''
    original_instructions = [line.split() for line in data.splitlines()]

    for i, (inst, val) in enumerate(original_instructions):
        if inst == 'acc': 
            continue
        new_instructions = original_instructions.copy()
        if inst == 'nop':
            new_instructions[i] = ('jmp', val)
        if inst == 'jmp':
            new_instructions[i] = ('nop', val)

        try:
            return run(new_instructions)
        except InfiniteLoop:
            continue

