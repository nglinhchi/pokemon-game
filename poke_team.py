from __future__ import annotations

"""
"""
__author__ = "Scaffold by Jackson Goerner, Code by ______________"

from enum import Enum, auto
from pokemon_base import PokemonBase

class Action(Enum):
    ATTACK = auto()
    SWAP = auto()
    HEAL = auto()
    SPECIAL = auto()
    
class Criterion(Enum):
    SPD = auto()
    HP = auto()
    LV = auto()
    DEF = auto()

class PokeTeam:

    class AI(Enum):
        ALWAYS_ATTACK = auto()
        SWAP_ON_SUPER_EFFECTIVE = auto()
        RANDOM = auto()
        USER_INPUT = auto()

    def __init__(self, team_name: str, team_numbers: list[int], battle_mode: int, ai_type: PokeTeam.AI, criterion=None, criterion_value=None) -> None:
        """
        Creates user-specified Poketeam
        """
    
    @classmethod
    def random_team(cls, team_name: str, battle_mode: int, team_size=None, ai_mode=None, **kwargs):
        """
        Creates random generated Poketeam
        """
        raise NotImplementedError()

    def return_pokemon(self, poke: PokemonBase) -> None:
        raise NotImplementedError()

    def retrieve_pokemon(self) -> PokemonBase | None:
        raise NotImplementedError()

    def special(self):
        raise NotImplementedError()

    def regenerate_team(self):
        raise NotImplementedError()

    def __str__(self):
        raise NotImplementedError()

    def is_empty(self):
        raise NotImplementedError()

    def choose_battle_option(self, my_pokemon: PokemonBase, their_pokemon: PokemonBase) -> Action:
        raise NotImplementedError()

    @classmethod
    def leaderboard_team(cls):
        raise NotImplementedError()
