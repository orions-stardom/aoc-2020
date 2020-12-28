from collections import deque
import more_itertools as mit

def parse_deck(string):
    return deque(int(l) for l in string.splitlines()[1:])

def score(deck):
    return sum(i*c for i,c in enumerate(reversed(deck), start=1))

def part_1(data):
    r'''
    >>> part_1("""\
    ... Player 1:
    ... 9
    ... 2
    ... 6
    ... 3
    ... 1
    ... 
    ... Player 2:
    ... 5
    ... 8
    ... 4
    ... 7
    ... 10""")
    306

    '''
    decks = [parse_deck(p) for p in data.split('\n\n')]

    round = 0
    while all(decks):
        round += 1
        cards = [d.popleft() for d in decks]
        winner = max(range(len(cards)), key=cards.__getitem__)
        decks[winner].extend(sorted(cards, reverse=True))

    winning_deck = mit.first(deck for deck in decks if deck)
    return score(winning_deck)

def part_2(data):
    r'''
    >>> part_2("""\
    ... Player 1:
    ... 9
    ... 2
    ... 6
    ... 3
    ... 1
    ... 
    ... Player 2:
    ... 5
    ... 8
    ... 4
    ... 7
    ... 10""")
    291

    '''
    if isinstance(data, str):
        decks = [parse_deck(p) for p in data.split('\n\n')]
        calc_score = True
    else:
        decks = data
        calc_score = False

    seen_states = set()

    while all(decks):
        state = tuple(score(deck) for deck in decks)
        if state in seen_states:
            winning_deck = 0
            break
        
        seen_states.add(state)
        
        cards = [d.popleft() for d in decks]

        if all(len(deck) >= card for card,deck in zip(cards,decks)):
            # Play a recursive game
            winner = part_2([deque(list(deck)[:val]) for deck, val in zip(decks,cards)])
        else:
            winner = max(range(len(cards)), key=cards.__getitem__)

        decks[winner].extend(cards if winner == 0 else reversed(cards))
    else:
        winning_deck = mit.first(ideck for ideck in range(len(decks)) if decks[ideck])
    
    if calc_score:
        #breakpoint()
        return score(decks[winning_deck])
    else:
        return winning_deck

