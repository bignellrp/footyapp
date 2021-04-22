from flask import Flask, render_template, request, Blueprint
from services.player import all_players, player_names
from services.teams import even_teams

index_blueprint = Blueprint('index', __name__, template_folder='templates', static_folder='static')

@index_blueprint.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST': 
    
        # Use GetList to put the data from the index template into the array
        available_players = []
        available_players = request.form.getlist('available_players')
        
        # Define game_players array for storing the players names 
        # and scores only if the names are listed in available_players
        # Unhash the prints when debugging
        game_players = []
        for obj in all_players: 
            if obj.name in available_players:
                game_players.append((obj.name , int(obj.score)))
        
        print(game_players)
        # Take the even teams elements from the heap function
        # Unhash the prints when debugging
        team_a, team_b = even_teams(game_players)
        print(team_a)
        print(team_b)
        # Take the first column and put names into team_a and team_b
        team_a_names = ([row[0] for row in team_a])
        team_b_names = ([row[0] for row in team_b])
        
        # Calculate the score
        team_a_score = ([row[1] for row in team_a])
        team_b_score = ([row[1] for row in team_b])

        # Sum the total of the scores
        team_a_total = (sum(team_a_score))
        team_b_total = (sum(team_b_score))

        # Return Team A and Team B to the results template
        return render_template('result.html', teama = team_a_names, teamb = team_b_names, scorea = team_a_total, scoreb = team_b_total)
    return render_template('index.html', player_names = player_names)