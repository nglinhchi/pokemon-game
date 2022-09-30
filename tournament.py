from __future__ import annotations
<<<<<<< Updated upstream
=======
from ast import operator
from multiprocessing.dummy import Array
from multiprocessing.sharedctypes import Value
#from nis import match
from bset import BSet
from linked_stack import LinkedStack
from pokemon_base import PokeType
from queue_adt import CircularQueue
from stack_adt import ArrayStack
from random_gen import RandomGen
"""
Creates tournament class that implements all methods needed to create and run a tournament between PokeTeams.
>>>>>>> Stashed changes

"""
"""
__author__ = "Scaffold by Jackson Goerner, Code by ______________"

from poke_team import PokeTeam
from battle import Battle
from linked_list import LinkedList

class Tournament:
    
    def __init__(self, battle: Battle|None=None) -> None:
        raise NotImplementedError()

    def set_battle_mode(self, battle_mode: int) -> None:
        raise NotImplementedError()

    def is_valid_tournament(self, tournament_str: str) -> bool:
        raise NotImplementedError()

    def is_balanced_tournament(self, tournament_str: str) -> bool:
        # 1054 only
        raise NotImplementedError()

    def start_tournament(self, tournament_str: str) -> None:
        raise NotImplementedError()

    def advance_tournament(self) -> tuple[PokeTeam, PokeTeam, int] | None:
        raise NotImplementedError()

    def linked_list_of_games(self) -> LinkedList[tuple[PokeTeam, PokeTeam]]:
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
