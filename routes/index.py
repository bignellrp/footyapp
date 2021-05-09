from flask import Flask, render_template, request, Blueprint
from services.json_date import next_wednesday
from services.getplayers import _make_players, _fetch_sheet, SERVICE, SCOPES, SPREADSHEET_ID, WRITE_RANGE_NAME, RANGE_NAME
from google.auth.transport.requests import Request
from itertools import combinations
import random

index_blueprint = Blueprint('index', __name__, template_folder='templates', static_folder='static')

@index_blueprint.route('/', methods=['GET', 'POST'])
def index():
    """Start the Web Form for pulling the checkbox data input"""
    all_players, player_names = _make_players(_fetch_sheet())
    if request.method == 'POST':

        # Use GetList to put the data from the index template into the array
        available_players = []
        available_players = request.form.getlist('available_players')

        def comp(team):
            return players - set(team)
        def team_score(team):
            return sum(game_players[member] for member in team)
        def score_diff(team):
            team2 = comp(team)
            return abs(team_score(team) - team_score(team2))
        
        # Define game_players array for storing the players names 
        # and scores only if the names are listed in available_players

        game_players = []
        for obj in all_players:
            if obj.name in available_players:
                game_players.append((obj.name , int(obj.score)))

        # Brute Force Method for comparing team scores
        # This method requires a dict with a key
        game_players = dict(game_players)
        #print(game_players)
        players = set(game_players.keys())
        all_teams = {frozenset(team) for team in combinations(game_players, 5)}
        paired_down = set()
        for team in all_teams: # remove complimentary teams
            if not comp(team) in paired_down:
                paired_down.add(team)
        sorted_teams = sorted(paired_down, key = score_diff)
        num = random.randint(0, 5)
        #print(num)
        team_a = set(sorted_teams[num])
        team_b = comp(team_a)
        team_a_total = (team_score(team_a))
        team_b_total = (team_score(team_b))
        #print(team_a)
        #print(team_b)
        #print(team_a_total)
        #print(team_b_total)

        # Post Results to Google Sheets if output is checked
        output_checked = []
        output_checked = request.form.getlist('output_checked')
        if output_checked == ['Yes']:
            # Format the google ouput into one long comma sep str
            google_output = []
            google_output.append((next_wednesday))
            google_output.append((0))
            google_output.append((0))
            google_output.append((team_a_total))
            google_output.append((team_b_total))
            for obj in team_a: 
                google_output.append((obj))
            for obj in team_b: 
                google_output.append((obj))
            # Format the google body for ROWS
            body = {
                'majorDimension': 'ROWS',
                'values': [
                    google_output,
                ],
                }
            # Print the result to google sheets with append enabled
            result = SERVICE.spreadsheets().values().append(
                spreadsheetId=SPREADSHEET_ID, range=WRITE_RANGE_NAME,
                valueInputOption='USER_ENTERED', body=body).execute()
        # Return Team A and Team B to the results template
        return render_template('result.html', teama = team_a, teamb = team_b, scorea = team_a_total, scoreb = team_b_total)
    return render_template('index.html', player_names=player_names)