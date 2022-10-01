from __future__ import annotations
from unicodedata import name
from bset import BSet
from poke_team import PokeTeam, Criterion
from battle import Battle
from linked_list import LinkedList
from random_gen import RandomGen
from stack_adt import ArrayStack
import unittest

"""
Creates battletower class that implements all methods needed to create and run a tower between user team and opponent teams
with the aid of battletower iterator.
"""

__author__ = "Scaffold by Jackson Goerner, Code by Chloe Nguyen"



class BattleTower:
    """
    Implements methods for battle tower creation.
    """

    def __init__(self, battle: Battle|None=None) -> None:
        """
        Instantiates new battletower instance
        :param arg1: battle instance that will be used to perform battles between user team and opponent teams
        :complexity:
            best case is O(1)
            worst case if O(1)
        """
        if battle is not None:
            self.battle = battle
        else:
            self.battle = Battle()
        self.me = None
        self.opponents = LinkedList()
        self.end_tower = False
    
    def set_my_team(self, team: PokeTeam) -> None:
        """
        Assigns the value for user team of the tower.
        :param arg1: user team that will be facing and battling with opponent teams
        :complexity:
            best case is O(1)
            worst case is O(1)
        """
        self.me = team

    def generate_teams(self, n: int) -> None:
        """ Generates a number of teams based on user input, where each time will be assigned with a random number of lives.
        These teams will be added to the opponents list of tower.
        :param arg1: number of opponent teams user would like to have in the tower
        :pre: n must be a positive integer
        :complexity:
            best case is O(n)
            worse case is O(n)
            where n is len(opponents) (i.e. n provided by user)
        """
        if type(n) is not int or n < 0:
            raise ValueError("n must be a positive integer")
        teams = LinkedList(n)
        for i in range(n):
            team_name = f"Team {i}"
            battle_mode = RandomGen.randint(0,1)
            opponent = PokeTeam.random_team(team_name, battle_mode)
            opponent.live = RandomGen.randint(2,10)
            teams.insert(i, opponent) 
        self.opponents = teams

    def __iter__(self):
        """
        Magic method, creates and returns an iterator for the tower
        :complexity:
            best case is O(1)
            worst case is O(1)
        """
        return BattleTowerIterator(self)

class BattleTowerIterator:

    def __init__(self, bt: BattleTower) -> None:
        """
        Instantiates the iterator for given battle tower.
        :param arg1: instance of battle tower that will be linked to the iterator
        :complexity:
            best case is O(1)
            worst case is O(1)
        """
        self.tower = bt
        self.current_opponent = bt.opponents.head
        self.previous_opponent = None
        
    def __iter__(self):
        """
        Returns itself, as required to be iterable.
        :complexity:
            best case is O(1)
            worst case is O(1)
        """
        return self

    def __next__(self):
        """ Performs 1 battle in tower, between current opponent and user team and returns battle result, 
        user team after battle, opponent team after battle, remaining lives of opponent team
        :raises StopIteration: if user previously lose a battle, or has defeated all opponent teams (i.e. opponents list is empty)
        :complexity:
            best case is O(1) if there's no oponnent teams in tower
            worst case is O(B), where there's at least one opponent team in tower, where B is complexity of battle()
        """
        if self.tower.end_tower:  
            raise StopIteration     
        else:                     

            # IF REACH END OF LIST + STILL CONTAINS OPPONENTS --> GO BACK TO HEAD TO ITERATE
            if (self.current_opponent is None) and (self.current_opponent is not self.tower.opponents.head):        
                self.current_opponent = self.tower.opponents.head                                                   
            
            # IF LIST STILL CONTAINTS OPPONENT --> BATTLE
            if self.current_opponent is not None:                                                                   
                # retrieve & regenerate user team and opponent team, get ready for battle
                opponent = self.current_opponent.item                                                               
                user = self.tower.me                                                                                
                user.regenerate_team()                                                                              
                opponent.regenerate_team()                                                                          
                
                # perform battle
                assert type(opponent) == PokeTeam and type(user) == PokeTeam, f"{opponent}, {user}"
                result = self.tower.battle.battle(user, opponent)

                # user team WIN/DRAW battle
                if result == 0 or result == 1:            
                    opponent.live -= 1                                      
                    # opponent has 0 lives, opponent is head -> change head
                    if opponent.live == 0 and opponent == self.tower.opponents.head.item:       
                        self.tower.opponents.head = self.current_opponent.next
                    # opponent has 0 lives, opponent is an intermediate node --> prev opponent point to current's next opponent (remove self from linked list)
                    elif opponent.live == 0:                                                    
                            self.previous_opponent.next = self.current_opponent.next
                    # opponent still have lives --> become the prev surviving opponent
                    elif opponent.live > 0:                                                     
                        self.previous_opponent = self.current_opponent
                    # standard assignment to point to next opponent
                    self.current_opponent = self.current_opponent.next                          
                
                # user team LOSE battle
                elif result == 2:
                     # set end_tower to false, next iter will raise StopIteration                                                           
                    self.tower.end_tower = True                                                

                # return (res, me, opponent, live)
                return (result, user, opponent, opponent.live)                             
            
            # IF LIST DOESN'T CONTAINS ANY OPPONENTS --> WIN
            else:
                self.tower.end_tower = True     
        
    def avoid_duplicates(self):
        """ Removes any opponent teams in tower that have more than 1 pokemons of the same type.
        :post: opponent teams' state remains unchanged
        :complexity:
            best case is O(N) if there's no opponent teams in tower,
            worst case is O(N*P) if there's at least 1 opponent team in tower,
            where N is the number of trainers remaining in the battle tower and P is the limit on the number of pokemon per team.
        """

        while self.current_opponent is not None:                           

            opponent_poke_team = self.current_opponent.item                 
            opponent_team = self.current_opponent.item.team                 
            type_set = BSet(len(opponent_team))                             
            contain_duplicates = False                                      
            
            # CHECK IF TEAM CONTAINS DUPLICATE
            # mode 0
            if opponent_poke_team.battle_mode == 0:                         
                temp_stack = ArrayStack(len(opponent_team))                 
                # iterate through stack -> check for duplicates
                for _ in range(len(opponent_team)):                         
                    pokemon = opponent_team.pop()                           
                    type_index = pokemon.get_type().get_type_index() + 1    
                    if type_index not in type_set:                          
                        type_set.add(type_index)                            
                    else:                                                   
                        contain_duplicates = True                           
                        break                                               
                # put back pokemon to team -> state of team remains unchanged
                for _ in range(len(temp_stack)):                             
                    opponent_team.push(temp_stack.pop())                    
            # mode 1
            elif opponent_poke_team.battle_mode == 1:
                undone_count = len(opponent_team)
                # iterate through queue -> check for duplicates
                for _ in range(len(opponent_team)):                         
                    pokemon = opponent_team.serve()                         
                    type_index = pokemon.get_type().get_type_index() + 1    
                    opponent_team.append(pokemon)   
                    undone_count -= 1                        
                    if type_index not in type_set:                          
                        type_set.add(type_index)
                    else:                                                   
                        contain_duplicates = True                           
                        break  
                # append the unserved pokemon to team -> state of team reamins unchanged
                for _ in range(undone_count):
                    opponent_team.append(opponent_team.serve())

            # HANDLE DELETION OF TEAMS WITH DUPLICATES
            if contain_duplicates:                                          
                if self.current_opponent == self.tower.opponents.head:      
                    self.tower.opponents.head = self.current_opponent.next  
                else:                                                       
                    self.previous_opponent.next = self.current_opponent.next
            
            # TEAM WITHOUT DUPLICATE BECOMES PREVIOUS OPPONENT
            else:                                                           
                self.previous_opponent = self.current_opponent              
            
            # STANDARD INCREMENT TO POINT TO NEXT OPPONENT FOR NEXT ITERATION
            self.current_opponent = self.current_opponent.next              