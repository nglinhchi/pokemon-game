from __future__ import annotations
import unittest

from poke_team import PokeTeam
from battle import Battle
from queue_adt import CircularQueue
from random_gen import RandomGen

class BattleTower:

    def __init__(self, battle: Battle|None=None) -> None:
            self.battle = battle
    
    def set_my_team(self, team: PokeTeam) -> None:
        self.me = team
    
    def generate_teams(self, n: int) -> None:
        if type(n) is not int:
            raise ValueError("n must be an integer")
        self = CircularQueue(n)
        #User Facing#
        for _ in range(n):
            battle_mode = RandomGen.randint(0,1)
            opp_team = PokeTeam.random_team(f"Opponent {n}", battle_mode)
            opp_team.num_lives = RandomGen.randint(2,10)    #assign num_lives to opp_team instance
            self.team.append(opp_team)

    def __iter__(self):
        return BattleTowerIterator(self)


class BattleTowerIterator:
    def __init__(self,tower_instance: BattleTower):
        self.tower = tower_instance
        self.team_queue = tower_instance.team
        self.counter = 1
        self.end = len(self.team_queue)
    
    def __iter__(self, ):
        return self
    
    def __next__(self):
        if self.team_queue.is_empty():
            raise StopIteration #win
        current_team = self.team_queue.serve()  #O(1)
        self.tower.me.regenerate_team()   #regen user team
        current_team.regenerate_team() #regen opponent team
        result = self.battle(self.tower.me, current_team) #O(B)
        if result == 0 or 1:    #O(1)
            current_team.num_lives -= 1 #O(1)
        result_tuple = (result, self.me, current_team, current_team.num_lives)
        if result == 2:
            return result_tuple #lose
        if current_team.num_lives != 0: #if equal to 0, it will not put it back into team queue.    O(1)
            self.team_queue.append(current_team) #O(1)
        return result_tuple


    def avoid_duplicates(self):
        unique_team_queue = CircularQueue(len(n))
        for _ in n(num of teams):
            current_trainer = self.serve()
            current_team = current_trainer.team
            current_team_size = len(current_team)
            aset = aset(len(current_team))
            for _ in range(len(current_team)):
                if current_trainer.battle_mode == 0:
                    poketype = current_team.pop().type()
                else:
                    poketype = current_team.serve().type()
                if poketype not in aset:
                    aset.add(poketype)
                else:
                    break #end check, go check next team
            if len(aset)==len(current_team_size):
                self.team_queue.append(current_trainer)

class TestBattleTower(unittest.TestCase):
    def test_iter(self):
        bt = BattleTower()
        bt.set_my_team(PokeTeam.random_team("Jackson", 0, team_size=6))
        bt.generate_teams(10)
        it = iter(bt)
        print(next(it))
        
if __name__ == '__main__':
    unittest.main()