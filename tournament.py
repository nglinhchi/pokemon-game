from __future__ import annotations

"""
"""
__author__ = "Scaffold by Jackson Goerner, Code by ______________"

from poke_team import PokeTeam
from battle import Battle
from linked_list import LinkedList

class Tournament:
    
    def __init__(self, battle: Battle|None=None) -> None:
        raise NotImplementedError()
        try:
            self.battle = battle
        except AttributeError as e:
            self.battle = Battle()

    def set_battle_mode(self, battle_mode: int) -> None:
        raise NotImplementedError()
        self.battle_mode = battle_mode

    def is_valid_tournament(self, tournament_str: str) -> bool:
        raise NotImplementedError()
        tournament_list = tournament_str.split(" ")
    def is_balanced_tournament(self, tournament_str: str) -> bool:
        # 1054 only
        raise NotImplementedError()

    def start_tournament(self, tournament_str: str) -> None:
        raise NotImplementedError()

    def advance_tournament(self) -> tuple[PokeTeam, PokeTeam, int] | None:
        raise NotImplementedError()

    def linked_list_of_games(self) -> LinkedList[tuple[PokeTeam, PokeTeam]]:
        raise NotImplementedError()
        l = LinkedList()
        while True:
            res = self.advance_tournament()
            if res is None:
                break
            l.insert(0, (res[0], res[1]))
        return l
    
    def linked_list_with_metas(self) -> LinkedList[tuple[PokeTeam, PokeTeam, list[str]]]:
        raise NotImplementedError()
    
    def flip_tournament(self, tournament_list: LinkedList[tuple[PokeTeam, PokeTeam]], team1: PokeTeam, team2: PokeTeam) -> None:
        # 1054
        raise NotImplementedError()
