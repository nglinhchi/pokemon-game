from inspect import Attribute
from multiprocessing.sharedctypes import Value
from pokemon_base import PokemonBase, PokeType

"""
Implements the different pokemons (both base and evolved) and their characteristics
"""
__author__ = "Scaffold by Jackson Goerner, Code by Chloe Nguyen | Joong Do Chiang"

# *******************************************


# CHARMANDER >> CHARIZARD
class Charizard(PokemonBase): 
    NAME = "Charizard"
    BASE_LEVEL = 3
    POKE_NO = 2 
    def __init__(self):
        """
        Initialises a Charizard instance
        """
        PokemonBase.__init__(self, 12, PokeType.FIRE)
    
    def get_name(self) -> str:
        return __class__.NAME  #Ensures name is set for pokemon

    def get_level(self) -> int:
        try:
            return self.level
        except AttributeError: #when first initialising
            return __class__.BASE_LEVEL #Ensures classes include base level.

    def get_max_hp(self) -> int:
        """
        Method containing HP scaling formula for individual pokemon. Calculates
        this max HP using base_hp and returns.
        :pre: base_hp must be defined
        :return: integer of pokemon's max hp
        :complexity: O(1)
        """
        return self.base_hp + 1 * self.level

    def attack_damage_formula(self) -> int:
        """
        Getter method returning current Attack stat calculated for individual Pokemon
        :return: integer of pokemon's attack damage
        :complexity: O(1)
        """
        return 10 + 2 * self.level

    def speed_formula(self) -> int:
        """
        Getter method returning current Speed stat calculated for individual Pokemon
        :return: integer of pokemon's speed
        :complexity: O(1)
        """
        return 9 + 1 * self.level

    def get_defence(self) -> int:
        """
        Getter method returning current Defence stat calculated for individual Pokemon
        :return: integer of pokemon's defence
        :complexity: O(1)
        """
        return 4
    
    def can_evolve(self) -> bool:
        """
        Returns whether an evolved version of the pokemon exists
        :return: True if Base pokemon, False for evolved pokemon
        :complexity: O(1)
        """
        return False

    def get_initial_evolved_version(self) -> PokemonBase:
        """
        Retrieves the base evolved pokemon
        :raises ValueError: if the pokemon is fully evolved
        :return: a pokemon base of the evolved version
        :complexity: O(1)
        """
        raise ValueError(f"{self.get_name()} does not have evolution")

    def defend(self, damage: int) -> None:
        """
        Method that calculates damage mitigation/damage to take depending on
        individual Pokemon's Defence Calculation attribute. Calls lose_hp to reflect
        damage amount onto Pokemon's health.
        :param: integer representing the value of the attack from the other pokemon
        :return: None
        :complexity: O(1)
        """
        if damage > self.get_defence():
            self.lose_hp(2*damage)
        else:
            self.lose_hp(damage)


# CHARMANDER
class Charmander(PokemonBase):
    NAME = "Charmander"
    BASE_LEVEL = 1
    POKE_NO = 1
    def __init__(self):
        """
        Initialises a Charmander instance
        """
        PokemonBase.__init__(self, 8, PokeType.FIRE)
    
    def get_name(self) -> str:
        return __class__.NAME  #Ensures name is set for pokemon

    def get_level(self) -> int:
        try:
            return self.level
        except AttributeError: #when first initialising
            return __class__.BASE_LEVEL #Ensures classes include base level.

    def get_max_hp(self) -> int:
        """
        Method containing HP scaling formula for individual pokemon. Calculates
        this max HP using base_hp and returns.
        :pre: base_hp must be defined
        :return: integer of pokemon's max hp
        :complexity: O(1)
        """
        return self.base_hp + 1 * self.level

    def attack_damage_formula(self) -> int:
        """
        Getter method returning current Attack stat calculated for individual Pokemon
        :return: integer of pokemon's attack damage
        :complexity: O(1)
        """
        return 6 + 1 * self.level

    def speed_formula(self) -> int:
        """
        Getter method returning current Speed stat calculated for individual Pokemon
        :return: integer of pokemon's speed
        :complexity: O(1)
        """
        return 7 + 1 * self.level

    def get_defence(self) -> int:
        """
        Getter method returning current Defence stat calculated for individual Pokemon
        :return: integer of pokemon's defence
        :complexity: O(1)
        """
        return 4
    
    def can_evolve(self) -> bool:
        """
        Returns whether an evolved version of the pokemon exists
        :return: True if Base pokemon, False for evolved pokemon
        :complexity: O(1)
        """
        return True

    def get_initial_evolved_version(self) -> PokemonBase:
        """
        Retrieves the base evolved pokemon
        :raises ValueError: if the pokemon is fully evolved
        :return: a pokemon base of the evolved version
        :complexity: O(1)
        """
        return Charizard()

    def defend(self, damage: int) -> None:
        """
        Method that calculates damage mitigation/damage to take depending on
        individual Pokemon's Defence Calculation attribute. Calls lose_hp to reflect
        damage amount onto Pokemon's health.
        :param: integer representing the value of the attack from the other pokemon
        :return: None
        :complexity: O(1)
        """
        if damage > self.get_defence():
            self.lose_hp(damage)

        else:
            self.lose_hp(damage//2)



# *******************************************


# BULBASAUR >> VENUSAUR
class Venusaur(PokemonBase):
    NAME = "Venusaur"
    BASE_LEVEL = 2
    POKE_NO = 4
    def __init__(self):
        """
        Initialises a Venusaur instance
        """
        PokemonBase.__init__(self, 20, PokeType.GRASS)

    def get_name(self) -> str:
        return __class__.NAME  #Ensures name is set for pokemon

    def get_level(self) -> int:
        try:
            return self.level
        except AttributeError: #when first initialising
            return __class__.BASE_LEVEL #Ensures classes include base level.
    
    def get_max_hp(self) -> int:
        """
        Method containing HP scaling formula for individual pokemon. Calculates
        this max HP using base_hp and returns.
        :pre: base_hp must be defined
        :return: integer of pokemon's max hp
        :complexity: O(1)
        """
        return self.base_hp + self.level//2

    def attack_damage_formula(self) -> int:
        """
        Getter method returning current Attack stat calculated for individual Pokemon
        :return: integer of pokemon's attack damage
        :complexity: O(1)
        """
        return 5

    def speed_formula(self) -> int:
        """
        Getter method returning current Speed stat calculated for individual Pokemon
        :return: integer of pokemon's speed
        :complexity: O(1)
        """
        return 3 + self.level//2

    def get_defence(self) -> int:
        """
        Getter method returning current Defence stat calculated for individual Pokemon
        :return: integer of pokemon's defence
        :complexity: O(1)
        """
        return 10
    
    def can_evolve(self) -> bool:
        """
        Returns whether an evolved version of the pokemon exists
        :return: True if Base pokemon, False for evolved pokemon
        :complexity: O(1)
        """
        return False
    
    def get_initial_evolved_version(self) -> PokemonBase:
        """
        Retrieves the base evolved pokemon
        :raises ValueError: if the pokemon is fully evolved
        :return: a pokemon base of the evolved version
        :complexity: O(1)
        """
        raise ValueError(f"{self.get_name()} does not have evolution")

    def defend(self, damage: int) -> None:
        """
        Method that calculates damage mitigation/damage to take depending on
        individual Pokemon's Defence Calculation attribute. Calls lose_hp to reflect
        damage amount onto Pokemon's health.
        :param: integer representing the value of the attack from the other pokemon
        :return: None
        :complexity: O(1)
        """
        if damage > (self.get_defence() + 5):
            self.lose_hp(damage)
        else:
            self.lose_hp(damage//2)


# BULBASAUR
class Bulbasaur(PokemonBase):
    NAME = "Bulbasaur"
    BASE_LEVEL = 1
    POKE_NO = 3
    def __init__(self):
        """
        Initialises a Bulbasaur instance
        """
        PokemonBase.__init__(self, 12, PokeType.GRASS)
    
    def get_name(self) -> str:
        return __class__.NAME  #Ensures name is set for pokemon

    def get_level(self) -> int:
        try:
            return self.level
        except AttributeError: #when first initialising
            return __class__.BASE_LEVEL #Ensures classes include base level.

    def get_max_hp(self) -> int:
        """
        Method containing HP scaling formula for individual pokemon. Calculates
        this max HP using base_hp and returns.
        :pre: base_hp must be defined
        :return: integer of pokemon's max hp
        :complexity: O(1)
        """
        return self.base_hp + 1 * self.level

    def attack_damage_formula(self) -> int:
        """
        Getter method returning current Attack stat calculated for individual Pokemon
        :return: integer of pokemon's attack damage
        :complexity: O(1)
        """
        return 5

    def speed_formula(self) -> int:
        """
        Getter method returning current Speed stat calculated for individual Pokemon
        :return: integer of pokemon's speed
        :complexity: O(1)
        """
        return 7 + self.level//2

    def get_defence(self) -> int:
        """
        Getter method returning current Defence stat calculated for individual Pokemon
        :return: integer of pokemon's defence
        :complexity: O(1)
        """
        return 5
    
    def can_evolve(self) -> bool:
        """
        Returns whether an evolved version of the pokemon exists
        :return: True if Base pokemon, False for evolved pokemon
        :complexity: O(1)
        """
        return True
    
    def get_initial_evolved_version(self) -> PokemonBase:
        """
        Retrieves the base evolved pokemon
        :raises ValueError: if the pokemon is fully evolved
        :return: a pokemon base of the evolved version
        :complexity: O(1)
        """
        return Venusaur()

    def defend(self, damage: int) -> None:
        """
        Method that calculates damage mitigation/damage to take depending on
        individual Pokemon's Defence Calculation attribute. Calls lose_hp to reflect
        damage amount onto Pokemon's health.
        :param: integer representing the value of the attack from the other pokemon
        :return: None
        :complexity: O(1)
        """
        if damage > (self.get_defence() + 5):
            self.lose_hp(damage)
        else:
            self.lose_hp(damage//2)    


# *******************************************


# SQUIRTLE >> BLASTOISE
class Blastoise(PokemonBase):
    NAME = "Blastoise"
    BASE_LEVEL = 3
    POKE_NO = 6
    def __init__(self):
        """
        Initialises a Blastoise instance
        """
        PokemonBase.__init__(self, 15, PokeType.WATER)
        self.level = 3 # base level
    
    def get_name(self) -> str:
        return __class__.NAME  #Ensures name is set for pokemon

    def get_level(self) -> int:
        try:
            return self.level
        except AttributeError: #when first initialising
            return __class__.BASE_LEVEL #Ensures classes include base level.

    def get_max_hp(self) -> int:
        """
        Method containing HP scaling formula for individual pokemon. Calculates
        this max HP using base_hp and returns.
        :pre: base_hp must be defined
        :return: integer of pokemon's max hp
        :complexity: O(1)
        """
        return self.base_hp + 2 * self.level

    def attack_damage_formula(self) -> int:
        """
        Getter method returning current Attack stat calculated for individual Pokemon
        :return: integer of pokemon's attack damage
        :complexity: O(1)
        """
        return 8 + self.level // 2

    def speed_formula(self) -> int:
        """
        Getter method returning current Speed stat calculated for individual Pokemon
        :return: integer of pokemon's speed
        :complexity: O(1)
        """
        return 10

    def get_defence(self) -> int:
        """
        Getter method returning current Defence stat calculated for individual Pokemon
        :return: integer of pokemon's defence
        :complexity: O(1)
        """
        return 8 + 1 * self.level
    
    def can_evolve(self) -> bool:
        """
        Returns whether an evolved version of the pokemon exists
        :return: True if Base pokemon, False for evolved pokemon
        :complexity: O(1)
        """
        return False

    def get_initial_evolved_version(self) -> PokemonBase:
        """
        Retrieves the base evolved pokemon
        :raises ValueError: if the pokemon is fully evolved
        :return: a pokemon base of the evolved version
        :complexity: O(1)
        """
        raise ValueError(f"{self.get_name()} does not have evolution")
        
    def defend(self, damage: int) -> None:
        """
        Method that calculates damage mitigation/damage to take depending on
        individual Pokemon's Defence Calculation attribute. Calls lose_hp to reflect
        damage amount onto Pokemon's health.
        :param: integer representing the value of the attack from the other pokemon
        :return: None
        :complexity: O(1)
        """
        if damage > (self.get_defence() * 2):
            self.lose_hp(damage)
        else:
            self.lose_hp(damage//2)


# SQUIRTLE
class Squirtle(PokemonBase):
    NAME = "Squirtle"
    BASE_LEVEL = 1
    POKE_NO = 5
    def __init__(self):
        """
        Initialises a Squirtle instance
        """
        PokemonBase.__init__(self, 9, PokeType.WATER)
    
    def get_name(self) -> str:
        return __class__.NAME  #Ensures name is set for pokemon

    def get_level(self) -> int:
        try:
            return self.level
        except AttributeError: #when first initialising
            return __class__.BASE_LEVEL #Ensures classes include base level.
            
    def get_max_hp(self) -> int:
        """
        Method containing HP scaling formula for individual pokemon. Calculates
        this max HP using base_hp and returns.
        :pre: base_hp must be defined
        :return: integer of pokemon's max hp
        :complexity: O(1)
        """
        return self.base_hp + 2 * self.level

    def attack_damage_formula(self) -> int:
        """
        Getter method returning current Attack stat calculated for individual Pokemon
        :return: integer of pokemon's attack damage
        :complexity: O(1)
        """
        return 4 + self.level//2

    def speed_formula(self) -> int:
        """
        Getter method returning current Speed stat calculated for individual Pokemon
        :return: integer of pokemon's speed
        :complexity: O(1)
        """
        return 7

    def get_defence(self) -> int:
        """
        Getter method returning current Defence stat calculated for individual Pokemon
        :return: integer of pokemon's defence
        :complexity: O(1)
        """
        return 6 + self.level
    
    def can_evolve(self) -> bool:
        """
        Returns whether an evolved version of the pokemon exists
        :return: True if Base pokemon, False for evolved pokemon
        :complexity: O(1)
        """
        return True

    def get_initial_evolved_version(self) -> PokemonBase:
        """
        Retrieves the base evolved pokemon
        :raises ValueError: if the pokemon is fully evolved
        :return: a pokemon base of the evolved version
        :complexity: O(1)
        """
        return Blastoise()

    def defend(self, damage: int) -> None:
        """
        Method that calculates damage mitigation/damage to take depending on
        individual Pokemon's Defence Calculation attribute. Calls lose_hp to reflect
        damage amount onto Pokemon's health.
        :param: integer representing the value of the attack from the other pokemon
        :return: None
        :complexity: O(1)
        """
        if damage > (self.get_defence() * 2):
            self.lose_hp(damage)
        else:
            self.lose_hp(damage//2)


# *******************************************


# GASTLY >> HAUNTER >> GENGAR
class Gengar(PokemonBase):
    NAME = "Gengar"
    BASE_LEVEL = 3
    POKE_NO = 9
    def __init__(self):
        """
        Initialises a Gengar instance
        """
        PokemonBase.__init__(self, 12, PokeType.GHOST)
        self.level = 3 # base level

    def get_max_hp(self) -> int:
        """
        Method containing HP scaling formula for individual pokemon. Calculates
        this max HP using base_hp and returns.
        :pre: base_hp must be defined
        :return: integer of pokemon's max hp
        :complexity: O(1)
        """
        return self.base_hp + self.level//2

    def attack_damage_formula(self) -> int:
        """
        Getter method returning current Attack stat calculated for individual Pokemon
        :return: integer of pokemon's attack damage
        :complexity: O(1)
        """
        return 18

    def speed_formula(self) -> int:
        """
        Getter method returning current Speed stat calculated for individual Pokemon
        :return: integer of pokemon's speed
        :complexity: O(1)
        """
        return 12

    def get_defence(self) -> int:
        """
        Getter method returning current Defence stat calculated for individual Pokemon
        :return: integer of pokemon's defence
        :complexity: O(1)
        """
        return 3
    
    def can_evolve(self) -> bool:
        """
        Returns whether an evolved version of the pokemon exists
        :return: True if Base pokemon, False for evolved pokemon
        :complexity: O(1)
        """
        return False
    
    def get_initial_evolved_version(self) -> PokemonBase:
        """
        Retrieves the base evolved pokemon
        :raises ValueError: if the pokemon is fully evolved
        :return: a pokemon base of the evolved version
        :complexity: O(1)
        """
        raise ValueError(f"{self.get_name()} does not have evolution")
        
    def defend(self, damage: int) -> None:
        """
        Method that calculates damage mitigation/damage to take depending on
        individual Pokemon's Defence Calculation attribute. Calls lose_hp to reflect
        damage amount onto Pokemon's health.
        :param: integer representing the value of the attack from the other pokemon
        :return: None
        :complexity: O(1)
        """
        self.lose_hp(damage)


# GASTLY >> HAUNTER
class Haunter(PokemonBase):
    NAME = "Haunter"
    BASE_LEVEL = 1
    POKE_NO = 8
    def __init__(self):
        """
        Initialises a Haunter instance
        """
        PokemonBase.__init__(self, 9, PokeType.GHOST)
        self.level = 1 # base level
    
    def get_name(self) -> str:
        return __class__.NAME  #Ensures name is set for pokemon

    def get_level(self) -> int:
        try:
            return self.level
        except AttributeError: #when first initialising
            return __class__.BASE_LEVEL #Ensures classes include base level.

    def get_max_hp(self) -> int:
        """
        Method containing HP scaling formula for individual pokemon. Calculates
        this max HP using base_hp and returns.
        :pre: base_hp must be defined
        :return: integer of pokemon's max hp
        :complexity: O(1)
        """
        return self.base_hp + self.level//2

    def attack_damage_formula(self) -> int:
        """
        Getter method returning current Attack stat calculated for individual Pokemon
        :return: integer of pokemon's attack damage
        :complexity: O(1)
        """
        return 8

    def speed_formula(self) -> int:
        """
        Getter method returning current Speed stat calculated for individual Pokemon
        :return: integer of pokemon's speed
        :complexity: O(1)
        """
        return 6

    def get_defence(self) -> int:
        """
        Getter method returning current Defence stat calculated for individual Pokemon
        :return: integer of pokemon's defence
        :complexity: O(1)
        """
        return 6
    
    def can_evolve(self) -> bool:
        """
        Returns whether an evolved version of the pokemon exists
        :return: True if Base pokemon, False for evolved pokemon
        :complexity: O(1)
        """
        return True

    def get_initial_evolved_version(self) -> PokemonBase:
        """
        Retrieves the base evolved pokemon
        :raises ValueError: if the pokemon is fully evolved
        :return: a pokemon base of the evolved version
        :complexity: O(1)
        """
        return Gengar()

    def defend(self, damage: int) -> None:
        """
        Method that calculates damage mitigation/damage to take depending on
        individual Pokemon's Defence Calculation attribute. Calls lose_hp to reflect
        damage amount onto Pokemon's health.
        :param: integer representing the value of the attack from the other pokemon
        :return: None
        :complexity: O(1)
        """
        self.lose_hp(damage)


# GASTLY
class Gastly(PokemonBase):
    NAME = "Gastly"
    BASE_LEVEL = 1
    POKE_NO = 7
    def __init__(self):
        """
        Initialises a Gastly instance
        """
        PokemonBase.__init__(self, 6, PokeType.GHOST)

    def get_name(self) -> str:
        return __class__.NAME  #Ensures name is set for pokemon

    def get_level(self) -> int:
        try:
            return self.level
        except AttributeError: #when first initialising
            return __class__.BASE_LEVEL #Ensures classes include base level.

    def get_max_hp(self) -> int:
        """
        Method containing HP scaling formula for individual pokemon. Calculates
        this max HP using base_hp and returns.
        :pre: base_hp must be defined
        :return: integer of pokemon's max hp
        :complexity: O(1)
        """
        return self.base_hp + self.level//2

    def attack_damage_formula(self) -> int:
        """
        Getter method returning current Attack stat calculated for individual Pokemon
        :return: integer of pokemon's attack damage
        :complexity: O(1)
        """
        return 4

    def speed_formula(self) -> int:
        """
        Getter method returning current Speed stat calculated for individual Pokemon
        :return: integer of pokemon's speed
        :complexity: O(1)
        """
        return 2

    def get_defence(self) -> int:
        """
        Getter method returning current Defence stat calculated for individual Pokemon
        :return: integer of pokemon's defence
        :complexity: O(1)
        """
        return 8
    
    def can_evolve(self) -> bool:
        """
        Returns whether an evolved version of the pokemon exists
        :return: True if Base pokemon, False for evolved pokemon
        :complexity: O(1)
        """
        return True
    
    def get_initial_evolved_version(self) -> PokemonBase:
        """
        Retrieves the base evolved pokemon
        :raises ValueError: if the pokemon is fully evolved
        :return: a pokemon base of the evolved version
        :complexity: O(1)
        """
        return Haunter()

    def defend(self, damage: int) -> None:
        """
        Method that calculates damage mitigation/damage to take depending on
        individual Pokemon's Defence Calculation attribute. Calls lose_hp to reflect
        damage amount onto Pokemon's health.
        :param: integer representing the value of the attack from the other pokemon
        :return: None
        :complexity: O(1)
        """
        self.lose_hp(damage)


# *******************************************


# EEVEE
class Eevee(PokemonBase):
    NAME = "Eevee"
    BASE_LEVEL = 1
    POKE_NO = 10
    def __init__(self):
        """
        Initialises an Eevee instance
        """
        PokemonBase.__init__(self, 10, PokeType.NORMAL)
    
    def get_name(self) -> str:
        return __class__.NAME  #Ensures name is set for pokemon
    
    def get_level(self) -> int:
        try:
            return self.level
        except AttributeError: #when first initialising
            return __class__.BASE_LEVEL #Ensures classes include base level.

    def get_max_hp(self) -> int:
        """
        Method containing HP scaling formula for individual pokemon. Calculates
        this max HP using base_hp and returns.
        :pre: base_hp must be defined
        :return: integer of pokemon's max hp
        :complexity: O(1)
        """
        return self.base_hp

    def attack_damage_formula(self) -> int:
        """
        Getter method returning current Attack stat calculated for individual Pokemon
        :return: integer of pokemon's attack damage
        :complexity: O(1)
        """
        return 6 + self.level

    def speed_formula(self) -> int:
        """
        Getter method returning current Speed stat calculated for individual Pokemon
        :return: integer of pokemon's speed
        :complexity: O(1)
        """
        return 7 + self.level

    def get_defence(self) -> int:
        """
        Getter method returning current Defence stat calculated for individual Pokemon
        :return: integer of pokemon's defence
        :complexity: O(1)
        """
        return 4 + self.level
    
    def can_evolve(self) -> bool:
        """
        Returns whether an evolved version of the pokemon exists
        :return: True if Base pokemon, False for evolved pokemon
        :complexity: O(1)
        """
        return False
    
    def get_initial_evolved_version(self) -> PokemonBase:
        """
        Retrieves the base evolved pokemon
        :raises ValueError: if the pokemon is fully evolved
        :return: a pokemon base of the evolved version
        :complexity: O(1)
        """
        raise ValueError(f"{self.get_name()} does not have evolution")
        
    def defend(self, damage: int) -> None:
        """
        Method that calculates damage mitigation/damage to take depending on
        individual Pokemon's Defence Calculation attribute. Calls lose_hp to reflect
        damage amount onto Pokemon's health.
        :param: integer representing the value of the attack from the other pokemon
        :return: None
        :complexity: O(1)
        """
        if damage >= self.get_defence():
            self.lose_hp(damage)
        else:
            self.lose_hp(0)

# *******************************************


