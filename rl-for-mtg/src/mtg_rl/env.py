
from __future__ import annotations
from dataclasses import dataclass, field
from typing import List, Tuple, Optional, Dict, Any
import random

from .cards import Card
from .deck import make_deck

DRAW = 0
MAIN = 1
COMBAT = 2
END = 3

@dataclass
class CreatureState:
    card: Card
    summoning_sick: bool = True
    tapped: bool = False
    damage_marked: int = 0

@dataclass
class PlayerState:
    life: int = 20
    deck: List[Card] = field(default_factory=list)
    hand: List[Card] = field(default_factory=list)
    graveyard: List[Card] = field(default_factory=list)
    battlefield: List[CreatureState] = field(default_factory=list)
    lands_in_play: int = 0
    lands_played_this_turn: int = 0
    mana_pool: int = 0

class MiniMTGEnv:
    def __init__(self, seed: int = 0):
        self.rng = random.Random(seed)
        self.players = [PlayerState(), PlayerState()]
        self.turn = 0
        self.phase = DRAW
        self.done = False
        self.winner: Optional[int] = None
        for p in self.players:
            p.deck = make_deck(seed=self.rng.randrange(10_000_000))
            for _ in range(7):
                p.hand.append(p.deck.pop())
        self.history: List[Dict[str, Any]] = []

    def legal_actions(self) -> List[Tuple[str, Any]]:
        a: List[Tuple[str, Any]] = []
        me = self.players[self.turn]
        opp = self.players[1 - self.turn]
        if self.done:
            return [("noop", None)]
        if self.phase == DRAW:
            a.append(("proceed", None))
        elif self.phase == MAIN:
            if me.lands_played_this_turn == 0:
                for i, c in enumerate(me.hand):
                    if c.type == "land":
                        a.append(("play_land", i))
            available = me.lands_in_play
            for i, c in enumerate(me.hand):
                if c.type != "land" and c.cost <= available:
                    if c.type == "creature":
                        a.append(("cast_creature", i))
                    elif c.type == "spell":
                        if c.effect in ("draw", "heal"):
                            a.append(("cast_spell", (i, None)))
                        elif c.effect == "bolt":
                            a.append(("cast_spell", (i, ("player", 1 - self.turn))))
                            for idx, _ in enumerate(opp.battlefield):
                                a.append(("cast_spell", (i, ("opp_creature", idx))))
                            for idx, _ in enumerate(me.battlefield):
                                a.append(("cast_spell", (i, ("my_creature", idx))))
            a.append(("to_combat", None))
            a.append(("end_turn", None))
        elif self.phase == COMBAT:
            attackables = [i for i, cr in enumerate(me.battlefield) if not cr.tapped and not cr.summoning_sick]
            a.append(("attack", []))
            subsets = [[]]
            for idx in attackables:
                subsets.append([idx])
            if len(attackables) > 1:
                subsets.append(attackables)
            seen = set()
            out = []
            for s in subsets:
                t = tuple(sorted(s))
                if t not in seen:
                    seen.add(t); out.append(s)
            for s in out:
                a.append(("attack", s))
            a.append(("skip_combat", None))
        elif self.phase == END:
            a.append(("proceed", None))
        return a

    def step(self, action: Tuple[str, Any]):
        me = self.players[self.turn]
        opp = self.players[1 - self.turn]
        reward = 0.0
        atype, payload = action

        if self.done:
            return self._observe(), 0.0, True, {}

        if self.phase == DRAW:
            me.mana_pool = me.lands_in_play
            me.lands_played_this_turn = 0
            for cr in me.battlefield:
                cr.tapped = False
                cr.summoning_sick = False
                cr.damage_marked = 0
            if me.deck:
                me.hand.append(me.deck.pop())
            self.phase = MAIN

        elif self.phase == MAIN:
            if atype == "play_land":
                idx = payload
                card = me.hand.pop(idx)
                assert card.type == "land"
                me.lands_in_play += 1
                me.lands_played_this_turn += 1
            elif atype == "cast_creature":
                idx = payload
                card = me.hand.pop(idx)
                assert card.type == "creature"
                me.battlefield.append(CreatureState(card=card, summoning_sick=True, tapped=False))
            elif atype == "cast_spell":
                idx, target = payload
                card = me.hand.pop(idx)
                assert card.type == "spell"
                if card.effect == "draw":
                    for _ in range(2):
                        if me.deck: me.hand.append(me.deck.pop())
                elif card.effect == "heal":
                    me.life += 3
                elif card.effect == "bolt":
                    if target is None:
                        opp.life -= 3
                    else:
                        kind, which = target
                        if kind == "player":
                            if which == 1 - self.turn:
                                opp.life -= 3
                            else:
                                me.life -= 3
                        elif kind == "opp_creature" and which < len(opp.battlefield):
                            opp.battlefield[which].damage_marked += 3
                        elif kind == "my_creature" and which < len(me.battlefield):
                            me.battlefield[which].damage_marked += 3
                me.graveyard.append(card)
            elif atype == "to_combat":
                self.phase = COMBAT
            elif atype == "end_turn":
                self.phase = END

        elif self.phase == COMBAT:
            if atype == "attack":
                attackers_idx = payload or []
                attackers = [me.battlefield[i] for i in attackers_idx if i < len(me.battlefield)]
                for cr in attackers:
                    cr.tapped = True
                blocks = [-1] * len(attackers)
                for ai, acr in enumerate(attackers):
                    bi = self._choose_blocker(self.players[1 - self.turn], acr)
                    blocks[ai] = bi
                    if bi != -1:
                        self.players[1 - self.turn].battlefield[bi].tapped = True
                for ai, acr in enumerate(attackers):
                    bi = blocks[ai]
                    if bi == -1:
                        opp.life -= acr.card.power
                    else:
                        bcr = opp.battlefield[bi]
                        bcr.damage_marked += acr.card.power
                        acr.damage_marked += bcr.card.power
                me.battlefield = [c for c in me.battlefield if c.damage_marked < c.card.toughness]
                opp.battlefield = [c for c in opp.battlefield if c.damage_marked < c.card.toughness]
                self.phase = END
            elif atype == "skip_combat":
                self.phase = END

        elif self.phase == END:
            if opp.life <= 0 and me.life <= 0:
                self.done = True; self.winner = None
            elif opp.life <= 0:
                self.done = True; self.winner = self.turn; reward = 1.0
            elif me.life <= 0:
                self.done = True; self.winner = 1 - self.turn; reward = -1.0
            self.turn = 1 - self.turn
            self.phase = DRAW

        obs = self._observe()
        return obs, reward, self.done, {}

    def _choose_blocker(self, defender, attacker):
        for i, cr in enumerate(defender.battlefield):
            if cr.tapped:
                continue
            if cr.card.power >= attacker.card.toughness or cr.card.toughness > attacker.card.power:
                return i
        return -1

    def _observe(self) -> Dict:
        me = self.players[self.turn]
        opp = self.players[1 - self.turn]
        return {
            "turn": self.turn,
            "phase": self.phase,
            "me": {
                "life": me.life,
                "hand": [c.name for c in me.hand],
                "lands_in_play": me.lands_in_play,
                "battlefield": [(c.card.name, c.tapped, c.summoning_sick, c.damage_marked) for c in me.battlefield],
                "graveyard": [c.name for c in me.graveyard],
                "library_count": len(me.deck),
            },
            "opp": {
                "life": opp.life,
                "hand_count": len(opp.hand),
                "lands_in_play": opp.lands_in_play,
                "battlefield": [(c.card.name, c.tapped, c.summoning_sick, c.damage_marked) for c in opp.battlefield],
                "graveyard": [c.name for c in opp.graveyard],
                "library_count": len(opp.deck),
            },
        }
