"""
"""
__author__ = "Scaffold by Jackson Goerner, Code by ______________"

from pokemon_base import PokemonBase, StatusEffect, PokeType


class Charizard(PokemonBase):
    def __init__(self):
        self.level = 3
        PokemonBase.__init__(self, 12, PokeType.FIRE)
        
        
    
    def hp_scaler(self) -> int:
        scaled_hp = self.base_hp + 1 * self.level
        return scaled_hp

class Charmander:
    


class Venusaur:
    pass

class Bulbasaur:
    pass


class Blastoise:
    pass

class Squirtle:
    pass


class Gengar:
    pass

class Haunter:
    pass

class Gastly:
    pass


class Eevee:
    pass
