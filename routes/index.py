from flask import render_template, request, Blueprint
from services.getplayers import _make_players, _fetch_player_sheet
from services.get_even_teams import _get_even_teams
# import pandas as pd

index_blueprint = Blueprint('index', __name__, template_folder='templates', static_folder='static')

@index_blueprint.route('/', methods=['GET', 'POST'])
def index():
    """Start the Web Form for pulling the checkbox data input"""
    all_players, player_names = _make_players(_fetch_player_sheet())
    if request.method == 'POST':

        # Use GetList to put the data from the index template into the array
        available_players = []
        available_players = request.form.getlist('available_players')
        #available_players = pd.DataFrame.from_records(available_players, columns=['Name', 'Score'])
        
        game_players = []
        for obj in all_players:
            if obj.name in available_players:
                game_players.append((obj.name , int(obj.score)))
        # contains_avaliable = all_players['Name'].isin(available_players['Name'])
        # game_players = all_players[~contains_available].copy()

        team_a,team_b,team_a_total,team_b_total = _get_even_teams(game_players)
        # Return Team A and Team B to the results template
        return render_template('result.html', teama = team_a, teamb = team_b, scorea = team_a_total, scoreb = team_b_total)
    return render_template('index.html', player_names = player_names)