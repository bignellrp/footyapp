from flask import render_template, \
                request, Blueprint, session, redirect, url_for
##from flask_discord import requires_authorization, DiscordOAuth2Session
from services.get_spread import player
import services.post_spread as post
from services.get_even_teams import get_even_teams
from services.get_oscommand import GITBRANCH, IFBRANCH
from services.lookup import lookup
#from services.get_auth import auth
import discord
#from zenora import APIClient

##discord_blueprint = DiscordOAuth2Session()
index_blueprint = Blueprint('index', 
                            __name__, 
                            template_folder='templates', 
                            static_folder='static')

@index_blueprint.route('/', methods=['GET', 'POST'])
##@requires_authorization
#@auth.login_required
def index():

    '''A function for building the index page.
    Takes in available players from a flask form 
    and returns an even set of two 5 a side teams'''

    ##user = discord_blueprint.fetch_user()
    #access_token = session.get("access_token")
    players = player()
    all_players = players.all_players()
    player_names = players.player_names()
    player_count = players.player_count()
    #bearer_client = APIClient(access_token, bearer=True)
    #current_user = bearer_client.users.get_current_user()

    if request.method == 'POST':
        if request.form['submit_button'] == 'Post':
            ##Use GetList to put the data 
            ##from the index template into the array
            available_players = request.form.getlist('available_players')
            error = None
            if len(available_players) < 10:
                '''If available players less than 10'''
                print("Not enough players!")
                error = "*ERROR*: Please select 10 players!"
                return render_template('index.html', 
                                        player_names = player_names, 
                                        player_count = player_count, 
                                        error = error)
            else:
                ##Build list of game_players if 
                ##name exists in available_players
                ##Also build a tally of available players 
                ##to use as a running session
                game_players = []
                for row in all_players:
                    '''Takes in row of all_players 
                    and returns tuple of game_players 
                    if name in available_players'''
                    if row[0] in available_players:
                        game_players.append((row[0] , int(row[1])))

                #game_player_tally = []
                ##To update in a batch this requires 
                ##the list to be alphabetical
                ##Updating these one by one takes too long.
                #post.sort_players()
                # for row in all_players:
                #     '''Takes in row of all_players 
                #     and returns a tally of those players
                #     that are available this week'''
                #     if row[0] in available_players:
                #         game_player_tally.append(("x"))
                #     else:
                #         game_player_tally.append(("o"))

                ##Save the tally of available players
                #result = post.update_tally(game_player_tally)
                result = post.update_tally(available_players)
                print("Running tally function")

                ##Takes in game_players and returns teams and totals
                team_a,team_b,team_a_total,team_b_total = get_even_teams(game_players)

                ##Add vars to a session to carry into results page
                session['team_a'] = team_a
                session['team_b'] = team_b
                session['team_a_total'] = team_a_total
                session['team_b_total'] = team_b_total
                print("Posting to results page")

                ##Send the teams to discord presave (only for main)
                file = discord.File("static/football.png")
                if IFBRANCH in GITBRANCH:
                    url = lookup("discord_webhook")
                    teama_json = "\n".join(item for item in team_a)
                    teamb_json = "\n".join(item for item in team_b)
                    webhook = discord.Webhook.from_url(url, 
                                                    adapter=discord.RequestsWebhookAdapter())
                    ##Embed Message
                    embed=discord.Embed(title="PRE-SAVE:",
                                        color=discord.Color.dark_green())
                    embed.set_author(name="footyapp")
                    embed.add_field(name="TeamA (" 
                                    + str(team_a_total) 
                                    + "):", value=teama_json, 
                                    inline=True)
                    embed.add_field(name="TeamB (" 
                                    + str(team_b_total) 
                                    + "):", value=teamb_json, 
                                    inline=True)
                    embed.set_thumbnail(url="attachment://football.png")
                    webhook.send(file = file, embed = embed)
                    
                # Return Team A and Team B to the results template
                return render_template('result.html', 
                                        teama = team_a, 
                                        teamb = team_b, 
                                        scorea = team_a_total, 
                                        scoreb = team_b_total)
        elif request.form['submit_button'] == 'Save':
            ##Use GetList to put the data 
            ##from the index template into the array
            available_players = request.form.getlist('available_players')
            ##Build a tally of available players 
            ##to use as a running session
            #game_player_tally = []
            ##To update in a batch this requires 
            ##the list to be alphabetical
            ##Updating these one by one takes too long.
            #post.sort_players()
            # for row in all_players:
            #     '''Takes in row of all_players 
            #     and returns a tally of those players
            #     that are available this week'''
            #     if row[0] in available_players:
            #         game_player_tally.append(("x"))
            #     else:
            #         game_player_tally.append(("o"))

            ##Save the tally of available players
            #result = post.update_tally(game_player_tally)
            result = post.update_tally(available_players)
            print("Running tally function")    
            return redirect(url_for('index.index'))
        elif request.form['submit_button'] == 'Wipe':
            result = post.wipe_tally()
            print("Running clear function")    
            return redirect(url_for('index.index'))
        else:
            available_players = request.form.getlist('available_players')
            print("No button pressed")
            return redirect(url_for('index.index'))
    elif request.method == 'GET':
        return render_template('index.html', 
                                player_names = player_names, 
                                player_count = player_count)
                                ##user=current_user)
                                ##user = user)