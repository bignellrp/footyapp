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
        await ctx.send(f'Added new player with a generic score of 77: {new_player}')
    
    @commands.command()
    async def teama(self, ctx):
        file = File("static/teama.png")
        result = results()
        teama = result.teama()
        teama = "\n".join(item for item in teama)
        # Embed Message
        embed=Embed(
            title="TeamA",
            color=Color.green()
        )
        embed.add_field(name="Team A", value=teama, inline="true")
        embed.set_thumbnail(url="attachment://teama.png")
        print("Posted Team A to discord!")
        try: 
            await ctx.send(file=file, embed=embed)
        except:
            print("Couldn't post teams!")
    
    @commands.command()
    async def teamb(self, ctx):
        file = File("static/teamb.png")
        result = results()
        teamb = result.teamb()
        teamb = "\n".join(item for item in teamb)
        # Embed Message
        embed=Embed(
            title="TeamB",
            color=Color.green()
        )
        embed.add_field(name="Team B", value=teamb, inline="true")
        embed.set_thumbnail(url="attachment://teamb.png")
        print("Posted Team B to discord!")
        try: 
            await ctx.send(file=file, embed=embed)
        except:
            print("Couldn't post teams!")

    @commands.command()
    async def top10(self, ctx):
        file = File("static/trophy.png")
        players = player()
        leaderboard = players.leaderboard()
        leaderboard = "\n".join(i for i,v in leaderboard)
        players = player() #Duplication - Should be in one loop
        score = players.leaderboard()
        score = "\n".join(str(v) for i,v in score)
        # Embed Message
        embed=Embed(title="Top10:",color=Color.dark_green())
        embed.add_field(name="Player", value=leaderboard, inline="true")
        embed.add_field(name="Score", value=score, inline="true")
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
        count = players.player_count()
        # Embed Message
        embed=Embed(
            title="Players Available",
            description="There are " + str(count) + " spaces left!",
            color=Color.dark_green()
        )
        embed.add_field(name=":", value=game_player_tally, inline="true")
        embed.set_thumbnail(url="attachment://football.png")
        await ctx.send(file = file, embed = embed)

def setup(bot):
    bot.add_cog(Commands(bot))