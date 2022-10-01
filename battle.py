from multiprocessing.connection import Listener
from os import popen
from tkinter import ACTIVE
from pokemon_base import PokemonBase
from random_gen import RandomGen
from poke_team import Action, PokeTeam, Criterion
from print_screen import *
import os, sys

"""
Creates Battle class and implements the methods to handle a battle between 2 teams
"""
__author__ = "Scaffold by Jackson Goerner, Code by Chloe Nguyen | Joong Do Chiang"

class HiddenPrints:
    
    def __enter__(self):
        self._original_stdout = sys.stdout
        sys.stdout = open(os.devnull, 'w')

    def __exit__(self, exc_type, exc_val, exc_tb):
        sys.stdout.close()
        sys.stdout = self._original_stdout

class Battle:
    
    def __init__(self, verbosity=0) -> None:
        """
        Initialises a battle instance
        """
        self.verbosity = verbosity

    def battle(self, team1: PokeTeam, team2: PokeTeam) -> int:
        """
        Performs the battle between two teams including choosing the action to be taken,
        retrieving/ returning pokemon and taking damage
        :param arg1: PokeTeam instance representing the current state of team 1
        :param arg2: PokeTeam instance representing the current state of team 2
        :return: an integer (either 0,1 or 2) represnting a draw, team 1 winning and team 2 winning respectively
        :complexity: best O(n), worst O(nlogn)
        """
        # with HiddenPrints():
        pokemon1 = None
        pokemon2 = None
        while True:
            
            if pokemon1 == None and team1.team.is_empty() and pokemon2 == None and team2.team.is_empty():
                return 0
            elif pokemon1 == None and team1.team.is_empty():
                team2.return_pokemon(pokemon2)
                return 2
            elif pokemon2 == None and team2.team.is_empty():
                # assert pokemon1 != None, f"{pokemon1}, {team1}, {pokemon2}, {team2}"``
                team1.return_pokemon(pokemon1)
                return 1
            else: # both teams still have pokemon -> battle
                if pokemon1 == None:
                    pokemon1 = team1.retrieve_pokemon()
                if pokemon2 == None: 
                    pokemon2 = team2.retrieve_pokemon()
                

                action1 = team1.choose_battle_option(pokemon1, pokemon2)
                action2 = team2.choose_battle_option(pokemon2, pokemon1)
                # PRE-ATTACKS -------------------------------------------------------------------

                if action1 == Action.SWAP:
                    team1.return_pokemon(pokemon1)
                    pokemon1 = team1.retrieve_pokemon()

                if action2 == Action.SWAP:
                    team2.return_pokemon(pokemon2)
                    pokemon2 = team2.retrieve_pokemon()

                if action1 == Action.SPECIAL:
                    team1.return_pokemon(pokemon1) #Should be implemented inside special
                    team1.special()
                    pokemon1 = team1.retrieve_pokemon()

                if action2 == Action.SPECIAL:
                    team2.return_pokemon(pokemon2)
                    team2.special()
                    pokemon2 = team2.retrieve_pokemon()

                if action1 == Action.HEAL:
                    if team1.heal_count < 0:
                        return 2
                    else:
                        team1.heal_count -= 1
                        pokemon1.heal()

                if action2 == Action.HEAL:
                    if team2.heal_count < 0:
                        return 1
                    else:
                        team2.heal_count -= 1
                        pokemon2.heal()
                
                # TEAM 1 AND 2 ATTACKS -------------------------------------------------------------------

                if action1 == Action.ATTACK and action2 == Action.ATTACK: # both attacks
                    # get speed
                    speed1 = pokemon1.get_speed()
                    speed2 = pokemon2.get_speed()
                    
                    # compare speed
                    if speed1 > speed2:
                        pokemon1.attack(pokemon2)
                        if not pokemon2.is_fainted():
                            pokemon2.attack(pokemon1)
                    elif speed1 < speed2:
                        pokemon2.attack(pokemon1)
                        if not pokemon1.is_fainted():
                            pokemon1.attack(pokemon2)
                    if speed1 == speed2:
                        pokemon1.attack(pokemon2)
                        pokemon2.attack(pokemon1)

                elif action1 == Action.ATTACK: # team 1 attacks
                    pokemon1.attack(pokemon2)
                    
                elif action2 == Action.ATTACK: # team 2 attacks
                    pokemon2.attack(pokemon1)

                # battle ends here ------------------------------------------------------------
                
                # both pokemons are not fainted --> both lose 1 hp
                if (not pokemon1.is_fainted()) and (not pokemon2.is_fainted()): #should not be elif next because the lose hp could make a pokemon faint, resulting in other one level up
                    pokemon1.lose_hp(1)
                    pokemon2.lose_hp(1)
                
                # one pokemon is fainted, the other is not -> surviving pokemon level up
                if (not pokemon1.is_fainted()) and pokemon2.is_fainted():
                    pokemon1.level_up()
                elif pokemon1.is_fainted() and (not pokemon2.is_fainted()):
                    pokemon2.level_up()
                
                # if any surviving pokemon can and should evolve -> it evolves
                if (not pokemon1.is_fainted()) and pokemon1.can_evolve() and pokemon1.should_evolve():
                    pokemon1 = pokemon1.get_evolved_version()
                    team1.poke_on_field = pokemon1
                if (not pokemon2.is_fainted()) and pokemon2.can_evolve() and pokemon2.should_evolve():
                    pokemon2 = pokemon2.get_evolved_version()
                    team2.poke_on_field = pokemon2

                # remove any fainted pokemons
                if pokemon1.is_fainted():
                    pokemon1 = None
                if pokemon2.is_fainted():
                    pokemon2 = None
