import unittest
from pokemon_base import *
from pokemon import *
from base_test import *
from unittest.mock import patch


class TestBattle(BaseTest):
    def test_simple_battle(self):
        # test simple battle where game is won after one pokemon dies
        team1 = PokeTeam("Team1", [1, 0, 0, 0, 0], 0, PokeTeam.AI.ALWAYS_ATTACK)
        team2 = PokeTeam("Team2", [0, 0, 0, 1, 0], 0, PokeTeam.AI.ALWAYS_ATTACK)
        b = Battle(verbosity=0)
        result = b.battle(team1, team2)
        self.assertEqual(result, 1)

    @patch('builtins.input', side_effect=[H, H, H, H, H])
    def test_forfeited_battle(self, mock_input):
        # test a battle where one team has healed too many times (giving the win to the other team)
        team1 = PokeTeam("Team1", [1, 2, 0, 3, 0], 0, PokeTeam.AI.USER_INPUT)
        team2 = PokeTeam("Team2", [0, 3, 1, 1, 1], 0, PokeTeam.AI.USER_INPUT)
        b = Battle(verbosity=0)
        result = b.battle(team1, team2)
        self.assertEqual(result, 2)

    def test_harder_battle(self):
        team1 = PokeTeam("Team1", [6, 0, 0, 0, 0], 0, PokeTeam.AI.SWAP_ON_SUPER_EFFECTIVE)
        team2 = PokeTeam("Team1", [0, 0, 0, 6, 0], 0, PokeTeam.AI.SWAP_ON_SUPER_EFFECTIVE)
        b = Battle(verbosity=0)
        result = b.battle(team1, team2)
        self.assertEqual(result, 1)