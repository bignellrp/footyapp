##https://flask-discord.readthedocs.io/en/latest/introduction.html
##https://gist.github.com/Peppermint777/c8465f9ce8b579a8ca3e78845309b832
import os
#from flask_discord import DiscordOAuth2Session
import discord
from discord.ext import commands
import json

# Initialise our app and the bot itself
# https://discordpy.readthedocs.io/en/latest/intents.html
intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix='!', intents=intents)

##Get keys from token json
path_to_token = "./services/tokens.json"
with open(path_to_token, "r") as handler:
    info = json.load(handler)

# os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "true"
# bot.config["DISCORD_CLIENT_ID"] = info["CLIENT_ID"]
# bot.config["DISCORD_CLIENT_SECRET"] = info["CLIENT_SECRET"]
# bot.config["DISCORD_REDIRECT_URI"] = info["RI"]
# bot.config["DISCORD_BOT_TOKEN"] = info["discord_token"]
token = info["discord_token"]

##Register Cogs with Discord
# discord = DiscordOAuth2Session(bot)
for file in os.listdir("cogs"):
    if file.endswith(".py"):
        name = file[:-3]
        bot.load_extension(f"cogs.{name}")

# if __name__ == "__main__":
#     bot.run(token)