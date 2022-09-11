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
        self.base_hp = hp   #Stores HP parameter in base_hp to be called during calculation of get_max_hp(). Allows for easy change of initial value of HP without level scaling.
        self.max_hp = self.get_max_hp()
        self.hp = self.max_hp
        self.poke_type = poke_type
        self.name = self.__class__.__name__
        self.status_effect = None


    def is_fainted(self) -> bool:
        return self.hp <= 0

    def level_up(self) -> None:
        self.level += 1
        self.hp = self.get_hp()

    @abstractmethod
    def get_max_hp(self) -> int:
        #When Max HP is called, update current hp, else only touch current hp while working.
        #Max hp should only be touched when levelling up, and comparing to current HP.
        pass

    def update_hp(self) -> None:
        """
        Default method to be called when attributes affecting hp change i.e. evolution/level
        """
        # save previous values
        previous_max_hp = self.max_hp   # taken from lower-level/pre-evolved pokemon
        previous_hp = self.hp           # taken from lower-level/pre-evolved pokemon
        # change max hp
        self.max_hp = self.get_max_hp() # compute the new max HP (since the level/pokemon type changed)
        # scale current hp
        self.hp = self.max_hp - (previous_max_hp - previous_hp) # ensure the difference remain the same 
        
    def get_hp(self) -> int:
        return self.hp

    def get_level(self) -> int:
        return self.level
    
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
        return f"LV.{self.level} {self.name}: {self.hp} HP"

    @abstractmethod
    def should_evolve(self) -> bool:
        pass

    @abstractmethod
    def can_evolve(self) -> bool:
        pass 

    @abstractmethod
    def get_evolved_version(self) -> PokemonBase:
        pass

    def inherit_traits(self, evolved: PokemonBase) -> None:
        """
        Takes instance of evolved Pokemon and passes Pre-Evolved Pokemon's necessary attributes onto it 
        """
        evolved.level, evolved.status_effect, evolved.hp, evolved.max_hp = self.level, self.status_effect, self.hp, self.max_hp #passes attributes that need to be inherited by evolved Pokemon
        evolved.update_hp() #updates HP using pre-evolution Pokemon's HP difference
        # return evolved