from __future__ import annotations
from abc import abstractmethod, ABC
from typing_extensions import Self
from random_gen import RandomGen

"""
"""
__author__ = "Scaffold by Jackson Goerner, Code by ______________"

class PokemonBase(ABC):

    def __init__(self, hp: int, poke_type) -> None:
        self.name = ""
        self.hp = hp
        self.poke_type = poke_type
        self.status_effect = None

        # if self.poke_type == "fire":
        #     self.status_effect = "burn"
        # elif self.poke_type == "grass":
        #     self.status_effect = "poison"
        # elif self.status_effect == "water":
        #     self.status_effect = "paralysis"
        # elif self.status_effect == "ghost":
        #     self.status_effect = "sleep"
        # elif self.status_effect == "normal":
        #     self.status_effect = "confusion"
        
        self.base_level = 1
        self.level = self.base_level

        self.base_attack = 0
        self.attack = self.base_attack

        self.base_speed = 0
        self.speed = self.base_speed

        self.defence = 0

        self.evolve = False

        # raise NotImplementedError()

    def is_fainted(self) -> bool:
        return self.hp <= 0
        # raise NotImplementedError()

    def level_up(self) -> None:
        self.level += 1
        # raise NotImplementedError()

    def get_speed(self) -> int:
        return self.speed
        # raise NotImplementedError()

    def get_attack_damage(self) -> int:
        return self.attack
        # raise NotImplementedError()

    def get_defence(self) -> int:
        return self.defence
        # raise NotImplementedError()

    def lose_hp(self, lost_hp: int) -> None:
        self.hp -= lost_hp
        # raise NotImplementedError()

    @abstractmethod
    def defend(self, damage: int) -> None:
        pass
        # raise NotImplementedError()

    def attack(self, other: PokemonBase):
        # raise NotImplementedError()

        # Step 1: Status effects on attack damage / redirecting attacks
        if self.status_effect == "sleep":
            return # TODO stop the attack
        elif self.status_effect == "confusion":
            if(RandomGen.random_chance(0.5)): # True 33% of the time, False 67% of the time.
                other = self
        elif self.status_effect == "paralysis":
            self.speed = self.speed // 2
                
        # Step 2: Do the attack TODO
        
        # calculate attack
        # check other.type
        # other.poke_type self.get_attack_damage
        
        # if (self.speed > other.speed):
        #     pass #  self attacks
        # elif (self.speed == other.speed):
        #     pass #  team 1 attacks


        # Step 3: Losing hp to status effects


        # Step 4: Possibly applying status effects

    def get_poke_name(self) -> str:
        return self.name
        # raise NotImplementedError()

    def __str__(self) -> str:
        return print(f"LV.{self.level} {self.name}: {self.hp} HP")
        # raise NotImplementedError()

    def should_evolve(self) -> bool:
        return (self.can_evolve() and not self.is_fainted() and self.level >= 16) # TODO level depends upon its class?
        # raise NotImplementedError()

    def can_evolve(self) -> bool: # TODO use ADT to check if it's a member of the evolvable list
        raise NotImplementedError()

    def get_evolved_version(self) -> PokemonBase:
        raise NotImplementedError()
