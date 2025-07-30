
from dataclasses import dataclass
from typing import Optional

@dataclass(frozen=True)
class Card:
    name: str
    cost: int
    type: str   # 'land', 'creature', 'spell'
    power: int = 0
    toughness: int = 0
    effect: Optional[str] = None  # 'bolt', 'draw', 'heal'

BASIC_CARDS = [
    Card("Plains", 0, "land"),
    Card("Island", 0, "land"),
    Card("Forest", 0, "land"),
    Card("Mountain", 0, "land"),
    Card("Swamp", 0, "land"),
    Card("Grizzly Bears", 2, "creature", power=2, toughness=2),
    Card("Hill Giant", 4, "creature", power=3, toughness=3),
    Card("Serra Angel", 5, "creature", power=4, toughness=4),
    Card("Lightning Bolt", 1, "spell", effect="bolt"),
    Card("Divination", 3, "spell", effect="draw"),
    Card("Healing Salve", 1, "spell", effect="heal"),
]
