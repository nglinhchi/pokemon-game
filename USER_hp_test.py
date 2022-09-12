from pokemon import *

pokemon_to_test = Venusaur()
def test_hp_init():
    p = pokemon_to_test
    print(p.get_hp())
    print(p.current_hp)
    print(p.max_hp)


def test_hp_levelup():
    p = pokemon_to_test
    p.level_up()
    print(p.current_hp)
    print(p.max_hp)
    print(p.base_hp)
    print(p.get_hp())
    print(p.level)

def test_lose_hp():
    p = pokemon_to_test
    print(p.get_hp())
    p.lose_hp(4)
    print(p.get_hp())

test_hp_init()
test_hp_levelup()