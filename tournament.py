from __future__ import annotations
from ast import operator
from multiprocessing.dummy import Array
from multiprocessing.sharedctypes import Value
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
        #End game: one remaining
        if type(tournament_str) is not str:
            return False
        valid_operator = ["+"]
        tournament_list = tournament_str.split(" ")
        temp_stack = ArrayStack(len(tournament_list))
        bracket_count = 0
        #CHECK FOR FIRST INDEX = +? BUT + COULD BE NAME
        if len(tournament_list) <= 2:
            return False
        for elt in tournament_list:   

            if elt not in valid_operator:
                temp_stack.push(elt)
            if elt in valid_operator and len(temp_stack) < 2:
                return False
            elif elt in valid_operator:
                #Get rid of one team and leave one remaining (represent winner)
                temp_stack.pop()
        #If one winner is not remaining at end, return false
        if len(temp_stack) != 1:
            return False
        
        return True   

            
            

    # def is_balanced_tournament(self, tournament_str: str) -> bool:
    #     # 1054 only
    #     raise NotImplementedError()

    def start_tournament(self, tournament_str: str) -> None:
        ### VALID CHECK ###
        if not self.is_valid_tournament(tournament_str):
            raise ValueError("Invalid tournament string")

        # ### IMPLEMENT 1 ###
        # operator = ["+"]

        # self.tournament_list = tournament_str.split(" ")
        # temp_stack = ArrayStack(len(self.tournament_list)) #won't be more than length of all elements
        # self.reverse_tournament = ArrayStack(len(self.tournament_list))
        # self.battle_count = 0
        # for elt in self.tournament_list:
        #     if elt not in operator:
        #         temp_stack.push(PokeTeam.random_team(elt, self.battle_mode))
        #     else:
        #         self.battle_count += 1
        #         temp_stack.push(0)   #push "+" as int 0 for faster comparison
        
        # while not temp_stack.is_empty():    #O(n)
        #     self.reverse_tournament.push(temp_stack.pop())
        # self.tournament = self.tournament_gen()
        # ###### END IMPLEMENT 1 ###############

        # ####IMPLEMENT 2 ####
        # operator = ["+"]
        # tournament_list = tournament_str.split(" ")
        # self.battle_count = 0   
        # self.reverse_tournament = ArrayStack(len(tournament_list))
        # #READ ELEMENTS BACKWARDS SO START OF TOURNAMENT IS AT TOP OF STACK
        # for elt in tournament_list[::-1]:
        #     if elt not in operator:
        #        self.reverse_tournament.push(PokeTeam.random_team(elt, self.battle_mode))
        #     else:
        #         self.battle_count += 1
        #         self.reverse_tournament.push(0)
        # self.tournament = self.tournament_gen()

        # ###IMPLEMENT 3###
        operator = ["+"]
        battle_count = 0
        tournament_list = tournament_str.split(" ")
        tournament_queue = CircularQueue(len(tournament_list))
        
        for elt in tournament_list:
            if elt not in operator:
               tournament_queue.append(PokeTeam.random_team(elt, self.battle_mode))
            else:
                battle_count += 1
                tournament_queue.append(0)
        # self.tournament_queue = tournament_queue
        self.tournament = self.tournament_gen(tournament_queue, battle_count)
    
    def tournament_gen(self, tournament_queue: CircularQueue, battle_count: int):
        # operator = ["+"]
        # tournament_stack = LinkedStack()
        #initialise teams   
        tournament_stack = ArrayStack(battle_count)    #For every battle there will only be one winner, so stack only needs to store these winners

        ### FOR IMPLEMENT 1 ####
        # for _ in range(self.battle_count):  #O(T) where T is number of tournament battles
        #     if type(self.reverse_tournament.peek()) is not int:
        #         team1 = self.reverse_tournament.pop()
        #         team2 = self.reverse_tournament.pop()
        #         self.reverse_tournament.pop()   #operator remove
        #         yield self.battle.battle(team1,team2)
        #         team1.regenerate_team()
        #         team2.regenerate_team()
        #         yield (team1, team2, self.result)
        #     else:   #if operator
        #         self.reverse_tournament.pop()   #remove operator
        #         team2 = tournament_stack.pop()
        #         team1 = tournament_stack.pop()
        #         yield self.battle.battle(team1,team2)
        #         team1.regenerate_team()
        #         team2.regenerate_team()
        #         yield (team1,team2, self.result)
        #     if self.result == 2:
        #             tournament_stack.push(team2)
        #     else:   #if draw team1 win
        #             tournament_stack.push(team1)
        #### END IMPLEMENT 1 ####

        for _ in range(battle_count):
            elt = tournament_queue.serve()
            if type(elt) is not int: #O(1) , if it is a competitor
            #     #  DONT NEED BECAUSE ALREADY SERVE FOR CHECKself.reverse_tournament.pop()   #get rid of + (0)
                team1 = elt
                team2 = tournament_queue.serve()
                tournament_queue.serve()   #remove operator
                yield self.battle.battle(team1,team2)
                team1.regenerate_team()
                team2.regenerate_team()
                yield (team1, team2, self.result)
            else:   #if operator
                team2 = tournament_stack.pop()
                team1= tournament_stack.pop()
                yield self.battle.battle(team1,team2)
                team1.regenerate_team()
                team2.regenerate_team()
                yield (team1,team2,self.result)
            if self.result == 2:
                tournament_stack.push(team2)
            else:   #if draw team1 win
                tournament_stack.push(team1)

    def advance_tournament(self) -> tuple[PokeTeam, PokeTeam, int] | None:
        """
        Complexity O(B+R) where B is complexity of battle, R is complexity of regenerate team
        """
        # next(self.tournament)
        try:
            self.result = next(self.tournament)   #result of battle (int)
            # print(self.result)
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
        # branch_set = None
        # new_branch_flag = 1
        #TODO: Way to flag new branch so that branch is reset if it starts from a new branch.
        #Need to store the old branch somewhere so that if it join with the new branch can merge the 2
        #LINKED LIST?
        lm = LinkedList()

        while True:
            not_in_match = []
            res = self.advance_tournament()
            if res is None:
                break
            team1 = res[0]
            team2 = res[1]
            result = res[2]
            if result == 0:
                winning_team = res[0]
            else:
                winning_team = res[result-1]    #-1 to match index
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
            #WHEN TEAM1 FIRST MATCH
            try:
                team1.branch_set
            except AttributeError:
                team1.branch_set = match_set   #SET TO CURRENT MATCH SET IF DOESN'T EXIST
            #WHEN TEAM2 FIRST MATCH
            try:
                team2.branch_set
            except AttributeError:
                team2.branch_set = match_set   #SET TO CURRENT MATCH SET IF DOESN'T EXIST
            
            #WHEN FIRST MATCH FOR ONE OR BOTH OF TEAMS
            # print("team1,team2,winningteam" , team1,team2, winning_team)
            winning_team.branch_set = team1.branch_set.union(team2.branch_set)  #WINNING TEAM BRANCH SET CONTAINS BOTH LOSING TEAM AND ITSELF BRANCHES I.E ABSORBS BRANCHES

            not_match_meta = winning_team.branch_set.difference(match_set)

            




            # if branch_set is None:  #First battle
            #     branch_set = match_set  
            # elif new_branch_flag == 1:
            #     #TODO do something 
            #     new_branch_flag = 0
            # else:
            #     branch_set = branch_set.union(match_set)    #keep total
            
            # #TODO: CHECK COMPLEXITY OF THIS APPROACH: IS CALLING len IN THIS INSTANCE MAKE IT P^2 OR JUST P
            # #EDIT USE SAFE BUT UGLY (NOT ENCAPSULATED) APPROACH FOR NOW
            for item in range(1, not_match_meta.elems.bit_length() + 1):
                #TODO DIFFERENT WAY ACCESS NAME
                # print("item in set", item)
                if item in not_match_meta:
                    not_in_match.append(list(PokeType)[item-1].name)
            
            output_tup = (team1, team2, not_in_match)
            # print("output tup", output_tup)
            # lm.insert(output_tup)
        return lm
                


            
            



    