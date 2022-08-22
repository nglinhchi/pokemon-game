from random_gen import RandomGen
from pokemon_base import PokemonBase, PokeType
from pokemon import Eevee, Gastly, Haunter
from tests.base_test import BaseTest

class TestPokemonBase(BaseTest):

    def test_cannot_init(self):
        """Tests that we cannot initialise PokemonBase, and that it raises the correct error."""
        self.assertRaises(TypeError, lambda: PokemonBase(30, PokeType.FIRE))

    def test_level(self):
        e = Eevee()
        self.assertEqual(e.get_level(), 1)
        e.level_up()
        self.assertEqual(e.get_level(), 2)
    
    def test_hp(self):
        e = Eevee()
        self.assertEqual(e.get_hp(), 10)
        e.lose_hp(4)
        self.assertEqual(e.get_hp(), 6)
        e.heal()
        self.assertEqual(e.get_hp(), 10)

    def test_status(self):
        RandomGen.set_seed(0)
        e1 = Eevee()
        e2 = Eevee()
        e1.attack(e2)
        # e2 now is confused.
        e2.attack(e1)
        # e2 takes damage in confusion.
        self.assertEqual(e1.get_hp(), 10)

    def test_evolution(self):
        g = Gastly()
        self.assertEqual(g.can_evolve(), True)
        self.assertEqual(g.should_evolve(), True)
        new_g = g.get_evolved_version()
        self.assertIsInstance(new_g, Haunter)
