from __future__ import annotations
from abc import abstractmethod, ABC
from contextlib import AbstractAsyncContextManager
from typing_extensions import Self
from random_gen import RandomGen

from enum import Enum, auto

"""

"""
__author__ = "Scaffold by Jackson Goerner, Code by ______________"




# class StatusEffects:
#     def __init__(self, type,)

#     def get_status


#     """
#     List of valid status effects with assigned values representing each effect's damage (where exists).
#     """
#     BURN = 1
#     POISON = 3
#     PARALYSIS = None
#     SLEEP = None
#     CONFUSION = 4
STATUS_EFFECTS = ["BURN", "POISON", "PARALYSIS", "SLEEP", "CONFUSION"]
STATUS_DAMAGE = [1, 3, 0, 0, 0]


class PokeType(Enum):
    """
    Assigns corresponding status effect and an index for each type to be referenced to calculate type_multiplier value, and type_effectiveness values in a list
    """
    
    FIRE =      (0,      [1,     2,      0.5,    1,      1])
    GRASS =     (1, [0.5,   1,      2,      1,      1])
    WATER =     (2, [2,     0.5,    1,      1,      1])
    GHOST =     (3,     [1.25,  1.25,   1.25,   2,      0])
    NORMAL =    (4,  [1.25,  1.25,   1.25,   0,      1])
    
    def __init__(self, type_index: int, type_effectiveness: list):
        self.type_index = type_index
        self.type_status_effect = STATUS_EFFECTS[type_index]
        self.status_effect_damage = STATUS_DAMAGE[type_index]
        self.type_effectiveness = type_effectiveness

    def type_multiplier(self, defend_poketype: PokeType):
        """
        Poketype is opponent poketype arg. returns effective multiplier against opponent 
        """
        multiplier = self.type_effectiveness[defend_poketype.type_index]
    
        return multiplier



class PokemonBase(ABC):

    def __init__(self, hp: int, poke_type: PokeType) -> None:
        ###TODO MAKE USER FACING: HP and POKE_TYPE ###
        self.name = self.get_name() #Ensures Pokemon Name is defined.
        self.poke_type = poke_type
        self.level = self.get_level()
        ### Deleted level - make abstract to provide base level for individual pokemon- return accurate level on initialisation###
        self.status_effect = None
        self.max_hp = self.get_max_hp()
        self.hp = self.get_max_hp()
        self.attack_damage = self.get_attack_damage()
        self.defence = self.get_defence()
        self.speed = self.get_speed


    def __str__(self) -> str:
        return f"LV. {self.get_level()} {self.get_name()}: {self.hp} HP"

    # GETTERS FOR 'STATIC' ATTRIBUTES ************************************************
    @abstractmethod
    def get_name(self) -> str:
        pass  
    
    def get_type(self) -> PokeType:
        return self.poke_type
    
    @abstractmethod
    def get_level(self) -> int:
        pass #Ensures classes include base level.

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

    def get_speed(self) -> int:
        """
        Getter method returning current Speed stat calculated for individual Pokemon after impact of status effects
        """
        speed = self.speed_formula()
        if self.status_effect == STATUS_EFFECTS[2]:
            speed = int(speed * 0.5)
        return speed

    @abstractmethod
    def speed_formula(self) -> int:
        """
        Abstract method returning speed stat calculated for individual pokemon without impact of status effects"""
        pass

    
    def get_attack_damage(self) -> int:
        ad = self.attack_damage_formula()
        if self.status_effect == STATUS_EFFECTS[0]:
            return ad * 0.5
        return ad
    
    @abstractmethod
    def attack_damage_formula(self):
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
        if self.status_effect == STATUS_EFFECTS[3]:
            return
        elif self.status_effect == STATUS_EFFECTS[4]:
            if(RandomGen.random_chance(0.5)): # 50% of attacking self
                other = self
        # >>> Step 2: Do the attack
        base_attack = self.get_attack_damage()
        multipler = self.poke_type.type_multiplier(other.poke_type)
        effective_attack = base_attack * multipler
        # print(f"Effective attack of {self} is: {effective_attack}")

        print(f"attack is {int(effective_attack)} \n {self}, {self.get_status_effect()}")
        other.defend(int(effective_attack))
        # >>> Step 3: Losing hp to status effects
        if self.get_status_effect() is not None:
            self.lose_hp(other.poke_type.status_effect_damage)
        # >>> Step 4: Possibly applying status effects
        if(RandomGen.random_chance(0.2)): # 20% of inflicting status effect
            other.status_effect = self.poke_type.type_status_effect

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