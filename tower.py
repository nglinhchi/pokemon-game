from __future__ import annotations

from poke_team import PokeTeam
from battle import Battle

class BattleTower:

    def __init__(self, battle: Battle|None=None) -> None:
        raise NotImplementedError()
    
    def set_my_team(self, team: PokeTeam) -> None:
        raise NotImplementedError()
    
    def generate_teams(self, n: int) -> None:
        raise NotImplementedError()

    def __iter__(self):
        raise NotImplementedError()

class BattleTowerIterator:
    
    def avoid_duplicates(self):
        raise NotImplementedError()

    def sort_by_lives(self):
        # 1054
        raise NotImplementedError()
