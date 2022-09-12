from __future__ import annotations
from multiprocessing.sharedctypes import Value
from random import Random

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
            
        # initialise
        self.team_name = team_name
        self.team_numbers = team_numbers
        self.battle_mode = battle_mode
        self.ai_type =  ai_type
        self.criterion = criterion



    # TODO
    @classmethod
    def random_team(cls, team_name: str, battle_mode: int, team_size=None, ai_mode=None, **kwargs):
        """
        Creates random generated Poketeam
        """
        # assign team_size
        if team_size == None:
            team_size = RandomGen.randint(PokeTeam.MAX_TEAM_SIZE//2, PokeTeam.MAX_TEAM_SIZE)

        # create team_numbers TODO ADT and sort --------------------------------
        team_numbers = []
        team_numbers.append(0)
        team_numbers.append(team_size)
        for i in range(PokeTeam.NUM_BASE_POKEMON-2): 
            team_numbers.append(RandomGen.randint(0,team_size))
        if ai_mode == None:
            ai_mode = PokeTeam.AI.RANDOM
        # ----------------------------------------------------------------------

        PokeTeam.__init__(team_name, team_numbers, battle_mode, ai_mode)
        

    # TODO
    def return_pokemon(self, poke: PokemonBase) -> None:
        if self.battle_mode == 0:
            pass
        elif self.battle_mode == 1:
            pass
        elif self.battle_mode == 2:
            pass


    # TODO
    def retrieve_pokemon(self) -> PokemonBase | None:
        if self.battle_mode == 0:
            pass
        elif self.battle_mode == 1:
            pass
        elif self.battle_mode == 2:
            pass


    # TODO
    def special(self):
        if self.battle_mode == 0:
            pass
        elif self.battle_mode == 1:
            pass
        elif self.battle_mode == 2:
            pass

    
    # TODO
    def regenerate_team(self):
        raise NotImplementedError()


    # TODO
    def __str__(self):
        raise NotImplementedError()

    # TODO
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
            return Action(Random.randint(1,4))
        
        elif self.battle_mode == PokeTeam.AI.USER_INPUT:
            prompt = "Select an action: \n"
            prompt += "1 - ATTACK \n"
            prompt += "2 - SWAP \n"
            prompt += "3 - HEAL \n"
            prompt += "4 - SPECIAL \n"
            prompt += "-----------------"
            while True:
                try:
                    action = int(input(prompt))
                    if not (action >=1 and action <= 4):
                        raise ValueError("Invalid input. Please enter a number from 1 to 4.")
                    break
                except TypeError:
                    print("Invalid input. Please enter a number")
            return Action(action)

    @classmethod
    def leaderboard_team(cls):
        raise NotImplementedError()
