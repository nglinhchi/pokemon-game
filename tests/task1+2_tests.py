"""
Tests the methods used in pokemon_base and pokemon files
"""
__author__ = "Jane Butcher"

import unittest
from pokemon_base import *
from pokemon import *
from base_test import *
from pokemon_base import StatusEffects

class Testpokemonbase(BaseTest):
    def test_init(self):
        self.assertRaises(TypeError, lambda: PokemonBase(9, PokeType.GHOST))
        s = Squirtle()
        self.assertEqual(s.poke_type, PokeType.WATER)
        self.assertEqual(s.name, Squirtle)
        b = Bulbasaur()
        self.assertEqual(b.hp, 13)
        self.assertEqual(b.status_effect, None)

    def test_level_up(self):
        e = Eevee()
        e.level_up()
        self.assertEqual(e.get_level(), 2)
        g = Gastly()
        g.level_up()
        self.assertEqual(g.get_level(), 2)
        c = Charizard
        c.level_up()
        self.assertEqual(c.get_level(), 4)

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
        self.assertEqual(g.get_level(), 1)

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
        v = Venusaur()
        self.assertEqual(v.get_max_hp(), 21)

    def test_get_hp(self):
        g = Gastly()
        self.assertEqual(g.get_hp(), 6)
        g.level_up()
        self.assertEqual(g.get_hp(), 7)
        e = Eevee()
        e.hp = 12
        self.assertEqual(e.get_hp(), 12)

    def test_get_speed(self):
        b = Bulbasaur
        self.assertEqual(b.get_speed(), 7)
        b.level_up()
        self.assertEqual(b.get_speed(), 8)
        c = Charizard()
        self.assertEqual(c.get_speed(), 12)

    def test_get_attack_damage(self):
        s = Squirtle()
        self.assertEqual(s.get_attack_damage(), 4)
        s.level_up()
        self.assertEqual(s.get_attack_damage(), 5)
        b = Blastoise()
        self.assertEqual(b.get_attack_damage(), 9)

    def test_get_defence(self):
        c = Charmander()
        self.assertEqual(c.get_defence(), 4)
        c = Charizard()
        self.assertEqual(c.get_defence(), 4)
        e = Eevee()
        self.assertEqual(e.get_defence(), 5)

    def test_is_fainted(self):
        h = Haunter()
        self.assertEqual(h.is_fainted, False)
        h.hp = 0
        self.assertEqual(h.is_fainted, True)
        g = Gengar()
        self.assertEqual(g.is_fainted, False)

    def test_lose_hp(self):
        c = Charmander()
        c.lose_hp(4)
        self.assertEqual(c.get_hp(), 5)
        c.lose_hp(0)
        self.assertEqual(c.get_hp(), 5)
        b = Bulbasaur()
        b.lose_hp(13)
        self.assertEqual(b.get_hp(), 0)

    def test_heal(self):
        s = Squirtle()
        s.lose_hp(2)
        s.status_effect = StatusEffects.BURN
        s.heal()
        self.assertEqual(s.get_hp(), 11)
        self.assertEqual(s.get_status_effect(), None)
        v = Venusaur()
        v.lose_hp(21)
        v.heal()
        self.assertEqual(v.get_hp(), 21)

    def test_defend(self):
        b = Blastoise()
        b.defend(22)
        self.assertEqual(b.get_hp(), 10)
        b = Blastoise()
        b.defend(23)
        self.assertEqual(b.get_hp(), -2)
        b = Blastoise()
        b.defend(21)
        self.assertEqual(b.get_hp(), 11)

    def test_attack(self):
        e = Eevee()
        g = Gastly()
        e.status_effect = g.poke_type.status_effect
        self.assertEqual(e.attack(g), None)
        e.attack(g)
        self.assertEqual(e.get_hp(), 10)

        #check if pokemon lose hp after successful attack if certain status effects apply
        e = Eevee()
        b = Bulbasaur()
        e.status_effect = b.poke_type.status_effect
        e.attack(b)
        self.assertEqual(e.get_hp(), 7)


    def test_should_evolve(self):
        e = Eevee()
        self.assertEqual(e.should_evolve(), False)
        g = Gastly()
        self.assertEqual(g.should_evolve(), True)
        h = Haunter()
        h.level_up()
        self.assertEqual(h.should_evolve(), False)

    def test_can_evolve(self):
        g = Gastly()
        self.assertEqual(g.can_evolve(), True)
        h = Haunter()
        self.assertEqual(h.can_evolve(), True)
        g = Gengar()
        self.assertEqual(g.can_evolve(), False)

    def test_get_initial_evolved_version(self):
        g = Gengar()
        with self.assertRaises(ValueError):
            g.get_initial_evolved_version()
        s = Squirtle()
        self.assertEqual(s.get_initial_evolved_version(), Blastoise())
        e = Eevee()
        with self.assertRaises(ValueError):
            e.get_initial_evolved_version()

    def test_get_evolved_version(self):
        g = Gastly
        g.status_effect = StatusEffects.BURN
        g.lose_hp(2)
        g.level_up()
        self.assertEqual(isinstance(g.get_evolved_version(), Haunter), True)
        g.get_evolved_version()
        self.assertEqual(g.get_level, 2)
        self.assertEqual(g.get_status_effect, 'BURN')
        self.assertEqual(g.get_hp, 8)

    def test_update_hp(self):
        s = Squirtle()
        s.level_up()
        self.assertEqual(s.get_hp(), 13)
        s.lose_hp(5)
        s.level_up()
        self.assertEqual(s.get_hp(), 10)
        s.lose_hp(2)
        s.level_up()
        self.assertEqual(s.get_hp(), 10)