from itertools import combinations
import random

def _get_even_teams(game_players):
    def comp(team):
        return players - set(team)
    def team_score(team):
        return sum(game_players[member] for member in team)
    def score_diff(team):
        team2 = comp(team)
        return abs(team_score(team) - team_score(team2))
    # Brute Force Method for comparing team scores
    # This method requires a dict with a key
    game_players = dict(game_players)
    players = set(game_players.keys())
    all_teams = {frozenset(team) for team in combinations(game_players, 5)}
    paired_down = set()
    for team in all_teams: # remove complimentary teams
        if not comp(team) in paired_down:
            paired_down.add(team)
    sorted_teams = sorted(paired_down, key = score_diff)
    num = random.randint(0, 5)
    team_a = set(sorted_teams[num])
    team_b = comp(team_a)
    # Convert Back to a list
    team_a = list(team_a)
    team_b = list(team_b)
    team_a_total = (team_score(team_a))
    team_b_total = (team_score(team_b))
    return team_a,team_b,team_a_total,team_b_total