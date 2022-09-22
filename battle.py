"""
"""
__author__ = "Scaffold by Jackson Goerner, Code by ______________"

from multiprocessing.connection import Listener
from os import popen
from tkinter import ACTIVE
from random_gen import RandomGen
from poke_team import Action, PokeTeam, Criterion
from print_screen import print_game_screen

class Battle:
    
    def __init__(self, verbosity=0) -> None:
        self.verbosity = verbosity


    def battle(self, team1: PokeTeam, team2: PokeTeam) -> int:
        
        pokemon1 = None
        pokemon2 = None

        while True:

            if pokemon1 == None and team1.team.is_empty() and pokemon2 == None and team2.team.is_empty():
                return 0
            elif pokemon1 == None and team1.team.is_empty():
                team2.return_pokemon(pokemon2)
                return 2
            elif pokemon2 == None and team2.team.is_empty():
                team1.return_pokemon(pokemon1)
                return 1
            else: # both teams still have pokemon -> battle
                if pokemon1 == None:
                    pokemon1 = team1.retrieve_pokemon()
                if pokemon2 == None: 
                    pokemon2 = team2.retrieve_pokemon()
                
                # battle here -----------------------------------------------------------------

                action1 = team1.choose_battle_option(pokemon1, pokemon2)
                action2 = team2.choose_battle_option(pokemon2, pokemon1)

                # PRE-ATTACKS -------------------------------------------------------------------
                # TODO if current implementation work -> change the order to SWAPS/SPECIALS/HEALS instead of
                # SWAP/SPECIAL/HEAL/SWAP/SPECIAL/HEAL

                if action1 == Action.SWAP:
                    team1.return_pokemon(pokemon1)
                    pokemon1 = team1.retrieve_pokemon()
                elif action1 == Action.SPECIAL:
                    # team1.return_pokemon(pokemon1) Should be implemented inside special
                    team1.special()
                    pokemon1 = team1.retrieve_pokemon()
                elif action1 == Action.HEAL:
                    if team1.heal_count < 0:
                        return 2
                    else:
                        team1.heal_count -= 1
                        pokemon1.heal()

                # TEAM 2 PRE-ATTACK -------------------------------------------------------------------

                if action2 == Action.SWAP:
                    team2.return_pokemon(pokemon2)
                    pokemon2 = team2.retrieve_pokemon()
                elif action2 == Action.SPECIAL:
                    team2.return_pokemon(pokemon2)
                    team2.special()
                    pokemon2 = team2.retrieve_pokemon()
                elif action2 == Action.HEAL:
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

                if (not pokemon1.is_fainted()) and (not pokemon2.is_fainted()): #should not be elif next because the lose hp could make a pokemon faint, resulting in other one level up
                    pokemon1.lose_hp(1)
                    pokemon2.lose_hp(1)
                
                if (not pokemon1.is_fainted()) and pokemon2.is_fainted():
                    pokemon1.level_up()
                elif pokemon1.is_fainted() and (not pokemon2.is_fainted()):
                    pokemon2.level_up()
                print(pokemon1.is_fainted(), pokemon2.is_fainted())
                print(pokemon1, pokemon2)
                if (not pokemon1.is_fainted()) and pokemon1.can_evolve() and pokemon1.should_evolve():
                    pokemon1 = pokemon1.get_evolved_version()
                
                if (not pokemon2.is_fainted()) and pokemon2.can_evolve() and pokemon2.should_evolve():
                    pokemon2 = pokemon2.get_evolved_version()

                if pokemon1.is_fainted():
                    pokemon1 = None
                if pokemon2.is_fainted():
                    pokemon2 = None
    

if __name__ == "__main__":
    b = Battle(verbosity=3)
    RandomGen.set_seed(16)
    t1 = PokeTeam.random_team("Cynthia", 0, criterion=Criterion.SPD)
    
    t1.ai_type = PokeTeam.AI.USER_INPUT
    t2 = PokeTeam.random_team("Barry", 1)
    print(b.battle(t1, t2))

