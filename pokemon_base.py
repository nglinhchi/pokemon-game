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

    def __init__(self, hp: int, poke_type: PokeType) -> None:
        self.name = self.__class__.__name__
        self.poke_type = poke_type
        self.level = 1
        self.status_effect = None
        self.max_hp = hp
        self.hp = hp

    def __str__(self) -> str:
        return print(f"LV.{self.level} {self.name}: {self.hp} HP")

    # GETTERS FOR 'STATIC' ATTRIBUTES ************************************************

    def get_name(self) -> str:
        return self.name

    def get_type(self) -> PokeType:
        return self.poke_type

    def get_level(self) -> int:
        return self.level

    def get_status_effect(self) -> StatusEffect:
        return self.status_effect

    @abstractmethod
    def get_max_hp(self) -> int: # only called once via update_hp()
        pass

    def get_hp(self) -> int:
        return self.hp

    # GETTERS FOR 'DYNAMIC' ATTRIBUTES ************************************************

    @abstractmethod
    def get_speed(self) -> int:
        # return self.speed
        pass

    @abstractmethod
    def get_attack_damage(self) -> int:
        # return self.attack
        pass

    @abstractmethod
    def get_defence(self) -> int:
        # return self.defence
        pass

    # OTHER METHODS ************************************************

    def is_fainted(self) -> bool:
        return self.hp <= 0

    def lose_hp(self, lost_hp: int) -> None:
        self.hp -= lost_hp

    @abstractmethod
    def defend(self, damage: int) -> None:
        pass

    def attack(self, other: PokemonBase):
        
        # >>> Step 1: Status effects on attack damage / redirecting attacks
        if self.status_effect == StatusEffect.SLEEP:
            return # TODO stop the attack
        elif self.status_effect == StatusEffect.CONFUSION:
            if(RandomGen.random_chance(0.5)): # 50% of attacking self
                other = self
        # elif self.status_effect == StatusEffect.PARALYSIS:
            # self.speed = self.speed // 2
        # TODO commented out since there's no attribute 'speed'
        
        # >>> Step 2: Do the attack
        base_attack = self.get_attack_damage() 
        multipler = self.poke_type.type_multiplier(other.poke_type)
        effective_attack = int(base_attack * multipler)
        other.defend(effective_attack)

        # >>> Step 3: Losing hp to status effects
        if (self.status_effect != None):
            self.lose_hp(self.status_effect.value)
        
        # >>> Step 4: Possibly applying status effects
        if(RandomGen.random_chance(0.2)): # 20% of inflicting status effect
            other.status_effect = self.poke_type.status_effect


    # LEVEL UP AND EVOLUTION ************************************************

    # @abstractmethod
    def should_evolve(self) -> bool:
        return self.level >= self.get_evolved_version().get_level()

    @abstractmethod
    def can_evolve(self) -> bool:
        # true for base pokemon
        # false for fully evolved pokemon
        pass

    @abstractmethod
    def get_initial_evolved_version(self) -> PokemonBase: 
        """
        Base pokemon return the initial evolved pokemon
        Fully evolved pokemon return error
        """
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

    # @abstractmethod
    def get_evolved_version(self) -> PokemonBase:
        """
        Takes instance of evolved Pokemon and passes Pre-Evolved Pokemon's necessary attributes onto it 
        """
        
        # get initial evolved version
        evolved = self.get_initial_evolved_version()

        # inherit from base
        evolved.level = self.level
        evolved.status_effect = self.status_effect
        evolved.hp = self.hp
        evolved.max_hp = self.max_hp

        # scale hp and max_hp
        evolved.update_hp()

    def level_up(self) -> None:
        self.level += 1
        # self.hp = self.get_hp()
        self.update_hp()
