from __future__ import annotations
from multiprocessing.sharedctypes import Value

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
    MAX_TEAM_SIZE = 6
    NUM_BASE_POKEMON = 5
    class AI(Enum):
        ALWAYS_ATTACK = auto()
        SWAP_ON_SUPER_EFFECTIVE = auto()
        RANDOM = auto()
        USER_INPUT = auto()

    def __init__(self, team_name: str, team_numbers: list[int], battle_mode: int, ai_type: PokeTeam.AI, criterion=None, criterion_value=None) -> None:
        """
        Creates user-specified Poketeam
        """ 

        #Check type(team_name) == str
        if not type(team_name) == str:
            raise TypeError("Team name must be string")

        #Check team_numbers: len == number of base pokemon (5), team_numbers[0] == 0, team_numbers[5] <= MAX_TEAM_SIZE, 0 <= team_numbers[1->4] <= team_numbers[5], check sorted == True

        if not len(team_numbers) == PokeTeam.NUM_BASE_POKEMON :  #Number of elements in list must equal number of base Pokemon
            raise ValueError(f"Team number length is not valid. The each base Pokemon must correspond to an element in list")

        for num in team_numbers:
            if type(num) != int:
                raise ValueError("Elements in list must be integers")
        
        # if not team_numbers == sorted(team_numbers):
        #     raise ValueError("Numbers must be sorted order (ascending)")

        if not sum(team_numbers) <= PokeTeam.MAX_TEAM_SIZE:
            raise ValueError("Number of Pokemon exceeds max team size")
    
        # elif team_numbers[-1] <= PokeTeam.MAX_TEAM_SIZE:
        #     raise ValueError(f"Last element in team numbers list must be <= max team size: {PokeTeam.MAX_TEAM_SIZE}")
        
        # if not (team_numbers[1] >= 0 and team_numbers[-2] <= team_numbers[-1]):   #Since we know from earlier check that list is sorted, only need to check second and second last element is valid as other element will be within that range.
        #     raise ValueError(f"Numbers in list not within valid range: 0:{PokeTeam.MAX_TEAM_SIZE}")
        
        #Check battle_mode in [0,1,2]
        if battle_mode not in [0,1,2]:
            raise ValueError("Not valid Battle Mode")
        #Check ai_type is valid (in PokeTeam.AI)
        if ai_type not in PokeTeam.AI:
            raise TypeError("AI Type is not valid")
        #If battle_mode == 2, criterion provided and in Criterion class
        if battle_mode == 2:
            assert criterion != None, "Criterion for sorting must be provided for Battle Mode 2"
            assert criterion in Criterion, f"{criterion} is not a valid criterion"
            
    



    
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
