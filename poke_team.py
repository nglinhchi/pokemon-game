from __future__ import annotations

"""
"""
__author__ = "Scaffold by Jackson Goerner, Code by ______________"

from enum import Enum, auto
from pokemon_base import PokemonBase
from random_gen import RandomGen

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
        ALWAYS_ATTACK = 0
        SWAP_ON_SUPER_EFFECTIVE = 1
        RANDOM = 2
        USER_INPUT = 3


    def __init__(self, team_name: str, team_numbers: list[int], battle_mode: int, ai_type: PokeTeam.AI, criterion=None, criterion_value=None) -> None:
        """
        Creates user-specified Poketeam
        """
        self.team_name = team_name
        self.team_numbers = team_numbers
        self.battle_mode = battle_mode
        self.ai_type =  ai_type
        self.criterion = criterion
        # self.criterion_value = criterion_value
    

    @classmethod
    def random_team(cls, team_name: str, battle_mode: int, team_size=None, ai_mode=None, **kwargs):
        """
        Creates random generated Poketeam
        """
        # assign team_size
        if team_size == None:
            team_size = RandomGen.randint(PokeTeam.MAX_TEAM_SIZE//2, PokeTeam.MAX_TEAM_SIZE)

        # create team_numbers TODO)switch to ADT
        team_numbers = []
        team_numbers.append(0)
        team_numbers.append(team_size)
        for i in range(PokeTeam.NUM_BASE_POKEMON-2): 
            team_numbers.append(RandomGen.randint(0,team_size))
        # TODO sort team_numbers

        if ai_mode == None:
            ai_mode = PokeTeam.AI.RANDOM

        PokeTeam.__init__(team_name, team_numbers, battle_mode, ai_mode)

        

        


    def return_pokemon(self, poke: PokemonBase) -> None:
        if self.battle_mode == 0:
            pass
        elif self.battle_mode == 1:
            pass
        elif self.battle_mode == 2:
            pass


    def retrieve_pokemon(self) -> PokemonBase | None:
        if self.battle_mode == 0:
            pass
        elif self.battle_mode == 1:
            pass
        elif self.battle_mode == 2:
            pass


    def special(self):
        if self.battle_mode == 0:
            pass
        elif self.battle_mode == 1:
            pass
        elif self.battle_mode == 2:
            pass


    def regenerate_team(self):
        raise NotImplementedError()


    def __str__(self):
        raise NotImplementedError()


    def is_empty(self):
        raise NotImplementedError()


    def choose_battle_option(self, my_pokemon: PokemonBase, their_pokemon: PokemonBase) -> Action:
        if self.battle_mode == PokeTeam.AI.ALWAYS_ATTACK:
            return Action.ATTACK
        elif self.battle_mode == PokeTeam.AI.SWAP_ON_SUPER_EFFECTIVE:
            if their_pokemon.poke_type.type_multiplier(my_pokemon.poke_type) >= 1.5:
                return Action.SWAP
            else:
                return Action.ATTACK
        elif self.battle_mode == PokeTeam.AI.RANDOM:
            
        elif self.battle_mode == PokeTeam.AI.USER_INPUT:
            pass


    @classmethod
    def leaderboard_team(cls):
        raise NotImplementedError()
