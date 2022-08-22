TEMPLATE_WINDOW = list(map(list, """\
  ........................................................................................................................................  
 *O                                                                                                                                      O. 
 oO                                                                                                                                      O. 
 oO                                                                                                                                     #O. 
 o#    @@o*************************************************°*                                                                          @#O° 
 o#    @°                                                    #                                                                          @#° 
 o#    @.*  P                             *  *  *  *  *  *   #                                                                          @#° 
 o#    @.*                                                   #                                                                          ##° 
 o#    @.*  LV: 00              HP: 00 / 00                  #                                                                          ##° 
 o#    @..  HP |------------------------------------------|  °O                                                                          #° 
 o#     #oooo°.                                             .  °o#                                                                      ##° 
 o#          @@##################################################                                                                       ##° 
 o#@                                                                                 @OOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO#@                 #O° 
 o#                                                                        #######OOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO#######       @#° 
 o#                                                                  ####OOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO####  #° 
 o#                                                               ####OOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO## O. 
 o#                                                               ####OOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO## O. 
 o#                                                                 ####OOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO##O    ##° 
 o#                                                                      @#####O*°********°°°***°°°*******************************o#@@@@@#° 
 o#                                                                          @O                                                    O@@@@##° 
 o#                                                                          @°                                                    o@@@@##° 
 o#                                                                          @°   P                             *  *  *  *  *  *   O@@@@##° 
 o#                                                                          @°                                                    o@@@@##° 
 o#                                                                          @°   LV: 00              HP: 00 / 00                   .#@@##° 
 o#                                                                          @°   HP |------------------------------------------|   .#@@##° 
 o#                                                                         @#.                                                     .#@@#O° 
 o#          #######OOOOOOOOOoOOOOOOoOo*****°°°o#OOO                       o°    ..°*.°°**..*°°°°°°°*°°°°°°°°°°°°°°°°*°°°°°°°°°°.  .o@@@@#° 
 *O#OOOOOooooooooooooooooooooo**ooo*°*°....  .°oooooooooooooooooooOOOOO###o*********o*o*o***oooooooooooooooooooooooooooooooooooo**oO####OO.""".split("\n")))

import copy
import os

os.system('')

STATUS_MAPPING = {
    "burn": ("\x1b[41mB", "R", "N\x1b[0m"),
    "sleep": ("\x1b[44mS", "L", "P\x1b[0m"),
    "paralysis": ("\x1b[43mP", "A", "R\x1b[0m"),
    "poison": ("\x1b[45mP", "S", "N\x1b[0m"),
    "confuse": ("\x1b[47m\x1b[30mC", "N", "F\x1b[0m"),
    "free": "   ",
}

CLEAR = "\x1b[0m"

HEALTH_HIGH = "\x1b[32m"
HEALTH_MED = "\x1b[33m"
HEALTH_LOW = "\x1b[31m"

POKEMON_COLORS = {
    "charmander": "\x1b[31m",
    "charizard": "\x1b[31m",
    "bulbasaur": "\x1b[32m",
    "venusaur": "\x1b[32m",
    "squirtle": "\x1b[34m",
    "blastoise": "\x1b[34m",
    "gastly": "\x1b[35m",
    "haunter": "\x1b[35m",
    "gengar": "\x1b[35m",
    "eevee": "\x1b[37m",
}

def print_game_screen(team1_pokemon_name, team2_pokemon_name, team1_cur_hp, team1_max_hp, team2_cur_hp, team2_max_hp, team1_lvl, team2_lvl, team1_status, team2_status, team1_remaining_pokemon, team2_remaining_pokemon):
    BATTLE_WINDOW = copy.deepcopy(TEMPLATE_WINDOW)
    team1_pokemon_name = team1_pokemon_name.lower()
    team2_pokemon_name = team2_pokemon_name.lower()
    # NAMES
    for i, c in enumerate(team1_pokemon_name.upper()):
        BATTLE_WINDOW[21][82 + i] = c
    for i, c in enumerate(team2_pokemon_name.upper()):
        BATTLE_WINDOW[6][12 + i] = c
    
    # LVL
    BATTLE_WINDOW[23][86], BATTLE_WINDOW[23][87] = str(team1_lvl).zfill(2)
    BATTLE_WINDOW[8][16], BATTLE_WINDOW[8][17] = str(team2_lvl).zfill(2)
    
    # HP
    BATTLE_WINDOW[23][106], BATTLE_WINDOW[23][107] = str(team1_cur_hp).zfill(2)
    BATTLE_WINDOW[23][111], BATTLE_WINDOW[23][112] = str(team1_max_hp).zfill(2)
    BATTLE_WINDOW[8][36], BATTLE_WINDOW[8][37] = str(team2_cur_hp).zfill(2)
    BATTLE_WINDOW[8][41], BATTLE_WINDOW[8][42] = str(team2_max_hp).zfill(2)
    
    HP_WIDTH = 57 - 16 + 1
    team1_hp_ratio = team1_cur_hp / team1_max_hp
    team2_hp_ratio = team2_cur_hp / team2_max_hp
    COVERED_1 = int(HP_WIDTH * team1_hp_ratio)
    COVERED_2 = int(HP_WIDTH * team2_hp_ratio)
    for x in range(HP_WIDTH):
        BATTLE_WINDOW[24][86 + x] = "█" if x < COVERED_1 else "-"
        BATTLE_WINDOW[9][16 + x] = "█" if x < COVERED_2 else "-"
    if team1_hp_ratio > 0.66:
        BATTLE_WINDOW[24][86] = HEALTH_HIGH + BATTLE_WINDOW[24][86]
    elif team1_hp_ratio > 0.33:
        BATTLE_WINDOW[24][86] = HEALTH_MED + BATTLE_WINDOW[24][86]
    else:
        BATTLE_WINDOW[24][86] = HEALTH_LOW + BATTLE_WINDOW[24][86]
    if team2_hp_ratio > 0.66:
        BATTLE_WINDOW[9][16] = HEALTH_HIGH + BATTLE_WINDOW[9][16]
    elif team2_hp_ratio > 0.33:
        BATTLE_WINDOW[9][16] = HEALTH_MED + BATTLE_WINDOW[9][16]
    else:
        BATTLE_WINDOW[9][16] = HEALTH_LOW + BATTLE_WINDOW[9][16]
        
    BATTLE_WINDOW[24][86 + COVERED_1 - 1] = BATTLE_WINDOW[24][86 + COVERED_1 - 1] + CLEAR
    BATTLE_WINDOW[9][16 + COVERED_2 - 1] = BATTLE_WINDOW[9][16 + COVERED_2 - 1] + CLEAR
    
    # STATUS
    BATTLE_WINDOW[21][102], BATTLE_WINDOW[21][103], BATTLE_WINDOW[21][104] = STATUS_MAPPING[team1_status]
    BATTLE_WINDOW[6][32], BATTLE_WINDOW[6][33], BATTLE_WINDOW[6][34] = STATUS_MAPPING[team2_status]
    
    # REMAINING POKEMON
    for x in range(6):
        BATTLE_WINDOW[6][42 + 3*x] = "█" if x < team2_remaining_pokemon else "*"
        BATTLE_WINDOW[21][112 + 3*x] = "█" if x < team1_remaining_pokemon else "*"
    
    # SPRITES
    team1_color = POKEMON_COLORS[team1_pokemon_name]
    with open("pokemon_printing/" + team1_pokemon_name + "_back.txt", "r") as f:
        team1_lines = f.read().split("\n")
    team1_sprite_width = len(team1_lines[0])
    team1_sprite_height = len(team1_lines)
    for x in range(team1_sprite_height):
        for y in range(team1_sprite_width):
            xind = 27 - team1_sprite_height + x
            yind = 31 - team1_sprite_width // 2 + y
            if 12 <= xind <= 27 and 5 <= yind <= 75:
                BATTLE_WINDOW[xind][yind] = (team1_color if y == 0 else "") + team1_lines[x][y] + (CLEAR if y == team1_sprite_width - 1 else "")

    team2_color = POKEMON_COLORS[team2_pokemon_name]
    with open("pokemon_printing/" + team2_pokemon_name + ".txt", "r") as f:
        team2_lines = f.read().split("\n")
    team2_sprite_width = len(team2_lines[0])
    team2_sprite_height = len(team2_lines)
    for x in range(team2_sprite_height):
        for y in range(team2_sprite_width):
            xind = 17 - team2_sprite_height + x
            yind = 101 - team2_sprite_width // 2 + y
            if 1 <= xind <= 17 and 65 <= yind <= 136:
                BATTLE_WINDOW[xind][yind] = (team2_color if y == 0 else "") + team2_lines[x][y] + (CLEAR if y == team2_sprite_width - 1 else "")
    
    print("\n".join(map(lambda z: "".join(z), BATTLE_WINDOW)))

if __name__ == "__main__":
    POKEMON = ["Charmander", "Charizard", "Bulbasaur", "Venusaur", "Squirtle", "Blastoise", "Gastly", "Haunter", "Gengar", "Eevee"]
    for pokemon in POKEMON:
        print_game_screen(pokemon, pokemon, 10, 20, 20, 60, 3, 5, 4, 3)
