from flask import render_template, Blueprint
#from services.get_spread_data import _fetch_players_table, _get_players_table
from services.get_spread import player

leaderboard_blueprint = Blueprint('leaderboard', __name__, template_folder='templates', static_folder='static')

@leaderboard_blueprint.route('/leaderboard', methods=['GET'])
def leaderboard():
    '''A function for building the leaderboard page.
    Takes in leaderboard from players table and returns top10 player names and scores'''

    #_,_,leaderboard,_,_,_ = _get_players_table(_fetch_players_table())
    players = player()
    leaderboard = players.leaderboard()
    
    return render_template('leaderboard.html', game_stats = leaderboard)