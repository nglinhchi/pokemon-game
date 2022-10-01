import unittest
from pokemon_base import *
from pokemon import *
from base_test import *
from battle import *
from tournament import *
from unittest.mock import patch

"""
Tests the methods used in tournament
"""
__author__ = "Jane Butcher"

class TestBattle(BaseTest):
    def test_set_battle_mode(self):
        """
        tests that battle mode is correctly set to the passed parameter
        """
        # tests an error is raised when something other than an integer is passed
        t = Tournament(Battle(verbosity=0))
        with self.assertRaises(ValueError):
            t.set_battle_mode("One")

        # tests an error is raised when given integer is out of range (0,1)
        t = Tournament(Battle(verbosity=0))
        with self.assertRaises(ValueError):
            t.set_battle_mode(5)

        # tests battle mode is set to the right number
        t = Tournament(Battle(verbosity=0))
        t.set_battle_mode(0)
        self.assertEqual(t.battle_mode, 0)

    def test_is_valid_tournament(self):
        """
        tests that is_valid_tournament returns the correct Boolean depending on whether the tournament string
        contains the right amount of teams vs operators and is of type string
        """
        # tests a valid tournament string returns True
        t = Tournament(Battle(verbosity=0))
        t.set_battle_mode(1)
        self.assertEqual(t.is_valid_tournament("Monfils Berrettini + Shapovalov Nadal + + Sinner Tsitsipas + Auger-Aliassime Medvedev + + +"), True)

        # tests tournament string with incorrect amount of '+' returns False
        t = Tournament(Battle(verbosity=0))
        t.set_battle_mode(1)
        self.assertEqual(t.is_valid_tournament("t1 t2 + t3 + +"), False)

        # tests input that isn't a string returns False
        t = Tournament(Battle(verbosity=0))
        t.set_battle_mode(1)
        self.assertEqual(t.is_valid_tournament(1234), False)

    def test_start_tournament(self):
        """
        tests that start_tournament yields the correct tuple (PokeTeam,PokeTeam,int) and implements the
        tournament aligning with the tournament string
        """
        # tests the tournament contains the right amount of battles
        t = Tournament(Battle(verbosity=0))
        t.set_battle_mode(0)
        t.start_tournament("Monfils Berrettini + Shapovalov Nadal + + Sinner Tsitsipas + Auger-Aliassime Medvedev + + +")
        self.assertEqual(t.battle_count, 7)

        # tests battle count for a simple tournament
        t = Tournament(Battle(verbosity=0))
        t.set_battle_mode(0)
        t.start_tournament("1 2 +")
        self.assertEqual(t.battle_count, 1)

        # tests that it raises the required error
        t = Tournament(Battle(verbosity=0))
        t.set_battle_mode(1)
        with self.assertRaises(ValueError):
            t.start_tournament("1 +")

def test_advance_tournament(self):
        """
        tests that advance_tournament returns the right tuple and implements battle sin the correct order including when to end
        """
        # tests initial setup and battle is right
        t = Tournament(Battle(verbosity=0))
        t.set_battle_mode(0)
        t.start_tournament("Monfils Berrettini + Shapovalov Nadal + + Sinner Tsitsipas + Auger-Aliassime Medvedev + + +")
        team1, team2, res = t.advance_tournament()
        self.assertEqual(team1.team_name, "Monfils")
        self.assertEqual(team2.team_name, "Berrettini")

        # tests that winning teams battle again
        t.advance_tournament()
        team1, team2, res = t.advance_tournament()
        team1_names = ["Monfils", "Berrettini"]
        team2_names = ["Shapovalov", "Nadal"]
        self.assertIn(team1.team_name, team1_names)
        self.assertEqual(team2.team_name, team2_names)

        # tests end of tournament
        t.advance_tournament()
        t.advance_tournament()
        t.advance_tournament()
        t.advance_tournament()
        self.assertEqual(t.advance_tournament, None)

    def test_linked_list_with_metas(self):
