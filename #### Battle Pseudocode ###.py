#### Battle Pseudocode ###

#Sequential order#

"""
1. Each team retrieve
2. Each team choose option
3. Perform these in order regardless of team: swap > special > heal > attack, if have same hierarchy then handle team 1 first*** (does not matter as both will be processed). 
***Except attack, this needs to be handled in attack handler.
    Heal: When losing due to heal > 3, return other team   
    Attack: 
        Case 1 (Both Attack, Speed diff): Compare current speed (can be affected by paralysis, need to change this in pokemon/pokemon_base class), faster attack first,
        defending attack next if still alive
        Case 2  (Both Attack, Speed same): Team 1 attack first, Team 2 attack second. Both MUST attack, even if fainted.
        From Ed: In the event of a speed tie, Team 1 Pokemon attacks Team 2 Pokemon, and then Team 2 Pokemon attacks Team 1 Pokemon, irrespective of whether Team 2 Pokemon is fainted.

4. Post Attack:
    Case 1: If both poke alive, both lose 1 hp
    Case 2: One alive, one fainted, the one alive levels up

5. Alive pokemon checks if can evolve (should_evolve & can_evolve), if true evolves
6. If pokemon fainted, return and retrieve new.
    Case 1: One team is empty, return other team number (win).
    Case 2: Both Team empty, return 0 (draw)
    Case 3: Both not empty, continue (loop to top?)
"""