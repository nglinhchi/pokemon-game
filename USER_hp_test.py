from pokemon import Charizard

def test_hp_init():
    c = Charizard()
    print(c.get_hp())
    print(c.current_hp)
    print(c.max_hp)


def test_hp_levelup():
    c = Charizard()
    c.level_up()
    print(c.current_hp)
    print(c.max_hp)
    print(c.base_hp)
    print(c.get_hp())
    print(c.level)

def test_lose_hp():
    c = Charizard()
    print(c.get_hp())
    c.lose_hp(4)
    print(c.get_hp())

test_hp_init()