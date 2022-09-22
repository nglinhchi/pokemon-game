from poke_team import Action, Criterion, PokeTeam
from random_gen import RandomGen
from pokemon import *
from pokemon_base *
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
        t = PokeTeam("team", [4, 0, 0, 0, 0], 1, PokeTeam.AI.RANDOM)
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
        t = PokeTeam("team2", [1, 1, 0, 0, 2], 2, PokeTeam.AI.RANDOM, Criterion.HP)
        t.retrieve_pokemon()
        self.assertIsInstance(t.poke_on_field, Bulbasaur)
        expected_classes = [Eevee, Eevee, Charmander]
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
        #test battle mode 0 special swaps the first and last pokemon
        t = PokeTeam("team0", [1, 1, 0, 0, 2], 0, PokeTeam.AI.RANDOM)
        t.special()
        expected_classes = [Eevee, Bulbasaur, Eevee, Charmander]
        pokemon = []
        while not t.is_empty():
            pokemon.append(t.retrieve_pokemon())
        for p, e in zip(pokemon, expected_classes):
            self.assertIsInstance(p, e)

        #test battle mode 1 special swaps the first and second halves of the team, reversing the order of the previously front half
        t = PokeTeam("team1", [1, 1, 0, 1, 2], 1, PokeTeam.AI.RANDOM)
        t.special()
        expected_classes = [Gastly, Eevee, Eevee, Bulbasaur, Charmander]
        pokemon = []
        while not t.is_empty():
            pokemon.append(t.retrieve_pokemon())
        for p, e in zip(pokemon, expected_classes):
            self.assertIsInstance(p, e)

        #test battle mode 2 special reverses the sorting order of the team
        t = PokeTeam("team2", [1, 1, 0, 0, 2], 2, PokeTeam.AI.RANDOM, Criterion.HP)
        t.special()
        expected_classes = [Charmander, Eevee, Eevee, Bulbasaur]
        pokemon = []
        while not t.is_empty():
            pokemon.append(t.retrieve_pokemon())
        for p, e in zip(pokemon, expected_classes):
            self.assertIsInstance(p, e)

    def test_regenerate_team(self):
        #test battle mode 0 regenerates team
        t = PokeTeam("team0", [1, 1, 0, 0, 2], 0, PokeTeam.AI.RANDOM)
        while not t.is_empty():             #all pokemon will eventually faint
            p = t.retrieve_pokemon()
            p.lose_hp(3)
            t.return_pokemon(p)
        t.regenerate_team()
        expected_classes = [Charmander, Bulbasaur, Eevee, Eevee]
        pokemon = []
        while not t.is_empty():
            pokemon.append(t.retrieve_pokemon())
        for p, e in zip(pokemon, expected_classes):
            self.assertIsInstance(p, e)

        #test battle mode 1 regenerates team
        t = PokeTeam("team1", [1, 1, 0, 0, 2], 1, PokeTeam.AI.RANDOM)
        while not t.is_empty():             #all pokemon will eventually faint
            p = t.retrieve_pokemon()
            p.lose_hp(3)
            t.return_pokemon(p)
        t.regenerate_team()
        expected_classes = [Charmander, Bulbasaur, Eevee, Eevee]
        pokemon = []
        while not t.is_empty():
            pokemon.append(t.retrieve_pokemon())
        for p, e in zip(pokemon, expected_classes):
            self.assertIsInstance(p, e)

        #test battle mode 2 regenerates team
        t = PokeTeam("team2", [1, 1, 0, 0, 2], 2, PokeTeam.AI.RANDOM, Criterion.HP)
        while not t.is_empty():             #all pokemon will eventually faint
            p = t.retrieve_pokemon()
            p.lose_hp(3)
            t.return_pokemon(p)
        t.regenerate_team()
        expected_classes = [Bulbasaur, Eevee, Eevee, Charmander]
        pokemon = []
        while not t.is_empty():
            pokemon.append(t.retrieve_pokemon())
        for p, e in zip(pokemon, expected_classes):
            self.assertIsInstance(p, e)

    def test_choose_battle_option(self):
        #test ALWAYS_ATTACK returns ATTACK
        t = PokeTeam("Bob", [1, 1, 0, 0, 2], 0, PokeTeam.AI.ALWAYS_ATTACK)
        p = t.retrieve_pokemon()
        b = Bulbasaur()
        self.assertEqual(t.choose_battle_option(p, b), Action.ATTACK)

        #test SWAP_ON_SUPER_EFFECTIVE when type multiplier < 1.5
        t = PokeTeam("Bob", [1, 1, 0, 0, 2], 1, PokeTeam.AI.SWAP_ON_SUPER_EFFECTIVE)
        p = t.retrieve_pokemon()
        b = Bulbasaur()
        self.assertEqual(t.choose_battle_option(p, b), Action.ATTACK)

        #test SWAP_ON_SUPER_EFFECTIVE when type multiplier > 1.5
        t = PokeTeam("Bob", [1, 1, 0, 0, 2], 1, PokeTeam.AI.SWAP_ON_SUPER_EFFECTIVE, Criterion.HP)
        p = t.retrieve_pokemon()
        c = Charmander
        self.assertEqual(t.choose_battle_option(p, c), Action.SWAP)

    def test_str(self):
        #test battle mode 0 prints the correct string
        t = PokeTeam("Bob", [1, 1, 0, 0, 2], 0, PokeTeam.AI.RANDOM)
        self.assertEqual(str(t), "Bob (0): [LV. 1 Charmander: 9 HP, LV. 1 Bulbasaur: 13 HP, LV. 1 Eevee: 10 HP, LV. 1 Eevee: 10 HP]")

        #test battle mode 1 prints the correct string
        t = PokeTeam("Bob", [1, 1, 0, 0, 2], 1, PokeTeam.AI.RANDOM)
        self.assertEqual(str(t), "Bob (1): [LV. 1 Charmander: 9 HP, LV. 1 Bulbasaur: 13 HP, LV. 1 Eevee: 10 HP, LV. 1 Eevee: 10 HP]")

        #test battle mode 2 prints the correct string
        t = PokeTeam("Bob", [1, 1, 0, 0, 2], 1, PokeTeam.AI.RANDOM, Criterion.HP)
        self.assertEqual(str(t), "Dawn (2): [LV. 1 Bulbasaur: 13 HP, LV. 1 Eevee: 10 HP, LV. 1 Eevee: 10 HP, LV. 1 Charmander: 9 HP]")

