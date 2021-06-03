from flask import render_template, request, Blueprint
from services.getplayers import _get_players_table, _fetch_players_table

compare_blueprint = Blueprint('compare', __name__, template_folder='templates', static_folder='static')

@compare_blueprint.route('/compare', methods=['GET', 'POST'])
def compare():
    all_players, player_names,_,_ = _get_players_table(_fetch_players_table())
    if request.method == 'POST':
        # Use GetList to put the data from the index template into the array
        available_players_a = []
        available_players_a = request.form.getlist('available_players_a')
        available_players_b = []
        available_players_b = request.form.getlist('available_players_b')
        team_a = []
        for row in all_players: 
            if row[0] in available_players_a:
                team_a.append((row[0] , int(row[1])))
        team_b = []
        for row in all_players: 
            if row[0] in available_players_b:
                team_b.append((row[0] , int(row[1])))
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
        # Return Team A and Team B to the results template
        return render_template('result.html', teama = team_a_names, teamb = team_b_names, scorea = team_a_total, scoreb = team_b_total)
    # If request method is not POST then it must be GET so render compare.html including player_names
    return render_template('compare.html', player_names = player_names)