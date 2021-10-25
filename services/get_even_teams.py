from itertools import combinations
import random

def get_even_teams(game_players):
    '''A brute force function for calulating even teams.
    Takes in a list of game_players and 
    returns two lists of even score.
        team_a: A list of teama players
        team_b: A list of teamb players
        team_a_total: Total of teama
        team_b_total: Total of teamb'''

    def comp(team):
        return players - set(team)
    def team_score(team):
        return sum(game_players[member] for member in team)
    def score_diff(team):
        team2 = comp(team)
        return abs(team_score(team) - team_score(team2))

    ##Requires a dict with a key
    game_players = dict(game_players)
    players = set(game_players.keys())
    all_teams = {frozenset(team) for team in combinations(game_players, 5)}
    paired_down = set()

    ##Remove complimentary teams
    for team in all_teams:
        if not comp(team) in paired_down:
            paired_down.add(team)
    sorted_teams = sorted(paired_down, key = score_diff)
    num = random.randint(0, 5)
    print(num)
    team_a = set(sorted_teams[num])
    print(f'Using Random Number {num} Team A: {team_a}')
    team_b = comp(team_a)
    print(f'Using Random Number {num} Team B: {team_b}')
    
    ##Convert Back to a list
    team_a = list(team_a)
    team_b = list(team_b)
    team_a_total = (team_score(team_a))
    team_b_total = (team_score(team_b))
    return team_a,team_b,team_a_total,team_b_total