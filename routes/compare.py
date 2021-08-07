from flask import render_template, request, Blueprint, session
#from services.get_spread_data import _get_players_table, _fetch_players_table
from services.get_spread import player

compare_blueprint = Blueprint('compare', __name__, template_folder='templates', static_folder='static')

@compare_blueprint.route('/compare', methods=['GET', 'POST'])
def compare():
    '''A function for building the compare page.
    Takes in available players from a flask form 
    and returns player names and total score for each team'''

    #all_players,player_names,_,_,_,_ = _get_players_table(_fetch_players_table())
    players = player()
    all_players = players.all_players()
    player_names = players.player_names()
    
    if request.method == 'POST':

        ##Use GetList to put the data from the index template into the array
        available_players_a = request.form.getlist('available_players_a')
        available_players_b = request.form.getlist('available_players_b')

        ##Build teams out of available players from all_players using an if 
        team_a = []
        team_b = []
        for row in all_players: 
            if row[0] in available_players_a:
                team_a.append((row[0] , int(row[1])))
            elif row[0] in available_players_b:
                team_b.append((row[0] , int(row[1])))

        ##Take the first column and put names into team_a and team_b
        team_a_names = sorted([row[0] for row in team_a])
        team_b_names = sorted([row[0] for row in team_b])

        ##Take the second element of the tuple and sum
        team_a_total = sum([row[1] for row in team_a])
        team_b_total = sum([row[1] for row in team_b])
        
        ##Add vars to a session to carry into results page
        session['team_a'] = team_a_names
        session['team_b'] = team_b_names
        session['team_a_total'] = team_a_total
        session['team_b_total'] = team_b_total

        ##Return Team A and Team B to the results template
        return render_template('result.html', teama = team_a_names, teamb = team_b_names, scorea = team_a_total, scoreb = team_b_total)
    ##If request method is not POST then it must be GET so render compare.html including player_names
    return render_template('compare.html', player_names = player_names)