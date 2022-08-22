from __future__ import annotations

"""
"""
__author__ = "Scaffold by Jackson Goerner, Code by ______________"

class PokemonBase:

    def __init__(self, hp: int, poke_type) -> None:
        raise NotImplementedError()

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

    def defend(self, damage: int) -> None:
        raise NotImplementedError()

    def attack(self, other: PokemonBase):
        raise NotImplementedError()
        # Step 1: Status effects on attack damage / redirecting attacks
        # Step 2: Do the attack
        # Step 3: Losing hp to status effects
        # Step 4: Possibly applying status effects

    def get_poke_name(self) -> str:
        raise NotImplementedError()

    def __str__(self) -> str:
        raise NotImplementedError()

    def should_evolve(self) -> bool:
        raise NotImplementedError()

    def can_evolve(self) -> bool:
        raise NotImplementedError()

    def get_evolved_version(self) -> PokemonBase:
        raise NotImplementedError()
