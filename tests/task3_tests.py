from poke_team import *
from random_gen import RandomGen
from pokemon import *
from tests.base_test import BaseTest

class TestPokeTeam(BaseTest):

    # test __init__ ??

    def test_random_team(self):
        RandomGen.set_seed(123456789)
        t = random_team("Bob", 1)
        self.assertIsInstance(t, PokeTeam)      #tests random_team returns a PokeTeam
        self.assertGreaterEqual(6, sum(t.team_numbers))     #tests that team numbers does not exceed the max team size
        t = random_team("Bob", 0, 4)
        self.assertEqual(sum(t.team_numbers), 4)            #tests that the specified team size is returned in team numbers

    def test_is_empty(self):
        t = PokeTeam("team", [0, 0, 0, 0, 0], 0, PokeTeam.AI.RANDOM)
        self.assertEqual(t.is_empty(), True)
        t = PokeTeam("team", [2, 0, 0, 1, 1], 1, PokeTeam.AI.RANDOM)
        self.assertEqual(t.is_empty(), False)
        t = PokeTeam("team", [4, 0, 0, , 0], 1, PokeTeam.AI.RANDOM)
        self.assertEqual(t.is_empty(), False)

    def test_retrieve_pokemon(self):
        # test battle mode 0 retrieves first pokemon in team
        t = PokeTeam("team0", [1, 1, 0, 0, 2], 0, PokeTeam.AI.RANDOM)
        t.retrieve_pokemon()
        self.assertIsInstance(t.poke_on_field, Charmander)
        expected_classes = [Eevee, Eevee, Bulbasaur]
        pokemon = []
        while not t.is_empty():
            pokemon.append(t.retrieve_pokemon())
        for p, e in zip(pokemon, expected_classes):
            self.assertIsInstance(p, e)

        # test battle mode 1 retrieves first pokemon in team
        t = PokeTeam("team1", [1, 1, 0, 0, 2], 1, PokeTeam.AI.RANDOM)
        t.retrieve_pokemon()
        self.assertIsInstance(t.poke_on_field, Charmander)
        expected_classes = [Bulbasaur, Eevee, Eevee]
        pokemon = []
        while not t.is_empty():
            pokemon.append(t.retrieve_pokemon())
        for p, e in zip(pokemon, expected_classes):
            self.assertIsInstance(p, e)

        # test battle mode 2 retrieves first pokemon in team
        t = PokeTeam("team2", [1, 1, 0, 0, 2], 2, PokeTeam.AI.RANDOM)
        t.retrieve_pokemon()
        self.assertIsInstance(t.poke_on_field, Charmander)
        expected_classes = [Eevee, Eevee, Bulbasaur]
        pokemon = []
        while not t.is_empty():
            pokemon.append(t.retrieve_pokemon())
        for p, e in zip(pokemon, expected_classes):
            self.assertIsInstance(p, e)

    def test_return_pokemon(self):
        #test battle mode 0 returns the pokemon to the front of the team
        t = PokeTeam("team0", [1, 1, 0, 0, 2], 0, PokeTeam.AI.RANDOM)
        p = t.retrieve_pokemon()
        t.return_pokemon(p)
        p = t.retrieve_pokemon()
        t.return_pokemon(p)
        expected_classes = [Charmander, Bulbasaur, Eevee, Eevee]
        pokemon = []
        while not t.is_empty():
            pokemon.append(t.retrieve_pokemon())
        for p, e in zip(pokemon, expected_classes):
            self.assertIsInstance(p, e)

        #test battle mode 1 returns the pokemon to the back of the team
        t = PokeTeam("team1", [1, 1, 0, 0, 2], 1, PokeTeam.AI.RANDOM)
        p = t.retrieve_pokemon()
        t.return_pokemon(p)
        p = t.retrieve_pokemon()
        t.return_pokemon(p)
        expected_classes = [Eevee, Eevee, Charmander, Bulbasaur]
        pokemon = []
        while not t.is_empty():
            pokemon.append(t.retrieve_pokemon())
        for p, e in zip(pokemon, expected_classes):
            self.assertIsInstance(p, e)

        #test battle mode 2 returns the pokemon to their correct position within the teams ordering
        t = PokeTeam("team2", [1, 1, 0, 0, 2], 2, PokeTeam.AI.RANDOM, Criterion.HP)
        p = t.retrieve_pokemon()
        p.lose_hp(5)
        t.return_pokemon(p)
        p = t.retrieve_pokemon()
        t.return_pokemon(p)
        expected_classes = [Eevee, Eevee, Charmander, Bulbasaur]
        pokemon = []
        while not t.is_empty():
            pokemon.append(t.retrieve_pokemon())
        for p, e in zip(pokemon, expected_classes):
            self.assertIsInstance(p, e)


    def test_special(self):

    def test_regenerate_team(self):

    def test_choose_battle_option(self):

    def test_str(self):
