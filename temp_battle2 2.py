from poke_team import PokeTeam, Action, StatusEffect

"""
A battle occurs between two PokeTeams, and each PokeTeam has the ability to return or retrieve pokemon for battling.
A battle starts with each PokeTeam retrieving a pokemon to send to the field, and face off. Then, each team has a choice of 4 options:
● Attack: The current pokemon on the field attacks the opposing team
● Swap: The current pokemon is returned to the field and another pokemon is retrieved
from the team (could be the same pokemon)
● Heal: 3 times per battle, each team can fully heal the pokemon and clear any status
effects.
● Special: Return your pokemon, do a special action on your team (depends on battle
mode) and then retrieve a new pokemon for the field. The battle then does the following, in order:
● Handle any swap actions
● Handle any special actions
● Handle any heal actions (If a heal is requested but that team has already healed
thrice, then they automatically lose the battle)
● Handle attacks. In the case of both pokemon attacking, the following is done:
○ The faster of the two pokemon attacks first. If the defending pokemon still has not fainted, then the defending pokemon attacks second.
○ In the event where both pokemon have the same speed stat, they both attack each other regardless, but team 1’s attack should be processed first (in the event of any status effects)
● If both pokemon are still alive, then they both lose 1 HP
● If one pokemon has fainted and the other has not, the remaining pokemon level up
● If pokemon have not fainted and can evolve, they evolve
● Fainted pokemon are returned and a new pokemon is retrieved from the team.
○ If no pokemon can be retrieved (the team is empty), then the opposing player wins. If both teams are empty, the result is a draw."""

def battle(self, team1: PokeTeam, team2: PokeTeam) -> int:


    pokemon1 = None
    pokemon2 = None

    while True:

        if pokemon1 == None and team1.is_empty() and pokemon2 == None and team2.is_empty():
            return 0
        elif pokemon1 == None and team1.is_empty():
            return 2
        elif pokemon2 == None and team2.is_empty():
            return 1
        else: # both teams still have pokemon -> battle
            if pokemon1 == None:
                pokemon1 = team1.retrieve_pokemon()
            if pokemon2 == None: 
                pokemon2 = team2.retrieve_pokemon()
            
            # battle here -----------------------------------------------------------------

            action1 = team1.choose_battle_option()
            action2 = team2.choose_battle_option()

            # PRE-ATTACKS -------------------------------------------------------------------

            if action1 == Action.SWAP:
                team1.return_pokemon(pokemon1)
                pokemon1 = team1.retrieve_pokemon()
            elif action1 == Action.SPECIAL:
                team1.return_pokemon(pokemon1)
                team1.special()
                pokemon1 = team1.retrieve_pokemon()
            elif action1 == Action.HEAL:
                if team1.heal_count == 0:
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
                if team2.heal_count == 0:
                    return 1
                else:
                    team2.heal_count -= 1
                    pokemon2.heal()

            # TEAM 1 AND 2 ATTACKS -------------------------------------------------------------------

            if action1 == Action.ATTACK and action2 == Action.ATTACK: # both attacks
                
                # get speed
                if pokemon1.get_status_effect() == StatusEffect.PARALYSIS:
                    speed1 = pokemon1.get_speed()//2
                else:
                    speed1 = pokemon1.get_speed()

                if pokemon2.get_status_effect() == StatusEffect.PARALYSIS:
                    speed2 = pokemon2.get_speed()//2
                else:
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

            if (not pokemon1.is_fainted()) and (not pokemon2.is_fainted()):
                pokemon1.lose_hp(1)
                pokemon2.lose_hp(1)
            elif (not pokemon1.is_fainted()) and pokemon2.is_fainted():
                pokemon1.level_up()
            elif pokemon1.is_fainted() and (not pokemon2.is_fainted()):
                pokemon2.level_up()
            
            if (not pokemon1.is_fainted) and pokemon1.can_evolve():
                pokemon1 = pokemon1.get_evolved_version()
            
            if (not pokemon2.is_fainted) and pokemon2.can_evolve():
                pokemon2 = pokemon2.get_evolved_version()

            if pokemon1.is_fainted():
                pokemon1 = None
            if pokemon2.is_fainted():
                pokemon2 = None
"""

[X] team1 and team2 retrieve pokemon
[X] team1 and team2 pick an action
[X] handle team1/swap and team2/swap
[X] handle team1/heal and team2/heal
[X] handle team1/special and team2/special
[X] handle team1/attack and team2/attack
    - if both attacks, have dif speed:
        - faster attack
        - slower not fainted -> attack
    - if both attacks, have same speed:
        - team1 attack
        - team2 attack

[X] if 2 pokemons are alive -> 2 pokemons lose hp 1
[X] if 1 pokemon is alive, 1 pokemon isn't -> alive one level up
[X] if pokemon is not fainted and can evolve -> they evolve
[X] any fainted pokemon -> delete, team have to retrieve new pokemon
[X] if no pokemon can be retrieved (is empty) -> opposing team wins
[X] if both teams are empty -> result is draw

"""




