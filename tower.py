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
Creates battletower class that implements all methods needed to create and run a tower between user team and opponent teams,
with the aid of battletower iterator
"""
__author__ = "Scaffold by Jackson Goerner, Code by Chloe Nguyen"



class BattleTower:

    def __init__(self, battle: Battle|None=None) -> None:
        """
        :param arg1: battle instance that will be used to perform battles between user team and opponent teams
        """
        if battle is not None:
            self.battle = battle
        else:
            self.battle = Battle()
        self.me = None
        self.opponents = LinkedList()
        self.end_tower = False
    
    def set_my_team(self, team: PokeTeam) -> None:
        """ Assigns the value for user team of the tower
        :param arg1: user team that will be facing and battling with opponent teams
        :complexity: best and worst O(1)
        """
        self.me = team

    def generate_teams(self, n: int) -> None:
        """ Generates a number of teams based on user input, where each time will be assigned with 
            a random number of lives. These teams will be added to the opponents list of tower
        :pre: n must be a positive integer
        :param arg1: number of opponent teams user would like to have in the tower
        :complexity: best and worst O(N) where N is the length of opponents
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
        """ Magic method, creates and returns an iterator for the tower """
        return BattleTowerIterator(self)

class BattleTowerIterator:

    def __init__(self, bt: BattleTower) -> None:
        """
        :param arg1: instance of battle tower that will be lnked to the iterator
        """
        self.tower = bt
        self.current_opponent = bt.opponents.head
        self.previous_opponent = None
        
    def __iter__(self):
        """ Returns itself, as required to be iterable. """
        return self

    def __next__(self):
        """ Performs 1 battle in tower, between current opponent and user team and returns battle result, 
        user team after battle, opponent team after battle, remaining lives of opponent team
        :raises StopIteration: if user previously lose a battle, or has defeated all opponent teams (i.e. opponents list is empty)
        :complexity: best O(1) if there's no oponnent teams in tower,
                     worst O(B), where there's at least one opponent team in tower,
                     where B is complexity of battle()
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
        :complexity: best O(1) if there's no opponent teams in tower,
                     worst O(N*P) if there's at least 1 opponent team in tower,
                     where N is the number of trainers remaining in the battle tower and
                     P is the limit on the number of pokemon per team.
        """

        while self.current_opponent is not None:                            # O(N)

            opponent_poke_team = self.current_opponent.item                 # O(1) * N = O(N)
            opponent_team = self.current_opponent.item.team                 # O(1) * N = O(N)
            type_set = BSet(len(opponent_team))                             # 0(1) * N = O(N)
            contain_duplicates = False                                      # 0(1) * N = O(N)
            
            # CHECK IF TEAM CONTAINS DUPLICATE
            if opponent_poke_team.battle_mode == 0:                         # 0(1) * N = O(N)
                temp_stack = ArrayStack(len(opponent_team))                 # 0(1) * N = O(N)
                for _ in range(len(opponent_team)):                         # 0(P) * N = O(N*P)
                    pokemon = opponent_team.pop()                           # O(1) * N * P = O(N*P)
                    type_index = pokemon.get_type().get_type_index() + 1    # O(1) * N * P = O(N*P)
                    if type_index not in type_set:                          # O(1) * N * P = O(N*P)
                        type_set.add(type_index)                            # O(1) * N * P = O(N*P)
                    else:                                                   # O(1) * N * P = O(N*P)
                        contain_duplicates = True                           # O(1) * N * P = O(N*P)
                        break                                               # O(1) * N * P = O(N*P)
                for _ in range(len(temp_stack)):                            # 0(P) * N = O(N*P) 
                    opponent_team.push(temp_stack.pop())                    # O(1) * N * P = O(N*P)
            elif opponent_poke_team.battle_mode == 1:                       # 0(1) * N = O(N)
                for _ in range(len(opponent_team)):                         # 0(P) * N = O(N*P)
                    pokemon = opponent_team.serve()                         # O(1) * N * P = O(N*P)
                    type_index = pokemon.get_type().get_type_index() + 1    # O(1) * N * P = O(N*P)
                    opponent_team.append(pokemon)                           # O(1) * N * P = O(N*P)
                    if type_index not in type_set:                          # O(1) * N * P = O(N*P)
                        type_set.add(type_index)                            # O(1) * N * P = O(N*P)
                    else:                                                   # O(1) * N * P = O(N*P)
                        contain_duplicates = True                           # O(1) * N * P = O(N*P)
                        break                                               # O(1) * N * P = O(N*P)

            # HANDLE DELETION OF TEAMS WITH DUPLICATES
            if contain_duplicates:                                          # O(1) * N = O(N)
                if self.current_opponent == self.tower.opponents.head:      # O(1) * N = O(N)
                    self.tower.opponents.head = self.current_opponent.next  # O(1) * N = O(N)
                else:                                                       # O(1) * N = O(N)
                    self.previous_opponent.next = self.current_opponent.next# O(1) * N = O(N)
            
            # TEAM WITHOUT DUPLICATE BECOMES PREVIOUS OPP
            else:                                                           # O(1) * N = O(N)
                self.previous_opponent = self.current_opponent              # O(1) * N = O(N)
            
            # STANDARD INCREMENT TO POINT TO NEXT OPPONENT
            self.current_opponent = self.current_opponent.next              # O(1) * N = O(N)


class TestBattleTower(unittest.TestCase):
    def test_iter(self):
        bt = BattleTower()
        bt.set_my_team(PokeTeam.random_team("Jackson", 0, team_size=6))
        bt.generate_teams(10)
        it = iter(bt)
        print(next(it))
