"""
"""
__author__ = "Scaffold by Jackson Goerner, Code by ______________"

from pokemon_base import PokemonBase, StatusEffect, PokeType


class Charizard(PokemonBase):
    def __init__(self):
        PokemonBase.__init__(self, 12, PokeType.FIRE)
        self.level = 3
    
    def hp_scaler(self) -> int:    
        scaled_hp = self.base_hp + (1 * self.level)
        return scaled_hp
    
    def can_evolve(self) -> bool:
        pass 

    def get_evolved_version(self) -> PokemonBase:
        pass

    def defend(self, damage: int) -> None:
        pass

class Charmander:
    pass


class Venusaur(PokemonBase):
    def __init__(self):
        PokemonBase.__init__(self, 20, PokeType.GRASS)
        self.level = 2
    
    def hp_scaler(self) -> int:    
        scaled_hp = self.base_hp + (self.level//2)
        return scaled_hp
    
    def can_evolve(self) -> bool:
        pass 

    def get_evolved_version(self) -> PokemonBase:
        pass

    def defend(self, damage: int) -> None:
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

