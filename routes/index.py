from flask import render_template, request, Blueprint
from services.get_players import _get_players_table, _fetch_players_table
from services.get_even_teams import _get_even_teams

index_blueprint = Blueprint('index', __name__, template_folder='templates', static_folder='static')

@index_blueprint.route('/', methods=['GET', 'POST'])
def index():
    '''A function for building the index page.
    Takes in available players from a flask form 
    and returns an even set of two 5 a side teams'''

    all_players, player_names,_,_ = _get_players_table(_fetch_players_table())
    
    if request.method == 'POST':

        ##Use GetList to put the data from the index template into the array
        available_players = request.form.getlist('available_players')

        ##Build list of game_players if name exists in available_players
        game_players = []
        for row in all_players:
            '''Takes in row of all_players 
            and returns tuple of game_players 
            if name in available_players'''
            if row[0] in available_players:
                game_players.append((row[0] , int(row[1])))
        
        ##Takes in game_players and returns teams and totals
        team_a,team_b,team_a_total,team_b_total = _get_even_teams(game_players)

        # Return Team A and Team B to the results template
        return render_template('result.html', teama = team_a, teamb = team_b, scorea = team_a_total, scoreb = team_b_total)
    return render_template('index.html', player_names = player_names)