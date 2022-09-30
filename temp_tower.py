from __future__ import annotations
from mimetypes import init
from multiprocessing.sharedctypes import Value
from random import Random
from re import S
import unittest

from poke_team import PokeTeam
from battle import Battle
from random_gen import RandomGen
from linked_list import LinkedList

class BattleTower:

    def __init__(self, battle: Battle|None=None) -> None:
        self.battle = battle
        self.me = None
        self.opponents = LinkedList()

    def set_my_team(self, team: PokeTeam) -> None:
        self.me = team

    def generate_teams(self, n: int) -> None:
        if type(n) is not int or n < 0:
            raise Value("n must be a positive integer")
        teams = LinkedList(n)
        for i in range(n):
            team_name = f"Team {i}"
            battle_mode = RandomGen.randint(0,1)
            opponent = PokeTeam.random_team(team_name, battle_mode)
            opponent.live = RandomGen.randint(2,10)
            teams.insert(i, opponent)
        self.opponents = teams

    def __iter__(self):
        return BattleTowerIterator(self) # TODO check argument


class BattleTowerIterator:

    def __init__(self, bt: BattleTower) -> None:
        self.tower = bt
        self.current_opponent = bt.opponents.head
        
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
        if self.current_opponent is not None: # not at end of list
            opponent = self.current_opponent.item # retrieve the next opponent team
            index = self.tower.opponents.index(opponent)
            self.current_opponent = self.current_opponent.link # set current to next node
            user = self.tower.me
            user.regenerate_team() # regen user team
            opponent.regenerate_team() # regen opponent team
            result = self.tower.battle.battle(user, opponent)
            if result == 0 or result == 1:
                opponent.live -= 1
                if opponent.live == 0:
                    self.tower[index] = opponent # set opponent team in the list with new live count
            return (result, user, opponent, opponent.live)   
        else:
            raise StopIteration # end of list

    def avoid_duplicates(self):
        pass