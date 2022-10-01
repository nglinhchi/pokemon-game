from __future__ import annotations
from array_sorted_list import ArraySortedList
from aset import ASet
from enum import Enum, auto
from pokemon_base import PokemonBase
from random_gen import RandomGen
from multiprocessing.dummy import Array
from multiprocessing.sharedctypes import Value
from tracemalloc import start
from stack_adt import ArrayStack
from sorted_list import ListItem
from pokemon import *
from queue_adt import CircularQueue

"""
Implements the methods to construct a team and implements the different battle modes.
"""

__author__ = "Scaffold by Jackson Goerner, Code by Chloe Nguyen | Joong Do Chiang"



class Action(Enum):
    """
    Enum class contains a list of valid actions
    """
    ATTACK = auto()
    SWAP = auto()
    HEAL = auto()
    SPECIAL = auto()
    
class Criterion(Enum):
    """
    Enum class contains a list of valid criterion to be used for sorting pokemon for battle mode 2
    """
    SPD = auto()
    HP = auto()
    LV = auto()
    DEF = auto()

class PokeTeam:
    """
    Implements methods related to poketeam creations and executions
    """
    
    POKEDEX_ORDER = [Charmander, Charizard, Bulbasaur, Venusaur, Squirtle, Blastoise, Gastly, Haunter, Gengar, Eevee]
    BASE_ORDER = [Charmander, Bulbasaur, Squirtle, Gastly, Eevee]
    MAX_TEAM_SIZE = 6
    NUM_BASE_POKEMON = 5

    class AI(Enum):
        """
        Enum class contains a list of valid AI modes to be used for choosing actions in a battle
        """
        ALWAYS_ATTACK = auto()
        SWAP_ON_SUPER_EFFECTIVE = auto()
        RANDOM = auto()
        USER_INPUT = auto()


    def __init__(self, team_name: str, team_numbers: list[int], battle_mode: int, ai_type: PokeTeam.AI, criterion=None, criterion_value=None) -> None:
        """
        Creates user-specified Poketeam
        :param arg1: string of the teams name
        :param arg2: list of integers representing the num of each base pokemon
        :param arg3: integer of the battle mode
        :param arg4: AI class variable
        :param arg5: optional Criterion class variable that determines the criteria for ordering
        :pre:
            arg1 is a string
            arg2 must have length equal to number of base pokemons (5), and must have a total less than max team size (6)
            arg3  must be a valid battle mode (0,1,2)
            arg4 must be a valid ai type (ai enum)
            arg5 if provided must be a valid criterion (criterion enum)
        :complexity:
            best case is O(1)
            worst case is O(n)
            where n is len(team_numbers)
        """ 
        if not type(team_name) == str:
            raise ValueError("Team name must be string")

        if not len(team_numbers) == PokeTeam.NUM_BASE_POKEMON :  #Number of elements in list must equal number of base Pokemon
            raise ValueError(f"Team number length is not valid. The each base Pokemon must correspond to an element in list")

        for num in team_numbers:
            if type(num) != int:
                raise ValueError("Elements in list must be integers")

        if not sum(team_numbers) <= PokeTeam.MAX_TEAM_SIZE:
            raise ValueError("Number of Pokemon exceeds max team size")

        if battle_mode not in [0,1,2]:
            raise ValueError("Not valid Battle Mode")

        if not ai_type in PokeTeam.AI:
            raise TypeError("AI Type is not valid")
        #If battle_mode == 2, criterion provided and in Criterion class
        if battle_mode == 2:
            assert criterion != None, "Criterion for sorting must be provided for Battle Mode 2"
            assert criterion in Criterion, f"{criterion} is not a valid criterion"
            
        # initialise
        self.team = None
        self.team_name = team_name
        self.team_numbers = team_numbers
        self.battle_mode = battle_mode
        self.ai_type =  ai_type
        self.criterion = criterion
        self.heal_count = 3
        self.break_by_init = False
        self.initial_order_exist = False
        self.poke_on_field = None   #initialise pokemon on field
        self.descending_order = False #Initially true by default descending
        self.regenerate_team()  #create team

    @classmethod
    def random_team(cls, team_name: str, battle_mode: int, team_size=None, ai_mode=None, **kwargs) -> PokeTeam:
        """
        Creates random generated Poketeam.
        :param arg1: string of the teams name
        :param arg2: integer of the battle mode
        :param arg3: optional integer representing team size
        :param arg4: optional AI class variable
        :pre: team_size must be positive integer
        :return: PokeTeam instance of the team
        :complexity:
            best case is O(1)
            worst case is O(n)
            where n is len(team_members)
        """
        # assign team_size:
        if team_size is not None:
            if not isinstance(team_size, int) or team_size <= 0:
                raise ValueError("Team size must be positive integer")
        
        if team_size == None:
            if cls.MAX_TEAM_SIZE % 2 != 0:
                half_team_max = cls.MAX_TEAM_SIZE // 2 + 1 #Between half of Pokemon limit and Pokemon limit- can't be less than half (floor division)
            else:
                half_team_max = cls.MAX_TEAM_SIZE//2
            team_size = RandomGen.randint(half_team_max, cls.MAX_TEAM_SIZE)

        start_val = ListItem(0, 0) #value and key to sort by are same
        end_val = ListItem(team_size, team_size)
        team_sorted_list = ArraySortedList((cls.NUM_BASE_POKEMON + 1))
        team_sorted_list.add(start_val) #add 0
        team_sorted_list.add(end_val)   #add team size
        
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

    def get_battle_mode(self) -> int:
        """
        Getter method returning battle mode in use
        :complexity:
            best case is O(1)
            worst case is O(1)
        """
        return self.battle_mode

    def get_ai_type(self):
        """
        Getter method returning ai type in use
        :complexity:
            best case is O(1)
            worst case is O(1)
        """
        return self.ai_type

    def get_heal_count(self):
        """
        Getter method returning remaining heal count
        :complexity:
            best case is O(1)
            worst case is O(1)
        """
        return self.heal_count

    def use_heal(self):
        """
        Performs heal action
        :complexity:
            best case is O(1)
            worst case is O(1)
        """
        self.heal_count = self.get_heal_count() - 1

    def return_pokemon(self, poke: PokemonBase) -> None:
        """
        Returns the on field pokemon back to the team.
        :param: a PokemonBase representing the team to return the pokemon to
        :return: None
        :complexity: 
            best case is O(1) if battle mode = 1
            worst case is O(n) when battle mode = 0 or 2
            where n is len(team)
        """
        if not (poke == None or poke.is_fainted()):
            poke.status_effect = None
            if self.battle_mode == 0:
                if self.team.is_full():
                    raise ValueError(f"print {self}")
                self.team.push(poke)
            elif self.battle_mode == 1:
                self.team.append(poke)
            elif self.battle_mode == 2:
                self.sort_into_team(poke)
        else:
            return
    
    def retrieve_pokemon(self) -> PokemonBase | None:
        """
        Retrieves a pokemon from the team and makes them the pokemon on field.
        :return: PokemonBase of the pokemon thats on the field or None if the team is empty
        :complexity:
            best case is O(1) when battle mode = 1
            worst case is O(n) when battle mode = 0 or 2
            where n is len(team)
        """
        if self.team.is_empty():
            raise ValueError("Team Empty")
        else:
            if self.battle_mode == 0:
                self.poke_on_field = self.team.pop()
            elif self.battle_mode == 1:
                self.poke_on_field = self.team.serve()
            elif self.battle_mode == 2:
                self.current_poke_key = self.team[0].key
                self.current_poke_order = self.team[0].order
                self.poke_on_field = self.team.delete_at_index(0).value  #First pokemon in list is the one for battle
        return self.poke_on_field
    
    def special(self):
        """
        Changes ordering for pokemon in team depending on battle mode. 
        :pre: All pokemon should be returned to team
        :post: All pokemon remain in team in new ordering
        :complexity:
            best case is O(n)
            worst case is O(n)
            where n is len(team)
        """
        if self.battle_mode == 0:
            if len(self.team) >= 2:
                first = self.team.pop()
                self.team = self.team.reverse()
                last = self.team.pop()
                self.team.push(first)
                self.team = self.team.reverse()
                self.team.push(last)
        elif self.battle_mode == 1:
            count_first_half = len(self.team)//2
            temp_stack = ArrayStack(count_first_half)
            for _ in range(count_first_half):
                temp_stack.push(self.team.serve())
            for _ in range(count_first_half):
                self.team.append(temp_stack.pop())
        elif self.battle_mode == 2:
            self.team = self.reverse_order()
            if self.descending_order == True:
                self.descending_order = False
            elif self.descending_order == False:
                self.descending_order = True
    def regenerate_team(self):
        """
        Regenerates the team based from the same battle numbers
        :return: None
        :complexity: 
            best case is O(n) when battle mode = 0 or 1
            worst case is O(nlogn) when battle mode = 2
            where n = sum(team_numbers)
        """
        self.heal_count = 3
        if self.battle_mode == 0:
            self.team = self.team_mode_0()
        elif self.battle_mode == 1:
            self.team = self.team_mode_1()
        elif self.battle_mode == 2:
            self.initial_order_exist = False
            self.descending_order = False
            self.team = self.team_mode_2()

    def get_team(self):
        """
        Getter methods returning team containing pokemons.
        :pre: team must be instantiated
        :complexity:
            best case is O(1)
            worst case is O(1)
        """
        if self.team == None:
            raise ValueError("Team has not been created")
        return self.team


    def __str__(self) -> str:
        """
        Returns a string output of the current state of the team.
        :return: string output of the team
        :complexity:
            best case is O(n)
            worst case is O(n)
        """
        str = f"{self.team_name} ({self.battle_mode}): ["
        if self.battle_mode == 0:
            str += self.stack_string()
        if self.battle_mode == 1:
            str += self.queue_string()
        if self.battle_mode == 2:
            str += self.list_string()
        str += "]"
        return str
    
    def stack_string(self) -> str:
        """
        Returns string containing all elements of stack
        :return: string output of the stack
        :complexity:
            best case is O(n)
            worst case is O(n)
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

    def queue_string(self) -> str:
        """
        Method that returns all the elements of a queue in string form
        :return: string output of the queue
        :complexity:
            best case is O(1)
            worst case is O(1)
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

    def list_string(self) -> str:
        """
        Method that returns a string with all list elements.
        :return: string output of the list
        :complexity:
            best case is O(1)
            worst case is O(1)
        """
        list_string = "" #initialise empty string
        for idx in range(len(self.team)):  #access ListItem elements
            list_string += str(self.team[idx].value) + ", "
        return list_string[:-2] #do not include last comma and whitespace

    def is_empty(self) -> bool:
        """
        Method determining if the team is empty.
        :return: True if the team is empty, False otherwise
        :complexity:
            best case is O(1)
            worst case is O(1)
        """
        return self.team.is_empty()


    def choose_battle_option(self, my_pokemon: PokemonBase, their_pokemon: PokemonBase) -> Action:
        """
        Selects what action should be taken in the battle.
        :param arg1: PokemonBase of the player's team
        :param arg2: PokemonBase of the opponent's team
        :return: action from Action class
        :complexity:
            best case is O(1) when ai type is ALWAYS_ATTACK or SWAP_ON_SUPER_EFFECTIVE
            worst case is O(n) when ai type is RANDOM or USER_INPUT where n is number of actions
        """
        if self.get_ai_type() == PokeTeam.AI.ALWAYS_ATTACK:
            return Action.ATTACK
        elif self.get_ai_type() == PokeTeam.AI.SWAP_ON_SUPER_EFFECTIVE:
            if their_pokemon.get_type().type_multiplier(my_pokemon.get_type()) >= 1.5:
                return Action.SWAP 
            else:
                return Action.ATTACK
        elif self.get_ai_type() == PokeTeam.AI.RANDOM:
            actions = list(Action)
            if self.get_heal_count() == 0:
                actions.remove(Action.HEAL)
            return actions[RandomGen.randint(0, len(actions)- 1)]
        elif self.get_ai_type() == PokeTeam.AI.USER_INPUT:
            prompt = "A [ATTACK], P [SWAP], H [HEAL], S [SPECIAL]"
            actions = list("APHS")
            while True:
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

    def get_base_pokemon(self, i: int) -> PokemonBase:
        """
        Creates an instance of the pokemon from the list of base pokemon order
        :return: PokemonBase of the required pokemon
        :complexity:
            best case is O(1)
            worst case is O(1)
        """
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

    def team_mode_0(self) -> ArrayStack:
        """
        Method generates a stack of pokemon instances from a list of base pokemon.
        :return: a stack of all the team's pokemon
        :complexity:
            best case is O(n)
            worst case is O(n)
            where n is the num of pokemon (ie. sum(team_numbers))
        """
        team_stack = ArrayStack(sum(self.team_numbers))
        for idx, num_pokemon in enumerate(self.team_numbers):
            for _ in range(num_pokemon):
                pokemon = self.get_base_pokemon(idx)
                team_stack.push(pokemon)

        return team_stack.reverse()


    def team_mode_1(self) -> CircularQueue:
        """
        Method generates a queue of pokemon instances from a list of base pokemon.
        :return: a queue of all the team's pokemon
        :complexity: 
            best case is O(n)
            worst case is O(n)
            where n is the num of pokemon(ie. sum(team_numbers))
        """
        team_queue = CircularQueue(sum(self.team_numbers))
        for i, num_pokemon in enumerate(self.team_numbers):
            for _ in range(num_pokemon):
                pokemon = self.get_base_pokemon(i)
                team_queue.append(pokemon)
        return team_queue


    def team_mode_2(self) -> ArraySortedList:
        """
        Initial team for battle mode 2.
        :return: sorted list of all the pokemon
        :complexity: 
            best case is O(nlogn)
            worst case is O(nlogn)
            where n is sum(team_numbers)
        """
        sort_by = self.criterion
             
        criterion_list = ArraySortedList(sum(self.team_numbers))
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
                criterion_list.add(ListItem(poke_to_add, key)) #Sorted list by first criterion.
        
        ### Sort initial team ###
        self.team = criterion_list 
        
        unique_keys = ASet(len(criterion_list)) 
        for idx, item in enumerate(criterion_list):
            if not item.key in unique_keys:
                unique_keys.add(item.key)
            else:   #If tie exist, sort by pokedex_order 
                tie_start_idx = idx - 1 #if the item is in set, means previous was the start of the tie
                tie_last_idx = criterion_list.get_last_index(item.key)
                self.break_tie(criterion_list, tie_start_idx, tie_last_idx)
        
        self.team = self.reverse_order()    #criterion list reversed
        self.descending_order = True
        for num, item in enumerate(self.team, 1):  #Assign all in sorted list an order number from 1- length of list
            item.order = num
        self.initial_order_exist = True
        return self.team
        
    def reverse_order(self):
        """
        Takes input array sorted in ascending order and reverses it using the same key so that the array is descending.
        :return: descending sorted array
        :complexity:
            best case is O(n)
            worst case is O(n)
            where n is len(team)
        """
        reverse_arr = ArraySortedList(len(self.get_team().array))
        for idx in range(len(self.get_team())):
            key = self.get_team()[idx].key * -1
            poke_to_add = self.get_team()[idx].value
            order = self.get_team()[idx].order 
            reverse_arr.add_in_front(ListItem(poke_to_add, key, order))
        return reverse_arr
    
    def sort_into_team(self, pokemon: PokemonBase) -> None:
        """
        Takes Pokemon and sorts back into team. Default method to be called when returning Pokemon in Battle Mode 2. 
        Sorts by Criterion order -> PokeDex Number -> Initial ordering.

        :pre: Pokemon must be of PokemonBase class, Poketeam must have already been initialised (have initial order)
        :return: None
        :complexity:
            best case is O(n)
            worst case is O(n)
            where n is length of self.team
        """
        if not isinstance(pokemon, PokemonBase):
            raise ValueError("Pokemon must be PokemonBase class")
        ### SORT BY FIRST KEY: CRITERION ###
        self.criterion_order(pokemon)
        ### CHECK IF TIE ###
        if len(self.team) >= 1:  #if not only pokemon on team 
            try:
                unique_key = ASet(len(self.team))   
                for idx in range(len(self.team)):
                # for idx, item in enumerate(self.team):
                    if not self.team[idx].key in unique_key:
                        unique_key.add(self.team[idx].key)
                    else:
                        tie_start_idx = idx - 1 #if the item is in set, means previous was the start of the tie
                        tie_end_idx = self.team.get_last_index(self.team[idx].key)
                ### SORT BY POKEDEX and INITIAL(Initial check done inside pokedex) ###
                        self.break_tie(self.team, tie_start_idx, tie_end_idx)
            except:
                raise ValueError(f" Set : {unique_key}, Team : {self.team}, {pokemon}, {self.team[idx].key}, {self.team[idx].order}")
        

    def criterion_order(self, pokemon) -> None:
        """
        Adds a pokemon to the team ordered based on the specified criterion
        :param: pokemon instance to be added
        :return: None
        :complexity:
            best case is O(logn)
            worst case is O(logn)
        """
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
            key = key * -1
        if not self.team.is_full():
            self.team.add(ListItem(poke_to_add, key, self.current_poke_order)) #Sorted list by first criterion.
        else:
            raise ValueError("Team is full")
    
    def break_tie(self, team_list: ArraySortedList, start_idx: int, end_idx: int):
        """
        Method breaks a tie by the pokemon order or further by their
        initial ordering of the team
        :param arg1: sorted array containing the team's pokemon
        :param arg2: integer representing the starting index where the pokemon have a tie
        :param arg3: integer representing the ending index where the pokemon have a tie
        :return: None
        :complexity:
            best case is O(mlogn)
            worst case is O(mlogn)
            where m is range of tie index and n is length of pokeorder_list
        """
        team_tie_start = start_idx   #store the start of tie in reference to team_list.
        tie_range = end_idx - start_idx
        pokeorder_list = ArraySortedList(tie_range +1)
        
        while start_idx <= end_idx:
            pokemon_item = team_list[start_idx]
            pokemon = pokemon_item.value
            key = pokemon.POKE_NO
            if self.descending_order == False:
                key = key * -1
            order = pokemon_item.order
            pokeorder_list.add(ListItem(pokemon,key, order))
            start_idx += 1
        assert len(pokeorder_list) == (tie_range+1), f"Number of elements in list do not match index range of tie: Tie Range: {(tie_range +1)}, Len Pokeorder list: {len(pokeorder_list)}, Tie List: {pokeorder_list}, Team State: {self.team}. "

        if self.initial_order_exist is True: #if true check/sort again
            unique_poke_nums = ASet(len(pokeorder_list))   
            for idx in range(len(pokeorder_list)):
                if not pokeorder_list[idx].key in unique_poke_nums:
                    unique_poke_nums.add(pokeorder_list[idx].key)
                else:
                    self.break_by_init = True
                    tie_start_idx = idx - 1 #if the item is in set, means previous was the start of the tie
                    tie_last_idx = pokeorder_list.get_last_index(pokeorder_list[idx].key)
                    
                    self.initial_order(pokeorder_list, tie_start_idx, tie_last_idx)
        #Otherwise Return. No more sorting left
        #Swap newly sorted items back into team_list
        for idx in range(len(pokeorder_list)):
            pokeorder_list[idx]
            team_list.swap_at_index(team_tie_start, pokeorder_list[idx])
            team_tie_start += 1  
        return
    
    def initial_order(self, pokeorder_list: ArraySortedList, start_idx: int, end_idx: int):
        """
        Breaks further ties using the initial ordering of the team
        :param arg1: sorted list of pokemon's order
        :param arg2: starting index of the pokemon which are tied
        :param arg2: ending index of the pokemon which are tied
        :return: None
        :complexity:
            best case is O(mlogn)
            worst case is O(mlogn)
            where m is the tie range and n is len(team)
        """
        assert [type(x) == ListItem for x in pokeorder_list], "Items must be ListItem type"
        assert type(pokeorder_list) == ArraySortedList
        tie_range = end_idx - start_idx
        init_order_list = ArraySortedList(tie_range+1)
        pokeorder_tie_start = start_idx #store start of tie within pokeorder_list for swap later
        while start_idx <= end_idx:
            pokemon_item = pokeorder_list[start_idx]
            pokemon = pokemon_item.value
            key  = pokemon_item.order
            if self.descending_order == False:
                key = key * -1
            order = pokemon_item.order
            item_to_add = ListItem(pokemon,key, order)
            assert type(pokemon_item.order) == int, f"{pokemon_item.order}"
            init_order_list.add(item_to_add)
            start_idx += 1
        assert len(init_order_list) == tie_range + 1, "Number of elements in list do not match index range of tie"
        for idx, item in enumerate(init_order_list, pokeorder_tie_start):
                #swap items according to initial order in poke_order_list
                pokeorder_list.swap_at_index(idx, item)
