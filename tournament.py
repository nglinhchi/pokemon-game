from __future__ import annotations
from ast import operator
from multiprocessing.dummy import Array
from multiprocessing.sharedctypes import Value
from nis import match
from bset import BSet
from linked_stack import LinkedStack
from pokemon_base import PokeType
from queue_adt import CircularQueue
from stack_adt import ArrayStack
from random_gen import RandomGen
"""
Creates tournament class that implements all methods needed to create and run a tournament between PokeTeams.

"""
__author__ = "Scaffold by Jackson Goerner, Code by Joong Do Chiang"

from poke_team import PokeTeam
from battle import Battle
from linked_list import LinkedList

class Tournament:
    
    def __init__(self, battle: Battle|None=None) -> None:
        """
        Initialises tournament with optional param battle which will set the battle instance for all tournament games. If none provided, creates
        new instance

        :param battle: Battle class instance, default None
        :return: None
        """
        if battle is not None:
            self.battle = battle
        else:
            self.battle = Battle()

    def set_battle_mode(self, battle_mode: int) -> None:
        """
        Sets instance variable battle_mode to be used by start_tournament to set battle mode for all teams generated within current
        tournament
        :param battle_mode: Integer between 0 and 1 that represents valid battle mode
        :return: None
        """
        self.battle_mode = battle_mode

    def is_valid_tournament(self, tournament_str: str) -> bool:
        """
        Takes string in post-fix notation representing the draw of the tournament and checks if it is valid, meaning there is one winner at
        the end and there are no unmatched opponents and number of battles corresponds to number of qualified opponents.
        
        :param tournament_str: String in postfix notation representing tournament draw
        :pre: Tournament string must be in postfix notation and competitor name must not be '+' as this is used for checking
        :post: Tournament string remains unchanged
        :return: True or False, depending on if string passes check (True means string is valid)
        """
      
        if type(tournament_str) is not str:
            return False
        valid_operator = ["+"]
        tournament_list = tournament_str.split(" ")
        temp_stack = ArrayStack(len(tournament_list))
        if len(tournament_list) <= 2:
            return False
        for elt in tournament_list:   

            if elt not in valid_operator:
                temp_stack.push(elt)
            if elt in valid_operator and len(temp_stack) < 2:
                return False
            elif elt in valid_operator:
                temp_stack.pop()    #Get rid of one team and leave one remaining (represent winner)
        if len(temp_stack) != 1:    #If one winner is not remaining at end, return false
            return False
        
        return True  

    def start_tournament(self, tournament_str: str) -> None:
        """
        Initiates tournament according to tournament_str, which is validated through is_valid_tournament. Generates random teams that represent
        tournament competitors. Places these teams in a queue according to order of the tournament and creates an instance of tournament_gen
        that represents the tournament instance itself.

        :param tournament_str: string representing tournament
        :pre: instance variable battle_mode must be set
        :post: instance variable tournament representing tournament is created by passing args into and calling tournament_gen method, that 
        can be iterated through
        :return: None
        :raises ValueError: if tournament_str param is not a valid form of tournament.
        """
        if not self.is_valid_tournament(tournament_str):
            raise ValueError("Invalid tournament string")

        operator = ["+"]
        battle_count = 0    #counts number of battles in tournament
        tournament_list = tournament_str.split(" ")
        tournament_queue = CircularQueue(len(tournament_list))
        
        for elt in tournament_list:
            if elt not in operator:
               tournament_queue.append(PokeTeam.random_team(elt, self.battle_mode))
            else:
                battle_count += 1
                tournament_queue.append(0)

        self.tournament = self.tournament_gen(tournament_queue, battle_count)
    
    def tournament_gen(self, tournament_queue: CircularQueue, battle_count: int):
        """
        
        """
        tournament_stack = ArrayStack(battle_count)    #For every battle there will only be one winner, so stack only needs to store these winners
        for _ in range(battle_count):
            elt = tournament_queue.serve()
            if type(elt) is not int: 
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
            # result = res[2]
            # print("res from advance", res)
            print("result",self.result)
            # team1.regenerate_team()
            # team2.regenerate_team()
            # if result == 0:
            #     winning_team = res[0]
            # else:
            #     winning_team = res[result-1]    #-1 to match index
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
            # print(match_set)
            print(team1, team1_set, team2, team2_set)
            #WHEN TEAM1 FIRST MATCH
            try:
                team1.branch_set
            except AttributeError:
                team1.branch_set = team1_set   #SET TO CURRENT MATCH SET IF DOESN'T EXIST
            #WHEN TEAM2 FIRST MATCH
            try:
                team2.branch_set
            except AttributeError:
                team2.branch_set = team2_set   #SET TO CURRENT MATCH SET IF DOESN'T EXIST
            print(team1.branch_set, team2.branch_set)
            #WHEN FIRST MATCH FOR ONE OR BOTH OF TEAMS
            # print("team1,team2,winningteam" , team1,team2, winning_team)
            # winning_team.branch_set = winning_team.branch_set.union(match_set)  #WINNING TEAM BRANCH SET CONTAINS BOTH LOSING TEAM AND ITSELF BRANCHES I.E ABSORBS BRANCHES
            # print("match, winning", match_set, winning_team.branch_set)
            # not_match_meta = winning_team.branch_set.difference(match_set)

            




            # if branch_set is None:  #First battle
            #     branch_set = match_set  
            # elif new_branch_flag == 1:
            #     #TODO do something 
            #     new_branch_flag = 0
            # else:
            #     branch_set = branch_set.union(match_set)    #keep total
            
            # #TODO: CHECK COMPLEXITY OF THIS APPROACH: IS CALLING len IN THIS INSTANCE MAKE IT P^2 OR JUST P
            # # #EDIT USE SAFE BUT UGLY (NOT ENCAPSULATED) APPROACH FOR NOW
            # for item in range(1, not_match_meta.elems.bit_length() + 1):
            #     #TODO DIFFERENT WAY ACCESS NAME
            #     # print("item in set", item)
            #     if item in not_match_meta:
            #         not_in_match.append(list(PokeType)[item-1].name)
            
            output_tup = (str(team1), str(team2), not_in_match)
            # print("output tup", output_tup)
            # print("lm",lm)
            lm.insert(0, output_tup)
        return lm
                


            
            



    