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
    def test_is_valid_tournament(self):
        t = Tournament(Battle(verbosity=0))
        t.set_battle_mode(1)
        self.assertEqual(t.is_valid_tournament("Monfils Berrettini + Shapovalov Nadal + + Sinner Tsitsipas + Auger-Aliassime Medvedev + + +"), True)

        t = Tournament(Battle(verbosity=0))
        t.set_battle_mode(1)
        self.assertEqual(t.is_valid_tournament("t1 t2 + t3 + +"), False)

        t = Tournament(Battle(verbosity=0))
        t.set_battle_mode(1)
        self.assertEqual(t.is_valid_tournament(1234), False)