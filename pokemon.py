"""
"""
__author__ = "Scaffold by Jackson Goerner, Code by ______________"

from pokemon_base import PokemonBase, StatusEffect, PokeType


class Charizard(PokemonBase):
    def __init__(self):
        PokemonBase.__init__(self, 12, PokeType.FIRE)
        self.level = 3
    
    def get_max_hp(self) -> int:    
        hp_formula = self.base_hp + (1 * self.level)
        return hp_formula
    
    
    def can_evolve(self) -> bool:
        pass 

    def get_evolved_version(self) -> PokemonBase:
        pass

    def defend(self, damage: int) -> None:
        pass

class Charmander(PokemonBase):
    def __init__(self):
        PokemonBase.__init__(self, 8, PokeType.FIRE)

    
    def get_max_hp(self) -> int:    
        hp_formula = self.base_hp + (1 * self.level)
        return hp_formula
    
    def can_evolve(self) -> bool:
        pass 

    def get_evolved_version(self) -> PokemonBase:
        pass

    def defend(self, damage: int) -> None:
        pass


class Venusaur(PokemonBase):
    def __init__(self):
        PokemonBase.__init__(self, 20, PokeType.GRASS)
        self.level = 2
    
    def get_max_hp(self) -> int:    
        hp_formula = self.base_hp + (self.level//2)
        return hp_formula
    
    def can_evolve(self) -> bool:
        pass 

    def get_evolved_version(self) -> PokemonBase:
        pass

    def defend(self, damage: int) -> None:
        pass

class Bulbasaur(PokemonBase):
    def __init__(self):
        PokemonBase.__init__(self, 12, PokeType.GRASS)
    
    def get_max_hp(self) -> int:    
        hp_formula = self.base_hp + (1 * self.level)
        return hp_formula
    
    def can_evolve(self) -> bool:
        pass 

    def get_evolved_version(self) -> PokemonBase:
        pass

    def defend(self, damage: int) -> None:
        pass


class Blastoise(PokemonBase):
    def __init__(self):
        PokemonBase.__init__(self, 15, PokeType.WATER)
        self.level = 3
    
    def get_max_hp(self) -> int:    
        hp_formula = self.base_hp + (2 * self.level)
        return hp_formula
    
    def can_evolve(self) -> bool:
        pass 

    def get_evolved_version(self) -> PokemonBase:
        pass

    def defend(self, damage: int) -> None:
        pass

class Squirtle(PokemonBase):
    def __init__(self):
        PokemonBase.__init__(self, 9, PokeType.WATER)
    
    def get_max_hp(self) -> int:    
        hp_formula = self.base_hp + (2 * self.level)
        return hp_formula
    
    def can_evolve(self) -> bool:
        pass 

    def get_evolved_version(self) -> PokemonBase:
        pass

    def defend(self, damage: int) -> None:
        pass


class Gengar(PokemonBase):
    def __init__(self):
        PokemonBase.__init__(self, 12, PokeType.GHOST)
        self.level = 3
    
    def get_max_hp(self) -> int:    
        hp_formula = self.base_hp + (self.level//2)
        return hp_formula
    
    def can_evolve(self) -> bool:
        pass 

    def get_evolved_version(self) -> PokemonBase:
        pass

    def defend(self, damage: int) -> None:
        pass

class Haunter(PokemonBase):
    def __init__(self):
        PokemonBase.__init__(self, 9, PokeType.GHOST)
    
    def get_max_hp(self) -> int:    
        hp_formula = self.base_hp + (self.level//2)
        return hp_formula
    
    def can_evolve(self) -> bool:
        pass 

    def get_evolved_version(self) -> PokemonBase:
        pass

    def defend(self, damage: int) -> None:
        pass

class Gastly(PokemonBase):
    def __init__(self):
        PokemonBase.__init__(self, 6, PokeType.GHOST)

    def get_max_hp(self) -> int:    
        hp_formula = self.base_hp + (self.level//2)
        return hp_formula
    
    def can_evolve(self) -> bool:
        pass 

    def get_evolved_version(self) -> PokemonBase:
        pass

    def defend(self, damage: int) -> None:
        pass


class Eevee(PokemonBase):
    def __init__(self):
        PokemonBase.__init__(self, 10, PokeType.NORMAL)
    
    def get_max_hp(self) -> int:    
        hp_formula = self.base_hp
        return hp_formula
    
    def can_evolve(self) -> bool:
        pass 

    def get_evolved_version(self) -> PokemonBase:
        pass

    def defend(self, damage: int) -> None:
        pass

