from __future__ import annotations
from unicodedata import name
from bset import BSet

from poke_team import PokeTeam, Criterion
from battle import Battle

from linked_list import LinkedList
from linked_queue import LinkQueue
from random_gen import RandomGen

import unittest

from stack_adt import ArrayStack

class BattleTower:

    def __init__(self, battle: Battle|None=None) -> None:
        if battle is not None:
            self.battle = battle
        else:
            self.battle = Battle()
        self.me = None
        self.opponents = LinkedList()
        self.end_tower = False
    
    def set_my_team(self, team: PokeTeam) -> None:
        self.me = team

    def generate_teams(self, n: int) -> None:
        if type(n) is not int or n < 0:
            raise ValueError("n must be a positive integer")
        teams = LinkedList(n)
        for i in range(n):
            team_name = f"Team {i}"
            battle_mode = RandomGen.randint(0,1)
            opponent = PokeTeam.random_team(team_name, battle_mode)
            opponent.live = RandomGen.randint(2,10)
            print(f"{opponent} >>> {opponent.live} <3")
            teams.insert(i, opponent) 
        self.opponents = teams

    def __iter__(self):
        return BattleTowerIterator(self)

class BattleTowerIterator:

    def __init__(self, bt: BattleTower) -> None:
        self.tower = bt
        self.current_opponent = bt.opponents.head
        self.previous_opponent = None
        
    def __iter__(self):
        return self

    def __next__(self):
        """
        - perform 1 battle in tower
        - return a tuple contain 4 values
        * result of battle 0/1/2 
        * player team after battle (me)
        * tower team after battle (opponents[i])
        * remaning lives of tower team (opponents[i].live)
        """
        if self.tower.end_tower:
            raise StopIteration
        else:
            
            # IF REACH END OF LIST + STILL CONTAINS OPPONENTS --> GO BACK TO HEAD TO ITERATE
            if (self.current_opponent is None) and (self.current_opponent is not self.tower.opponents.head):
                self.current_opponent = self.current_opponent.head  # assign CURRENT to HEAD again
            
            # IF LIST STILL CONTAINTS OPPONENT --> BATTLE
            if self.current_opponent is not None:                      
                opponent = self.current_opponent.item                       # retrieve the current opponent
                user = self.tower.me                                        # get user team
                user.regenerate_team()                                      # regen user team
                opponent.regenerate_team()                                  # regen opponent team
                
                print("###################################################")
                print("PRE BATTLE")
                print(f"User team: {user} ")
                print(f"Opponent team: {opponent} || {opponent.live} <3")
                print("###################################################")

                # TODO assert 
                result = self.tower.battle.battle(user, opponent)           # perform 1 battle

                print("###################################################")
                print("POST BATTLE")
                print(f"User team: {user} ")
                print(f"Opponent team: {opponent} || {opponent.live} <3")
                print("###################################################")

                if result == 0 or result == 1:                                              # user team WIN/DRAW battle
                    opponent.live -= 1                                      
                    if opponent.live == 0 and opponent == self.tower.opponents.head.item:       # opponent has 0 lives, opponent is head -> change head
                        self.tower.opponents.head = self.current_opponent.next
                    elif opponent.live == 0:                                                    # opponent has 0 lives, opponent is an intermediate node --> prev opponent point to current's next opponent (remove self from linked list)
                            self.previous_opponent.next = self.current_opponent.next
                    elif opponent.live > 0:                                                     # opponent still have lives --> become the prev surviving opponent
                        self.previous_opponent = self.current_opponent
                    self.current_opponent = self.current_opponent.next                          # standard assignment to point to next opponent

                elif result == 2:                                                           # user team LOSE battle
                    self.tower.end_tower = True                                                 # set end_tower to false, next iter will raise StopIteration

                return (result, user, opponent, opponent.live)                              # return (res, me, opponent, live)
            
            # IF LIST DOESN'T CONTAINS ANY OPPONENTS --> WIN
            else:
                self.tower.end_tower = True     
        
        
    
    def avoid_duplicates(self):
        # if current_team.item.get_battle_mode() = 0:
        dup_start = True   #mark current opponent as start of duplicate
        idx = 0
        end_idx = len(self.tower.opponents)
        while True:
            #Maybe have an index counter? 
            idx += 1
            if dup_start == True:
                current= self.current_opponent
                current_opp = self.current_opponent.item
                start_next = current.next
            else:   #not the start
                previous = self.current_opponent
                current = previous.next
                current_opp = current.item
        
            for _ in range(len(current_opp.team)): #number of pokemon O(p)
                temp_stack = ArrayStack(len(current_opp.team))
                type_set = BSet(len(current_opp.team))
                poke = current_opp.retrieve_pokemon()    #O(1) for stack pop
                type_index = poke.get_type().get_type_index() + 1 #O(1) -> O(1) return int type_index + 1 because bit vector must be pos
                if type_index not in type_set:  #O(1) return, bitwise and arithmetic O(1)
                    type_set.add(type_index)
                else:   #is duplicate
                    if dup_start == True:  #O(1)
                        dup_start_delete = 1
                        dup_start == False
                        break
                    else:
                        previous.next = current.next    #set previous node next to current next
                        self.current_opponent = current.next
                        if dup_start_delete == 1 and idx == end_idx:   #O(1) comparing 2 integers, means reached end of list
                            self.current_opponent.next = start_next 
                            # dup_start_delete = 0- No need as will break at end of list- check is done
                            return
                        break
            
        # next return (res, me, other, lives)
        # for (res, me, other, lives) in self.tower:
        #     for num in other.team_numbers:
        #         if num > 1:
        #             index = self.tower.opponents.index(other)
        #             self.tower.opponents.delete_at_index(index)
        #             next
        
        # lst = []

        # for (res, me, other, lives) in self.tower:
        #     for num in other.team_numbers:
        #         if num > 1:
        #             lst.append(other.team_name)
        #             next
        # print(lst)
            

        # while self.current_opponent is not None:
        #     team = current_opponent.item     # retrieve item in current node
        #     current_opponent = current_opponent.next  # reset to next node
        #     for num in team.team_numbers: # iterate through team_numbers
        #         if num > 1:
        #             index = self.tower.opponents.index(team)
        #             self.tower.opponents.delete_at_index(index)
                    
        # raise StopIteration


class TestBattleTower(unittest.TestCase):
    def test_iter(self):
        bt = BattleTower()
        bt.set_my_team(PokeTeam.random_team("Jackson", 0, team_size=6))
        bt.generate_teams(10)
        it = iter(bt)
        print(next(it))
        
if __name__ == '__main__':
    
    
    # unittest.main()
    RandomGen.set_seed(51234)
    bt = BattleTower(Battle(verbosity=0))
    bt.set_my_team(PokeTeam.random_team("N", 2, team_size=6, criterion=Criterion.HP))
    bt.generate_teams(4)
    # Teams have 7, 10, 10, 3 lives.
    RandomGen.set_seed(1029873918273)
    it = iter(bt)
    print(next(it)) # 1, 6
    print(next(it)) # 1, 9
    print(next(it)) # 1, 9
    print(next(it)) # 1, 2
    print(next(it)) # 1, 5
    print(next(it)) # 2, 9
    
    # -------------------------------------------------------------------------------

    # RandomGen.set_seed(29183712400123)
    # bt = BattleTower(Battle(verbosity=0))
    # bt.set_my_team(PokeTeam.random_team("Jackson", 0, team_size=6))
    # bt.generate_teams(10)

    # # Team numbers before:
    # # [0, 4, 1, 0, 0], 6
    # # [1, 0, 2, 0, 0], 5
    # # [1, 1, 0, 1, 0], 8
    # # [1, 2, 1, 1, 0], 10
    # # [0, 0, 2, 1, 1], 8
    # # [1, 1, 3, 0, 0], 4
    # # [0, 2, 0, 1, 0], 5
    # # [1, 0, 0, 4, 0], 3
    # # [1, 1, 1, 0, 2], 7
    # # [0, 1, 1, 1, 0], 9
    # it = iter(bt)
    # it.avoid_duplicates()
    # # Team numbers after:
    # # [1, 1, 0, 1, 0], 8
    # # [0, 1, 1, 1, 0], 9