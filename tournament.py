from __future__ import annotations
from ast import operator
from bset import BSet
from linked_stack import LinkedStack
from pokemon_base import PokeType
from queue_adt import CircularQueue
from stack_adt import ArrayStack

"""
"""
__author__ = "Scaffold by Jackson Goerner, Code by ______________"

from poke_team import PokeTeam
from battle import Battle
from linked_list import LinkedList

class Tournament:
    
    def __init__(self, battle: Battle|None=None) -> None:
        self.battle = Battle()

    def set_battle_mode(self, battle_mode: int) -> None:
        self.battle_mode = battle_mode

    def is_valid_tournament(self, tournament_str: str) -> bool:
        #Valid: 2 opp then operator, or if operator there is at least 2 on stack
        valid_operator = ["+"]
        tournament_list = tournament_str.split(" ")
        for elt in tournament_list:
            pass
    # def is_balanced_tournament(self, tournament_str: str) -> bool:
    #     # 1054 only
    #     raise NotImplementedError()

    def start_tournament(self, tournament_str: str) -> None:
        # if not self.is_valid_tournament(tournament_str):
        #     raise ValueError("Invalid tournament string")
        operator = ["+"]
        ### Run is valid tournament ###s
        self.tournament_list = tournament_str.split(" ")
        temp_stack = ArrayStack(len(self.tournament_list)) #won't be more than length of all elements
        self.reverse_tournament = ArrayStack(len(self.tournament_list))
        self.battle_count = 0
        for elt in self.tournament_list:
            if elt not in operator:
                temp_stack.push(PokeTeam.random_team(elt, self.battle_mode))
            else:
                self.battle_count += 1
                temp_stack.push(0)   #push "+" as int 0 for faster comparison
        
        while not temp_stack.is_empty():    #O(n)
            self.reverse_tournament.push(temp_stack.pop())
        self.tournament = self.tournament_gen()

        
    def tournament_gen(self):
        # operator = ["+"]
        # tournament_stack = LinkedStack()
        #initialise teams   
        tournament_stack = LinkedStack()
        """
        Alternate index list [::-1] to make link
        
        """

        for _ in range(self.battle_count):  #O(T) where T is number of tournament battles
            if type(self.reverse_tournament.peek()) is not int:
                team1 = self.reverse_tournament.pop()
                team2 = self.reverse_tournament.pop()
                self.reverse_tournament.pop()   #operator remove
                yield self.battle.battle(team1,team2)
                team1.regenerate_team()
                team2.regenerate_team()
                yield (team1, team2, self.result)
            else:   #if operator
                self.reverse_tournament.pop()   #remove operator
                team2 = tournament_stack.pop()
                team1 = tournament_stack.pop()
                yield self.battle.battle(team1,team2)
                team1.regenerate_team()
                team2.regenerate_team()
                yield (team1,team2, self.result)
            if self.result == 2:
                    tournament_stack.push(team2)
            else:   #if draw team1 win
                    tournament_stack.push(team1)
                # if type(self.reverse_tournament.peek()) is not int: #O(1)
                #     # self.reverse_tournament.pop()   #get rid of + (0)
                #     team2 = tournament_stack.pop()
                #     team1 = tournament_stack.pop()
                #     team1.regenerate_team()
                #     team2.regenerate_team()

                #     # print(team1,team2)
                #     yield self.battle.battle(team1,team2)
                #     yield (team1, team2, self.result)
                #     if self.result == 2:
                #         tournament_stack.push(team2)
                #     else:   #if draw team1 win
                #         tournament_stack.push(team1)
                # else:
                #     self.battle_count += 1
                #     tournament_stack.push(self.reverse_tournament.pop())      
                #     tournamentstack.push(self.reverse_tournament.pop())  
        

    def advance_tournament(self) -> tuple[PokeTeam, PokeTeam, int] | None:
        """
        Complexity O(B+R) where B is complexity of battle, R is complexity of regenerate team
        """
        # next(self.tournament)
        try:
            self.result = next(self.tournament)   #result of battle (int)
            print(self.result)
            return next(self.tournament)   #res tuple   (team1,team2, result(int))
        except StopIteration as e:
            return None
        # res = next(self.tournament)   #returns tuple

        # count = 0 
        #max 2 iteration  
        # 
          
        # self.advance_stack = LinkedStack()  #O(1)
        # if self.tournament_order.is_empty():    #O(1)
        #     return None
        # for _ in range(2):  #O(1)
        #     if self.tournament_order.peek() == 0:   #if next element is 0 (+), O(1)
        #         self.tournament_order.pop() #get rid of + O(1)
        #         break   #O(1) exit loop
        #     else: 
        #         self.advance_stack.push(self.tournament_order.pop())    #O(1)
        # team_2 = self.advance_stack.pop()
        # team_1 = self.advance_stack.pop()
        # team_2.regenerate_team()    #O(R)
        # team_1.regenerate_team()    #O(R)
        # result = self.battle.battle(team_1, team_2) #O(B)
        # res_tuple = (team_1, team_2, result)    #O(1)
        # if result == 1: #O(1) int comparison
        #     self.advance_stack.push(team_1) #O(1)
        # else:   #team 2 win OR draw
        #     self.advance_stack.push(team_2) #O(1)
        #     return res_tuple    #O(1)
            
    
        # if self.tournament_list[idx] not in operator:
        #     self.advance_stack.push(PokeTeam.random_team(self.tournament_list[idx], self.battle_mode))
        # else:
        #     team_2 = self.advance_stack.pop()
        #     team_1 = self.advance_stack.pop()

    def linked_list_of_games(self) -> LinkedList[tuple[PokeTeam, PokeTeam]]:
        l = LinkedList()
        while True:
            res = self.advance_tournament()
            if res is None:
                break
            l.insert(0, (res[0], res[1]))
        return l
    
    def linked_list_with_metas(self) -> LinkedList[tuple[PokeTeam, PokeTeam, list[str]]]:
        ###Access match tuple###
        branch_set = None
        new_branch_flag = 1
        #TODO: Way to flag new branch so that branch is reset if it starts from a new branch.
        #Need to store the old branch somewhere so that if it join with the new branch can merge the 2
        #LINKED LIST?
        while True:
            not_in_match = []
            res = self.advance_tournament()
            if res is None:
                break
            team1 = res[0]
            team2 = res[1]
            ###TODO: DECIDE REGEN HERE OR INSIDE ADVANCE(TOURNAMENT GEN)
            #NOTE: RETRIEVE IS NOT O(1) FOR BM2
            team1_set = BSet()
            team2_set = BSet()
            #SETS ARE CAPPED BY MAX LIM OF POKEMON ON TEAM
            for _ in range(len(team1.team)):
                poke1type = team1.retrieve_pokemon().get_type().get_type_index()
                team1_set.add(poke1type + 1)    #+1 because type index starts form 0                       
            for _ in range(len(team1.team)):
                poke2type = team2.retrieve_pokemon().get_type().get_type_index()
                team2_set.add(poke2type + 1)
            match_set = team1_set.union(team2_set)
            if branch_set is None:  #First battle
                branch_set = match_set  
            elif new_branch_flag == 1:
                #TODO do something 
                new_branch_flag = 0
            else:
                branch_set = branch_set.union(match_set)    #keep total
            not_match_meta = branch_set.difference(match_set)
            #TODO: CHECK COMPLEXITY OF THIS APPROACH: IS CALLING len IN THIS INSTANCE MAKE IT P^2 OR JUST P
            #EDIT USE SAFE BUT UGLY (NOT ENCAPSULATED) APPROACH FOR NOW
            for item in range(1, not_match_meta.elems.bit_length() + 1):
                #TODO DIFFERENT WAY ACCESS NAME?
                if item in not_match_meta:
                    not_in_match.append(list(PokeType)[item-1].name)

                


            
            



    