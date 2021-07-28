from discord.ext import commands

class Events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.bot.user.name} logged in successfully")

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return
        if message.content.startswith('in'):
            roster = 10
            msg = 'You are on the team {0.author.mention}. There are {1} places remaining'.format(message,roster)
            await message.channel.send(msg)
        if message.content.startswith('out'):
            msg = 'Ok, hopefully see you next week {0.author.mention}'.format(message)
            await message.channel.send(msg)
            
def setup(bot):
    bot.add_cog(Events(bot))