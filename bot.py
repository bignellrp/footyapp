import os
import discord
from discord.ext import commands
from threading import Thread
import asyncio
from services.lookup import lookup
from services.get_oscommand import GITBRANCH, IFBRANCH

##Initialise our app and the bot itself
##https://discordpy.readthedocs.io/en/latest/intents.html

intents = discord.Intents.default()
intents.members = True
if  IFBRANCH in GITBRANCH:
    token = lookup("discord_token")
    bot = commands.Bot(command_prefix='!', intents=intents)
else:
    token = lookup("discord_token_dev")
    bot = commands.Bot(command_prefix='$', intents=intents)

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

discord_thread = async_discord_thread()