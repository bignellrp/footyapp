from flask import render_template, Blueprint
from services.get_players import _fetch_players_table, _get_players_table

leaderboard_blueprint = Blueprint('leaderboard', __name__, template_folder='templates', static_folder='static')

@leaderboard_blueprint.route('/leaderboard', methods=['GET'])
def leaderboard():
    _,_,leaderboard,_ = _get_players_table(_fetch_players_table())
    return render_template('leaderboard.html', game_stats = leaderboard)