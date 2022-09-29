"""
"""
__author__ = "Scaffold by Jackson Goerner, Code by ______________"

from multiprocessing.connection import Listener
from os import popen
from queue import Queue
from tkinter import ACTIVE
from pokemon_base import PokemonBase, StatusEffect
from random_gen import RandomGen
from poke_team import Action, PokeTeam, Criterion
from print_screen import print_game_screen
from array_sorted_list import ArraySortedList
from queue_adt import CircularQueue
from sorted_list import ListItem, SortedList
from stack_adt import ArrayStack

class Battle:
    
    ORDER_ACTION = [Action.SWAP, Action.SPECIAL, Action.HEAL, Action.ATTACK]
    
    def __init__(self, verbosity=0) -> None:
        raise NotImplementedError()

    def battle(self, team1: PokeTeam, team2: PokeTeam) -> int:
    
        while True:

            # TODO print out the interface

            # each team choose an action
            team_sorted_actions = ArraySortedList(2)
            team_sorted_actions.add(ListItem(1, self.ORDER_ACTION.index(team1.choose_battle_option())))
            team_sorted_actions.add(ListItem(2, self.ORDER_ACTION.index(team2.choose_battle_option())))
            # team_sorted_actions contains ListItem(team_number, action_index) sorted by action _index

            pokemons_sorted_team = ArraySortedList(2)
            # pokemons_sorted_team contains ListItem(pokemon, team_number) sorted by team_number

            pokemons_sorted_speed = ArraySortedList(2)
            # pokemons_sorted_speed contains ListItem(pokemon, speed) sorted speed


            for i in range (len(team_sorted_actions)):

                # get team of current PokeTeam
                team_number = team_sorted_actions[i].value
                if team_number == 1:
                    team = team1
                elif team_number == 2:
                    team = team2

                # get action of current PokeTeam
                action = team.choose_battle_option()

                # get pokemon of current PokeTeam
                pokemon = team.retrieve_pokemon()
                pokemons_sorted_team.add(ListItem(pokemon, team_number))
                if pokemon.get_status_effect() == StatusEffect.PARALYSIS:
                    speed = pokemon.get_speed()//2
                else:
                    speed = pokemon.get_speed()
                pokemons_sorted_speed.add(ListItem(pokemon, speed))
                
                # count attack actions
                attack_count = 0

                if action == Action.SWAP:
                    team.return_pokemon(pokemon)
                    pokemon = team.retrieve_pokemon()

                elif action == Action.SPECIAL:
                    team.return_pokemon(pokemon)
                    team.special()
                    pokemon = team.retrieve_pokemon()

                elif action == Action.HEAL:
                    if team.heal_count == 0:
                        pass # lose immediately
                    else:
                        team.heal_count -= 1
                        if team.battle_mode == 0:
                            temp = ArrayStack(len(team.team))
                            for _ in range(len(team.team)):
                                temp.push(team.team.pop().heal())
                            temp.reverse()
                            team = temp
                        elif team.battle_mode == 1:
                            for _ in range(len(team.team)):
                                team.team.append(team.team.serve().heal())
                        elif team.battle_mode == 2:
                            pass # ? implmentation TODO

                elif action == Action.ATTACK:
                    attack_count += 1
                    pokemon_attack = ListItem(pokemon, speed)
                    
                if i == 1: # after 2 iterations, handle attacks
                    if attack_count == 1:
                        pokemons_sorted_speed.remove(pokemon_attack)
                        pokemon_attack = pokemon_attack.value
                        pokemon_defend = pokemons_sorted_speed[0].value
                        pokemon_attack.attack(pokemon_defend)
                    elif attack_count == 2:
                        if pokemons_sorted_speed[0].key == pokemons_sorted_speed[1].key: # same speed
                            pokemon_team1 = pokemons_sorted_team[0].value
                            pokemon_team2 = pokemons_sorted_team[1].value
                            pokemon_team1.attack(pokemon_team2) # team 1 attack first
                            pokemon_team2.attack(pokemon_team1) # team 2 attack second
                        else: # faster pokemon attack first
                            pokemon_attack = pokemons_sorted_speed[0].value
                            pokemon_defend = pokemons_sorted_speed[1].value
                            pokemon_attack.attack(pokemon_defend)
                            if not pokemon_defend.is_fainted:
                                pokemon_defend.attack(pokemon_attack)
                    
                    pokemon_team1 = pokemons_sorted_team[0].value
                    pokemon_team2 = pokemons_sorted_team[1].value

                    if (not pokemon_team1.is_fainted()) and (not pokemon_team2.is_fainted()):
                        pokemon_team1.lose_hp(1)
                        pokemon_team2.lose_hp(1)
                    elif pokemon_team1.is_fainted() and (not pokemon_team2.is_fainted()):
                        pokemon_team2.level_up()
                    elif pokemon_team2.is_fainted() and (not pokemon_team1.is_fainted()):
                        pokemon_team1.level_up()
                    
                    if (not pokemon_team1.is_fainted()) and pokemon_team1.can_evolve():
                        pokemon_team1 = pokemon_team1.get_evolved_version()
                    if (not pokemon_team2.is_fainted()) and pokemon_team2.can_evolve():
                        pokemon_team2 = pokemon_team2.get_evolved_version()
                    


                
                           
                

if __name__ == "__main__":
    b = Battle(verbosity=3)
    RandomGen.set_seed(16)
    t1 = PokeTeam.random_team("Cynthia", 0, criterion=Criterion.SPD)
    t1.ai_type = PokeTeam.AI.USER_INPUT
    t2 = PokeTeam.random_team("Barry", 1)
    print(b.battle(t1, t2))

