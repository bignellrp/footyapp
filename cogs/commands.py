import discord
from discord.ext import commands
from six import b
import services.post_spread as post
from services.get_spread import player, results
from services.get_even_teams import get_even_teams
from services.get_date import next_wednesday

class Commands(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    @commands.has_permissions(administrator=True)
    async def nick(self, ctx, member: discord.Member, nick):
        """Usage: !nick old_name new_name - Change users nickname"""
        players = player()
        player_names = players.player_names()
        player_names = [pname[0] for pname in player_names]
        try:
            await member.edit(nick=nick)
            await ctx.send(f'Nickname was changed for {member.mention} ')
        except:
            await ctx.send(f'Error: Theres an issue with that nickname!')
        if nick in player_names:
            await ctx.send(f'{member.mention} is in the player list.')
        else:
            await ctx.send(f'*Note* {member.mention} is not in the player list. Use the *new* command to add them.')

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def new(self, ctx, new_player):
        """Usage: !new player_name - Adds player to db"""
        players = player()
        player_names = players.player_names()
        player_names = [pname[0] for pname in player_names]
        if new_player in player_names:
            print(f'{new_player} already exists!')
            await ctx.send(f'{new_player} already exists!')
        else:
            post.add_new_player(new_player)
            await ctx.send(f'Added new player with a generic score of 77: {new_player}')
    
    @commands.command()
    @commands.has_permissions(administrator=True)
    async def stats(self, ctx):
        """All Player Stats"""
        file = discord.File("static/trophy.png")
        players = player()
        player_stats = players.player_stats()
        name = [el[0] for el in player_stats]
        name = "\n".join(item for item in name)
        wins = [el[1] for el in player_stats]
        wins = "\n".join(item for item in wins)
        draws = [el[2] for el in player_stats]
        draws = "\n".join(item for item in draws)
        losses = [el[3] for el in player_stats]
        losses = "\n".join(item for item in losses)
        total = [el[4] for el in player_stats]
        total = "\n".join(item for item in total)
        # Embed Message
        embed=discord.Embed(
            title="Stats",
            color=discord.Color.green()
        )
        embed.add_field(name="Name", value=name, inline="true")
        embed.add_field(name="Wins", value=wins, inline="true")
        embed.add_field(name="Draws", value=draws, inline="true")
        embed.add_field(name="Losses", value=losses, inline="true")
        embed.add_field(name="Total", value=total, inline="true")
        embed.set_thumbnail(url="attachment://trophy.png")
        embed.set_footer(text="[View full stats here](http://football.richardbignell.co.uk/stats)",)
        print("Posted Stats to discord!")
        await ctx.send(file=file, embed=embed)

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def teams(self, ctx):
        """Generate teams. Needs 10 players"""
        file = discord.File("static/football.png")
        players = player()
        game_player_tally_with_score = players.game_player_tally_with_score()
        result = results()
        scorea = result.scorea()
        date = result.date()
        count = players.player_count()
        if count > 0:
            print(f'Not enough players!')
            await ctx.send(f'We still need {count} more players! Type *!play* to find out whos on the list.')
        elif count < 0:
            print('Too many players!')
            await ctx.send("Too many players!")
        else:
            print('Running even teams function!')
            team_a,team_b,team_a_total,team_b_total = get_even_teams(game_player_tally_with_score)
            google_output = []
            google_output.append((next_wednesday))
            google_output.append(str("-"))
            google_output.append(str("-"))
            google_output.append((team_a_total))
            google_output.append((team_b_total))
            google_output.extend((team_a))
            google_output.extend((team_b))
            team_a = "\n".join(item for item in team_a)
            team_b = "\n".join(item for item in team_b)
            # Embed Message
            embed=discord.Embed(
                title="Here are the teams:",
                color=discord.Color.dark_green()
            )
            embed.add_field(name="TeamA (" + str(team_a_total) + "):", value=team_a, inline="true")
            embed.add_field(name="TeamB (" + str(team_b_total) + "):", value=team_b, inline="true")
            embed.set_thumbnail(url="attachment://football.png")
            embed.set_footer(text="Save results? *Type SAVE*  (10 second timeout)")
            await ctx.send(file=file, embed=embed)
            def check(m):
                return m.content == "SAVE" and m.channel == ctx.channel
            msg = await self.bot.wait_for("message", timeout=10.0, check=check)
            if date == next_wednesday and scorea == "-":
                result = post.update_result(google_output)
                print("Running update function")
            else:
                result = post.append_result(google_output)
                print("Running append function")
            await ctx.send(f"Teams Saved!")

    # @commands.command()
    # @commands.has_permissions(administrator=True)
    # async def newplayer(self, ctx, member: discord.Member = None):
    #     """Add a new player"""
    #     member = member or ctx.author
    #     new_player = member.display_name
    #     add_new_player(new_player)
    #     await ctx.send(f'Added new player with a generic score of 77: {new_player}')

    # @commands.command()
    # async def hello(self, ctx, *, member: discord.Member = None):
    #     """Says hello"""
    #     member = member or ctx.author
    #     await ctx.send('Hello {0.display_name}~'.format(member))

    @commands.command()
    async def teama(self, ctx):
        """A list of players on team A"""
        file = discord.File("static/teama.png")
        result = results()
        teama = result.teama()
        date = result.date()
        scorea = result.scorea()
        teama = "\n".join(item for item in teama)
        # Embed Message
        embed=discord.Embed(
            title="Date: " + date,
            color=discord.Color.green()
        )
        embed.add_field(name="Team A", value=teama, inline="true")
        embed.set_thumbnail(url="attachment://teama.png")
        embed.set_footer(text="Team A Score: "+str(scorea))
        print("Posted Team A to discord!")
        try: 
            await ctx.send(file=file, embed=embed)
        except:
            print("Couldn't post teams!")
    
    @commands.command()
    async def teamb(self, ctx):        
        """A list of players on team B"""
        file = discord.File("static/teamb.png")
        result = results()
        teamb = result.teamb()
        scoreb = result.scoreb()
        date = result.date()
        teamb = "\n".join(item for item in teamb)
        # Embed Message
        embed=discord.Embed(
            title="Date: " + date,
            color=discord.Color.green()
        )
        embed.add_field(name="Team B", value=teamb, inline="true")
        embed.set_thumbnail(url="attachment://teamb.png")
        embed.set_footer(text="Team B Score: "+str(scoreb))
        print("Posted Team B to discord!")
        try: 
            await ctx.send(file=file, embed=embed)
        except:
            print("Couldn't post teams!")

    @commands.command()
    async def top10(self, ctx):
        """Top10 Leaderboard"""
        file = discord.File("static/trophy.png")
        players = player()
        leaderboard = players.leaderboard()
        leaderboard = "\n".join(i for i,v in leaderboard)
        players = player()
        score = players.leaderboard()
        score = "\n".join(str(v) for i,v in score)
        # Embed Message
        embed=discord.Embed(title="Top10:",color=discord.Color.dark_green())
        embed.add_field(name="Player", value=leaderboard, inline="true")
        embed.add_field(name="Score", value=score, inline="true")
        embed.set_thumbnail(url="attachment://trophy.png")
        print("Sending top10 to discord")
        await ctx.send(file = file, embed = embed)
    
    @commands.command()
    @commands.has_permissions(administrator=True)
    async def add(self, ctx, name): #How do i make this a comma separated list
        """Usage: !add player_name - Add player to playing list"""
        players = player()
        player_names = players.player_names()
        player_names = [pname[0] for pname in player_names]
        #player_list=['Bernard','Rik'] #Need to change this to user input but validation could be an issue
        if name in player_names:
            post.update_playing_status(name)
            await ctx.send(f'Updated status for: {name}')
        else:
            print(f'{name} doesnt exist!')
            await ctx.send(f'{name} doesnt exist!')

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def mod(self, ctx, name): #How do i make this a comma separated list
        """Usage: !mod player_name - Remove player from playing list"""
        players = player()
        player_names = players.player_names()
        player_names = [pname[0] for pname in player_names]
        #player_list=['Bernard','Rik'] #Need to change this to user input but validation could be an issue
        if name in player_names:
            post.modify_playing_status(name)
            await ctx.send(f'Updated status for: {name}')
        else:
            print(f'{name} doesnt exist!')
            await ctx.send(f'{name} doesnt exist!')

    @commands.command()
    async def play(self, ctx):
        """Whos playing this week."""
        file = discord.File("static/football.png")
        players = player()
        game_player_tally = players.game_player_tally()
        game_player_tally = "\n".join(item for item in game_player_tally)
        count = players.player_count()
        # Embed Message
        embed=discord.Embed(
            title="Players Available",
            description="There are " + str(count) + " spaces left!",
            color=discord.Color.dark_green()
        )
        embed.add_field(name=":", value=game_player_tally, inline="true")
        embed.set_thumbnail(url="attachment://football.png")
        await ctx.send(file = file, embed = embed)

def setup(bot):
    bot.add_cog(Commands(bot))