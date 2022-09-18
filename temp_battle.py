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
from sorted_list import ListItem
from stack_adt import ArrayStack

class Battle:
    
    ORDER_ACTION = [Action.SWAP, Action.SPECIAL, Action.HEAL, Action.ATTACK]
    
    def __init__(self, verbosity=0) -> None:
        raise NotImplementedError()

    def battle(self, team1: PokeTeam, team2: PokeTeam) -> int:
        
        # >>> TASK SUMMARY
        """
        - each team retrieve a pokemon to send to field and face off
        - maybe print it out?
        - handle swap
        - handle special
        - handle heal (if heal_count == 0 -> lose)
        - handle attacks
            - if both attack:
                - faster get to attack first
                - if defending pokemon isn't fainted -> attack second
                - if same speed:
                    both attac each other (team 1 should be proceesed first)
        - if both pokemon are still alive, lose 1hp
        - if one pokemon has fainted and other has not, remainign pokemon level ip
        - fainted pokemon are returned and a new pokemon is retrieved from team
            if no pokemon can be retrieved (team is empty) -> opposing player wins if both are empty -> result is a draw
        """


        # >>> APPROACH 1 [INCOMPLETE] - HANDLE SWAPX2 / SPECIALX2 / HEALX2
        """
        # TODO print out the interface

        # each team choose an action
        # teams are added to a list, sorted by action chosen
        team_sorted_actions = ArraySortedList(2)
        team_sorted_actions.add(ListItem(team1, self.ORDER_ACTION.index(team1.choose_battle_option())))
        team_sorted_actions.add(ListItem(team2, self.ORDER_ACTION.index(team2.choose_battle_option())))

        # store team/pokemon that will perform attacks, sorted by pokemon speed
        team_sorted_attacks = ArraySortedList(2)

        # handle SWAP, SPECIAL, HEAL actions
        for i in range (len(team_sorted_actions)):
            
            team = team_sorted_actions[i].value
            action = team.choose_battle_option()
            pokemon = team.retrieve_pokemon()

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
            # ???
            pass
        
        """
            

        # >>> APPROACH 2 [COMPLETE] - HANDLE SWAP/SPECIAL/HEAL X2 REPETITIVE
        
        team1_action = team1.choose_battle_option()
        team1_pokemon = team1.retrieve_pokemon()


        # TEAM 1 PRE-ATTACK -------------------------------------------------------------------

        if team1_action == Action.SWAP:
            team1.return_pokemon(team1_pokemon)
            team1_pokemon = team1.retrieve_pokemon()
        elif team1_action == Action.SPECIAL:
            team1.return_pokemon(team1_pokemon)
            team1.special()
            team1_pokemon = team1.retrieve_pokemon()
        elif team1_action == Action.HEAL:
            if team1.heal_count == 0:
                pass # TODO lose immediately
            else:
                team1.heal_count -= 1
                if team1.battle_mode == 0:
                    temp = ArrayStack(len(team1.team))
                    for _ in range(len(team1.team)):
                        temp.push(team1.team.pop().heal())
                    temp.reverse()
                    team1.team = temp
                elif team1.battle_mode == 1:
                    for _ in range(len(team1.team)):
                        team1.team.append(team1.team.serve().heal())
                elif team1.battle_mode == 2:
                    pass # ? implmentation TODO

        # TEAM 2 PRE-ATTACK -------------------------------------------------------------------

        team2_action = team2.choose_battle_option()
        team2_pokemon = team2.retrieve_pokemon()

        if team2_action == Action.SWAP:
            team2.return_pokemon(team2_pokemon)
            team2_pokemon = team2.retrieve_pokemon()
        elif team2_action == Action.SPECIAL:
            team2.return_pokemon(team2_pokemon)
            team2.special()
            team2_pokemon = team2.retrieve_pokemon()
        elif team2_action == Action.HEAL:
            if team2.heal_count == 0:
                pass # TODO lose immediately
            else:
                team2.heal_count -= 1
                if team2.battle_mode == 0:
                    temp = ArrayStack(len(team2.team))
                    for _ in range(len(team2.team)):
                        temp.push(team2.team.pop().heal())
                    temp.reverse()
                    team2.team = temp
                elif team2.battle_mode == 1:
                    for _ in range(len(team2.team)):
                        team2.team.append(team2.team.serve().heal())
                elif team2.battle_mode == 2:
                    pass # ? implmentation TODO

        # TEAM 1 AND 2 ATTACKS -------------------------------------------------------------------

        if team1_action == Action.ATTACK and team2_action == Action.ATTACK:
            
            # compare speed
            if team1_pokemon.get_status_effect() == StatusEffect.PARALYSIS:
                team1_speed = team1_pokemon.get_speed()//2
            else:
                team1_speed = team1_pokemon.get_speed()

            if team2_pokemon.get_status_effect() == StatusEffect.PARALYSIS:
                team2_speed = team2_pokemon.get_speed()//2
            else:
                team2_speed = team2_pokemon.get_speed()

            if team1_speed > team2_speed:
                team1_pokemon.attack(team2_pokemon)
                if not team2_pokemon.is_fainted():
                    team2_pokemon.attack(team1_pokemon)
            if team1_speed < team2_speed:
                team2_pokemon.attack(team1_pokemon)
                if not team1_pokemon.is_fainted():
                    team1_pokemon.attack(team2_pokemon)
            if team1_speed == team2_speed:
                team1_pokemon.attack(team2_pokemon)
                team2_pokemon.attack(team1_pokemon)

        elif team1_action == Action.ATTACK:
            team1_pokemon.attack(team2_pokemon)
            
        elif team2_action == Action.ATTACK:
            team2_pokemon.attack(team1_pokemon)
        

        # >>> OPTIMISE PRE-ATTACK (NON-REPETITIVE) -------------------------------------------------------------------

        def pre_attack(team: PokeTeam, p: PokemonBase):
            pokemon = p
            action = team.choose_battle_option()
            if action == Action.SWAP:
                team.return_pokemon(pokemon)
                pokemon = team.retrieve_pokemon()
            elif action == Action.SPECIAL:
                team.return_pokemon(pokemon)
                team.special()
                pokemon = team.retrieve_pokemon()
            elif team == Action.HEAL:
                if team.heal_count == 0:
                    pass # TODO lose immediately
                else:
                    team.heal_count -= 1
                    if team.battle_mode == 0:
                        temp = ArrayStack(len(team.team))
                        for _ in range(len(team.team)):
                            temp.push(team.team.pop().heal())
                        temp.reverse()
                        team.team = temp
                    elif team.battle_mode == 1:
                        for _ in range(len(team.team)):
                            team.team.append(team.team.serve().heal())
                    elif team.battle_mode == 2:
                        pass # TODO ? implmentation
        
        team1_pokemon = team1.retrieve_pokemon()
        team2_pokemon = team2.retrieve_pokemon()

        pre_attack(team1, team1_pokemon)
        pre_attack(team2, team2_pokemon)

        # ------------------------------------------------------------------------------------------------------------

if __name__ == "__main__":
    b = Battle(verbosity=3)
    RandomGen.set_seed(16)
    t1 = PokeTeam.random_team("Cynthia", 0, criterion=Criterion.SPD)
    t1.ai_type = PokeTeam.AI.USER_INPUT
    t2 = PokeTeam.random_team("Barry", 1)
    print(b.battle(t1, t2))

