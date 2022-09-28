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
    
    # LINKED QUEUE IMPLEMENTATION
    # def generate_teams(self, n: int) -> None:
    #     if type(n) is not int or n < 0:
    #         raise ValueError("n must be a positive integer")
    #     teams = LinkQueue()
    #     for i in range(n):
    #         team_name = f"Team {i}"
    #         battle_mode = RandomGen.randint(0,1)
    #         opponent = PokeTeam.random_team(team_name, battle_mode)
    #         opponent.live = RandomGen.randint(2,10)
    #         teams.append(opponent)
    #     self.opponents = teams

    # LINKED LIST IMPLEMENTATION
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
        self.start = True
        
    def __iter__(self):
        return self

    # LINKED QUEUE IMPLEMENTATION
    # def __next__(self):
    #     if self.current_opponent is not None:
    #         opponent = self.current_opponent.item

    # LINKED LIST IMPLEMENTATION
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
            # if (self.current_opponent is None) and (self.current_opponent is not self.tower.opponents.head): # iterate through whole list ???
            #     self.current_opponent = self.current_opponent.head  # go back to head and iterate again
            if self.current_opponent is not None:                       # still have opponents in the list
                # if self.current_opponent == self.tower.opponents.head:  #if current opponent is the head
                if self.start == True:

                    opponent = self.current_opponent.item
                    user = self.tower.me
                    assert type(opponent) == PokeTeam and type(user) == PokeTeam, f"{opponent}, {user}"
                    result = self.tower.battle.battle(user, opponent)
                    
                    # if opponent.live == 0:
                    #     self.delete_start_flag = 1
                    #     self.second_node = self.current_opponent.next     #the next of the head, i.e second in list

                    # self.start = False
                    

                else:   #if not start- all other cases
                # self.previous = self.current_opponent                   #current opp = head
                # self.current_opponent
                    self.previous = self.current_opponent                      # retrieve the next opponent
                    if self.previous.next == self.tower.opponents.head and self.delete_start_flag == 1: #if previous next points to head and delete flag is raise
                        self.previous.next = self.second_node   #skip the current node to the second node stored earlier
                        self.delete_start_flag = 0  #unflag delete so head does not get deleted again
                    # index = self.tower.opponents.index(opponent)                # get index of opponent
                    # self.p
                    self.current_opponent = self.previous.next          # reset current opponent to next opponent
                    opponent = self.current_opponent.item
                    user = self.tower.me                                        # get user team
                    user.regenerate_team()                                      # regen user team
                    opponent.regenerate_team()                                  # regen opponent team

                    print("###################################################")
                    print("PRE BATTLE")
                    print(f"User team: {user} ")
                    print(f"Opponent team: {opponent} || {opponent.live} <3")
                    print("###################################################")

                    result = self.tower.battle.battle(user, opponent)           # perform 1 battle

                    print("###################################################")
                    print("POST BATTLE")
                    print(f"User team: {user} ")
                    print(f"Opponent team: {opponent} || {opponent.live} <3")
                    print("###################################################")

                if result == 0 or result == 1:                              # user team win/draw
                    opponent.live -= 1                                          # opposing team lose 1 live
                    if opponent.live == 0:                                      # opposing team has no more lives
                        if self.start == True:  #if start, flag for delete when get to end node (the node that points to head)
                            self.delete_start_flag = 1
                            self.second_node = self.current_opponent.next
                            self.start = False
                        else:   #if not start, delete normal
                            self.previous.next = self.current_opponent.next     #set previous to currents next- skip over the current one- delete
                    #     self.tower.opponents.delete_at_index(index)             # remove opponent with 0 lives 
                    # else:           
                    #     self.tower.opponents[index] = opponent                            # set opponent with new live count
                else:                                                       # user team LOSE
                    self.tower.end_tower = True                                 # set end_tower to false, next iter will raise StopIteration- lose case when result = 2
                return (result, user, opponent, opponent.live)              # return (res, me, other, live)
            else:
                self.tower.end_tower = True                             # has no more opponents in list list, WIN
            
    
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