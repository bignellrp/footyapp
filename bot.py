import os
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
token = info["discord_token"]

##Register Cogs with Discord
for file in os.listdir("cogs"):
    if file.endswith(".py"):
        name = file[:-3]
        bot.load_extension(f"cogs.{name}")

#bot.run(token) #If enabled then it starts first and webserver does not start

# if __name__ == "__main__":
#     bot.run(token)