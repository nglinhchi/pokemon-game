from __future__ import annotations
from abc import abstractmethod, ABC
from typing_extensions import Self
from random_gen import RandomGen

from enum import Enum, auto

"""

"""
__author__ = "Scaffold by Jackson Goerner, Code by ______________"

class StatusEffect(Enum):
    BURN = 1
    POISON = 3
    PARALYSIS = 0
    SLEEP = 0
    CONFUSION = 0

class PokeType(Enum):
    FIRE = (0, StatusEffect.BURN)
    GRASS = (1, StatusEffect.POISON)
    WATER = (2, StatusEffect.PARALYSIS)
    GHOST = (3, StatusEffect.SLEEP)
    NORMAL = (4, StatusEffect.CONFUSION)
    def __init__(self, type_index: int, status_effect: StatusEffect):
        self.type_index = type_index
        self.type_status_effect = status_effect
    
class PokemonBase(ABC):

    EFFECTIVE_ATTACK = [[1,     2,      0.5,    1,      1],
                        [0.5,   1,      2,      1,      1],
                        [2,     0.5,    1,      1,      1],
                        [1.25,  1.25,   1.25,   2,      0],
                        [1.25,  1.25,   1.25,   0,      1]]

    def __init__(self, hp: int, poke_type: PokeType) -> None:
        self.hp = hp
        self.poke_type = poke_type
        self.name = None
        self.status_effect = None
        self.level = 1
        self.base_attack = 0
        self.attack = self.base_attack
        self.base_speed = 0
        self.speed = self.base_speed
        self.defence = 0
        self.evolve = False

    def is_fainted(self) -> bool:
        return self.hp <= 0

    def level_up(self) -> None:
        self.level += 1

    def get_speed(self) -> int:
        return self.speed

    def get_attack_damage(self) -> int:
        return self.attack

    def get_defence(self) -> int:
        return self.defence

    def lose_hp(self, lost_hp: int) -> None:
        self.hp -= lost_hp

    @abstractmethod
    def defend(self, damage: int) -> None:
        pass

    def attack(self, other: PokemonBase):

        # Step 1: Status effects on attack damage / redirecting attacks
        if self.status_effect == StatusEffect.SLEEP:
            return # TODO stop the attack
        elif self.status_effect == StatusEffect.CONFUSION:
            if(RandomGen.random_chance(0.5)): # True 33% of the time, False 67% of the time.
                other = self
        elif self.status_effect == StatusEffect.PARALYSIS:
            self.speed = self.speed // 2
                
        # Step 2: Do the attack
        
        # calculate attack
        base_ad = self.get_attack_damage() 
        multipler = PokemonBase.EFFECTIVE_ATTACK[self.poke_type.type_index][other.poke_type.type_index]
        effective_ad = int(base_ad * multipler)

        # defend and lose hp
        other.defend(effective_ad)

        # Step 3: Losing hp to status effects
        if (self.status_effect != None):
            self.lose_hp(self.status_effect.value)
        
        # Step 4: Possibly applying status effects
        if(RandomGen.random_chance(0.2)): # True 33% of the time, False 67% of the time.
            other.status_effect = self.poke_type.type_status_effect

    def get_poke_name(self) -> str:
        return self.name

    def __str__(self) -> str:
        return print(f"LV.{self.level} {self.name}: {self.hp} HP")

    def should_evolve(self) -> bool:\
        return (self.can_evolve() and not self.is_fainted() and (self.level == self.get_evolved_version().level))

    @abstractmethod
    def can_evolve(self) -> bool:
        pass 

    @abstractmethod
    def get_evolved_version(self) -> PokemonBase:
        pass
