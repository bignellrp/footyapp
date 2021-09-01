import discord
from discord.ext import commands
import services.post_spread as post
from services.get_spread import player, results
from services.get_even_teams import get_even_teams
from services.get_date import next_wednesday
import re
import asyncio

class Commands(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    # @commands.command(pass_context = True)
    # @commands.has_permissions(administrator=True)
    # async def clear(self, ctx, number):
    #     number = int(number)
    #     try:
    #         await ctx.channel.purge(limit=number)
    #     except:
    #         await ctx.send('Couldnt delete these messages!')
    
    # @commands.command(pass_context=True)
    # @commands.has_permissions(administrator=True)
    # async def nick(self, ctx, member: discord.Member, nick):
    #     """Change users nickname"""
    #     players = player()
    #     player_names = players.player_names()
    #     player_names = [pname[0] for pname in player_names]
    #     try:
    #         await member.edit(nick=nick)
    #         await ctx.send(f'Nickname was changed for {member.mention} ')
    #     except:
    #         await ctx.send(f'Error: Theres an issue with that nickname!')
    #     if nick in player_names:
    #         await ctx.send(f'{member.mention} is in the player list.')
    #     else:
    #         await ctx.send(f'*Note* {member.mention} is not in the player list. Use the *new* command to add them.')

    # @commands.command()
    # @commands.has_permissions(administrator=True)
    # async def new(self, ctx, *args):
    #     """Adds player to db"""
    #     players = player()
    #     player_names = players.player_names()
    #     player_names = [pname[0] for pname in player_names]
    #     for new_player in args:
    #         if new_player in player_names:
    #             print(f'{new_player} already exists!')
    #             await ctx.send(f'{new_player} already exists!')
    #         else:
    #             post.add_new_player(new_player)
    #             await ctx.send(f'Added new player with a generic score of 77: {new_player}')

    # @commands.command()
    # @commands.has_permissions(administrator=True)
    # async def score(self, ctx):
    #     """Update score"""
    #     file = discord.File("static/football.png")
    #     result = results()
    #     teama = result.teama()
    #     teamb = result.teamb()
    #     date = result.date()
    #     scorea = result.scorea()
    #     scoreb = result.scoreb()
    #     teama = "\n".join(item for item in teama)
    #     teamb = "\n".join(item for item in teamb)
    #     if scorea != "-":
    #         print('Score already entered for this week')
    #         await ctx.send('Score already entered for this week')
    #     else:
    #         print('Display this weeks teams')
    #         # Embed Message
    #         embed=discord.Embed(
    #             title="Here were the teams for:"+str(date),
    #             url="http://football.richardbignell.co.uk/score",
    #             color=discord.Color.dark_green()
    #         )
    #         embed.add_field(name="TeamA Score (" + str(scorea) + "):", value=teama, inline=True)
    #         embed.add_field(name="TeamB Score (" + str(scoreb) + "):", value=teamb, inline=True)
    #         embed.set_thumbnail(url="attachment://football.png")
    #         embed.set_footer(text="Enter on the website if you prefer using the link above")
    #         await ctx.send(file=file, embed=embed)
    #         await ctx.send("Please enter the score for TeamA: (1 or 2 digits)")
    #         def check(m):
    #             match = re.match("(^[0-9]{1,2}$)",m.content)
    #             return m.channel == ctx.channel and match
    #         try:
    #             msg = await self.bot.wait_for("message", timeout=60.0, check=check)
    #         except asyncio.TimeoutError:
    #             await ctx.send("You didnt enter a 1 or 2 digit number in 60 seconds.")
    #             return
    #         else:
    #             result = post.update_scorea(msg.content)
    #             print("Team A Score saved!")
    #             await ctx.send("Score saved! Please enter the score for TeamB: (1 or 2 digits)")
    #             def check(m):
    #                 match = re.match("(^[0-9]{1,2}$)",m.content)
    #                 return m.channel == ctx.channel and match
    #             try:
    #                 msg = await self.bot.wait_for("message", timeout=60.0, check=check)
    #             except asyncio.TimeoutError:
    #                 await ctx.send("You didnt enter a 1 or 2 digit number in 60 seconds.")
    #                 return
    #             else:
    #                 result = post.update_scoreb(msg.content)
    #                 print("Team B Score saved!")
    #                 await ctx.send("Scores saved!")
    #                 return

    # @commands.command()
    # @commands.has_permissions(administrator=True)
    # async def matches(self, ctx):
    #     """Last 10 Matches"""
    #     res = results()
    #     game_stats = res.game_stats()
    #     rows = "\n".join(str(row) for row in game_stats)
    #     # date = [el[0] for el in game_stats]
    #     # date = "\n".join(str(item) for item in date)
    #     # teama = [el[1] for el in game_stats]
    #     # teama = "\n".join(str(item) for item in teama)
    #     # teamb = [el[2] for el in game_stats]
    #     # teamb = "\n".join(str(item) for item in teamb)
    #     # Embed Message
    #     embed=discord.Embed(
    #         title="Stats",
    #         url="http://football.richardbignell.co.uk/stats",
    #         color=discord.Color.green()
    #     )
    #     embed.add_field(name="Date/TeamA/TeamB", value=rows, inline=True)
    #     #embed.add_field(name="Date", value=date, inline=True)
    #     #embed.add_field(name="TeamA", value=teama, inline=True)
    #     #embed.add_field(name="TeamB", value=teamb, inline=True)
    #     embed.set_footer(text="Click stats link above for full stats.")
    #     print("Posted Stats to discord!")
    #     await ctx.send(embed=embed)

    # @commands.command()
    # async def mystats(self, ctx, member: discord.Member = None):
    #     """Individual Player Stats"""
    #     file = discord.File("static/football.png")
    #     member = member or ctx.author
    #     players = player()
    #     player_names = players.player_names()
    #     player_names = [pname[0] for pname in player_names]
    #     all_player_stats = players.player_stats()
    #     if member.display_name in player_names:
    #         player_stats = []
    #         for row in all_player_stats:
    #             if row[0] == member.display_name:
    #                 player_stats.append((row[0],int(row[1]),int(row[2]),int(row[3]),int(row[4])))
    #         ##Build the table
    #         name = [el[0] for el in player_stats]
    #         name = "\n".join(str(item) for item in name)
    #         wins = [el[1] for el in player_stats]
    #         wins = "\n".join(str(item) for item in wins)
    #         draws = [el[2] for el in player_stats]
    #         draws = "\n".join(str(item) for item in draws)
    #         losses = [el[3] for el in player_stats]
    #         losses = "\n".join(str(item) for item in losses)
    #         total = [el[4] for el in player_stats]
    #         total = "\n".join(str(item) for item in total)
    #         ##Embed Message
    #         embed=discord.Embed(
    #             title="Stats",
    #             url="http://football.richardbignell.co.uk/stats",
    #             color=discord.Color.green()
    #         )
    #         embed.add_field(name="Name:", value=name, inline=False)
    #         embed.add_field(name="Wins:", value=wins, inline=False)
    #         embed.add_field(name="Draws:", value=draws, inline=False)
    #         embed.add_field(name="Losses:", value=losses, inline=False)
    #         embed.add_field(name="Total:", value=total, inline=False)
    #         embed.set_thumbnail(url="attachment://football.png")
    #         embed.set_footer(text="Click stats link above for full stats.")
    #         print("Posted Stats to discord!")
    #         await ctx.send(file=file, embed=embed)
    #     else:
    #         print(f"Cannot find player called {member.display_name}")
    #         await ctx.send(f"Cannot find any stats for {member.display_name}")

    # @commands.command()
    # @commands.has_permissions(administrator=True)
    # async def stats(self, ctx):
    #     """All Player Stats"""
    #     file = discord.File("static/football.png")
    #     players = player()
    #     player_stats = players.player_stats()
    #     rows = "\n".join(str(row) for row in player_stats)
    #     # name = [el[0] for el in player_stats]
    #     # name = "\n".join(str(item) for item in name)
    #     # wins = [el[1] for el in player_stats]
    #     # wins = "\n".join(str(item) for item in wins)
    #     # draws = [el[2] for el in player_stats]
    #     # draws = "\n".join(str(item) for item in draws)
    #     # losses = [el[3] for el in player_stats]
    #     # losses = "\n".join(str(item) for item in losses)
    #     # total = [el[4] for el in player_stats]
    #     # total = "\n".join(str(item) for item in total)
    #     # Embed Message
    #     embed=discord.Embed(
    #         title="Stats",
    #         url="http://football.richardbignell.co.uk/stats",
    #         color=discord.Color.green()
    #     )
    #     embed.set_thumbnail(url="attachment://football.png")
    #     embed.add_field(name="Name/W/D/L/T", value=rows, inline=True)
    #     # embed.add_field(name="Name", value=name, inline=True)
    #     # embed.add_field(name="W", value=wins, inline=True)
    #     # embed.add_field(name="D", value=draws, inline=True)
    #     # embed.add_field(name="L", value=losses, inline=True)
    #     # embed.add_field(name="T", value=total, inline=True)
    #     embed.set_footer(text="Click stats link above for full stats.")
    #     print("Posted Stats to discord!")
    #     await ctx.send(file=file, embed=embed)

    # @commands.command()
    # @commands.has_permissions(administrator=True)
    # async def teams(self, ctx):
    #     """Generate teams"""
    #     file = discord.File("static/football.png")
    #     players = player()
    #     game_player_tally_with_score = players.game_player_tally_with_score()
    #     result = results()
    #     scorea = result.scorea()
    #     date = result.date()
    #     count = players.player_count()
    #     if count > 0:
    #         print(f'Not enough players!')
    #         await ctx.send(f'We still need {count} more players! Type *!play* to find out whos on the list.')
    #     elif count < 0:
    #         print('Too many players!')
    #         await ctx.send("Too many players!")
    #     else:
    #         print('Running even teams function!')
    #         team_a,team_b,team_a_total,team_b_total = get_even_teams(game_player_tally_with_score)
    #         google_output = []
    #         google_output.append((next_wednesday))
    #         google_output.append(str("-"))
    #         google_output.append(str("-"))
    #         google_output.append((team_a_total))
    #         google_output.append((team_b_total))
    #         google_output.extend((team_a))
    #         google_output.extend((team_b))
    #         team_a = "\n".join(item for item in team_a)
    #         team_b = "\n".join(item for item in team_b)
    #         # Embed Message
    #         embed=discord.Embed(
    #             title="Here are the teams:",
    #             url="http://football.richardbignell.co.uk",
    #             color=discord.Color.dark_green()
    #         )
    #         embed.add_field(name="TeamA (" + str(team_a_total) + "):", value=team_a, inline=True)
    #         embed.add_field(name="TeamB (" + str(team_b_total) + "):", value=team_b, inline=True)
    #         embed.set_thumbnail(url="attachment://football.png")
    #         embed.set_footer(text="Enter on the website if you prefer using the link above")
    #         await ctx.send(file=file, embed=embed)
    #         await ctx.send("Type *SAVE* to store the results.")
    #         await ctx.send("*You need to save in 10 seconds or this team will be lost*")
    #         def check(m):
    #             return m.content == "SAVE" and m.channel == ctx.channel
    #         try:
    #             msg = await self.bot.wait_for("message", timeout=10.0, check=check)
    #         except asyncio.TimeoutError: 
    #             print("Teams command timeout!")
    #             await ctx.send("You didnt type SAVE in 10 seconds. Run !teams again")
    #             return
    #         else:
    #             if date == next_wednesday and scorea == "-":
    #                 result = post.update_result(google_output)
    #                 print("Running update function")
    #                 await ctx.send(f"Teams Saved!")
    #             else:
    #                 result = post.append_result(google_output)
    #                 print("Running append function")
    #                 await ctx.send(f"Teams Saved!")
    #             return

    # # @commands.command()
    # # @commands.has_permissions(administrator=True)
    # # async def newplayer(self, ctx, member: discord.Member = None):
    # #     """Add a new player"""
    # #     member = member or ctx.author
    # #     new_player = member.display_name
    # #     add_new_player(new_player)
    # #     await ctx.send(f'Added new player with a generic score of 77: {new_player}')

    # # @commands.command()
    # # async def hello(self, ctx, *, member: discord.Member = None):
    # #     """Says hello"""
    # #     member = member or ctx.author
    # #     await ctx.send('Hello {0.display_name}~'.format(member))

    # @commands.command()
    # async def teama(self, ctx):
    #     """Team A List"""
    #     file = discord.File("static/teama.png")
    #     result = results()
    #     teama = result.teama()
    #     date = result.date()
    #     scorea = result.scorea()
    #     teama = "\n".join(item for item in teama)
    #     # Embed Message
    #     embed=discord.Embed(
    #         title="Date: " + date,
    #         color=discord.Color.green()
    #     )
    #     embed.add_field(name="Team A", value=teama, inline=True)
    #     embed.set_thumbnail(url="attachment://teama.png")
    #     embed.set_footer(text="Team A Score: "+str(scorea))
    #     print("Posted Team A to discord!")
    #     try: 
    #         await ctx.send(file=file, embed=embed)
    #     except:
    #         print("Couldn't post teams!")
    
    # @commands.command()
    # async def teamb(self, ctx):        
    #     """A list of players on team B"""
    #     file = discord.File("static/teamb.png")
    #     result = results()
    #     teamb = result.teamb()
    #     scoreb = result.scoreb()
    #     date = result.date()
    #     teamb = "\n".join(item for item in teamb)
    #     # Embed Message
    #     embed=discord.Embed(
    #         title="Date: " + date,
    #         color=discord.Color.green()
    #     )
    #     embed.add_field(name="Team B", value=teamb, inline=True)
    #     embed.set_thumbnail(url="attachment://teamb.png")
    #     embed.set_footer(text="Team B Score: "+str(scoreb))
    #     print("Posted Team B to discord!")
    #     try: 
    #         await ctx.send(file=file, embed=embed)
    #     except:
    #         print("Couldn't post teams!")

    # @commands.command()
    # async def top10(self, ctx):
    #     """Leaderboard"""
    #     file = discord.File("static/trophy.png")
    #     players = player()
    #     leaderboard = players.leaderboard()
    #     leaderboard = '\n'.join(str(row) for row in leaderboard)
    #     #leaderboard = "\n".join(i for i,v in leaderboard)
    #     #players = player()
    #     #score = players.leaderboard()
    #     #score = "\n".join(str(v) for i,v in score)
    #     # Embed Message
    #     embed=discord.Embed(title="Top10:",color=discord.Color.dark_green())
    #     embed.add_field(name="Player/Score", value=leaderboard, inline=True)
    #     #embed.add_field(name="Player/Score", value=leaderboard, inline=True)
    #     #embed.add_field(name="Score", value=score, inline=True)
    #     embed.set_thumbnail(url="attachment://trophy.png")
    #     print("Sending top10 to discord")
    #     await ctx.send(file = file, embed = embed)
    
    # @commands.command()
    # @commands.has_permissions(administrator=True)
    # async def add(self, ctx, *args):
    #     """Add player to playing list"""
    #     players = player()
    #     player_names = players.player_names()
    #     player_names = [pname[0] for pname in player_names]
    #     for name in args:
    #         if name in player_names:
    #             players = player()
    #             count = players.player_count()
    #             if count > 0:
    #                 post.update_playing_status(name) #Should this allow lower case?
    #                 print("Player is in:", name)
    #                 players = player()
    #                 count = players.player_count()
    #                 msg = f'{name} is on the team! There are {count} places remaining'
    #                 await ctx.send(msg)
    #             else:
    #                 msg = "Sorry there are no places left this week."
    #                 await ctx.send(msg)
    #         else:
    #             print(f'{name} doesnt exist!')
    #             await ctx.send(f'{name} is not in the db. Add him using command !new {name}')

    # @commands.command()
    # @commands.has_permissions(administrator=True)
    # async def mod(self, ctx, *args):
    #     """Remove player from playing list"""
    #     players = player()
    #     player_names = players.player_names()
    #     player_names = [pname[0] for pname in player_names]
    #     for name in args:
    #         if name in player_names:
    #             post.modify_playing_status(name)
    #             print("Player is out:", name)
    #             players = player()
    #             count = players.player_count()
    #             await ctx.send(f'We now have {count} places. Hopefully see you next week {name}')
    #         else:
    #             print(f'{name} doesnt exist!')
    #             await ctx.send(f'{name} is not in the db. Add him using command !new {name}')

    # @commands.command()
    # async def play(self, ctx):
    #     """Whos playing this week."""
    #     file = discord.File("static/football.png")
    #     players = player()
    #     game_player_tally = players.game_player_tally()
    #     game_player_tally = "\n".join(item for item in game_player_tally)
    #     count = players.player_count()
    #     if count < 10:
    #         # Embed Message
    #         embed=discord.Embed(
    #             title="Players Available",
    #             description="There are " + str(count) + " spaces left!",
    #             color=discord.Color.dark_green()
    #         )
    #         embed.add_field(name=":", value=game_player_tally, inline=True)
    #         embed.set_thumbnail(url="attachment://football.png")
    #         await ctx.send(file = file, embed = embed)
    #     else:
    #         print(f'{count} places available!')
    #         await ctx.send(f'{count} places available!')

def setup(bot):
    bot.add_cog(Commands(bot))