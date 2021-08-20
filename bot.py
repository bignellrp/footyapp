import os
from flask_discord import DiscordOAuth2Session
import discord
from discord.ext import commands
import json
from main import app

# Initialise our app and the bot itself
# https://discordpy.readthedocs.io/en/latest/intents.html
intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix='!', intents=intents)

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

if __name__ == "__main__":
    bot.run(token)