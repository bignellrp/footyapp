##https://flask-discord.readthedocs.io/en/latest/introduction.html
##https://gist.github.com/Peppermint777/c8465f9ce8b579a8ca3e78845309b832
import os
from flask import Flask, url_for, redirect
from flask_discord import DiscordOAuth2Session, requires_authorization, Unauthorized
from routes.compare import compare_blueprint
from routes.index import index_blueprint
from routes.leaderboard import leaderboard_blueprint
from routes.stats import stats_blueprint
from routes.result import result_blueprint
from routes.score import score_blueprint
from threading import Thread
from functools import partial
from discord.ext import commands
from services.get_players import _get_results_table, _fetch_results_table
import json

# Initialize our app and the bot itself
bot = commands.Bot(command_prefix="$")
app = Flask(__name__)

##Register the blueprint for each route
app.register_blueprint(index_blueprint)
app.register_blueprint(compare_blueprint)
app.register_blueprint(leaderboard_blueprint)
app.register_blueprint(stats_blueprint)
app.register_blueprint(result_blueprint)
app.register_blueprint(score_blueprint)

##Flask session needs a key.
##https://flask.palletsprojects.com/en/1.1.x/config/#configuring-from-files
app.config.from_pyfile('config.py')
app.config['SESSION_TYPE'] = 'filesystem'

##Get keys from token json
path_to_token = "./services/tokens.json"
with open(path_to_token, "r") as handler:
    info = json.load(handler)

app.secret_key = info["session"]
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "true"
app.config["DISCORD_CLIENT_ID"] = info["CLIENT_ID"]
app.config["DISCORD_CLIENT_SECRET"] = info["CLIENT_SECRET"]
app.config["DISCORD_REDIRECT_URI"] = info["RI"]
app.config["DISCORD_BOT_TOKEN"] = info["discord_token"]
token = info["discord_token"]

##Get information for bot
_,teama,teamb,_,date,_ = _get_results_table(_fetch_results_table())

discord = DiscordOAuth2Session(app)
##Bot Events
@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    if message.content.startswith('in'):
        roster = 10
        msg = 'You are on the team {0.author.mention}. There are {1} places remaining'.format(message,roster)
        await message.channel.send(msg)
    if message.content.startswith('out'):
        msg = 'Ok, hopefully see you next week {0.author.mention}'.format(message)
        await message.channel.send(msg)
    await bot.process_commands(message)

##Bot Commands
@bot.command()
async def last(ctx):
    await ctx.send('The last match was {}'.format(date))
@bot.command()
async def team1(ctx):
    await ctx.send('TeamA: {}'.format(teama))
@bot.command()
async def team2(ctx):
    await ctx.send('TeamB: {}'.format(teamb))
@bot.command()
async def roster1(ctx):
    await ctx.send('Roster: {}'.format(teama))
@bot.command()
async def poll(ctx, *, question):
    await ctx.channel.purge(limit=1)
    message = await ctx.send('{}: \n✅ = Yes**\n**❎ = No**'.format(question))
    await message.add_reaction('✅')
    await message.add_reaction('❎')

# Make a partial app.run to pass args/kwargs to it
partial_run = partial(app.run, host="127.0.0.1", port=5000, debug=True, use_reloader=False)

# Run the Flask app in another thread.
# Unfortunately this means we can't have hot reload
# (We turned it off above)
# Because there's no signal support.

t = Thread(target=partial_run)
t.start()

# Run the bot
bot.run(token)