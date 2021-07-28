from discord.ext import commands
from services.get_players import _get_results_table, _fetch_results_table

##Get information for bot
_,teama,teamb,_,date,_ = _get_results_table(_fetch_results_table())

class FunCommands(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def last1(self, ctx):
        await ctx.send('The last match was {}'.format(date))
    
    @commands.command()
    async def team1(self, ctx):
        await ctx.send('TeamA: {}'.format(teama))
    
    @commands.command()
    async def team2(self, ctx):
        await ctx.send('TeamB: {}'.format(teamb))
    
    @commands.command()
    async def roster1(self, ctx):
        await ctx.send('Roster: {}'.format(teama))

    @commands.command()
    async def poll(self, ctx, *, question):
        await ctx.channel.purge(limit=1)
        message = await ctx.send('{}: \n✅ = Yes**\n**❎ = No**'.format(question))
        await message.add_reaction('✅')
        await message.add_reaction('❎')

def setup(bot):
    bot.add_cog(FunCommands(bot))