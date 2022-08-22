from random_gen import RandomGen
from tournament import Tournament
from battle import Battle
from tests.base_test import BaseTest

class TestTournament(BaseTest):

    def test_creation(self):
        t = Tournament(Battle(verbosity=0))
        t.set_battle_mode(1)
        self.assertRaises(ValueError, lambda: t.start_tournament("Roark Gardenia + Maylene Crasher_Wake + + + Fantina Byron + Candice Volkner + + +"))
        t.start_tournament("Roark Gardenia + Maylene Crasher_Wake + Fantina Byron + + + Candice Volkner + +")

    def test_random(self):
        RandomGen.set_seed(123456)
        t = Tournament(Battle(verbosity=0))
        t.set_battle_mode(0)
        t.start_tournament("Roark Gardenia + Maylene Crasher_Wake + Fantina Byron + + + Candice Volkner + +")

        team1, team2, res = t.advance_tournament() # Roark vs Gardenia
        self.assertEqual(res, 1)
        self.assertTrue(str(team1).startswith("Roark"))
        self.assertTrue(str(team2).startswith("Gardenia"))

        team1, team2, res = t.advance_tournament() # Maylene vs Crasher_Wake
        self.assertEqual(res, 1)
        self.assertTrue(str(team1).startswith("Maylene"))
        self.assertTrue(str(team2).startswith("Crasher_Wake"))

        team1, team2, res = t.advance_tournament() # Fantina vs Byron
        self.assertEqual(res, 1)
        self.assertTrue(str(team1).startswith("Fantina"))
        self.assertTrue(str(team2).startswith("Byron"))

        team1, team2, res = t.advance_tournament() # Maylene vs Fantina
        self.assertEqual(res, 2)
        self.assertTrue(str(team1).startswith("Maylene"))
        self.assertTrue(str(team2).startswith("Fantina"))

        team1, team2, res = t.advance_tournament() # Roark vs Fantina
        self.assertEqual(res, 1)
        self.assertTrue(str(team1).startswith("Roark"))
        self.assertTrue(str(team2).startswith("Fantina"))

        team1, team2, res = t.advance_tournament() # Candice vs Volkner
        self.assertEqual(res, 1)
        self.assertTrue(str(team1).startswith("Candice"))
        self.assertTrue(str(team2).startswith("Volkner"))

        team1, team2, res = t.advance_tournament() # Roark vs Candice
        self.assertEqual(res, 2)
        self.assertTrue(str(team1).startswith("Roark"))
        self.assertTrue(str(team2).startswith("Candice"))

    def test_metas(self):
        RandomGen.set_seed(123456)
        t = Tournament(Battle(verbosity=0))
        t.set_battle_mode(0)
        t.start_tournament("Roark Gardenia + Maylene Crasher_Wake + Fantina Byron + + + Candice Volkner + +")
        l = t.linked_list_with_metas()
        # Roark = [0, 2, 1, 1, 1]
        # Garderia = [0, 0, 2, 0, 1]
        # Maylene = [6, 0, 0, 0, 0]
        # Crasher_Wake = [0, 2, 0, 1, 0]
        # Fantina = [0, 0, 1, 1, 1]
        # Byron = [0, 2, 0, 0, 1]
        # Candice = [2, 2, 1, 0, 0]
        # Volkner = [0, 5, 0, 0, 0]
        expected = [
            [],
            [],
            ['FIRE'], # Roark Fantina do not have Fire types, but Maylene does (lost to Fantina)
            ['GRASS'], # Maylene Fantina do not have Grass types, but Byron/Crasher_Wake does (lost to Fantina/Maylene)
            [],
            [],
            [],
        ]
        for x in range(len(l)):
            team1, team2, types = l[x]
            self.assertEqual(expected[x], types)

    def test_balance(self):
        # 1054
        t = Tournament()
        self.assertFalse(t.is_balanced_tournament("Roark Gardenia + Maylene Crasher_Wake + Fantina Byron + + + Candice Volkner + +"))
