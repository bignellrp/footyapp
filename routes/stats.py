from flask import render_template, Blueprint
from services.getplayers import _fetch_players_table, _get_players_table, _fetch_results_table, _get_results_table

stats_blueprint = Blueprint('stats', __name__, template_folder='templates', static_folder='static')

@stats_blueprint.route('/stats', methods=['GET'])
def stats():
    ##Grab game stats from google sheets and display them in a stats table
    _,_,_,player_stats = _get_players_table(_fetch_players_table())
    _,_,_,_,_,game_stats = _get_results_table(_fetch_results_table())
    return render_template('stats.html', game_stats = game_stats, player_game_stats = player_stats)