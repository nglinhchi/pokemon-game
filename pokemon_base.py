from __future__ import annotations
from abc import abstractmethod, ABC
from typing_extensions import Self
from random_gen import RandomGen

from enum import Enum, auto

"""

"""
__author__ = "Scaffold by Jackson Goerner, Code by ______________"

class StatusEffect(Enum):
    """
    List of valid status effects with assigned values representing each effect's damage (where exists).
    """

    BURN = 1
    POISON = 3
    PARALYSIS = 0
    SLEEP = 0
    CONFUSION = 0

class PokeType(Enum):
    """
    Assigns corresponding status effect and an index for each type to be referenced to calculate type_multiplier value, and type_effectiveness values in a list
    """

    FIRE = (0, StatusEffect.BURN, [1,     2,      0.5,    1,      1])
    GRASS = (1, StatusEffect.POISON, [0.5,   1,      2,      1,      1])
    WATER = (2, StatusEffect.PARALYSIS, [2,     0.5,    1,      1,      1])
    GHOST = (3, StatusEffect.SLEEP, [1.25,  1.25,   1.25,   2,      0])
    NORMAL = (4, StatusEffect.CONFUSION, [1.25,  1.25,   1.25,   0,      1])
    def __init__(self, type_index, status_effect, type_effectiveness):
        self.type_index = type_index
        self.status_effect = status_effect
        self.type_effectiveness = type_effectiveness
    def type_multiplier(self, PokeType):
        """
        Poketype is opponent poketype arg. returns effective multiplier against opponent 
        """
        return self.type_effectiveness[PokeType.type_index]




    
class PokemonBase(ABC):

    

    def __init__(self, hp: int, poke_type: PokeType) -> None:
        self.level = 1
        self.current_hp= None #Will get updated by update_max_hp
        self.max_hp = self.update_max_hp(hp)
        self.poke_type = poke_type
        self.name = self.__class__.__name__
        self.status_effect = None
        self.attack_damage = None
        self.speed = None
        self.defence = None

        self.evolve = False

    def is_fainted(self) -> bool:
        return self.hp <= 0

    def level_up(self) -> None:
        self.level += 1
        self.current_hp = self.get_hp()

    @abstractmethod
    def update_max_hp(self, base_hp) -> int:
        #When Max HP is called, update current hp, else only touch current hp while working.
        #Max hp should only be touched when levelling up, and comparing to current HP.
        pass

    def get_hp(self) -> int:
        """
        Return current hp
        """
        if self.get_level() == 1:
            if self.current_hp != self.max_hp:  #if health lost calculate new max health and keep same diff between current and max health
                diff = self.max_hp - self.current_hp
                return self.update_max_hp() - diff
            else:   #update to be same value if no health lost (for overwriting base level by pokemon child classes)
                self.max_hp = self.update_max_hp()
                self.current_hp = self.update_max_hp()
                return self.current_hp


    def get_level(self) -> int:
        #Return current level, should call in HP calculation?
        return self.level
    
    def get_speed(self) -> int:
        return self.speed

    def get_attack_damage(self) -> int:
        return self.attack

    def get_defence(self) -> int:
        return self.defence

    def lose_hp(self, lost_hp: int) -> None:
        self.current_hp -= lost_hp

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
        multipler = self.poke_type.type_multiplier(other.poke_type)
        effective_ad = int(base_ad * multipler)

        # defend and lose hp
        other.defend(effective_ad)

        # Step 3: Losing hp to status effects
        if (self.status_effect != None):
            self.lose_hp(self.status_effect.value)
        
        # Step 4: Possibly applying status effects
        if(RandomGen.random_chance(0.2)): # True 33% of the time, False 67% of the time.
            other.status_effect = self.poke_type.status_effect

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