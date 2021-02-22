from flask import Flask, render_template, request, Blueprint
from services.json_date import next_wednesday
from services.getplayers import _make_players, _fetch_sheet, SERVICE, SCOPES, SPREADSHEET_ID, WRITE_RANGE_NAME, RANGE_NAME
from google.auth.transport.requests import Request
from services.teams import even_teams

index_blueprint = Blueprint('index', __name__, template_folder='templates', static_folder='static')

@index_blueprint.route('/', methods=['GET', 'POST'])
def index():
    """Start the Web Form for pulling the checkbox data input"""
    all_players, player_names = _make_players(_fetch_sheet())
    if request.method == 'POST':

        # Use GetList to put the data from the index template into the array
        available_players = []
        available_players = request.form.getlist('available_players')

        # Define game_players array for storing the players names 
        # and scores only if the names are listed in available_players
        game_players = []
        for obj in all_players:
            if obj.name in available_players:
                game_players.append((obj.name , int(obj.score)))

        # Add the even teams into team a and team b
        team_a, team_b = even_teams(game_players)

        # Take the first column and put names into team_a and team_b
        team_a_names = ([row[0] for row in team_a])
        team_b_names = ([row[0] for row in team_b])
        
        # Sort the names alphabetically
        team_a_names.sort()
        team_b_names.sort()

        # Calculate the score
        team_a_score = ([row[1] for row in team_a])
        team_b_score = ([row[1] for row in team_b])

        # Sum the total of the scores
        team_a_total = (sum(team_a_score))
        team_b_total = (sum(team_b_score))

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
            for obj in team_a_names: 
                google_output.append((obj))
            for obj in team_b_names: 
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
        return render_template('result.html', teama = team_a_names, teamb = team_b_names, scorea = team_a_total, scoreb = team_b_total)
    return render_template('index.html', player_names=player_names)