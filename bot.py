import os
import discord
from discord.ext import commands
from threading import Thread
import asyncio
#import json
from services.lookup import lookup
from services.get_oscommand import GITBRANCH, IFBRANCH
#import aiocron
#from services.post_spread import wipe_tally

##Initialise our app and the bot itself
##https://discordpy.readthedocs.io/en/latest/intents.html

intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix='!', intents=intents)
CHANNEL_ID=868980424955801681

##Get keys from token json
# path_to_token = "./services/tokens.json"
# with open(path_to_token, "r") as handler:
#     info = json.load(handler)
# token = info["discord_token"]

token = lookup("discord_token")

##Register Cogs with Discord
for file in os.listdir("cogs"):
    if file.endswith(".py"):
        name = file[:-3]
        bot.load_extension(f"cogs.{name}")

##Class for Running Discord in a thread
##https://www.reddit.com/r/Discord_Bots/comments/pa57zv/discord_py_flask_uwsgi/
##
##ValueError: set_wakeup_fd only works in main thread
##https://github.com/Rapptz/discord.py/issues/1598

class async_discord_thread(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.loop = asyncio.get_event_loop()
        self.start()

    async def starter(self):
        await bot.start(token) #Changed to start from run

    def run(self):
        self.name = 'Discord.py'
        self.loop.create_task(self.starter())
        self.loop.run_forever()

# @aiocron.crontab('0 6 * * SUN')
# async def cronmsg():
#     channel = bot.get_channel(CHANNEL_ID)
#     wipe_tally()
#     await channel.send('Whos available to play this week?')

if  IFBRANCH in GITBRANCH: #Equals not working for some reason
    discord_thread = async_discord_thread()
else:
    print("Not running footyapp bot!")
    discord_thread = async_discord_thread()