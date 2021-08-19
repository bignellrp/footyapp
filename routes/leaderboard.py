from quart import render_template, Blueprint
from services.get_spread import player

leaderboard_blueprint = Blueprint('leaderboard', __name__, template_folder='templates', static_folder='static')

@leaderboard_blueprint.route('/leaderboard', methods=['GET'])
async def leaderboard():
    '''A function for building the leaderboard page.
    Takes in leaderboard from players table and returns top10 player names and scores'''

    players = player()
    leaderboard = players.leaderboard()
    
    return await render_template('leaderboard.html', game_stats = leaderboard)