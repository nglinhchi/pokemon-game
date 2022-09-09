"""
"""
__author__ = "Scaffold by Jackson Goerner, Code by ______________"

from lib2to3.pgen2.token import NAME
from operator import truediv
from pokemon_base import PokeType, PokemonBase


class Charmander(PokemonBase):

    def __init__ (self) -> None:
        PokemonBase.__init__(self, PokeType.FIRE, 9)

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

    def get_max_hp(self) -> int:
        return 8 + 1 * self.level



class Charizard(PokemonBase):
    
    BASE_LEVEL = 3

    def __init__ (self, previous: Charmander) -> None:
        PokemonBase.__init__(self, PokeType.FIRE, previous.max_hp)
        self.level = previous.level
        self.hp = previous.hp
        self.update_hp()

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
