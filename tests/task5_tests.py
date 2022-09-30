import unittest
from pokemon_base import *
from pokemon import *
from base_test import *
from tower import *
from battle import *


class TestTower(BaseTest):
    def test_set_my_team(self):
        RandomGen.set_seed(2)
        b = BattleTower(Battle(verbosity=0))
        b.set_my_team(PokeTeam.random_team("my_team", 0))
        self.assertIsInstance(b.me, PokeTeam)
        self.assertEqual(b.me.team_name, "my_team")

        b = BattleTower(Battle(verbosity=0))
        b.set_my_team(PokeTeam("Bob", [1, 3, 1, 0, 0], 1, PokeTeam.AI.ALWAYS_ATTACK))
        self.assertIsInstance(b.me, PokeTeam)
        self.assertEqual(b.me.battle_mode, 1)

    def test_generate_teams(self):
        # tests that an error is raised when anything but an int is passed
        RandomGen.set_seed(2)
        b = BattleTower(Battle(verbosity=0))
        b.set_my_team(PokeTeam.random_team("my_team", 0))
        with self.assertRaises(ValueError):
            b.generate_teams(Hi)

        # tests that all teams have the required amount of lives
        RandomGen.set_seed(2)
        b = BattleTower(Battle(verbosity=0))
        b.set_my_team(PokeTeam.random_team("my_team", 0))
        b.generate_teams(5)
        teams = iter(b)
        for team in teams:
            self.assertTrue(2 <= team.num_lives <= 10)

        # tests that the function generates the expected number of teams
        RandomGen.set_seed(2)
        b = BattleTower(Battle(verbosity=0))
        b.set_my_team(PokeTeam.random_team("my_team", 0))
        b.generate_teams(10)
        teams = iter(b)
        count = 0
        for team in teams:
            count += 1
        self.assertEqual(count, 10)

    def test_next(self):
        # tests a simple tower returns the required tuple
        RandomGen.set_seed(2)
        b = BattleTower(Battle(verbosity=0))
        b.set_my_team(PokeTeam.random_team("my_team", 2, team_size=6, criterion=Criterion.HP))
        b.generate_teams(4)
        results = iter(b)
        self.assertEqual(next(results)[0], 1)
        self.assertEqual(next(results)[3], 2)

        # tests the same simple tower as it progresses through the tower
        next(results)
        next(results)
        self.assertEqual(next(results)[0], 1)
        self.assertEqual(next(results)[3], 3)

        # tests the function always returns the required length of the tuple
        RandomGen.set_seed(2)
        b = BattleTower(Battle(verbosity=0))
        b.set_my_team(PokeTeam.random_team("my_team", 2, team_size=6, criterion=Criterion.HP))
        b.generate_teams(4)
        results = iter(b)
        for tuple in results:
            self.assertEqual(len(tuple), 4)

    def test_avoid_duplicates(self):
        RandomGen.set_seed(2)
        b = BattleTower(Battle(verbosity=0))
        b.set_my_team(PokeTeam.random_team("my_team", 2, team_size=6, criterion=Criterion.HP))
        b.generate_teams(2)
        results = iter(b)
        results.avoid_duplicates()
        for tuple in results:
            pokemon_numbers = tuple[2].team_numbers
            for num in pokemon_numbers:
                self.assertLessEqual(num, 1)

        # tests function with higher amount of teams
        RandomGen.set_seed(10)
        b = BattleTower(Battle(verbosity=0))
        b.set_my_team(PokeTeam.random_team("my_team", 1, team_size=2, criterion=Criterion.HP))
        b.generate_teams(10)
        results = iter(b)
        results.avoid_duplicates()
        for tuple in results:
            pokemon_numbers = tuple[2].team_numbers
            for num in pokemon_numbers:
                self.assertLessEqual(num, 1)

        RandomGen.set_seed(100)
        b = BattleTower(Battle(verbosity=0))
        b.set_my_team(PokeTeam.random_team("my_team", 1, team_size=2, criterion=Criterion.HP))
        b.generate_teams(10)
        results = iter(b)
        results.avoid_duplicates()
        for tuple in results:
            pokemon_numbers = tuple[2].team_numbers
            for num in pokemon_numbers:
                self.assertLessEqual(num, 1)
