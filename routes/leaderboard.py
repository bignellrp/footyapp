from flask import Flask, render_template, request, Blueprint
from services.json_date import next_wednesday
from services.getplayers import _make_players, _fetch_sheet, SERVICE, SCOPES, SPREADSHEET_ID, WRITE_RANGE_NAME, RANGE_NAME
from google.auth.transport.requests import Request
from services.teams import even_teams
from operator import itemgetter

leaderboard_blueprint = Blueprint('leaderboard', __name__, template_folder='templates', static_folder='static')

@leaderboard_blueprint.route('/leaderboard', methods=['GET'])
def leaderboard():
    all_players, player_names = _make_players(_fetch_sheet())
    # Define game_players array for storing the players names 
    # and scores only if the names are listed in available_players
    game_stats = []
    for obj in all_players:
        game_stats.append((obj.name , int(obj.stat)))
    game_stats = sorted(game_stats,key=itemgetter(1), reverse=True)
    game_stats = game_stats[0:5]
    print(game_stats)
    return render_template('leaderboard.html', game_stats = game_stats)