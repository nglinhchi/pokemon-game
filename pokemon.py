"""
"""
__author__ = "Scaffold by Jackson Goerner, Code by ______________"

from pokemon_base import PokemonBase, StatusEffect, PokeType


class Charizard(PokemonBase):
    
    def __init__(self, previous: PokemonBase):
        PokemonBase.__init__(self, previous.max_hp, PokeType.FIRE)
        # PokemonBase.__init__(self, 12, PokeType.FIRE)
        self.level = previous.level # overwrite base_level = 1
        self.hp = previous.hp
        self.update_hp()

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

    def get_evolved_version(self) -> PokemonBase:
        return None

    def defend(self, damage: int) -> None:
        if damage > self.get_defence():
            self.lose_hp(2*damage)
        else:
            self.lose_hp(damage)


class Charmander(PokemonBase):
    
    def __init__(self, previous: PokemonBase):
        PokemonBase.__init__(self, previous.max_hp, PokeType.FIRE)
        
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

    def get_evolved_version(self) -> PokemonBase:
        return Charizard()

    def defend(self, damage: int) -> None:
        if damage > self.get_defence():
            self.lose_hp(damage)
        else:
            self.lose_hp(damage//2)


class Venusaur(PokemonBase):
    pass


class Bulbasaur(PokemonBase):
    pass


class Blastoise(PokemonBase):
    def __init__(self):
        PokemonBase.__init__(self, 15, PokeType.WATER)
        self.level = 3
    
    def hp_scaler(self) -> int:    
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
    
    def hp_scaler(self) -> int:    
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
    
    def hp_scaler(self) -> int:    
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
    
    def hp_scaler(self) -> int:    
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

    def hp_scaler(self) -> int:    
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
    
    def hp_scaler(self) -> int:    
        hp_formula = self.base_hp
        return hp_formula
    
    def can_evolve(self) -> bool:
        pass 

    def get_evolved_version(self) -> PokemonBase:
        pass

    def defend(self, damage: int) -> None:
        pass

