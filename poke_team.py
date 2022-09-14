from __future__ import annotations
from multiprocessing.sharedctypes import Value
from random import Random
from sorted_list import ListItem
from pokemon import *
from array_sorted_list import ArraySortedList
from queue_adt import CircularQueue
from stack_adt import ArrayStack
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
    POKEDEX_ORDER = [Charmander, Charizard, Bulbasaur, Venusaur, Squirtle, 
    Blastoise, Gastly, Haunter, Gengar, Eevee]
    BASE_ORDER = [Charmander, ]
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
            raise ValueError("Team name must be string")

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
        self.heal_count = 3

        if self.battle_mode == 0:
            self.team = self.pokemonsStack()
        elif self.battle_mode == 1:
            self.team = self.pokemonsCircularQueue()
        elif self.battle_mode == 2:
            pass



    # TODO
    # TODO
    @classmethod
    def random_team(cls, team_name: str, battle_mode: int, team_size=None, ai_mode=None, **kwargs):
        """
        Creates random generated Poketeam
        """
        # assign team_size
        
        if team_size == None:
            if cls.MAX_TEAM_SIZE % 2 != 0:
                half_team_max = cls.MAX_TEAM_SIZE // 2 + 1 #Between half of Pokemon limit and Pokemon limit- can't be less than half (floor division)
            else:
                half_team_max = cls.MAX_TEAM_SIZE//2
            team_size = RandomGen.randint(half_team_max, cls.MAX_TEAM_SIZE)

        #sorted list
        #add 0 and team size
        start_val = ListItem(0, 0) #value and key to sort by are same
        end_val = ListItem(team_size, team_size)
        team_sorted_list = ArraySortedList()
        team_sorted_list.add(start_val) #add 0
        team_sorted_list.add(end_val)   #add team size
        
        #TODO fix wording: 
        # Algorithm is calculated by getting difference of adjacent value in list (ascending),
        #therefore requires number of base pokemon + 1 to assign to every base. First and 
        #last numbers are 0 and team size, therefore need to generate number of base 
        #pokemon - 1 random numbers

        for _ in range(1, cls.NUM_BASE_POKEMON):   
            rand_num = RandomGen.randint(0,team_size)
            team_sorted_list.add(ListItem(rand_num, rand_num))  #add to team_numbers
            
        #Store calculated number of base pokemon in team_numbers list to be initialised
        team_numbers = []   #list for storing output of random team gen
        for i in range(1, len(team_sorted_list)):  #access index of list for pokemon calc 1-last index
            team_numbers[i-1]= team_sorted_list[i].value - team_sorted_list[i-1].value  

        if ai_mode == None:
            ai_mode = PokeTeam.AI.RANDOM

        return PokeTeam(team_name, team_numbers, battle_mode, ai_mode)
        # ----------------------------------------------------------------------

     
        

    # TODO
    def return_pokemon(self, poke: PokemonBase) -> None:
        if self.battle_mode == 0:
            self.team.reverse()
            self.team.push(poke)
            self.team.reverse()
        elif self.battle_mode == 1:
            self.team.append(poke)
        elif self.battle_mode == 2:
            pass

    # TODO
    def retrieve_pokemon(self) -> PokemonBase | None:
        if self.battle_mode == 0:
            self.team.reverse()
            item = self.team.pop()
            self.team.reverse()
            return item
        elif self.battle_mode == 1:
            return self.team.serve()
        elif self.battle_mode == 2:
            pass

    # TODO
    def special(self):
        if self.battle_mode == 0:
            last = self.team.pop()
            self.team.reverse()
            first = self.team.pop()
            self.team.push(last)
            self.team.reverse()
            self.team.push(first)
        elif self.battle_mode == 1:
            count_first_half = len(self.team)//2
            temp_stack = ArrayStack(count_first_half)
            for _ in range(count_first_half):
                temp_stack.push(self.team.serve())
            for _ in range(count_first_half):
                self.team.append(temp_stack.pop())
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
            actions = list(Action)
            if self.heal_count == 0:
                actions.remove(Action.HEAL)
            return Action(RandomGen.randint(len(actions)))
        
        elif self.battle_mode == PokeTeam.AI.USER_INPUT:
            prompt = "A [ATTACK], P [SWAP], H [HEAL], S [SPECIAL]"
            actions = list("A", "P", "H", "S")
            while True:
                print(prompt)
                action = input("   Your Move: ")
                if action not in actions:
                    raise ValueError("Invalid action. Please try again.")
                break
            if action == "A":
                return Action.ATTACK
            elif action == "P":
                return Action.SWAP
            elif action == "H":
                return Action.HEAL
            elif action == "S":
                return Action.SPECIAL

    @classmethod
    def leaderboard_team(cls):
        raise NotImplementedError()

    def pokemonsStack(self) -> ArrayStack: # TODO convert team_members to a reversed stack
        pass

    def pokemonsCircularQueue(self) -> CircularQueue: # TODO convert team_members to a circular queue
        pass


