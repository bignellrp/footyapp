import discord
from discord.ext import commands
from services.get_spread import player, results

class Commands(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def mystats(self, ctx, member: discord.Member = None):
        """My Player Stats"""
        file = discord.File("static/football.png")
        member = member or ctx.author
        players = player()
        player_names = players.player_names()
        player_names = [pname[0] for pname in player_names]
        all_player_stats = players.player_stats()
        if member.display_name in player_names:
            player_stats = []
            for row in all_player_stats:
                if row[0] == member.display_name:
                    player_stats.append((
                                        row[0],
                                        int(row[1]),
                                        int(row[2]),
                                        int(row[3]),
                                        int(row[4]),
                                        int(row[5])
                                        ))
            ##Build the table
            name = [el[0] for el 
                            in player_stats]
            name = "\n".join(str(item) for item 
                            in name)
            wins = [el[1] for el 
                            in player_stats]
            wins = "\n".join(str(item) for item 
                            in wins)
            draws = [el[2] for el 
                            in player_stats]
            draws = "\n".join(str(item) for item 
                            in draws)
            losses = [el[3] for el 
                            in player_stats]
            losses = "\n".join(str(item) for item 
                            in losses)
            total = [el[4] for el 
                            in player_stats]
            total = "\n".join(str(item) for item 
                            in total)
            percent = [el[5] for el 
                            in player_stats]
            percent = "\n".join(str(item) for item 
                            in percent)
            ##Embed Message
            embed=discord.Embed(
                title="Player Stats",
                url="http://football.richardbignell.co.uk/stats",
                color=discord.Color.green()
            )
            embed.add_field(name="Name:", 
                            value=name, inline=False)
            embed.add_field(name="Wins:", 
                            value=wins, inline=False)
            embed.add_field(name="Draws:", 
                            value=draws, inline=False)
            embed.add_field(name="Losses:", 
                            value=losses, inline=False)
            embed.add_field(name="Total:", 
                            value=total, inline=False)
            embed.add_field(name="Percent:", 
                            value=percent, inline=False)
            embed.set_thumbnail(url="attachment://football.png")
            embed.set_footer(text="Click stats link above for full stats.")
            print("Posted Stats to discord!")
            await ctx.send(file=file, embed=embed)
        else:
            print(f"Cannot find player called {member.display_name}")
            await ctx.send(f"Cannot find any stats for {member.display_name}")

    @commands.command()
    async def stats(self, ctx):
        """All Player Stats"""
        file = discord.File("static/football.png")
        players = player()
        player_stats = players.player_stats()
        rows = "\n".join(
                        str(wins) 
                        + " | " 
                        + str(draws) 
                        + " | " 
                        + str(losses) 
                        + " | " 
                        + str(total) 
                        + " | " 
                        + str(percent)
                        + " | "
                        + name
                        for name,wins,draws,losses,total,percent 
                            in player_stats)
        ##Commented below as mobile doesnt support more than one field
        # name = [el[0] for el in player_stats]
        # name = "\n".join(str(item) for item in name)
        # wins = [el[1] for el in player_stats]
        # wins = "\n".join(str(item) for item in wins)
        # draws = [el[2] for el in player_stats]
        # draws = "\n".join(str(item) for item in draws)
        # losses = [el[3] for el in player_stats]
        # losses = "\n".join(str(item) for item in losses)
        # total = [el[4] for el in player_stats]
        # total = "\n".join(str(item) for item in total)
        # percent = [el[5] for el in player_stats]
        # percent = "\n".join(str(item) for item in percent)
        # Embed Message
        embed=discord.Embed(
            title="Player Stats",
            url="http://football.richardbignell.co.uk/stats",
            color=discord.Color.green()
        )
        embed.set_thumbnail(url="attachment://football.png")
        embed.add_field(name="W|D|L|T|%|Name", value=rows, inline=True)
        ##Commented below as mobile doesnt support more than one field
        # embed.add_field(name="Name", value=name, inline=True)
        # embed.add_field(name="W", value=wins, inline=True)
        # embed.add_field(name="D", value=draws, inline=True)
        # embed.add_field(name="L", value=losses, inline=True)
        # embed.add_field(name="T", value=total, inline=True)
        # embed.add_field(name="%", value=percent, inline=True)
        embed.set_footer(text="Click stats link above for full stats.")
        print("Posted Stats to discord!")
        await ctx.send(file=file, embed=embed)

    @commands.command()
    async def matches(self, ctx):
        """Match stats"""
        res = results()
        game_stats = res.game_stats()
        rows = "\n".join(str(date) 
                         + " | " 
                         + str(scorea) 
                         + " | " 
                         + str(scoreb) for date,scorea,scoreb 
                                        in game_stats)
        # date = [el[0] for el in game_stats]
        # date = "\n".join(str(item) for item in date)
        # teama = [el[1] for el in game_stats]
        # teama = "\n".join(str(item) for item in teama)
        # teamb = [el[2] for el in game_stats]
        # teamb = "\n".join(str(item) for item in teamb)
        # Embed Message
        embed=discord.Embed(
            title="Match Stats",
            url="http://football.richardbignell.co.uk/stats",
            color=discord.Color.green()
        )
        embed.add_field(name="Date|TeamA|TeamB", 
                        value=rows, inline=True)
        #embed.add_field(name="Date", value=date, inline=True)
        #embed.add_field(name="TeamA", value=teama, inline=True)
        #embed.add_field(name="TeamB", value=teamb, inline=True)
        embed.set_footer(text="Click stats link above for full stats.")
        print("Posted Stats to discord!")
        await ctx.send(embed=embed)

    @commands.command()
    async def teama(self, ctx):
        """Players on Team B"""
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
        embed.add_field(name="Team A", value=teama, inline=True)
        embed.set_thumbnail(url="attachment://teama.png")
        embed.set_footer(text="Team A Score: "+str(scorea))
        print("Posted Team A to discord!")
        try: 
            await ctx.send(file=file, embed=embed)
        except:
            print("Couldn't post teams!")
    
    @commands.command()
    async def teamb(self, ctx):        
        """Players on Team B"""
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
        embed.add_field(name="Team B", value=teamb, inline=True)
        embed.set_thumbnail(url="attachment://teamb.png")
        embed.set_footer(text="Team B Score: "+str(scoreb))
        print("Posted Team B to discord!")
        try: 
            await ctx.send(file=file, embed=embed)
        except:
            print("Couldn't post teams!")

    @commands.command()
    async def top10(self, ctx):
        """Leaderboard"""
        file = discord.File("static/trophy.png")
        players = player()
        leaderboard = players.leaderboard()
        leaderboard = '\n'.join(str(score) 
                                + " | " 
                                + name for name,score 
                                        in leaderboard)
        #leaderboard = "\n".join(i for i,v in leaderboard)
        #players = player()
        #score = players.leaderboard()
        #score = "\n".join(str(v) for i,v in score)
        # Embed Message
        embed=discord.Embed(title="Top10:",
                            color=discord.Color.dark_green())
        embed.add_field(name="Score | Player", 
                        value=leaderboard, inline=True)
        #embed.add_field(name="Player/Score", 
        #               value=leaderboard, inline=True)
        #embed.add_field(name="Score", 
        #               value=score, inline=True)
        embed.set_thumbnail(url="attachment://trophy.png")
        print("Sending top10 to discord")
        await ctx.send(file = file, embed = embed)
    
    @commands.command()
    async def percent(self, ctx):
        """Win Percentage"""
        file = discord.File("static/percent.png")
        players = player()
        leaderboard = players.winpercentage()
        leaderboard = '\n'.join(str(score) 
                                + " | " 
                                + name for name,score 
                                        in leaderboard)
        embed=discord.Embed(title="Win Percentage:",
                            color=discord.Color.dark_green())
        embed.add_field(name="Score | Player", 
                            value=leaderboard, inline=True)
        embed.set_thumbnail(url="attachment://percent.png")
        print("Sending Win Percentage to discord")
        await ctx.send(file = file, embed = embed)

    @commands.command()
    async def play(self, ctx):
        """Playing this week"""
        file = discord.File("static/football.png")
        players = player()
        game_player_tally = players.game_player_tally_with_index()
        game_player_tally = "\n".join(str(count) 
                                      + " " 
                                      + value for count,value 
                                                in game_player_tally)
        count = players.player_count()
        if count < 10:
            # Embed Message
            embed=discord.Embed(
                title="Players Available",
                description="There are " + str(count) + " spaces left!",
                color=discord.Color.dark_green()
            )
            embed.add_field(name=":", value=game_player_tally, inline=True)
            embed.set_thumbnail(url="attachment://football.png")
            await ctx.send(file = file, embed = embed)
        else:
            print(f'{count} places available!')
            await ctx.send(f'{count} places available!')

    @commands.command()
    async def allplayers(self, ctx):
        """List all players"""
        players = player()
        all_players = players.all_players()
        game_player_tally = []
        num = 1
        for row in all_players:
            '''Takes in row of all_players 
            and returns tuple of game_players with index'''
            game_player_tally.append((num,row[0]))
            num = num+1
        file = discord.File("static/football.png")
        game_player_tally = "\n".join(str(count) 
                                      + " " 
                                      + value for count,value 
                                                in game_player_tally)
        # Embed Message
        embed=discord.Embed(
            title="Players Available",
            color=discord.Color.dark_green()
        )
        embed.add_field(name=":", 
                        value=game_player_tally, inline=True)
        embed.set_thumbnail(url="attachment://football.png")
        await ctx.send(file = file, embed = embed)

def setup(bot):
    bot.add_cog(Commands(bot))