from flask import render_template, request, Blueprint
from services.json_date import next_wednesday
from services.getplayers import _make_players, result1, SERVICE, SPREADSHEET_ID, WRITE_RANGE_NAME

compare_blueprint = Blueprint('compare', __name__, template_folder='templates', static_folder='static')

@compare_blueprint.route('/compare', methods=['GET', 'POST'])
def compare():
    all_players, player_names = _make_players(result1)
    if request.method == 'POST':
        # Use GetList to put the data from the index template into the array
        available_players_a = []
        available_players_a = request.form.getlist('available_players_a')
        available_players_b = []
        available_players_b = request.form.getlist('available_players_b')
        game_players_a = []
        for obj in all_players: 
            if obj.name in available_players_a:
                game_players_a.append((obj.name , obj.score))
        game_players_b = []
        for obj in all_players: 
            if obj.name in available_players_b:
                game_players_b.append((obj.name , obj.score))
        # Take the first column and put names into team_a and team_b
        team_a = game_players_a
        team_b = game_players_b
        # Take the first column and put names into team_a and team_b
        team_a_names = ([row[0] for row in team_a])
        team_b_names = ([row[0] for row in team_b])
        # Sort the names alphabetically
        team_a_names.sort()
        team_b_names.sort()
        # Calculate the score
        team_a_score = ([row[1] for row in team_a])
        team_b_score = ([row[1] for row in team_b])
        team_a_score = [int(i) for i in team_a_score]
        team_b_score = [int(i) for i in team_b_score]
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
    # If request method is not POST then it must be GET so render compare.html including player_names
    return render_template('compare.html', player_names = player_names)