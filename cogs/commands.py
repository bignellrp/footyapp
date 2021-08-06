import discord
from discord.ext import commands
from services.update_sheet import _add_new_player, _update_playing_status_list #Move this to post_spread_results
from services.get_spread_data import _get_players_table, _fetch_players_table, _get_results_table, _fetch_results_table

class Commands(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def new(self, ctx, new_player):
        _add_new_player(new_player)
        await ctx.send('Added new player with a generic score of 77: {}'.format(new_player))
    
    @commands.command()
    async def teama(self, ctx):
        _,teama,_,_,_,_ = _get_results_table(_fetch_results_table())
        await ctx.send('TeamA: {}'.format(teama))
    
    @commands.command()
    async def teamb(self, ctx):
        _,_,teamb,_,_,_ = _get_results_table(_fetch_results_table())
        await ctx.send('TeamB: {}'.format(teamb))

    @commands.command()
    async def top10(self, ctx):
        _,_,leaderboard,_,_,_ = _get_players_table(_fetch_players_table())
        embed = discord.Embed(title = 'Top10', description = leaderboard)
        await ctx.send(embed = embed)
    
    @commands.command()
    async def status(self, ctx):
        player_list=['Bernard','Rik'] #Need to change this to user input but validation could be an issue
        _update_playing_status_list(player_list)
        await ctx.send('Updated status for: {}'.format(player_list))

    @commands.command()
    async def playing(self, ctx):
        _,_,_,_,player_count,game_player_tally = _get_players_table(_fetch_players_table())
        await ctx.send(f'The following {player_count} players are playing: {game_player_tally}')

def setup(bot):
    bot.add_cog(Commands(bot))