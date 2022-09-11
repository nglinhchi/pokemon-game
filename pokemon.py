"""
"""
__author__ = "Scaffold by Jackson Goerner, Code by ______________"

from multiprocessing.sharedctypes import Value
from pokemon_base import PokemonBase, StatusEffect, PokeType


class Charizard(PokemonBase):
    def __init__(self):
        PokemonBase.__init__(self, 12, PokeType.FIRE)
        self.level = 3  #Default base level
    
    def get_max_hp(self) -> int:
        return self.base_hp + 1 * self.level

    def get_attack_damage(self) -> int:
        return 10 + 2 * self.level

    def get_speed(self) -> int:
        return 9 + 1 * self.level

    def get_defence(self) -> int:
        return 4
    
    def can_evolve(self) -> bool:
        return False

    def should_evolve(self) -> bool:
        return False
    
    def get_evolved_version(self) -> PokemonBase:
        raise ValueError(f"{self.name} does not have evolution")

    def defend(self, damage: int) -> None:
        if damage > self.get_defence():
            self.lose_hp(2*damage)
        else:
            self.lose_hp(damage)


    

class Charmander(PokemonBase):
    def __init__(self):
        PokemonBase.__init__(self, 8, PokeType.FIRE)

    
    def get_max_hp(self) -> int:
        return self.base_hp + 1 * self.level

    def get_attack_damage(self) -> int:
        return 6 + 1 * self.level

    def get_speed(self) -> int:
        return 7 + 1 * self.level

    def get_defence(self) -> int:
        return 4
    
    def can_evolve(self) -> bool:
        return True

    def should_evolve(self) -> bool:
        if self.level >= Charizard().get_level():
            return True
        return False
    
    def get_evolved_version(self) -> PokemonBase:
        evolution = Charizard()
        self.inherit_traits(evolution)
        return evolution

    def defend(self, damage: int) -> None:
        if damage > self.get_defence():
            self.lose_hp(damage)
        else:
            self.lose_hp(damage//2)


class Venusaur(PokemonBase):
    def __init__(self):
        PokemonBase.__init__(self, 20, PokeType.GRASS)
        self.level = 2
    
    def get_max_hp(self) -> int:
        return self.base_hp + self.level//2

    def get_attack_damage(self) -> int:
        return 5

    def get_speed(self) -> int:
        return 3 + self.level//2

    def get_defence(self) -> int:
        return 10
    
    def can_evolve(self) -> bool:
        return False
    
    def should_evolve(self) -> bool:
        return False
    
    def get_evolved_version(self) -> PokemonBase:
        raise ValueError(f"{self.name} does not have evolution")

    def defend(self, damage: int) -> None:
        if damage > (self.get_defence() + 5):
            self.lose_hp(damage)
        else:
            self.lose_hp(damage//2)

class Bulbasaur(PokemonBase):
    def __init__(self):
        PokemonBase.__init__(self, 12, PokeType.GRASS)
    
    def get_max_hp(self) -> int:
        return self.base_hp + 1 * self.level

    def get_attack_damage(self) -> int:
        return 5

    def get_speed(self) -> int:
        return 7 + self.level//2

    def get_defence(self) -> int:
        return 5
    
    def can_evolve(self) -> bool:
        return True

    def should_evolve(self) -> bool:
        if self.level >= Venusaur().get_level():
            return True
        return False
    
    def get_evolved_version(self) -> PokemonBase:
        evolution = Venusaur()
        self.inherit_traits(evolution)
        return evolution


    def defend(self, damage: int) -> None:
        if damage > (self.get_defence() + 5):
            self.lose_hp(damage)
        else:
            self.lose_hp(damage//2)    


class Blastoise(PokemonBase):
    def __init__(self):
        PokemonBase.__init__(self, 15, PokeType.WATER)
        self.level = 3
    
    def get_max_hp(self) -> int:
        return self.base_hp + 2 * self.level

    def get_attack_damage(self) -> int:
        return 8 + self.level//2

    def get_speed(self) -> int:
        return 10

    def get_defence(self) -> int:
        return 8 + 1 * self.level
    
    def can_evolve(self) -> bool:
        return False

    def should_evolve(self) -> bool:
        return False
    
    def get_evolved_version(self) -> PokemonBase:
        raise ValueError(f"{self.name} does not have evolution")
        
    def defend(self, damage: int) -> None:
        if damage > (self.get_defence() * 2):
            self.lose_hp(damage)
        else:
            self.lose_hp(damage//2)

class Squirtle(PokemonBase):
    def __init__(self):
        PokemonBase.__init__(self, 9, PokeType.WATER)
    
    def get_max_hp(self) -> int:
        return self.base_hp + 2 * self.level

    def get_attack_damage(self) -> int:
        return 4 + self.level//2

    def get_speed(self) -> int:
        return 7

    def get_defence(self) -> int:
        return 6 + self.level
    
    def can_evolve(self) -> bool:
        return True

    def should_evolve(self) -> bool:
        if self.level >= Blastoise().get_level():
            return True
        return False
    
    def get_evolved_version(self) -> PokemonBase:
        evolution = Blastoise()
        self.inherit_traits(evolution)
        return evolution


    def defend(self, damage: int) -> None:
        if damage > (self.get_defence() * 2):
            self.lose_hp(damage)
        else:
            self.lose_hp(damage//2)

class Gengar(PokemonBase):
    def __init__(self):
        PokemonBase.__init__(self, 12, PokeType.GHOST)
        self.level = 3
    
    def get_max_hp(self) -> int:
        return self.base_hp + self.level//2

    def get_attack_damage(self) -> int:
        return 18

    def get_speed(self) -> int:
        return 12

    def get_defence(self) -> int:
        return 3
    
    def can_evolve(self) -> bool:
        return False

    def should_evolve(self) -> bool:
        return False
    
    def get_evolved_version(self) -> PokemonBase:
        raise ValueError(f"{self.name} does not have evolution")
        
    def defend(self, damage: int) -> None:
        self.lose_hp(damage)

class Haunter(PokemonBase):
    def __init__(self):
        PokemonBase.__init__(self, 9, PokeType.GHOST)
    
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

    def should_evolve(self) -> bool:
        if self.level >= Gengar().get_level():
            return True
        return False
    
    def get_evolved_version(self) -> PokemonBase:
        evolution = Gengar()
        self.inherit_traits(evolution)
        return evolution

        
    def defend(self, damage: int) -> None:
        self.lose_hp(damage)
    
class Gastly(PokemonBase):
    def __init__(self):
        PokemonBase.__init__(self, 6, PokeType.GHOST)

    def get_max_hp(self) -> int:
        return self.base_hp + self.level//2

    def get_attack_damage(self) -> int:
        return 4

    def get_speed(self) -> int:
        return 2

    def get_defence(self) -> int:
        return 8
    
    def can_evolve(self) -> bool:
        return True

    def should_evolve(self) -> bool:
        if self.level >= Haunter().get_level():
            return True
        return False
    
    def get_evolved_version(self) -> PokemonBase:
        evolution = Haunter()
        self.inherit_traits(evolution)
        return evolution


    def defend(self, damage: int) -> None:
        self.lose_hp(damage)

    

class Eevee(PokemonBase):
    def __init__(self):
        PokemonBase.__init__(self, 10, PokeType.NORMAL)
    
    def get_max_hp(self) -> int:
        return self.base_hp

    def get_attack_damage(self) -> int:
        return 6 + self.level

    def get_speed(self) -> int:
        return 7 + self.level

    def get_defence(self) -> int:
        return 4 + self.level
    
    def can_evolve(self) -> bool:
        return False

    def should_evolve(self) -> bool:
        return False
    
    def get_evolved_version(self) -> PokemonBase:
        raise ValueError(f"{self.name} does not have evolution")
        
    def defend(self, damage: int) -> None:
        if damage >= self.get_defence():
            self.lose_hp(damage)
        else:
            self.lose_hp(0)

    
