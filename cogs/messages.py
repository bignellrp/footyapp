from discord.ext import commands

class Messages(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        roster = 10
        if message.author == self.bot.user:
            return
        if message.content.startswith('in'):
            msg = 'You are on the team {0.author.mention}. There are {1} places remaining'.format(message,roster)
            await message.channel.send(msg)
            roster -= 1
        if message.content.startswith('out'):
            msg = 'Ok, hopefully see you next week {0.author.mention}'.format(message)
            await message.channel.send(msg)

def setup(bot):
    bot.add_cog(Messages(bot))