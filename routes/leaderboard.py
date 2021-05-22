from flask import render_template, Blueprint
from services.getplayers import _make_players, _fetch_player_sheet
from operator import itemgetter

leaderboard_blueprint = Blueprint('leaderboard', __name__, template_folder='templates', static_folder='static')

@leaderboard_blueprint.route('/leaderboard', methods=['GET'])
def leaderboard():
    all_players, player_names = _make_players(_fetch_player_sheet())
    # Grab game stats from google sheets and display them in a leaderboard table
    game_stats = []
    for obj in all_players:
        game_stats.append((obj.name , int(obj.stat)))
    game_stats = sorted(game_stats,key=itemgetter(1), reverse=True)
    game_stats = game_stats[0:10]
    #print(game_stats)
    return render_template('leaderboard.html', len = len(game_stats), game_stats = game_stats)