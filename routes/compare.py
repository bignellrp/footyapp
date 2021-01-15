from flask import Flask, render_template, request, Blueprint
from services.player import all_players, player_names
from services.teams import even_teams

compare_blueprint = Blueprint('compare', __name__, template_folder='templates', static_folder='static')

@compare_blueprint.route('/compare', methods=['GET', 'POST'])
def compare():
    if request.method == 'POST': 

        # Use GetList to put the data from the index template into the array
        available_players_a = []
        available_players_a = request.form.getlist('available_players_a')
        available_players_b = []
        available_players_b = request.form.getlist('available_players_b')
        
        # Define game_players array for storing the players names 
        # and scores only if the names are listed in available_players
        game_players_a = []
        for obj in all_players: 
            if obj.name in available_players_a:
                game_players_a.append((obj.name , int(obj.score)))
        game_players_b = []
        for obj in all_players: 
            if obj.name in available_players_b:
                game_players_b.append((obj.name , int(obj.score)))
        
        # Use the same names as index function
        team_a = game_players_a
        team_b = game_players_b

        # Take the first column and put names into team_a and team_b
        team_a_names = ([row[0] for row in team_a])
        team_b_names = ([row[0] for row in team_b])
        
        # Calculate the score
        team_a_score = ([row[1] for row in team_a])
        team_b_score = ([row[1] for row in team_b])

        # Sum the total of the scores
        team_a_total = (sum(team_a_score))
        team_b_total = (sum(team_b_score))
        
        # Return results to result_compare.html template
        return render_template('result.html', teama = team_a_names, teamb = team_b_names, scorea = team_a_total, scoreb = team_b_total)
    # If request method is not POST then it must be GET so render compare.html including player_names
    return render_template('compare.html', player_names = player_names)