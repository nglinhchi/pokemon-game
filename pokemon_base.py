from __future__ import annotations

"""
"""
__author__ = "Scaffold by Jackson Goerner, Code by ______________"

<<<<<<< Updated upstream
class PokemonBase:

    def __init__(self, hp: int, poke_type) -> None:
        raise NotImplementedError()
<<<<<<< Updated upstream

    def is_fainted(self) -> bool:
        raise NotImplementedError()

    def level_up(self) -> None:
        raise NotImplementedError()

    def get_speed(self) -> int:
        raise NotImplementedError()

    def get_attack_damage(self) -> int:
        raise NotImplementedError()

    def get_defence(self) -> int:
        raise NotImplementedError()

    def lose_hp(self, lost_hp: int) -> None:
        raise NotImplementedError()
=======
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

=======
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
    TYPE_EFFECTIVENESS = [[1,     2,      0.5,    1,      1],
                        [0.5,   1,      2,      1,      1],
                        [2,     0.5,    1,      1,      1],
                        [1.25,  1.25,   1.25,   2,      0],
                        [1.25,  1.25,   1.25,   0,      1]]
    """
    Assigns corresponding status effect and an index for each type to be used with TYPE_EFFECTIVENESS table.
    """
    FIRE = (0, StatusEffect.BURN)
    GRASS = (1, StatusEffect.POISON)
    WATER = (2, StatusEffect.PARALYSIS)
    GHOST = (3, StatusEffect.SLEEP)
    NORMAL = (4, StatusEffect.CONFUSION)
    def __init__(self, type_index: int, status_effect: StatusEffect):
        self.type_index = type_index
        self.type_status_effect = status_effect

class PokemonBase(ABC):

    

    def __init__(self, hp: int, poke_type: PokeType) -> None:

        self.base_hp = hp
        self.max_hp = self.hp_scaler()
        self.current_hp= self.get_hp()
        self.poke_type = poke_type
        self.name = self.__class__.__name__
        self.status_effect = None
        self.level = 1
        self.attack_damage = None
        self.speed = None
        self.defence = None
>>>>>>> Stashed changes
        self.evolve = False

        # raise NotImplementedError()

    def is_fainted(self) -> bool:
        raise NotImplementedError()
        return self.hp <= 0
        # raise NotImplementedError()

    def level_up(self) -> None:
<<<<<<< Updated upstream
        raise NotImplementedError()
        self.level += 1
        # raise NotImplementedError()
=======
        #TODO call methods to increase hp, atk, defence etc.
        self.level += 1
        self.current_hp = self.get_hp()
        
        
        
    
    @abstractmethod
    def hp_scaler(self) -> int:
        pass
    
    
    def get_hp(self) -> int:
        """
        Return current hp
        """
        if self.current_hp != self.max_hp:
            diff = self.max_hp - self.current_hp
            self.max_hp = self.hp_scaler()
            return self.max_hp - diff
        else: 
            self.current_hp = self.max_hp   #else condition on initiation
            return self.current_hp
>>>>>>> Stashed changes

    @abstractmethod
    def get_speed(self) -> int:
<<<<<<< Updated upstream
        raise NotImplementedError()
        return self.speed
        # raise NotImplementedError()

    def get_attack_damage(self) -> int:
        raise NotImplementedError()
        return self.attack
        # raise NotImplementedError()
=======
        #TODO implement formula in child classes
        pass
    
    @abstractmethod
    def get_attack_damage(self) -> int:
        #TODO implement formula in child classes
        pass
>>>>>>> Stashed changes

    @abstractmethod
    def get_defence(self) -> int:
<<<<<<< Updated upstream
        raise NotImplementedError()
=======
        #TODO implement formula in child classes
>>>>>>> Stashed changes
        return self.defence
        # raise NotImplementedError()

    def lose_hp(self, lost_hp: int) -> None:
<<<<<<< Updated upstream
        raise NotImplementedError()
        self.hp -= lost_hp
        # raise NotImplementedError()
>>>>>>> Stashed changes
=======
        self.current_hp -= lost_hp
>>>>>>> Stashed changes

    def defend(self, damage: int) -> None:
        raise NotImplementedError()
<<<<<<< Updated upstream

    def attack(self, other: PokemonBase):
        raise NotImplementedError()
        # Step 1: Status effects on attack damage / redirecting attacks
        # Step 2: Do the attack
=======
        pass
        # raise NotImplementedError()

    def attack(self, other: PokemonBase):
        raise NotImplementedError()
        # raise NotImplementedError()

        # Step 1: Status effects on attack damage / redirecting attacks
        # Step 2: Do the attack
        if self.status_effect == "sleep":
            return # TODO stop the attack
<<<<<<< Updated upstream
        elif self.status_effect == "confusion":
            if(RandomGen.random_chance(0.5)): # True 33% of the time, False 67% of the time.
=======
        elif self.status_effect == StatusEffect.CONFUSION:
            if(RandomGen.random_chance(0.5)): # 50% chance of hitting self
>>>>>>> Stashed changes
                other = self
        elif self.status_effect == "paralysis":
            self.speed = self.speed // 2
                
        # Step 2: Do the attack TODO
        
        # calculate attack
<<<<<<< Updated upstream
        # check other.type
        # other.poke_type self.get_attack_damage
        
        # if (self.speed > other.speed):
        #     pass #  self attacks
        # elif (self.speed == other.speed):
        #     pass #  team 1 attacks
=======
        base_ad = self.get_attack_damage() 
        multipler = PokeType.TYPE_EFFECTIVENESS[self.poke_type.type_index][other.poke_type.type_index]
        effective_ad = int(base_ad * multipler)
>>>>>>> Stashed changes


>>>>>>> Stashed changes
        # Step 3: Losing hp to status effects
        # Step 4: Possibly applying status effects
<<<<<<< Updated upstream

    def get_poke_name(self) -> str:
        raise NotImplementedError()
<<<<<<< Updated upstream

    def __str__(self) -> str:
        raise NotImplementedError()

    def should_evolve(self) -> bool:
        raise NotImplementedError()

    def can_evolve(self) -> bool:
=======
        return self.name
        # raise NotImplementedError()
=======
        if(RandomGen.random_chance(0.2)): # 20% chance of applying status effect    
            other.status_effect = self.poke_type.type_status_effect

    def get_poke_name(self) -> str:
        return str(self.name)  #name of instance class
>>>>>>> Stashed changes

    def __str__(self) -> str:
        raise NotImplementedError()
        return print(f"LV.{self.level} {self.name}: {self.hp} HP")
        # raise NotImplementedError()

    def should_evolve(self) -> bool:
<<<<<<< Updated upstream
        raise NotImplementedError()
        return (self.can_evolve() and not self.is_fainted() and self.level >= 16) # TODO level depends upon its class?
        # raise NotImplementedError()
=======
        if not can_evolve(self):
            pass
            #TODO raise error this pokemon cannot evolve
        else:
            return (self.can_evolve() and not self.is_fainted() and (self.level == self.get_evolved_version().level))
>>>>>>> Stashed changes

    def can_evolve(self) -> bool:
    def can_evolve(self) -> bool: # TODO use ADT to check if it's a member of the evolvable list
>>>>>>> Stashed changes
        raise NotImplementedError()

    def get_evolved_version(self) -> PokemonBase:
<<<<<<< Updated upstream
=======
        pass

    @abstractmethod
    def calculate_attack(self):
        pass
    def heal(self):
        self.current_hp+=4
>>>>>>> Stashed changes
