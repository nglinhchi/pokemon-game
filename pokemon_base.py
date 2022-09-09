from __future__ import annotations
from abc import abstractmethod, ABC
import string
from typing_extensions import Self
from random_gen import RandomGen

from enum import Enum, auto

"""

"""
__author__ = "Scaffold by Jackson Goerner, Code by ______________"



class StatusEffect(Enum): # key = status effect, value = hp lost on status effect
    BURN = 1
    POISON = 3
    PARALYSIS = 0
    SLEEP = 0
    CONFUSION = 0



class PokeType(Enum): # key = poketype, value = (type status effect, status effect)
    
    FIRE = (0, StatusEffect.BURN)
    GRASS = (1, StatusEffect.POISON)
    WATER = (2, StatusEffect.PARALYSIS)
    GHOST = (3, StatusEffect.SLEEP)
    NORMAL = (4, StatusEffect.CONFUSION)

    def __init__(self, type_index: int, status_effect: StatusEffect):
        self.type_index = type_index
        self.status_effect = status_effect
    


class PokemonBase(ABC):

    EFFECTIVE_ATTACK = [[1,     2,      0.5,    1,      1],
                        [0.5,   1,      2,      1,      1],
                        [2,     0.5,    1,      1,      1],
                        [1.25,  1.25,   1.25,   2,      0],
                        [1.25,  1.25,   1.25,   0,      1]]

    def __init__(self, name: string, type: PokeType, level: int, hp: int) -> None:
        self.name = name
        self.type = type
        self.level = level
        self.max_hp = hp
        self.hp = self.max_hp
        self.status_effect = None

    def is_fainted(self) -> bool:
        return self.hp <= 0

    def lose_hp(self, lost_hp: int) -> None:
        self.hp -= lost_hp

    def level_up(self) -> None:
        self.level += 1
        # max_hp = 

    @abstractmethod
    def get_speed(self) -> int:
        pass

    @abstractmethod
    def get_attack_damage(self) -> int:
        pass

    @abstractmethod
    def get_defence(self) -> int:
        pass

    @abstractmethod
    def defend(self, damage: int) -> None:
        pass

    def attack(self, other: PokemonBase):
        # >>>>> Step 1: Status effects on attack damage / redirecting attacks
        # if a pokemon is asleep, stop the attack
        if self.status_effect == StatusEffect.SLEEP:
            return
        # if a pokemon is confused, see if defending pokemon should change to be self
        elif self.status_effect == StatusEffect.CONFUSION:
            if(RandomGen.random_chance(0.5)): # 50% chance of attacking self
                other = self
        # if a pokemon is paralysed, half its speed
        elif self.status_effect == StatusEffect.PARALYSIS: # TODO not so sure
            self.speed = self.speed // 2
                
        # >>>>> Step 2: Calculate effective attack and do attack
        # calculate attack
        attack_damage = self.get_attack_damage()
        multiplier = PokemonBase.EFFECTIVE_ATTACK[self.poke_type.type_index][other.poke_type.type_index]
        effective_attack = int(attack_damage * multiplier)
        # defend and lose hp
        other.defend(effective_attack)

        # >>>>> Step 3: Lose hp to status effects
        if (self.status_effect != None):
            self.lose_hp(self.status_effect.value)
        
        # Step 4: Possibly apply status effects onto other
        if(RandomGen.random_chance(0.2)): # 20% chance of inflicting other
            other.status_effect = self.poke_type.status_effect

    def get_poke_name(self) -> str:
        return self.name

    def __str__(self) -> str:
        return print(f"LV.{self.level} {self.name}: {self.hp} HP")

    def should_evolve(self) -> bool:
        return (self.can_evolve() and \
                not self.is_fainted() and \
                self.level == self.get_evolved_version().BASE_LEVEL) # TODO


    @abstractmethod
    def can_evolve(self) -> bool:
        pass

    @abstractmethod
    def get_evolved_version(self) -> PokemonBase:
        pass