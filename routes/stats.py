from flask import render_template, Blueprint
from services.getplayers import _make_stats, result2

stats_blueprint = Blueprint('stats', __name__, template_folder='templates', static_folder='static')

@stats_blueprint.route('/stats', methods=['GET'])
def stats():
    all_stats = _make_stats(result2)
    # Grab game stats from google sheets and display them in a stats table

    game_stats = []
    for obj in all_stats:
        game_stats.append((obj.date , obj.team_a_result , obj.team_b_result))
    
    for line in game_stats:
        print(line)

    return render_template('stats.html', len = len(game_stats), game_stats = game_stats)