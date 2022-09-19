from __future__ import annotations
from ast import Num
from multiprocessing.dummy import Array
from multiprocessing.sharedctypes import Value
from random import Random
from tracemalloc import start
from typing import List
from sorted_list import ListItem
from pokemon import *
from array_sorted_list import ArraySortedList
from queue_adt import CircularQueue
from stack_adt import ArrayStack, Stack
from aset import ASet
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
    BASE_ORDER = [Charmander, Bulbasaur, Squirtle, Gastly, Eevee]
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
        if not ai_type in PokeTeam.AI:
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
        self.initial_order_exist = False
        self.poke_on_field = None   #initialise pokemon on field
        self.descending_order = True #Initially true by default descending
        self.regenerate_team()


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
        team_sorted_list = ArraySortedList((cls.NUM_BASE_POKEMON + 1))
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
        team_numbers = [0]* (cls.NUM_BASE_POKEMON) #list for storing output of random team gen
        for i in range(1, len(team_sorted_list)):  #access index of list for pokemon calc 1-last index
            team_numbers[i-1]= team_sorted_list[i].value - team_sorted_list[i-1].value  

        if ai_mode == None:
            ai_mode = PokeTeam.AI.RANDOM
        
        return PokeTeam(team_name, team_numbers, battle_mode, ai_mode, **kwargs)
        # ----------------------------------------------------------------------

    # TODO
    def return_pokemon(self, poke: PokemonBase) -> None:
        if not poke.is_fainted():
            if self.battle_mode == 0:
                self.team = self.team.reverse()
                self.team.push(poke)
                self.team = self.team.reverse()
            elif self.battle_mode == 1:
                self.team.append(poke)
            elif self.battle_mode == 2:
                self.sort_into_team(poke)
        else:
            return
    # TODO
    def retrieve_pokemon(self) -> PokemonBase | None:
        if self.battle_mode == 0:
            self.team = self.team.reverse()
            self.poke_on_field = self.team.pop()
            self.team = self.team.reverse()
        elif self.battle_mode == 1:
            self.poke_on_field = self.team.serve()
        elif self.battle_mode == 2:
            # self.current_poke_order = self.team[0].order    #store order and key for return
            # self.current_poke_key = self.team[0].key
            self.poke_on_field = self.team[0].value  #First pokemon in list is the one for battle
            self.team.delete_at_index(0)
            
        return self.poke_on_field
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
            self.return_pokemon(self.poke_on_field)
            self.team.reverse_order()

    
    # TODO
    def regenerate_team(self):
        if self.battle_mode == 0:
            self.team = self.team_mode_0()
        elif self.battle_mode == 1:
            self.team = self.team_mode_1()
        elif self.battle_mode == 2:
            self.initial_order_exist = False
            self.descending_order = True
            self.team = self.team_mode_2()


    # TODO
    def __str__(self):
        # Dawn (2): [LV. 1 Gastly: 6 HP, LV. 1 Squirtle: 11 HP, LV. 1 Eevee: 10 HP, LV. 1 Bulbasaur: 13 HP, LV. 1 Charmander: 9 HP]"
        # "LV. 5 Venusaur: 17 HP"
        str = f"{self.team_name} ({self.battle_mode}): ["
        if self.battle_mode == 0:
            str += self.stack_string()
        if self.battle_mode == 1:
            str += self.queue_string()
        if self.battle_mode == 2:
            str += self.list_string()
        str += "]"
        return str
    
    def stack_string(self):
        """
        Returns string containing all elements of stack
        """
        stack_string = "" #initialise empty string for input of stack elements
        temp_stack = ArrayStack(len(self.team)) #initialise empty storage stack for holding popped elements for return
        while not self.team.is_empty():
            top = self.team.pop()
            stack_string += str(top) + ", "
            temp_stack.push(top)
        while not temp_stack.is_empty():
            self.team.push(temp_stack.pop())    #return all elements back to original stack
        return stack_string[:-2]    #do not include last comma and whitespace

    def queue_string(self):
        """
        Method that returns all the elements of a queue in string form
        """
        queue_string = "" #initialise empty string for input of stack elements
        temp_queue = CircularQueue(len(self.team)) #initialise empty storage stack for holding popped elements for return
        while not self.team.is_empty():
            top = self.team.serve()
            queue_string += str(top) + ", "
            temp_queue.append(top)
        while not temp_queue.is_empty():
            self.team.append(temp_queue.serve())    #return all elements back to original stack
        return queue_string[:-2]    #do not include last comma and whitespace

    def list_string(self):
        """
        Method that returns a string with all list elements
        """
        list_string = "" #initialise empty string
        for item in self.team:  #access ListItem elements
            list_string += str(item.value) + ", "
        return list_string[:-2] #do not include last comma and whitespace

    def is_empty(self):
        return self.team.is_empty()


    def choose_battle_option(self, my_pokemon: PokemonBase, their_pokemon: PokemonBase) -> Action:
        
        if self.ai_type == PokeTeam.AI.ALWAYS_ATTACK:
            return Action.ATTACK
        
        elif self.ai_type == PokeTeam.AI.SWAP_ON_SUPER_EFFECTIVE:
            if their_pokemon.poke_type.type_multiplier(my_pokemon.poke_type) >= 1.5:
                return Action.SWAP 
            else:
                return Action.ATTACK
        
        elif self.ai_type == PokeTeam.AI.RANDOM:
            actions = list(Action)
            if self.heal_count == 0:
                actions.remove(Action.HEAL)
            return Action(RandomGen.randint(len(actions)))
        
        elif self.ai_type == PokeTeam.AI.USER_INPUT:
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

    def team_mode_0(self) -> ArrayStack:
        team_stack = ArrayStack(sum(self.team_numbers))
        for idx, num_pokemon in enumerate(self.team_numbers):
            for _ in range(num_pokemon):
                pokemon = self.get_base_pokemon(idx)
                team_stack.push(pokemon)
        return team_stack

    def team_mode_1(self) -> CircularQueue:
        team_queue = CircularQueue(sum(self.team_numbers))
        for i, num_pokemon in enumerate(self.team_numbers):
            for _ in range(num_pokemon):
                pokemon = self.get_base_pokemon(i)
                team_queue.append(pokemon)
        return team_queue

    def get_base_pokemon(self, i: int) -> PokemonBase:
        pokemon = PokeTeam.BASE_ORDER[i]
        if pokemon == Charmander:
            p_instance = Charmander()
        elif pokemon == Bulbasaur:
            p_instance = Bulbasaur()
        elif pokemon == Squirtle:
            p_instance = Squirtle()
        elif pokemon == Gastly:
            p_instance = Gastly()
        elif pokemon == Eevee:
            p_instance = Eevee()
        return p_instance

    def team_mode_2(self):
        """
        Initial team for battle mode 2
        """
        sort_by = self.criterion
             
        team_list = ArraySortedList(sum(self.team_numbers))
        ### Add to list by team_numbers###
        for poke_idx, num_of_poke in enumerate(self.team_numbers):
            for _ in range(1, num_of_poke+1):
                poke_to_add = self.get_base_pokemon(poke_idx)
                if sort_by == Criterion.DEF:
                    key = poke_to_add.get_defence()
                elif sort_by == Criterion.HP:
                    key = poke_to_add.get_hp()
                elif sort_by == Criterion.LV:
                    key = poke_to_add.get_level()
                elif sort_by == Criterion.SPD:
                    key = poke_to_add.get_speed()
                assert type(key) == int, "Key is invalid: not an integer"
                team_list.add(ListItem(poke_to_add, key)) #Sorted list by first criterion.
                
            # for _ in range(1, num_of_poke+1):
            #     team_list.add(ListItem(poke_to_add, key)) #Sorted list by first criterion.
        
        ### Sort initial team ###
        criterion_list = team_list.reverse_order()  #criterion descending initially.
        
        unique_keys = ASet(len(criterion_list)) 
        for idx, item in enumerate(criterion_list):
            if not item.key in unique_keys:
                unique_keys.add(item.key)
            else:   #If tie exist, sort by pokedex_order 
                tie_start_idx = idx - 1 #if the item is in set, means previous was the start of the tie
                tie_last_idx = criterion_list.get_last_index(item.key)
                self.break_tie(criterion_list, tie_start_idx, tie_last_idx)
        
        
        for num, item in enumerate(criterion_list, 1):  #Assign all in sorted list an order number from 1- length of list
            item.order = num
        self.initial_order_exist = True
        return criterion_list

    
    # def check_break_tie(self, criterion_list: ArraySortedList):
    #     unique_keys = Aset()
    #     for idx, item in enumerate(criterion_list):
    #         if not item.key in unique_keys:
    #             unique_keys.add(item.key)
    #             if len(unique_keys) == len(criterion_list):
    #                 return criterion_list   #early exit condition, if all unique return list mark true?
    #         else:
    #             tie_start_idx = idx - 1 #if the item is in set, means previous was the start of the tie
    #             tie_last_idx = criterion_list.get_last_index(item.key)
    #             pokedex_ordered_list = criterion_list.break_by_pokeno(tie_start_idx, tie_last_idx)

    #             for idx in range(tie_start_idx, tie_last_idx + 1):
    #                 criterion_list.swap_at_index(idx, pokedex_ordered_list[idx])
        
    #     #if no initial order (first time calling)
    #     if self.initial_order is False:
    #         for init_order, item in enumerate(criterion_list, 1):
    #             item.order = init_order
    #     else:
    #         self.sort_by_init(criterion_list)
            
    # def sort_by_init(self, list_to_sort: ArraySortedList):
    #     unique_keys = Aset()
    #     for idx, item in enumerate(list_to_sort):
    #             if not item.key in unique_keys:
    #                 unique_keys.add(item.key)
    #             else:
    #                 tie_start_idx = idx - 1 #if the item is in set, means previous was the start of the tie
    #                 tie_last_idx = list_to_sort.get_last_index(item.key)
    #                 pokedex_ordered_list = list_to_sort.break_by_order(tie_start_idx, tie_last_idx)
    #                 for idx in range(tie_start_idx, tie_last_idx + 1):
    #                     list_to_sort.swap_at_index(idx, pokedex_ordered_list[idx])

    #     # if self.is_tied():
    #     #     #use initial ordering to break again
    #     #     #if initial ordering not none: sort by initial
    #     #     if 
        #     #else set initial ordering.



                # unique_poke_keys.add(key)   #add key to set of keys

                # #If there is new element added to set, remove 
                # if key in unique_poke_keys: #Case where there is a tie
                #     new_key = poke_to_add.POKE_NO
                #     pokeorder_break.add
                #     pokeorder_break.add(poke_to_add, new_key)
                
                # else:
                #     pokeorder_break.add(poke_to_add, poke_to_add.POKE_NO)  #sort by pokedex ordering


    
    def sort_into_team(self, pokemon):
        """
        Takes Pokemon and sorts back into team
        :pre: Pokemons key must be valid (already reversed for descending order)
        """
        ### SORT BY FIRST KEY: CRITERION ###
        # if self.descending_order == True:
        #     self.team = self.team.reverse_order()
        self.criterion_order(pokemon)
        ### CHECK IF TIE ###
        unique_key = ASet(len(self.team))   
        for idx, item in enumerate(self.team):
            if not item.key in unique_key:
                unique_key.add(item.key)
            else:
                tie_start_idx = idx - 1 #if the item is in set, means previous was the start of the tie
                tie_end_idx = self.team.get_last_index(item.key)
        ### SORT BY POKEDEX and INITIAL(Initial check done inside pokedex) ###
                self.break_tie(self.team, tie_start_idx, tie_end_idx)
        
        

    
                
    def criterion_order(self, pokemon):
    
        poke_to_add = pokemon
        if self.criterion == Criterion.DEF:
            key = poke_to_add.get_defence()
        elif self.criterion == Criterion.HP:
            key = poke_to_add.get_hp()
        elif self.criterion == Criterion.LV:
            key = poke_to_add.get_level()
        elif self.criterion == Criterion.SPD:
            key = poke_to_add.get_speed()
        if self.descending_order == True:
            key = key * -1 #reverse order by default. Could be problem if team is positive and this reverses
        # self.current_poke_key = key
        if not self.team.is_full():
            self.team.add(ListItem(poke_to_add, key)) #Sorted list by first criterion.
        else:
            raise ValueError("Team is full")
    
    def break_tie(self, team_list: ArraySortedList, start_idx: int, end_idx: int):
        team_tie_start = start_idx   #store the start of tie in reference to team_list.
        tie_range = end_idx - start_idx
        pokeorder_list = ArraySortedList(tie_range +1)
        
        while start_idx <= end_idx:
            pokemon = team_list[start_idx].value
            # previous_key = team_list[start_idx].key
            key = pokemon.POKE_NO
            pokeorder_list.add(ListItem(pokemon,key))
            start_idx += 1
        assert len(pokeorder_list) == (tie_range+1), f"Number of elements in list do not match index range of tie: Tie Range: {(tie_range +1)}, Len Pokeorder list: {len(pokeorder_list)}, Tie List: {pokeorder_list}, Team State: {self.team}. "

        if self.initial_order_exist is True: #if true check/sort again
            unique_poke_nums = ASet(len(pokeorder_list))   
            for idx, item in enumerate(pokeorder_list):
                if not item.key in unique_poke_nums:
                    unique_poke_nums.add(item.key)
                else:
                    
                    tie_start_idx = idx - 1 #if the item is in set, means previous was the start of the tie
                    tie_last_idx = pokeorder_list.get_last_index(item.key)
                    
                    self.initial_order(pokeorder_list, tie_start_idx, tie_last_idx)
        
        #Otherwise Return. No more sorting left
        #Swap newly sorted items back into team_list
        for idx, item in enumerate(pokeorder_list, team_tie_start):
            # item.order = idx can be done at end by controller
            #previous key should be set by swap at index
            team_list.swap_at_index(idx, item)
            
        
        return
    
    def initial_order(self, pokeorder_list: ArraySortedList, start_idx: int, end_idx: int):
        assert [type(x) == ListItem for x in pokeorder_list], "Items must be ListItem type"
        assert type(pokeorder_list) == ArraySortedList
        tie_range = end_idx - start_idx
        init_order_list = ArraySortedList(tie_range+1)
        pokeorder_tie_start = start_idx #store start of tie within pokeorder_list for swap later
        while start_idx <= end_idx:
            pokemon_item = pokeorder_list[start_idx]
            pokemon = pokemon_item.value
            # previous_key = team_list[start_idx].key
            key  = pokemon_item.order
            order = pokemon_item.order
            init_order_list.add(ListItem(pokemon,key, order))
            start_idx += 1
        assert len(init_order_list) == tie_range + 1, "Number of elements in list do not match index range of tie"
        for idx, item in enumerate(init_order_list, pokeorder_tie_start):
                #swap items according to initial order in poke_order_list
                pokeorder_list.swap_at_index(idx, item)
    
    # while start_idx <= end_idx:
    #         pokemon = team_list[start_idx].value
    #         # previous_key = team_list[start_idx].key
    #         key = pokemon.POKE_NO
    #         pokeorder_list.add(ListItem(pokemon,key))
    #         start_idx += 1

    ### TESTS LEFT ###

    #Test battle option attack

    #test special mode 1
