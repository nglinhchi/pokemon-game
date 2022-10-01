from __future__ import annotations
from abc import abstractmethod, ABC
from contextlib import AbstractAsyncContextManager
from dataclasses import dataclass
from multiprocessing.sharedctypes import Value
from typing_extensions import Self
from random_gen import RandomGen
from enum import Enum, auto

"""
Implements the base functions/moves that are required to be performed by all pokemon.
"""

__author__ = "Scaffold by Jackson Goerner, Code by Joong Do Chiang | Chloe Nguyen | Jane Butcher"



class StatusEffects(Enum):
    """
    List of valid status effects with assigned values representing each effect's damage (where exists).
    """
    BURN = auto()
    POISON = auto()
    PARALYSIS = auto()
    SLEEP = auto()
    CONFUSE = auto()

    def get_effect_damage(self):
        if self.name == 'BURN':
            self.effect_damage = 1
        elif self.name == 'POISON':
            self.effect_damage = 3
        else:
            self.effect_damage = 0
        return self.effect_damage

class PokeType(Enum):
    """
    Assigns corresponding status effect and an index for each type to be referenced to calculate type_multiplier value, and type_effectiveness values in a list

    :pre: Each PokeType defined must include a type_effectiveness list against other types, and be assigned to unique index that corresponds to
    own place in type_effectiveness table. Type must include corresponding status effect from StatusEffect Enum class.
    """
    
    FIRE =      (0,     [1,     2,      0.5,    1,      1], StatusEffects.BURN)
    GRASS =     (1,     [0.5,   1,      2,      1,      1], StatusEffects.POISON)
    WATER =     (2,     [2,     0.5,    1,      1,      1], StatusEffects.PARALYSIS)
    GHOST =     (3,     [1.25,  1.25,   1.25,   2,      0], StatusEffects.SLEEP)
    NORMAL =    (4,     [1.25,  1.25,   1.25,   0,      1], StatusEffects.CONFUSE)
    
    def __init__(self, type_index: int, type_effectiveness: list, effect: StatusEffects):
        if not isinstance(type_index, int):
            raise ValueError("Type index must be unique integer")
        if not isinstance(type_effectiveness, list) or len(type_effectiveness) < 0:
            raise ValueError("Type effectiveness table must be a list and non-empty")
        if not isinstance(effect, StatusEffects):
            raise ValueError("Status effect must be of StatusEffects class")
        
        self.type_index = type_index
        self.effect = effect
        self.type_effectiveness = type_effectiveness

    def get_type_index(self):
        """
        Return index of the poketype
        """
        return self.type_index

    def type_multiplier(self, defend_poketype: PokeType):
        """
        Poketype is opponent poketype arg. returns effective multiplier against opponent 

        :pre: defend_poketype must be of PokeType class
        """
        if not isinstance(defend_poketype, PokeType):
            raise ValueError("Type of defending Pokemon not in PokeType class")
        
        multiplier = self.type_effectiveness[defend_poketype.get_type_index()]
    
        return multiplier


class PokemonBase(ABC):

    def __init__(self, hp: int, poke_type: PokeType) -> None:
        """
        Initialises a PokemonBase instance

        :pre: hp must be positive integer, poke_type must be of Enum class PokeType
        """
        self.name = self.get_name() # Ensures Pokemon Name is defined.
        self.set_poketype(poke_type)    # Check for valid poke_type
        self.set_base_hp(hp)    # Check for valid hp
        self.level = self.get_level()
        self.status_effect = None
        self.max_hp = self.get_max_hp()
        self.hp = self.get_max_hp()
        self.attack_damage = self.get_attack_damage()
        self.defence = self.get_defence()
        self.speed = self.get_speed

    def set_poketype(self, poke_type: PokeType):
        """
        Validates poke_type argument passed into init

        :param: poke_type from init class
        """
        if poke_type not in PokeType:
            raise ValueError("Invalid Poke Type")
        self.type = poke_type

    def set_base_hp(self, hp: int):
        """
        Validates hp argument passed into init

        :param: hp from init class
        """
        if not isinstance(hp, int) or hp <= 0:
            raise ValueError("HP must be positive integer")
        else:
            self.base_hp = hp
            
    def __str__(self) -> str:
        """
        :return: string output of the pokemon
        :complexity: O(1)
        """
        return f"LV. {self.get_level()} {self.get_name()}: {self.hp} HP"


    # GETTERS FOR 'STATIC' ATTRIBUTES ************************************************

    @abstractmethod
    def get_name(self) -> str:
        """
        Getter method returning the name of the pokemon
        :return: string of the pokemon's name
        :complexity: O(1)
        """
        pass  

    
    def get_type(self) -> PokeType:
        """
        Getter method returning the type of the pokemon
        :return: pokemon's poketype
        :complexity: O(1)
        """
        return self.type
    
    def get_type_effect(self):
        return self.get_type().effect
    
    @abstractmethod
    def get_level(self) -> int:
        """
        Getter method returning current Level
        :return: integer of the pokemon's current level
        :complexity: O(1)
        """
        pass

    def get_status_effect(self) -> StatusEffects:
        """
        Getter method returning the status effects currently inflicted on a pokemon
        :return: pokemon's current status effects
        :complexity: O(1)
        """
        return self.status_effect

    @abstractmethod
    def get_max_hp(self) -> int:
        """
        Abstract method containing HP scaling formula for individual pokemon. Calculates
        this max HP using base_hp and returns.
        :pre: base_hp must be defined
        :return: integer of pokemon's max hp
        :complexity: O(1)
        """
        pass

    def get_hp(self) -> int:
        """
        Getter method returning current HP
        :return: integer of the pokemon's current HP
        :complexity: O(1)
        """
        return self.hp




    # GETTERS FOR 'DYNAMIC' ATTRIBUTES ************************************************

    def get_speed(self) -> int:
        """
        Getter method returning current Speed stat calculated for individual Pokemon with impact of status effects
        :return: integer of pokemon's speed
        :complexity: O(1)
        """
        speed = self.speed_formula()
        if self.get_status_effect() == StatusEffects.PARALYSIS:
            speed = int(speed * 0.5)
        return speed

    @abstractmethod
    def speed_formula(self) -> int:
        """
        Abstract method returning speed stat calculated for individual pokemon without impact of status effects
        """
        pass
    
    def get_attack_damage(self) -> int:
        """
        Getter method returning current Attack stat calculated for individual Pokemon with impact of status effects
        :return: integer of pokemon's attack damage
        :complexity: O(1)
        """
        ad = self.attack_damage_formula()
        if self.get_status_effect() == StatusEffects.BURN:
            return ad * 0.5
        return ad
    
    @abstractmethod
    def attack_damage_formula(self) -> int:
        """
        Abstract method returning current current attack stat for individual without impact of status effects
        :return: integer of pokemon's attack manage without impaact of staus efects
        :complexity: O(1)
        """
        pass

    @abstractmethod
    def get_defence(self) -> int:
        """
        Abstract getter method returning current Defence stat calculated for individual Pokemon
        :return: integer of pokemon's defence
        :complexity: O(1)
        """
        pass



    # OTHER METHODS ************************************************

    def is_fainted(self) -> bool:
        """
        Method determining whether a pokemon has fainted or not
        :return: True if pokemon has fainted, False if it hasn't
        :complexity: O(1)
        """
        return self.hp <= 0

    def lose_hp(self, lost_hp: int) -> None:
        """
        Lose hp equal to amount passed as arg. Subtract this amount from current HP (stored in hp)
        and set as current HP
        :pre: hp to lose must be non negative integer
        :param: integer representing the value of hp for the pokemon to lose
        :return: None
        :complexity: O(1)
        """
        if not isinstance(lost_hp, int) or lost_hp < 0:
            raise ValueError("Lost hp must be non-negative integer")
        self.hp -= lost_hp

    def heal(self) -> None:
        """
        Restores current HP to full and removes any status effects
        :return: None
        :complexity: O(1)
        """
        self.hp = self.max_hp
        self.status_effect = None

    @abstractmethod
    def defend(self, damage: int) -> None:
        """
        Abstract method that calculates damage mitigation/damage to take depending on
        individual Pokemon's Defence Calculation attribute. Calls lose_hp to reflect
        damage amount onto Pokemon's health.
        :pre: damage must be non negative integer
        :param: integer representing the value of the attack from the other pokemon
        :return: None
        :complexity: O(1)
        """
        pass

    def attack(self, other: PokemonBase) -> None:
        """
        Attack handler that takes another Pokemon as arg and checks if attacking 
        Pokemon is capable of attacking, applying relevant (changes) due to status
        effects. Calculates effective attack amount based on attack stat and types
        of the Pokemon, and applies defending Pokemon's defence calc to this amount.
        Then takes any relevant damage due to status effects and has chance of inflicting
        own status effect onto defending Pokemon
        :pre: other must be a Pokemon of PokemonBase class
        :param: a PokemonBase that represents the other pokemon to attack
        :return: None
        :complexity: O(1)
        """
        if not isinstance(other, PokemonBase):
            raise ValueError("Pokemon to attack must be an instance of PokemonBase class")
        # >>> Step 1: Status effects on attack damage / redirecting attacks
        if self.get_status_effect() == StatusEffects.SLEEP:
            return
        elif self.get_status_effect() == StatusEffects.CONFUSE:
            if(RandomGen.random_chance(0.5)): # 50% of attacking self
                other = self
        # >>> Step 2: Do the attack
        base_attack = self.get_attack_damage()
        multipler = self.get_type().type_multiplier(other.get_type())
        effective_attack = base_attack * multipler
        other.defend(int(effective_attack))
        # >>> Step 3: Losing hp to status effects
        if self.get_status_effect() is not None:
            self.lose_hp(self.get_status_effect().get_effect_damage())
        # >>> Step 4: Possibly applying status effects
        if(RandomGen.random_chance(0.2)): # 20% of inflicting status effect
            other.status_effect = self.get_type_effect()

    
    
    
    # LEVEL UP AND EVOLUTION ************************************************

    def should_evolve(self) -> bool:
        """
        Check if pokemon has met level requirement to evolve
        :return: boolean expression depending on whether the pokemon has met the requirements
        :complexity: O(1)
        """
        return self.level >= self.get_initial_evolved_version().get_level()

    @abstractmethod
    def can_evolve(self) -> bool:
        """
        Returns whether an evolved version of the pokemon exists
        :return: True if Base pokemon, False for evolved pokemon
        :complexity: O(1)
        """
        pass

    @abstractmethod
    def get_initial_evolved_version(self) -> PokemonBase: 
        """
        Retrieves the base evolved pokemon
        :raises ValueError: if the pokemon is fully evolved
        :return: a pokemon base of the evolved version
        :complexity: O(1)
        """
        pass

    def update_hp(self) -> None:
        """
        Default method to be called when attributes affecting hp change i.e. evolution/level
        Scales max HP by calling get_max_hp(), and calculates HP lost prior to HP modification, 
        updating current HP by subtracting from new max HP.
        :pre: max_hp and hp must be defined
        :return: None
        :complexity: O(1)
        """
        previous_max_hp = self.max_hp  
        previous_hp = self.hp          
        self.max_hp = self.get_max_hp()
        self.hp = self.max_hp - (previous_max_hp - previous_hp)

    
    def get_evolved_version(self) -> PokemonBase:
        """
        Take instance of evolved Pokemon and passes Pre-Evolved Pokemon's necessary attributes onto it
        :return: PokemonBase of the evolved version
        :complexity: O(1)
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
        :return: None
        :complexity: O(1)
        """
        self.level += 1
        self.update_hp()
    