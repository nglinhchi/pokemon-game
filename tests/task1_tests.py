import unittest
from pokemon_base import *
from pokemon import *
from base_test import *

class Testpokemonbase(BaseTest):
    def test_get_name(self):
        e = Eevee()
        self.assertEqual(e.get_name(), 'Eevee')
        v = Venusaur()
        self.assertEqual(v.get_name(), 'Venusaur')
        s = Squirtle()
        self.assertEqual(s.get_name(), 'Squirtle')

    def test_get_type(self):
        b = Blastoise()
        self.assertEqual(b.get_type(), 'WATER')
        b = Bulbasaur()
        self.assertEqual(b.get_type(), 'GRASS')
        g = Gengar()
        self.assertEqual(g.get_type(), 'GHOST')

    def test_get_level(self):
        g = Gengar()
        self.assertEqual(g.get_level(), 3)
        h = Haunter()
        self.assertEqual(h.get_level(), 1)
        g = Gastly()
        self.assertEqual(g.get_level(), 1)          # should gastly be level 1?

    def test_get_status_effect(self):
        c = Charizard()
        self.assertEqual(c.get_status_effect(), None)
        b = Bulbasaur()
        c.status_effect = b.poke_type.status_effect
        self.assertEqual(c.get_status_effect(), 'POISON')
        b.status_effect = c.poke_type.status_effect
        self.assertEqual(b.get_status_effect(), 'BURN')

    def test_get_max_hp(self):
        c = Charmander()
        self.assertEqual(c.get_max_hp(), 9)
        s = Squirtle()
        self.assertEqual(s.get_max_hp(), 11)
        v = Venusaur
        self.assertEqual(v.get_max_hp(), 21)

    def test_get_hp(self):
        g = Gastly()
        self.assertEqual(g.get_hp(), 6)

    def test_get_speed(self):
        b = Bulbasaur
        self.assertEqual(b.get_speed(), 7)
        b.level_up()
        self.assertEqual(b.get_speed(), 8)
        # TODO: test get_speed when they have paralysis

    def test_get_attack_damage(self):

    def test_get_defence(self):

    def test_is_fainted(self):

    def test_lose_hp(self):
        c = Charmander()
        c.lose_hp(4)
        self.assertEqual(c.get_hp(), 5)
        c.lose_hp(2)
        self.assertEqual(c.get_hp(), 3)
        b = Bulbasaur()
        b.lose_hp(13)
        self.assertEqual(b.get_hp(), 0)

    def test_heal(self):
        s = Squirtle()
        s.lose_hp(2)
        s.status_effect = 'BURN'
        s.heal()
        self.assertEqual(s.get_hp(), 11)
        self.assertEqual(s.get_status_effect(), None)

    def test_defend(self):

    def test_attack(self):

    def test_should_evolve(self):

    def test_can_evolve(self):
        g = Gastly()
        self.assertEqual(g.can_evolve(), True)
        h = Haunter()
        self.assertEqual(h.can_evolve(), True)
        g = Gengar()
        self.assertEqual(g.can_evolve(), False)

    def test_get_initial_evolved_version(self):

    def test_update_hp(self):


    def test_get_evolved_version(self):

    def test_level_up(self):
        e = Eevee()
        e.lose_hp(3)
        e.level_up()
        self.assertEqual(e.get_level(), 2)
        self.assertEqual(e.get_hp(), 7)
        g = Gastly()
        g.lose_hp(5)
        g.level_up()
        self.assertEqual(g.get_level(), 2)





