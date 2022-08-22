"""
Run leaderboard matches against the leaderboard team.
"""

from battle import Battle
from poke_team import PokeTeam, Criterion
from random_gen import RandomGen

def leaderboard():    
    RandomGen.set_seed((1<<16) + 1029348)

    leaderboard_team = PokeTeam.leaderboard_team()
    teams = [
        PokeTeam.random_team(f"Team {x}", RandomGen.randint(0, 2), criterion=Criterion(RandomGen.randint(1, len(Criterion))))
        for x in range(1000)
    ]

    streak = 0
    max_streak = 0
    played = 0
    won = 0
    draw = 0
    loss = 0
    b = Battle()
    for team in teams:
        res = b.battle(leaderboard_team, team)
        if res == 0:
            draw += 1
        elif res == 1:
            won += 1
            streak += 1
            max_streak = max(max_streak, streak)
        elif res == 2:
            loss += 1
            streak = 0
        played += 1
        leaderboard_team.regenerate_team()

    return [
        {"name": "Percentage Won", "value": f"{100*won/played:.2f}%"},
        {"name": "Percentage Lost", "value": f"{100*loss/played:.2f}%"},
        {"name": "Percentage Draw", "value": f"{100*draw/played:.2f}%"},
        {"name": "Longest Streak", "value": f"{max_streak}"},
    ]

if __name__ == "__main__":
    print(leaderboard())
