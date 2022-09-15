"""
"""
__author__ = "Scaffold by Jackson Goerner, Code by Joong Do Chiang, Chloe Nguyen"

from multiprocessing.sharedctypes import Value
from pokemon_base import PokemonBase, StatusEffect, PokeType


# *******************************************


# CHARMANDER >> CHARIZARD
class Charizard(PokemonBase): 
    def __init__(self):
        PokemonBase.__init__(self, -1, PokeType.FIRE)
        self.level = 3 # base level
    
    def get_max_hp(self) -> int:
        """
        Abstract method containing HP scaling formula for individual pokemon. Calculates
        this max HP using base_hp and returns.
        :pre: base_hp must be defined
        """
        return 12 + 1 * self.level

    def get_attack_damage(self) -> int:
        return 10 + 2 * self.level

    def get_speed(self) -> int:
        return 9 + 1 * self.level

    def get_defence(self) -> int:
        return 4
    
    def can_evolve(self) -> bool:
        return False

    def get_initial_evolved_version(self) -> PokemonBase:
        raise ValueError(f"{self.name} does not have evolution")

    def defend(self, damage: int) -> None:
        if damage > self.get_defence():
            self.lose_hp(2*damage)
        else:
            self.lose_hp(damage)


# CHARMANDER
class Charmander(PokemonBase):
    
    def __init__(self):
        PokemonBase.__init__(self, 9, PokeType.FIRE)
    
    def get_max_hp(self) -> int:
        return 8 + 1 * self.level

    def get_attack_damage(self) -> int:
        return 6 + 1 * self.level

    def get_speed(self) -> int:
        return 7 + 1 * self.level

    def get_defence(self) -> int:
        return 4
    
    def can_evolve(self) -> bool:
        return True

    def get_initial_evolved_version(self) -> PokemonBase:
        return Charizard()

    def defend(self, damage: int) -> None:
        if damage > self.get_defence():
            self.lose_hp(damage)
        else:
            self.lose_hp(damage//2)


# *******************************************


# BULBASAUR >> VENUSAUR
class Venusaur(PokemonBase):

    def __init__(self):
        PokemonBase.__init__(self, -1, PokeType.GRASS)
        self.level = 2 # base level
    
    def get_max_hp(self) -> int:
        return 20 + self.level//2

    def get_attack_damage(self) -> int:
        return 5

    def get_speed(self) -> int:
        return 3 + self.level//2

    def get_defence(self) -> int:
        return 10
    
    def can_evolve(self) -> bool:
        return False
    
    def get_initial_evolved_version(self) -> PokemonBase:
        raise ValueError(f"{self.name} does not have evolution")

    def defend(self, damage: int) -> None:
        if damage > (self.get_defence() + 5):
            self.lose_hp(damage)
        else:
            self.lose_hp(damage//2)


# BULBASAUR
class Bulbasaur(PokemonBase):

    def __init__(self):
        PokemonBase.__init__(self, 13, PokeType.GRASS)
    
    def get_max_hp(self) -> int:
        return 12 + 1 * self.level

    def get_attack_damage(self) -> int:
        return 5

    def get_speed(self) -> int:
        return 7 + self.level//2

    def get_defence(self) -> int:
        return 5
    
    def can_evolve(self) -> bool:
        return True
    
    def get_initial_evolved_version(self) -> PokemonBase:
        return Venusaur()

    def defend(self, damage: int) -> None:
        if damage > (self.get_defence() + 5):
            self.lose_hp(damage)
        else:
            self.lose_hp(damage//2)    


# *******************************************


# SQUIRTLE >> BLASTOISE
class Blastoise(PokemonBase):
    def __init__(self):
        PokemonBase.__init__(self, -1, PokeType.WATER)
        self.level = 3 # base level
    
    def get_max_hp(self) -> int:
        return 15 + 2 * self.level

    def get_attack_damage(self) -> int:
        return 8 + self.level // 2

    def get_speed(self) -> int:
        return 10

    def get_defence(self) -> int:
        return 8 + 1 * self.level
    
    def can_evolve(self) -> bool:
        return False

    def get_initial_evolved_version(self) -> PokemonBase:
        raise ValueError(f"{self.name} does not have evolution")
        
    def defend(self, damage: int) -> None:
        if damage > (self.get_defence() * 2):
            self.lose_hp(damage)
        else:
            self.lose_hp(damage//2)


# SQUIRTLE
class Squirtle(PokemonBase):

    def __init__(self):
        PokemonBase.__init__(self, 11, PokeType.WATER)
    
    def get_max_hp(self) -> int:
        return 9 + 2 * self.level

    def get_attack_damage(self) -> int:
        return 4 + self.level//2

    def get_speed(self) -> int:
        return 7

    def get_defence(self) -> int:
        return 6 + self.level
    
    def can_evolve(self) -> bool:
        return True

    def get_initial_evolved_version(self) -> PokemonBase:
        return Blastoise()

    def defend(self, damage: int) -> None:
        if damage > (self.get_defence() * 2):
            self.lose_hp(damage)
        else:
            self.lose_hp(damage//2)


# *******************************************


# GASTLY >> HAUNTER >> GENGAR
class Gengar(PokemonBase):

    def __init__(self):
        PokemonBase.__init__(self, -1, PokeType.GHOST)
        self.level = 3 # base level
    
    def get_max_hp(self) -> int:
        return 12 + self.level//2

    def get_attack_damage(self) -> int:
        return 18

    def get_speed(self) -> int:
        return 12

    def get_defence(self) -> int:
        return 3
    
    def can_evolve(self) -> bool:
        return False
    
    def get_initial_evolved_version(self) -> PokemonBase:
        raise ValueError(f"{self.name} does not have evolution")
        
    def defend(self, damage: int) -> None:
        self.lose_hp(damage)


# GASTLY >> HAUNTER
class Haunter(PokemonBase):

    def __init__(self):
        PokemonBase.__init__(self, -1, PokeType.GHOST)
        self.level = 1 # base level
    
    def get_max_hp(self) -> int:
        return 9 + self.level//2

    def get_attack_damage(self) -> int:
        return 8

    def get_speed(self) -> int:
        return 6

    def get_defence(self) -> int:
        return 6
    
    def can_evolve(self) -> bool:
        return True

    def get_initial_evolved_version(self) -> PokemonBase:
        return Gengar()

    def defend(self, damage: int) -> None:
        self.lose_hp(damage)


# GASTLY
class Gastly(PokemonBase):

    def __init__(self):
        PokemonBase.__init__(self, 6, PokeType.GHOST)

    def get_max_hp(self) -> int:
        return 6 + self.level//2

    def get_attack_damage(self) -> int:
        return 4

    def get_speed(self) -> int:
        return 2

    def get_defence(self) -> int:
        return 8
    
    def can_evolve(self) -> bool:
        return True
    
    def get_initial_evolved_version(self) -> PokemonBase:
        return Haunter()

    def defend(self, damage: int) -> None:
        self.lose_hp(damage)


# *******************************************


# EEVE
class Eevee(PokemonBase):
    
    def __init__(self):
        PokemonBase.__init__(self, 10, PokeType.NORMAL)
    
    def get_max_hp(self) -> int:
        return 10

    def get_attack_damage(self) -> int:
        return 6 + self.level

    def get_speed(self) -> int:
        return 7 + self.level

    def get_defence(self) -> int:
        return 4 + self.level
    
    def can_evolve(self) -> bool:
        return False
    
    def get_initial_evolved_version(self) -> PokemonBase:
        raise ValueError(f"{self.name} does not have evolution")
        
    def defend(self, damage: int) -> None:
        if damage >= self.get_defence():
            self.lose_hp(damage)
        else:
            self.lose_hp(0)


# *******************************************