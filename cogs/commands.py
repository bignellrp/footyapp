from discord import Embed, File, Color
from discord.ext import commands
from services.post_spread import _add_new_player, _update_playing_status_list
from services.get_spread import player, results

class Commands(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def new(self, ctx, new_player):
        _add_new_player(new_player)
        await ctx.send('Added new player with a generic score of 77: {}'.format(new_player))
    
    @commands.command()
    async def teama(self, ctx):
        result = results()
        teama = result.teama()
        teama = "\n".join(item for item in teama)
        # Embed Message
        embed=Embed(
            title="Here are this weeks teams:",
            color=Color.green()
        )
        embed.add_field(name="Team A", value=teama, inline="true")
        embed.set_thumbnail(
            url="https://e7.pngegg.com/pngimages/347/591/png-clipart-football-team-sport-ball-white-sport-thumbnail.png"
        )
        print("Posted Team A to discord!")
        try: 
            await ctx.send(embed=embed)
        except:
            print("Couldn't post teams!")
    
    @commands.command()
    async def teamb(self, ctx):
        result = results()
        teamb = result.teamb()
        await ctx.send(f'TeamB: {teamb}')

    @commands.command()
    async def top10(self, ctx):
        file = File("static/trophy.png")
        players = player()
        leaderboard = players.leaderboard()
        leaderboard = "\n".join(item[0] for item in leaderboard)
        #score = "\n".join(item[1] for item in leaderboard)
        # Embed Message
        embed=Embed(title="Top10:",color=Color.dark_green())
        embed.add_field(name="Player", value=leaderboard, inline="true")
        embed.add_field(name="Score", value="score", inline="true")
        embed.set_thumbnail(url="attachment://trophy.png")
        print("Sending top10 to discord")
        await ctx.send(file = file, embed = embed)
    
    @commands.command()
    async def status(self, ctx):
        player_list=['Bernard','Rik'] #Need to change this to user input but validation could be an issue
        _update_playing_status_list(player_list)
        await ctx.send(f'Updated status for: {player_list}')

    @commands.command()
    async def playing(self, ctx):
        file = File("static/football.png")
        players = player()
        game_player_tally = players.game_player_tally()
        game_player_tally = "\n".join(item for item in game_player_tally)
        # Embed Message
        embed=Embed(
            title="The following" + players.player_count() + "are playing:",
            color=Color.dark_green()
        )
        embed.add_field(name="Available Players:", value=game_player_tally, inline="true")
        embed.set_thumbnail(url="attachment://football.png")
        await ctx.send(file = file, embed = embed)

def setup(bot):
    bot.add_cog(Commands(bot))