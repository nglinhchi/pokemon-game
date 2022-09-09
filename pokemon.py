"""
"""
__author__ = "Scaffold by Jackson Goerner, Code by ______________"

from lib2to3.pgen2.token import NAME
from operator import truediv
from pokemon_base import PokeType, PokemonBase


class Charmander(PokemonBase):

    NAME = "Charmander"
    BASE_LEVEL = 1
    TYPE = PokeType.FIRE

    def __init__ (self) -> None:
        PokemonBase.__init__(self, Charmander.NAME, Charmander.TYPE, Charmander.BASE_LEVEL, Charmander.BASE_LEVEL)

    def get_speed(self) -> int:
        return 7 + 1 * self.level

    def get_attack_damage(self) -> int:
        return 6 + 1 * self.level

    def get_defence(self) -> int:
        return 4

    def defend(self, damage: int) -> None:
        if damage > self.get_defence():
            self.lose_hp(damage)
        else:
            self.lose_hp(damage//2)

    def can_evolve(self) -> bool:
        return True

    def get_evolved_version(self) -> PokemonBase:
        return Charizard()



class Charizard:
    
    BASE_LEVEL = 3
    NAME = "Charizard"

    def __init__ (self, previous: Charmander) -> None:
        # PokemonBase.__init__(self, Charizard.NAME, Charizard.TYPE, Charizard.BASE_LEVEL, Charizard.BASE_LEVEL - (previous.))
        pass

    def get_speed(self) -> int:
        return 7 + 1 * self.level

    def get_attack_damage(self) -> int:
        return 6 + 1 * self.level

    def get_defence(self) -> int:
        return 4

    def defend(self, damage: int) -> None:
        if damage > self.get_defence():
            self.lose_hp(damage)
        else:
            self.lose_hp(damage//2)

    def can_evolve(self) -> bool:
        return True

    def get_evolved_version(self) -> PokemonBase:
        return Charizard()



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
