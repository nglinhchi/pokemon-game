"""
"""
__author__ = "Scaffold by Jackson Goerner, Code by ______________"

from inspect import Attribute
from multiprocessing.sharedctypes import Value
from pokemon_base import PokemonBase, StatusEffect, PokeType


# *******************************************


# CHARMANDER >> CHARIZARD
class Charizard(PokemonBase): 
    NAME = "Charizard"
    BASE_LEVEL = 3
    POKE_NO = 2 
    def __init__(self):
        PokemonBase.__init__(self, -1, PokeType.FIRE)
    
    def get_name(self) -> str:
        return __class__.NAME  #Ensures name is set for pokemon

    def get_level(self) -> int:
        try:
            return self.level
        except AttributeError: #when first initialising
            return __class__.BASE_LEVEL #Ensures classes include base level.

    def get_max_hp(self) -> int:
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
        raise ValueError(f"{self.get_name()} does not have evolution")

    def defend(self, damage: int) -> None:
        if damage > self.get_defence():
            self.lose_hp(2*damage)
        else:
            self.lose_hp(damage)


# CHARMANDER
class Charmander(PokemonBase):
    NAME = "Charmander"
    BASE_LEVEL = 1
    POKE_NO = 1
    def __init__(self):
        PokemonBase.__init__(self, 9, PokeType.FIRE)
    
    def get_name(self) -> str:
        return __class__.NAME  #Ensures name is set for pokemon

    def get_level(self) -> int:
        try:
            return self.level
        except AttributeError: #when first initialising
            return __class__.BASE_LEVEL #Ensures classes include base level.

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
    NAME = "Venusaur"
    BASE_LEVEL = 2
    POKE_NO = 4
    def __init__(self):
        PokemonBase.__init__(self, -1, PokeType.GRASS)

    def get_name(self) -> str:
        return __class__.NAME  #Ensures name is set for pokemon

    def get_level(self) -> int:
        try:
            return self.level
        except AttributeError: #when first initialising
            return __class__.BASE_LEVEL #Ensures classes include base level.
    
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
        raise ValueError(f"{self.get_name()} does not have evolution")

    def defend(self, damage: int) -> None:
        if damage > (self.get_defence() + 5):
            self.lose_hp(damage)
        else:
            self.lose_hp(damage//2)


# BULBASAUR
class Bulbasaur(PokemonBase):
    NAME = "Bulbasaur"
    BASE_LEVEL = 1
    POKE_NO = 3
    def __init__(self):
        PokemonBase.__init__(self, 13, PokeType.GRASS)
    
    def get_name(self) -> str:
        return __class__.NAME  #Ensures name is set for pokemon

    def get_level(self) -> int:
        try:
            return self.level
        except AttributeError: #when first initialising
            return __class__.BASE_LEVEL #Ensures classes include base level.

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
    NAME = "Blastoise"
    BASE_LEVEL = 3
    POKE_NO = 6
    def __init__(self):
        PokemonBase.__init__(self, -1, PokeType.WATER)
        self.level = 3 # base level
    
    def get_name(self) -> str:
        return __class__.NAME  #Ensures name is set for pokemon

    def get_level(self) -> int:
        try:
            return self.level
        except AttributeError: #when first initialising
            return __class__.BASE_LEVEL #Ensures classes include base level.

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
        raise ValueError(f"{self.get_name()} does not have evolution")
        
    def defend(self, damage: int) -> None:
        if damage > (self.get_defence() * 2):
            self.lose_hp(damage)
        else:
            self.lose_hp(damage//2)


# SQUIRTLE
class Squirtle(PokemonBase):
    NAME = "Squirtle"
    BASE_LEVEL = 1
    POKE_NO = 5
    def __init__(self):
        PokemonBase.__init__(self, 11, PokeType.WATER)
    
    def get_name(self) -> str:
        return __class__.NAME  #Ensures name is set for pokemon

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
    NAME = "Gengar"
    BASE_LEVEL = 3
    POKE_NO = 9
    def __init__(self):
        PokemonBase.__init__(self, -1, PokeType.GHOST)
        self.level = 3 # base level

    def get_name(self) -> str:
        return __class__.NAME  #Ensures name is set for pokemon

    def get_level(self) -> int:
        try:
            return self.level
        except AttributeError: #when first initialising
            return __class__.BASE_LEVEL #Ensures classes include base level.

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
        raise ValueError(f"{self.get_name()} does not have evolution")
        
    def defend(self, damage: int) -> None:
        self.lose_hp(damage)


# GASTLY >> HAUNTER
class Haunter(PokemonBase):
    NAME = "Haunter"
    BASE_LEVEL = 1
    POKE_NO = 8
    def __init__(self):
        PokemonBase.__init__(self, -1, PokeType.GHOST)
        self.level = 1 # base level
    
    def get_name(self) -> str:
        return __class__.NAME  #Ensures name is set for pokemon

    def get_level(self) -> int:
        try:
            return self.level
        except AttributeError: #when first initialising
            return __class__.BASE_LEVEL #Ensures classes include base level.

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
    NAME = "Gastly"
    BASE_LEVEL = 1
    POKE_NO = 7
    def __init__(self):
        PokemonBase.__init__(self, 6, PokeType.GHOST)

    def get_name(self) -> str:
        return __class__.NAME  #Ensures name is set for pokemon

    def get_level(self) -> int:
        try:
            return self.level
        except AttributeError: #when first initialising
            return __class__.BASE_LEVEL #Ensures classes include base level.

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


# EEVEE
class Eevee(PokemonBase):
    NAME = "Eevee"
    BASE_LEVEL = 1
    POKE_NO = 10
    def __init__(self):
        PokemonBase.__init__(self, 10, PokeType.NORMAL)
    
    def get_name(self) -> str:
        return __class__.NAME  #Ensures name is set for pokemon
    
    def get_level(self) -> int:
        try:
            return self.level
        except AttributeError: #when first initialising
            return __class__.BASE_LEVEL #Ensures classes include base level.

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
        raise ValueError(f"{self.get_name()} does not have evolution")
        
    def defend(self, damage: int) -> None:
        if damage >= self.get_defence():
            self.lose_hp(damage)
        else:
            self.lose_hp(0)

# *******************************************


