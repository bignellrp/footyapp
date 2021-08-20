##https://flask-discord.readthedocs.io/en/latest/introduction.html
##https://gist.github.com/Peppermint777/c8465f9ce8b579a8ca3e78845309b832
import os
from flask import Flask, url_for, redirect
from flask_discord import DiscordOAuth2Session
from routes.compare import compare_blueprint
from routes.index import index_blueprint
from routes.leaderboard import leaderboard_blueprint
from routes.stats import stats_blueprint
from routes.result import result_blueprint
from routes.score import score_blueprint
from threading import Thread
#from functools import partial
import discord
from discord.ext import commands
import json

# Initialise our app and the bot itself
# https://discordpy.readthedocs.io/en/latest/intents.html
intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix='!', intents=intents)
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

##Discord Variables
app.secret_key = info["session"]
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "true"
app.config["DISCORD_CLIENT_ID"] = info["CLIENT_ID"]
app.config["DISCORD_CLIENT_SECRET"] = info["CLIENT_SECRET"]
app.config["DISCORD_REDIRECT_URI"] = info["RI"]
app.config["DISCORD_BOT_TOKEN"] = info["discord_token"]
token = info["discord_token"]

##Register Cogs with Discord
discord = DiscordOAuth2Session(app)
for file in os.listdir("cogs"):
    if file.endswith(".py"):
        name = file[:-3]
        bot.load_extension(f"cogs.{name}")

def run():
  #app.run(host="127.0.0.1", debug=False, port=5000)
  app.run(host="0.0.0.0", port=5000, debug=False, use_reloader=False)
  #bot.run(token) #ValueError: set_wakeup_fd only works in main thread

t = Thread(target=run)
t.start()
bot.run(token)

if __name__ == "__main__":
    t = Thread(target=run)
    t.start()
    #app.run(host="127.0.0.1", debug=False, port=5000)
    bot.run(token)