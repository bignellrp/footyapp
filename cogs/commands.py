from discord.ext import commands
from services.get_players import _get_results_table, _fetch_results_table
from services.update_sheet import _add_new_player, _update_playing_status

##Get information for bot
_,teama,teamb,_,date,_ = _get_results_table(_fetch_results_table())
player_list=['Bernard','Rik']
new_player=["Player100",int(77)]

class Commands(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def new(self, ctx):
        _add_new_player(new_player)
        await ctx.send('Added new player with a generic score of 77: {}'.format(new_player))
    
    @commands.command()
    async def teama(self, ctx):
        await ctx.send('TeamA: {}'.format(teama))
    
    @commands.command()
    async def teamb(self, ctx):
        await ctx.send('TeamB: {}'.format(teamb))
    
    @commands.command()
    async def status(self, ctx):
        _update_playing_status(player_list)
        await ctx.send('Updated status for: {}'.format(player_list))

def setup(bot):
    bot.add_cog(Commands(bot))