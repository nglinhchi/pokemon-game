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
    
        # TODO print out the interface

        # each team choose an action
        # teams are added to a list, sorted by action chosen
        team_sorted_actions = ArraySortedList(2)
        team_sorted_actions.add(ListItem(1, self.ORDER_ACTION.index(team1.choose_battle_option())))
        team_sorted_actions.add(ListItem(2, self.ORDER_ACTION.index(team2.choose_battle_option())))
        # team_sorted_actions contains ListItem(team_number, action_index) sorted by action _index

        pokemons_sorted_team = ArraySortedList(2)
        # pokemons_sorted_team contains Listem(pokemon, team_number) sorted by team_number

        pokemons_attack = CircularQueue(2)

        for i in range (len(team_sorted_actions)):

            team_number = team_sorted_actions[i].value

            # get team, action, pokemon of current PokeTeam
            if team_number == 1:
                team = team1
            elif team_number == 2:
                team = team2
            action = team.choose_battle_option()
            pokemon = team.retrieve_pokemon()
            pokemons_sorted_team.add(ListItem(pokemon, team_number))
            

            # count attack
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
                pokemons_attack.append(pokemon)
                
            if i == 1: # after 2 iterations, handle attacks
                
                if attack_count == 0:
                    pass
                elif attack_count == 1:
                    all_pokemons = CircularQueue(2)
                    for i in range(len(pokemons_sorted_team)):
                        all_pokemons.append(pokemons_sorted_team[i].value)
                    


                elif attack_count == 2:
                    pass

                # get speed value to sort team
                if pokemon.get_status_effect() == StatusEffect.PARALYSIS:
                    speed = pokemon.get_speed() // 2
                else:
                    speed = pokemon.get_speed()
                
                # add to 2nd sorted list
                team_sorted_attacks.add(ListItem(pokemon, speed))  # pass in team or pokemon? TODO

                if i == 1: # i = 1, after both iteration
                    pass
                    
                
        if len(team_sorted_attacks) == 2 and team_sorted_attacks[0].key == team_sorted_attacks[1].key: # if both team has same speed
            # sorted list is stable --> use correspondig index 0 and 1 for team1 and team2
            pokemon_team1 = team_sorted_attacks[0].value
            pokemon_team2 = team_sorted_attacks[1].value
            pokemon_team1.attack(pokemon_team2)
            pokemon_team2.attack(pokemon_team1)
        elif len(team_sorted_attacks) == 2: # do attacks in order
            pass
            

if __name__ == "__main__":
    b = Battle(verbosity=3)
    RandomGen.set_seed(16)
    t1 = PokeTeam.random_team("Cynthia", 0, criterion=Criterion.SPD)
    t1.ai_type = PokeTeam.AI.USER_INPUT
    t2 = PokeTeam.random_team("Barry", 1)
    print(b.battle(t1, t2))

