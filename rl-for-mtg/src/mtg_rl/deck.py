
import random
from typing import List
from .cards import Card, BASIC_CARDS

def make_deck(seed: int = 0) -> List[Card]:
    rng = random.Random(seed)
    lands = [c for c in BASIC_CARDS if c.type == "land"]
    spells = [c for c in BASIC_CARDS if c.type != "land"]
    deck = []
    for _ in range(16):
        deck.append(lands[rng.randrange(len(lands))])
    for _ in range(24):
        deck.append(spells[rng.randrange(len(spells))])
    rng.shuffle(deck)
    return deck
