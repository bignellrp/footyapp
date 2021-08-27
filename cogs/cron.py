from discord.ext import commands
from bot import CHANNEL_ID
import aiocron
from services.post_spread import wipe_tally
from bot import bot

class Cron(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @aiocron.crontab('0 6 * * SUN')
    @commands.Cog.listener()
    async def cronmsg():
        channel = bot.get_channel(CHANNEL_ID)
        wipe_tally()
        await channel.send('Whos available to play this week?')

def setup(bot):
    bot.add_cog(Cron(bot))