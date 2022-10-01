from __future__ import annotations
from bset import BSet
from pokemon_base import PokeType
from queue_adt import CircularQueue
from stack_adt import ArrayStack
from random_gen import RandomGen
from poke_team import PokeTeam
from battle import Battle
from linked_list import LinkedList

"""
Creates tournament class that implements all methods needed to create and run a tournament between PokeTeams.
"""

__author__ = "Scaffold by Jackson Goerner, Code by Joong Do Chiang"



class Tournament:
    
    def __init__(self, battle: Battle|None=None) -> None:
        """
        Initialises tournament with optional param battle which will set the battle instance for all tournament games. 
        If none provided, creates new instance
        :param battle: Battle class instance, default None
        :return: None
        :complexity:
            best case is O(1)
            worst case is O(1)
        """
        if battle is not None:
            self.battle = battle
        else:
            self.battle = Battle()

    def set_battle_mode(self, battle_mode: int) -> None:
        """
        Sets instance variable battle_mode to be used by start_tournament to set battle mode for all teams generated within current tournament
        
        :pre: battle_mode must be 0 or 1
        :param arg1: Integer between 0 and 1 that represents valid battle mode
        :return: None
        :complexity:
            best case is O(1)
            worst case is O(1)
        """
        if not isinstance(battle_mode, int) or battle_mode not in [0,1]:
            raise ValueError("Invalid battle mode") 
        self.battle_mode = battle_mode

    def is_valid_tournament(self, tournament_str: str) -> bool:
        """
        Takes string in post-fix notation representing the draw of the tournament and checks if it is valid, meaning there is one winner at
        the end and there are no unmatched opponents and number of battles corresponds to number of qualified opponents.
        
        :param tournament_str: String in postfix notation representing tournament draw
        :pre: Tournament string must be in postfix notation and competitor name must not be '+' as this is used for checking
        :post: Tournament string remains unchanged
        :return: True or False, depending on if string passes check (True means string is valid)
        :complexity:
            best case is O(1) when invalid user input
            worst case is O(n) where n is length of temp_stack
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
                temp_stack.pop()    # Get rid of one team and leave one remaining (represent winner)
        if len(temp_stack) != 1:    # If one winner is not remaining at end, return false
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
        :complexity:
            best case is TODO
            worst case is TODO
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
                tournament_queue.append(0)  #append 0 in place of '+' because cheaper comparison
        self.battle_count = battle_count
        self.tournament = self.tournament_gen(tournament_queue)
    
    def tournament_gen(self, tournament_queue: CircularQueue) -> tuple[PokeTeam,PokeTeam,int]:
        """
        Method that represents an instance of the tournament. Takes queue generated in start_tournament as arg, then runs the battles sequentially
        according to the order set in the queue. Is a generator that is iterated through by advance_tournament
        :param tournament_queue: CircularQueue representing the tournament draw, with first battle at front of queue
        :pre: self.battle_count set by start_tournament, representing num of battles in tournament, function must be called inside start_tournament,
        :post: After iterations are exhausted, tournament should be complete with winner returned.
        :return: tuple containing 3 values (team one, team two, result of match)
        :complexity:
            - 1 iteration:
                best case is O(B+R)
                worst case is O(B+R)
                where B is the cost of running a Battle between 2 teams and R is the cost of regenerating team,
            - iterate through entire tournament:
                best case is O(T*(B+R))
                worst case is O(T*(B+R))
                where T is number of battles in tournament
        """
        tournament_stack = ArrayStack(self.battle_count)    #For every battle there will only be one winner, so stack only needs to store these winners
        for _ in range(self.battle_count):
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
        Performs next battle in tournament by calling next method (iteration) through the tournament generator store in self.tournament.
        Returns result tuple received from the generator. If iterations have been exhausted in generator (i.e. no battles remaining), returns None.
        :pre: tournament generator instance must have been created through start_tournament -> tournament_gen method.
        :post: result from tournament gen is unmodified.
        :return: None or tuple(team one: PokeTeam, team two: PokeTeam, result of battle: int)
        :complexity:
            best case is O(B+R)
            worst case is O(B+R)
            where B is complexity of battle, R is complexity of regenerate team
        """
        try:
            self.result = next(self.tournament)   #result of battle (int)
            return next(self.tournament)   #res tuple   (team1,team2, result(int))
        except StopIteration as e:
            return None

    def linked_list_of_games(self) -> LinkedList[tuple[PokeTeam, PokeTeam]]:
        """
        Method that creates a linked list containing all matches performed in tournament.
        :pre: start_tournament, set_battle_mode must have been called
        :post:  tournament battles have all resulted.
        :return: linked list of tuples containing the teams who fought in each battle, in descending sequential order (last match is at head)
        :complexity:
            best case is O(T)
            worst case is O(T)
            where T is the number of matches in tournament
        """
        l = LinkedList()
        while True:
            res = self.advance_tournament()
            if res is None:
                break
            l.insert(0, (res[0], res[1]))
        return l


    def linked_list_with_metas(self) -> LinkedList[tuple[PokeTeam, PokeTeam, list[str]]]:
        """
        Returns linked list containing each battle of the tournament, the same as linked_list_of_games, but also includes a list of PokeTypes in
        the meta: types that were not present in that battle, but were present in battles fought by either party previously.
        :pre: start_tournament, set_battle_mode must have been called. 
        :post: does not modify outcome of tournament or battles.
        :return: linked list of tuples (team one: PokeTeam, team two: PokeTeam, list of PokeTypes: str)
        :complexity:
            best case is O(T*(B+P))
            worst case is O(T*(B+P))
            where T is the number of matches played in tournament, B is cost of running one battle, and P is max number of pokemon in a team.
        """
        l = self.linked_list_of_games()
        lm = LinkedList()
        temp_stack = ArrayStack(self.battle_count) 
        for match_idx in range(self.battle_count): 
            temp_stack.push(l[match_idx])
        for _ in range(self.battle_count):    
            not_in_match = []
            item = temp_stack.pop()
            team1 = item[0]
            team2 = item[1]
            team1_set = BSet()
            team2_set = BSet()
            team1.regenerate_team()
            team2.regenerate_team()
            for _ in range(len(team1.team)):
                poke1type = team1.retrieve_pokemon().get_type().get_type_index()
                team1_set.add(poke1type + 1)    # + 1 because type_index starts at 0                  
            for _ in range(len(team2.team)):
                poke2type = team2.retrieve_pokemon().get_type().get_type_index()
                team2_set.add(poke2type + 1)
            match_set = team1_set.union(team2_set)
            try:
                team1.branch_set
            except AttributeError:
                team1.branch_set = team1_set   #SET TO CURRENT MATCH SET IF DOESN'T EXIST
            try:
                team2.branch_set
            except AttributeError:
                team2.branch_set = team2_set   #SET TO CURRENT MATCH SET IF DOESN'T EXIST
            combined_branch_set = team1.branch_set.union(team2.branch_set)
            not_match_meta = combined_branch_set.difference(match_set)
            team1.branch_set = team1.branch_set.union(match_set)
            team2.branch_set = team2.branch_set.union(match_set)
            for item in range(1, not_match_meta.elems.bit_length() + 1):
                if item in not_match_meta:
                    not_in_match.append(list(PokeType)[item-1].name)
            
            output_tup = (str(team1), str(team2), not_in_match)
            lm.insert(0, output_tup)
        return lm    