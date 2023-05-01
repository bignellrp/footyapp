from flask import render_template, \
                request, Blueprint
from services.get_spread import player
import services.post_spread as post
from services.get_auth import auth

##discord_blueprint = DiscordOAuth2Session()
playertotals_blueprint = Blueprint('playertotals', 
                            __name__, 
                            template_folder='templates', 
                            static_folder='static')

@playertotals_blueprint.route('/playertotals', methods=['GET', 'POST'])
##@requires_authorization
#@auth.login_required
def playertotals():

    '''A function for building the playerstotal page.
    Takes in players from a flask form and the new totals'''

    players = player()

    all_players = players.all_players()
    all_player_names = []
    for name,total in all_players:
        all_player_names.append((name))

    if request.method == 'POST':
        if request.form['submit_button'] == 'Player':
            ##Use GetList to put the data 
            ##from the index template into the array
            modified_names = request.form.getlist('player_name')
            error = None
            ##Using re.match to check if score input is 2 digits
            #match_a = re.match("(^[0-9]{1,2}$)",score_input_a)
            #match_b = re.match("(^[0-9]{1,2}$)",score_input_b)
            #if match_a == None or match_b == None:
            if 2 > 3:
                '''If score is not numeric then error'''
                print("Score is not a valid input")
                error = "Score is not a valid input"
            else:
                merged_player_names = [(all_player_names[i], modified_names[i]) for i in range(0, len(all_player_names))]
                result = post.update_player_names(merged_player_names)
                ##If post successful render the post page.
                return render_template('post.html')
            ##If there was an error return the score page with error
            return render_template('playertotals.html', 
                                    player_names = all_players, 
                                    error = error)
        elif request.form['submit_button'] == 'Total':
            ##Use GetList to put the data 
            ##from the index template into the array
            modified_totals = request.form.getlist('player_total')
            error = None
            ##Using re.match to check if score input is 2 digits
            #match_a = re.match("(^[0-9]{1,2}$)",score_input_a)
            #match_b = re.match("(^[0-9]{1,2}$)",score_input_b)
            #if match_a == None or match_b == None:
            if 2 > 3:
                '''If score is not numeric then error'''
                print("Score is not a valid input")
                error = "Score is not a valid input"
            else:
                merged_player_totals = [(all_player_names[i], modified_totals[i]) for i in range(0, len(all_player_names))]
                result = post.update_player_totals(merged_player_totals)
                ##If post successful render the post page.
                return render_template('post.html')
            ##If there was an error return the score page with error
            return render_template('playertotals.html', 
                                    player_names = all_players, 
                                    error = error)
        elif request.form['submit_button'] == 'Add':
            ##Use GetList to put the data 
            add_player = request.form.get('add_player')
            error = None
            if 2 > 3:
                '''Need some validation on player name e.g Capital'''
                print("Player name is not a valid input")
                error = "Player name is not a valid input"
            else:
                print(add_player)
                result = post.add_new_player(add_player)
                ##If post successful render the post page.
                return render_template('post.html')
            ##If there was an error return the score page with error
            return render_template('playertotals.html', 
                                    player_names = all_players, 
                                    error = error)
    ##If request method is not POST then it must be GET
    return render_template('playertotals.html', 
                            player_names = all_players)