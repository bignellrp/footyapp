from discord import Embed, File, Color, Member
import discord
from discord.ext import commands
from services.post_spread import _add_new_player, _update_playing_status_list
from services.get_spread import player, results
from services.get_even_teams import _get_even_teams
from services.get_date import next_wednesday
from services.post_spread import _update_result, _append_result

class Commands(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    @commands.has_permissions(administrator=True)
    async def nick(self, ctx, member: discord.Member, nick):
        players = player()
        player_names = players.player_names()
        try:
            await member.edit(nick=nick)
            await ctx.send(f'Nickname was changed for {member.mention} ')
        except:
            await ctx.send(f'Error: Theres an issue with that nickname!')
        if nick not in str(player_names):
            await ctx.send(f'*Note* {member.mention} is not in the player list. Use the *new* command to add them.')
        else:
            await ctx.send(f'{member.mention} is in the player list.')

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def new(self, ctx, new_player):
        players = player()
        player_names = players.player_names()
        if new_player in str(player_names):
            print(f'{new_player} already exists!')
            await ctx.send(f'{new_player} already exists!')
        else:
            _add_new_player(new_player)
            await ctx.send(f'Added new player with a generic score of 77: {new_player}')

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def teams(self, ctx):
        file = File("static/football.png")
        players = player()
        game_player_tally_with_score = players.game_player_tally_with_score()
        result = results()
        dash = result.dash()
        date = result.date()
        count = players.player_count()
        if count > 0:
            print(f'Not enough players!')
            await ctx.send(f'We still need {count} more players! Run *playing* to find out whos on the list.')
        elif count < 0:
            print('Too many players!')
            await ctx.send("Too many players!")
        else:
            print('Running even teams function!')
            team_a,team_b,team_a_total,team_b_total = _get_even_teams(game_player_tally_with_score)
            google_output = []
            google_output.append((next_wednesday))
            google_output.append(str("-"))
            google_output.append(str("-"))
            google_output.append((team_a_total))
            google_output.append((team_b_total))
            google_output.extend((team_a))
            google_output.extend((team_b))
            print(google_output)
            team_a = "\n".join(item for item in team_a)
            team_b = "\n".join(item for item in team_b)
            # Embed Message
            embed=Embed(
                title="Here are the teams:",
                color=Color.dark_green()
            )
            embed.add_field(name="TeamA (" + str(team_a_total) + "):", value=team_a, inline="true")
            embed.add_field(name="TeamB (" + str(team_b_total) + "):", value=team_b, inline="true")
            embed.set_thumbnail(url="attachment://football.png")
            #embed.set_footer('Save results') #Takes 1 pos 2 were given?
            await ctx.send(file=file, embed=embed)
            await ctx.send("Save results? *Type SAVE*")
            def check(m):
                return m.content == "SAVE" and m.channel == ctx.channel
            msg = await self.bot.wait_for("message", check=check) #timeout??
            if date == next_wednesday and dash == "-":
                result = _update_result(google_output)
                print("Running update function")
            else:
                result = _append_result(google_output)
                print("Running append function")
            await ctx.send(f"Teams Saved!")

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def newplayer(self, ctx, member: discord.Member = None):
        member = member or ctx.author
        new_player = member.display_name
        _add_new_player(new_player)
        await ctx.send(f'Added new player with a generic score of 77: {new_player}')

    @commands.command()
    async def hello(self, ctx, *, member: discord.Member = None):
        """Says hello"""
        member = member or ctx.author
        await ctx.send('Hello {0.display_name}~'.format(member))
    
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