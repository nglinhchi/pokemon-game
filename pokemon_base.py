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
    FIRE =      (0, StatusEffect.BURN,      [1,     2,      0.5,    1,      1])
    GRASS =     (1, StatusEffect.POISON,    [0.5,   1,      2,      1,      1])
    WATER =     (2, StatusEffect.PARALYSIS, [2,     0.5,    1,      1,      1])
    GHOST =     (3, StatusEffect.SLEEP,     [1.25,  1.25,   1.25,   2,      0])
    NORMAL =    (4, StatusEffect.CONFUSION, [1.25,  1.25,   1.25,   0,      1])

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

    def __init__(self, hp: int, type: PokeType) -> None:
        self.name = self.__class__.__name__
        self.type = type
        self.level = 1

        # self.base_hp = hp 
        # WHY DELETED: this is ommitted as it can be directly included in get_max_hp() method (previously hp_scaler())
        
        # self.max_hp = self.hp_scaler()
        self.max_hp = hp 
        # for base pokemon, MAX_HP will be passed a harcoded value
        # for evolved pokemon, MAX_HP will be previous base pokemon's max hp

        # self.current_hp= self.get_hp()
        self.hp = hp
        # for base pokemon, HP will be equal to MAX_HP as it initially has full health
        # for evolved pokemon, this value will be overwritten in its __init__ later on (meaning that the current value doesn't matter)

        self.status_effect = None
        
        # self.attack_damage = None
        # self.speed = None
        # self.defence = None
        # WHY DELETED: these values are dependent on self.level, and each pokemon also has its own calculation 
        #                --> therefore using getter methods instead (making it dynamic instead of hardcoded)

        # self.evolve = False
        # WHY DELETED: not sure why we needed it in first place... (since we already have can_evolve())

    def level_up(self) -> None:
        self.level += 1
        self.current_hp = self.get_hp()
        
    def is_fainted(self) -> bool:
        return self.hp <= 0

    def lose_hp(self, lost_hp: int) -> None:
        self.current_hp -= lost_hp
    
    def update_hp(self) -> None:
        # save previous values
        previous_max_hp = self.max_hp   # taken from lower-level/pre-evolved pokemon
        previous_hp = self.hp           # taken from lower-level/pre-evolved pokemon
        # change max hp
        self.max_hp = self.get_max_hp() # compute the new max HP (since the level/pokemon type changed)
        # scale current hp
        self.hp = self.max_hp - (previous_max_hp - previous_hp) # ensure the difference remain the same 

    # def get_hp(self) -> int:
    #     """
    #     Return current hp
    #     """
    #     try:
    #         if self.current_hp != self.max_hp:  #if health lost calculate new max health and keep same diff between current and max health
    #             diff = self.max_hp - self.current_hp
    #             return self.hp_scaler() - diff
    #         else:   #update to be same value if no health lost (for overwriting base level by pokemon child classes)
    #             self.max_hp = self.hp_scaler()
    #             self.current_hp = self.hp_scaler()
    #             return self.current_hp
    #     except AttributeError:
    #         return self.max_hp  #initiation

    @abstractmethod
    def get_max_hp(self) -> int: # just thought this name is clearer and makes more sense
    # def hp_scaler(self) -> int:
        pass

    @abstractmethod
    def get_speed(self) -> int: # PREVIOUSLY return a hardcoded value
        # return self.speed
        pass

    @abstractmethod
    def get_attack_damage(self) -> int: # PREVIOUSLY return a hardcoded value
        # return self.attack
        pass

    @abstractmethod
    def get_defence(self) -> int: # PREVIOUSLY return a hardcoded value
        # return self.defence
        pass

    @abstractmethod
    def defend(self, damage: int) -> None:
        pass

    def attack(self, other: PokemonBase):
        # *** Step 1: Status effects on attack damage / redirecting attacks
        if self.status_effect == StatusEffect.SLEEP:
            return
        elif self.status_effect == StatusEffect.CONFUSION:
            if(RandomGen.random_chance(0.5)): # True 33% of the time, False 67% of the time.
                other = self
        # elif self.status_effect == StatusEffect.PARALYSIS:
        #     self.speed = self.speed // 2
        # TODO changing spped no longer works cause speed is no longer an attribute of a pokemon,
        # this can be fixed easily by using self.get_speed()//2 as a value on the spot
        # *** Step 2: Do the attack
        base_ad = self.get_attack_damage() 
        multipler = self.poke_type.type_multiplier(other.poke_type)
        effective_ad = int(base_ad * multipler)
        other.defend(effective_ad)
        # *** Step 3: Losing hp to status effects
        if (self.status_effect != None):
            self.lose_hp(self.status_effect.value)
        # *** Step 4: Possibly applying status effects
        if(RandomGen.random_chance(0.2)): # True 33% of the time, False 67% of the time.
            other.status_effect = self.poke_type.status_effect

    def get_poke_name(self) -> str:
        return self.name

    def __str__(self) -> str:
        return print(f"LV.{self.level} {self.name}: {self.hp} HP")

    def should_evolve(self) -> bool:
        return (self.can_evolve() and \
                not self.is_fainted() and \
                self.level == self.get_evolved_version().level)

    @abstractmethod
    def can_evolve(self) -> bool:
        pass 

    @abstractmethod
    def get_evolved_version(self) -> PokemonBase:
        pass