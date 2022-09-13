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

    def type_multiplier(self, defend_poketype: PokeType):
        """
        Poketype is opponent poketype arg. returns effective multiplier against opponent 
        """
        return self.type_effectiveness[defend_poketype.type_index]



class PokemonBase(ABC):

    def __init__(self, hp: int, poke_type: PokeType) -> None:
        self.name = self.__class__.__name__
        self.poke_type = poke_type
        self.level = 1
        self.status_effect = None
        self.max_hp = self.get_max_hp()
        self.hp = self.max_hp

    def __str__(self) -> str:
        return f"LV.{self.level} {self.name}: {self.hp} HP"

    # GETTERS FOR 'STATIC' ATTRIBUTES ************************************************

    def get_name(self) -> str:
        return self.name

    def get_type(self) -> PokeType:
        return self.poke_type

    def get_level(self) -> int:
        """
        Getter method returning current Level
        """
        return self.level

    def get_status_effect(self) -> StatusEffect:
        return self.status_effect

    @abstractmethod
    def get_max_hp(self) -> int:
        """
        Abstract method containing HP scaling formula for individual pokemon. Calculates 
        this max HP using base_hp and returns.
        :pre: base_hp must be defined
        """
        pass

    def get_hp(self) -> int:
        """
        Getter method returning current HP
        """
        return self.hp

    # GETTERS FOR 'DYNAMIC' ATTRIBUTES ************************************************

    @abstractmethod
    def get_speed(self) -> int:
        """
        Abstract getter method returning current Speed stat calculated for individual Pokemon
        """
        pass

    @abstractmethod
    def get_attack_damage(self) -> int:
        """
        Abstract getter method returning current Attack stat calculated for individual Pokemon
        """
        pass

    @abstractmethod
    def get_defence(self) -> int:
        """
        Abstract getter method returning current Defence stat calculated for individual Pokemon
        """
        pass

    # OTHER METHODS ************************************************

    def is_fainted(self) -> bool:
        return self.hp <= 0

    def lose_hp(self, lost_hp: int) -> None:
        """
        Lose hp equal to amount passed as arg. Subtract this amount from current HP (stored in hp)
        and set as current HP
        """
        self.hp -= lost_hp

    def heal(self) -> None:
        """
        Restores current HP to full and removes any status effects
        """
        self.hp = self.max_hp
        self.status_effect = None

    @abstractmethod
    def defend(self, damage: int) -> None:
        """
        Abstract method that calculates damage mitigation/damage to take depending on 
        individual Pokemon's Defence Calculation attribute. Calls lose_hp to reflect 
        damage amount onto Pokemon's health.
        """
        pass

    def attack(self, other: PokemonBase):
        """
        Attack handler that takes another Pokemon as arg and checks if attacking 
        Pokemon is capable of attacking, applying relevant (changes) due to status
        effects. Calculates effective attack amount based on attack stat and types
        of the Pokemon, and applies defending Pokemon's defence calc to this amount.
        Then takes any relevant damage due to status effects and has chance of inflicting
        own status effect onto defending Pokemon
        """
        # >>> Step 1: Status effects on attack damage / redirecting attacks
        if self.status_effect == StatusEffect.SLEEP:
            return
        elif self.status_effect == StatusEffect.CONFUSION:
            if(RandomGen.random_chance(0.5)): # 50% of attacking self
                other = self
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

    def should_evolve(self) -> bool:
        """
        Check if pokemon has met level requirement to evolve
        """
        return self.level >= self.get_initial_evolved_version().get_level()

    @abstractmethod
    def can_evolve(self) -> bool:
        """
        Base pokemon returns true
        Fully evolved pokemon returns false
        """
        pass

    @abstractmethod
    def get_initial_evolved_version(self) -> PokemonBase: 
        """
        Base pokemon return the base evolved pokemon
        Fully evolved pokemon return error
        """
        pass

    def update_hp(self) -> None:
        """
        Default method to be called when attributes affecting hp change i.e. evolution/level
        Scales max HP by calling get_max_hp(), and calculates HP lost prior to HP modification, 
        updating current HP by subtracting from new max HP.
        :pre: max_hp and hp must be defined
        """
        previous_max_hp = self.max_hp  
        previous_hp = self.hp          
        self.max_hp = self.get_max_hp()
        self.hp = self.max_hp - (previous_max_hp - previous_hp)

    
    def get_evolved_version(self) -> PokemonBase:
        """
        Take instance of evolved Pokemon and passes Pre-Evolved Pokemon's necessary attributes onto it 
        """
        evolved = self.get_initial_evolved_version()
        evolved.level = self.level
        evolved.status_effect = self.status_effect
        evolved.hp = self.hp
        evolved.max_hp = self.max_hp
        evolved.update_hp()
        return evolved

    def level_up(self) -> None:
        """
        Increase pokemon's level, scale hp and max_hp
        """
        self.level += 1
        self.update_hp()