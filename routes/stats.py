from flask import render_template, Blueprint
from services.get_spread import results, player

stats_blueprint = Blueprint('stats', 
                            __name__, 
                            template_folder='templates', 
                            static_folder='static')

@stats_blueprint.route('/stats', methods=['GET'])
def stats():
    '''A function for building the stats page.
    Takes in game stats from google sheets 
    and return them to stats page'''

    result = results()
    players = player()
    game_stats = result.game_stats()
    player_stats = players.player_stats()

    #Fix Internal Server Error if Stats are empty
    if len(game_stats) == 0:
        print("List is Empty!")
        game_stats = ["Empty", "Empty", "Empty"]
    
    return render_template('stats.html', 
                           game_stats = game_stats, 
                           player_game_stats = player_stats)