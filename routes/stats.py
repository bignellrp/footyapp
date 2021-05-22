from flask import render_template, Blueprint
from services.getplayers import _make_stats, _make_player_stats, _fetch_player_sheet, _fetch_stats_sheet
from operator import itemgetter

stats_blueprint = Blueprint('stats', __name__, template_folder='templates', static_folder='static')

@stats_blueprint.route('/stats', methods=['GET'])
def stats():
    all_stats = _make_stats(_fetch_stats_sheet())
    player_stats = _make_player_stats(_fetch_player_sheet())
    # Grab game stats from google sheets and display them in a stats table

    game_stats = []
    for obj in all_stats:
        game_stats.append((obj.date , obj.team_a_result , obj.team_b_result))

    player_game_stats = []
    for obj in player_stats:
        player_game_stats.append((obj.name , int(obj.wins) , int(obj.draws), int(obj.losses), int(obj.total)))
    player_game_stats = sorted(player_game_stats,key=itemgetter(4), reverse=True)

    return render_template('stats.html', game_stats = game_stats, player_game_stats = player_game_stats)