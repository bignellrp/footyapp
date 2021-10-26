import discord
from discord.ext import commands
import services.post_spread as post
from services.get_spread import player, results
from services.get_even_teams import get_even_teams
from services.get_date import next_wednesday
import re
import asyncio

class AdminCommands(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context = True)
    @commands.has_permissions(administrator=True)
    async def clear(self, ctx, number):
        """Clear messages"""
        number = int(number)
        try:
            await ctx.channel.purge(limit=number)
        except:
            await ctx.send('Couldnt delete these messages!')
    
    @commands.command(pass_context = True)
    @commands.has_permissions(administrator=True)
    async def wipe(self, ctx):
        """Wipe Tally"""
        try:
            post.wipe_tally()
            await ctx.send('Tally wiped!')
        except:
            await ctx.send('Error: Couldnt wipe tally!')

    @commands.command(pass_context=True)
    @commands.has_permissions(administrator=True)
    async def nick(self, ctx, member: discord.Member, nick):
        """Change nickname"""
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
    async def new(self, ctx, *args):
        """Adds player to db"""
        players = player()
        player_names = players.player_names()
        player_names = [pname[0] for pname in player_names]
        for new_player in args:
            if new_player in player_names:
                print(f'{new_player} already exists!')
                await ctx.send(f'{new_player} already exists!')
            else:
                post.add_new_player(new_player)
                await ctx.send(f'Added new player with a generic score of 77: {new_player}')

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def score(self, ctx, *args):
        """Update score (no args for lineup)"""
        result = results()
        teama = result.teama()
        teamb = result.teamb()
        date = result.date()
        scorea = result.scorea()
        scoreb = result.scoreb()
        teama_colour = result.coloura()
        teamb_colour = result.colourb()
        fileA = discord.File("static/"+teama_colour+".png")
        fileB = discord.File("static/"+teamb_colour+".png")
        teama = "\n".join(item for item in teama)
        teamb = "\n".join(item for item in teamb)
        if scorea != "-":
            print('Score already entered for this week')
            await ctx.send('Score already entered for this week')
        elif not args:
            print('Display this weeks teams')
            # Embed Message A
            embeda=discord.Embed(
                title="Here were the teams for:"+str(date),
                url="http://football.richardbignell.co.uk/score",
                color=discord.Color.dark_green()
            )
            embeda.add_field(name="TeamA (" 
                            + str(scorea) 
                            + "):", value=teama, 
                            inline=True)
            embeda.set_thumbnail(url="attachment://"+teama_colour+".png")
            embeda.set_footer(text="Use the website above to rerun the saved lineup")
            # Embed Message B
            embedb=discord.Embed(
                title="Here were the teams for:"+str(date),
                url="http://football.richardbignell.co.uk/score",
                color=discord.Color.dark_green()
            )
            embedb.add_field(name="TeamB (" 
                            + str(scoreb) 
                            + "):", value=teamb, 
                            inline=True)
            embedb.set_thumbnail(url="attachment://"+teamb_colour+".png")
            embedb.set_footer(text="Use the website above to rerun the saved lineup")
            await ctx.send(file=fileA, embed=embeda)
            await ctx.send(file=fileB, embed=embedb)
            await ctx.send("Please enter the score for TeamA: (1 or 2 digits)")
            def check(m):
                match = re.match("(^[0-9]{1,2}$)",m.content)
                return m.channel == ctx.channel and match
            try:
                msg = await self.bot.wait_for("message", 
                                              timeout=60.0, check=check)
            except asyncio.TimeoutError:
                await ctx.send("You didnt enter a 1 or 2 digit number in 60 seconds.")
                return
            else:
                post.update_scorea(msg.content)
                print("Team A Score saved!")
                await ctx.send("Score saved! Please enter the score for TeamB: (1 or 2 digits)")
                def check(m):
                    match = re.match("(^[0-9]{1,2}$)",m.content)
                    return m.channel == ctx.channel and match
                try:
                    msg = await self.bot.wait_for("message", 
                                                  timeout=60.0, check=check)
                except asyncio.TimeoutError:
                    await ctx.send("You didnt enter a 1 or 2 digit number in 60 seconds.")
                    return
                else:
                    post.update_scoreb(msg.content)
                    print("Team B Score saved!")
                    await ctx.send("Scores saved!")
                    return
        else:
            args_count = len(args) #Count the args to use in validation
            #args = list(map(int, args)) #Convert all args in list to ints
            print(args[0])
            print(args[1])
            match_a = re.match("(^[0-9]{1,2}$)",args[0])
            match_b = re.match("(^[0-9]{1,2}$)",args[1])
            if args_count != 2:
                await ctx.send('You must enter 2 scores')
            elif match_a == None or match_b == None:
                await ctx.send('One or more of your scores is not a valid number')
            else:
                post.update_scorea(args[0])
                post.update_scoreb(args[1])
                print("Scores saved!")
                await ctx.send("Scores saved!")

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def teams(self, ctx):
        """Generate teams"""
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
            team_a,team_b,team_a_total,team_b_total = get_even_teams(
                game_player_tally_with_score)
            google_output = []
            google_output.append((next_wednesday))
            google_output.append(str("-"))
            google_output.append(str("-"))
            google_output.append((team_a_total))
            google_output.append((team_b_total))
            google_output.extend((team_a))
            google_output.extend((team_b))
            google_output.append(str("teama"))
            google_output.append(str("teamb"))
            team_a = "\n".join(item for item in team_a)
            team_b = "\n".join(item for item in team_b)
            # Embed Message
            embed=discord.Embed(
                title="Here are the teams:",
                url="http://football.richardbignell.co.uk",
                color=discord.Color.dark_green()
            )
            embed.add_field(name="TeamA (" 
                            + str(team_a_total) 
                            + "):", value=team_a, 
                            inline=True)
            embed.add_field(name="TeamB (" 
                            + str(team_b_total) 
                            + "):", value=team_b, 
                            inline=True)
            embed.set_thumbnail(url="attachment://football.png")
            embed.set_footer(text="Enter on the website if you prefer using the link above")
            await ctx.send(file=file, embed=embed)
            await ctx.send("Type *SAVE* to store the results.")
            await ctx.send("*You need to save in 10 seconds or this team will be lost*")
            def check(m):
                return m.content == "SAVE" and m.channel == ctx.channel
            try:
                msg = await self.bot.wait_for("message", 
                                              timeout=10.0, check=check)
            except asyncio.TimeoutError: 
                print("Teams command timeout!")
                await ctx.send("You didnt type SAVE in 10 seconds. Run !teams again")
                return
            else:
                if date == next_wednesday and scorea == "-":
                    result = post.update_result(google_output)
                    print("Running update function")
                    await ctx.send(f"Teams Saved!")
                else:
                    result = post.append_result(google_output)
                    print("Running append function")
                    await ctx.send(f"Teams Saved!")
                return
    
    @commands.command()
    @commands.has_permissions(administrator=True)
    async def swap(self, ctx, *args):
        """Swap player"""
        players = player()
        player_names = players.player_names()
        player_names = [pname[0] for pname in player_names]
        result = results()
        teama = result.teama()
        teamb = result.teamb()
        scorea = result.scorea()
        teams = teama + teamb
        if len(args) != 2:
            print('You must have 2 players!')
            await ctx.send('You must have 2 players!')
        elif scorea != "-":
            print('Game has already been played this week!')
            await ctx.send('Game has already been played this week!')
        elif args[0] not in teams:
            print(f'{args[0]} is not in the {teams} list!')
            await ctx.send(f'{args[0]} is not in the team list!')
        elif args[1] not in player_names:
            print(f'{args[1]} is not in the player list!')
            await ctx.send(f'{args[1]} is not in the player list!')
        elif all([args[0] in teama, args[1] in teama]):
            print(f'{args[0]} and {args[1]} are in Team A: {teama}')
            await ctx.send(f'{args[0]} and {args[1]} are on the same team!')
        elif all([args[0] in teamb, args[1] in teamb]):
            print(f'{args[0]} and {args[1]} are in Team B: {teamb}')
            await ctx.send(f'{args[0]} and {args[1]} are on the same team!')
        elif args[1] in teams:
            '''Using a separate function for swapping players
            between teams when both players are playing'''
            post.swap_existing_player(args)
            await ctx.send(f'{args[0]} swapped with {args[1]}')
            await ctx.send(f'Run command !lineup for updated teams/scores')
        else:
            post.swap_player(args)
            await ctx.send(f'{args[0]} swapped with {args[1]}')
            await ctx.send(f'Run command !lineup for updated teams/scores')

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def lineup(self, ctx):
        """Lineup"""
        result = results()
        teama = result.teama()
        teamb = result.teamb()
        totala = result.totala()
        totalb = result.totalb()
        date = result.date()
        teama_colour = result.coloura()
        teamb_colour = result.colourb()
        fileA = discord.File("static/"+teama_colour+".png")
        fileB = discord.File("static/"+teamb_colour+".png")
        team_a = "\n".join(item for item in teama)
        team_b = "\n".join(item for item in teamb)
        # Embed Message A
        embeda=discord.Embed(
            title="Here were the teams for:"+str(date),
            url="http://football.richardbignell.co.uk/score",
            color=discord.Color.dark_green()
        )
        embeda.add_field(name="TeamA (" 
                        + str(totala) 
                        + "):", value=team_a, 
                        inline=True)
        embeda.set_thumbnail(url="attachment://"+teama_colour+".png")
        embeda.set_footer(text="Use the website above to rerun the saved lineup")
        # Embed Message B
        embedb=discord.Embed(
            title="Here were the teams for:"+str(date),
            url="http://football.richardbignell.co.uk/score",
            color=discord.Color.dark_green()
        )
        embedb.add_field(name="TeamB (" 
                        + str(totalb) 
                        + "):", value=team_b, 
                        inline=True)
        embedb.set_thumbnail(url="attachment://"+teamb_colour+".png")
        embedb.set_footer(text="Use the website above to rerun the saved lineup")
        await ctx.send(file=fileA, embed=embeda)
        await ctx.send(file=fileB, embed=embedb)

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def swap(self, ctx, *args):
        """Swap player"""
        players = player()
        player_names = players.player_names()
        player_names = [pname[0] for pname in player_names]
        result = results()
        teama = result.teama()
        teamb = result.teamb()
        scorea = result.scorea()
        teams = teama + teamb
        if len(args) != 2:
            print('You must have 2 players!')
            await ctx.send('You must have 2 players!')
        elif scorea != "-":
            print('Game has already been played this week!')
            await ctx.send('Game has already been played this week!')
        elif args[0] not in teams:
            print(f'{args[0]} is not in the {teams} list!')
            await ctx.send(f'{args[0]} is not in the team list!')
        elif args[1] not in player_names:
            print(f'{args[1]} is not in the player list!')
            await ctx.send(f'{args[1]} is not in the player list!')
        elif all([args[0] in teama, args[1] in teama]):
            print(f'{args[0]} and {args[1]} are in Team A: {teama}')
            await ctx.send(f'{args[0]} and {args[1]} are on the same team!')
        elif all([args[0] in teamb, args[1] in teamb]):
            print(f'{args[0]} and {args[1]} are in Team B: {teamb}')
            await ctx.send(f'{args[0]} and {args[1]} are on the same team!')
        elif args[1] in teams:
            '''Using a separate function for swapping players
            between teams when both players are playing'''
            post.swap_existing_player(args)
            await ctx.send(f'{args[0]} swapped with {args[1]}')
        else:
            post.swap_player(args)
            await ctx.send(f'{args[0]} swapped with {args[1]}')
            
            post.swap_player(args)
            await ctx.send(f'{args[0]} swapped with {args[1]}')

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def add(self, ctx, *args):
        """Add player(Play)"""
        players = player()
        player_names = players.player_names()
        player_names = [pname[0] for pname in player_names]
        for name in args:
            if name in player_names:
                players = player()
                count = players.player_count()
                if count > 0:
                    ##Should this allow lower case?
                    post.update_playing_status(name) 
                    print("Player is in:", name)
                    players = player()
                    count = players.player_count()
                    msg = f'{name} is on the team! There are {count} places remaining'
                    await ctx.send(msg)
                else:
                    msg = "Sorry there are no places left this week."
                    await ctx.send(msg)
            else:
                print(f'{name} doesnt exist!')
                await ctx.send(f'{name} is not in the db. Add him using command !new {name}')

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def rem(self, ctx, *args):
        """Remove player(Play)"""
        players = player()
        player_names = players.player_names()
        player_names = [pname[0] for pname in player_names]
        for name in args:
            if name in player_names:
                post.modify_playing_status(name)
                print("Player is out:", name)
                players = player()
                count = players.player_count()
                await ctx.send(f'We now have {count} places. Hopefully see you next week {name}')
            else:
                print(f'{name} doesnt exist!')
                await ctx.send(f'{name} is not in the db. Add him using command !new {name}')

    @commands.has_permissions(administrator=True)
    @commands.command()
    async def manplay(self, ctx, *args):
        """Manual(All list)"""
        file = discord.File("static/football.png")
        players = player()
        game_player_tally = players.game_player_tally_with_score_and_index()
        args_count = len(args) #Count the args to use in validation
        args = list(map(int, args)) #Convert all args in list to ints
        arg_match = all(i <= 10 for i in args) #True if all args are <= 10

        ##If no args added then send playing list so user can choose from list
        if not args: 
            await ctx.invoke(self.bot.get_command('play'))
        if args_count != 5:
            await ctx.send('You must enter 5 numbers')
        elif arg_match == False:
            await ctx.send('Number must be 1 - 10')
        else:
            #Get current result data ready to update results
            result = results()
            scorea = result.scorea()
            date = result.date()
            team_a, team_b, team_a_score, team_b_score = [], [], [], []
            for i, p, s in game_player_tally:
                if i in args:
                    team_a.append(p)
                    team_a_score.append(s)
                else:
                    team_b.append(p)
                    team_b_score.append(s)
            team_a_total = sum(team_a_score)
            team_b_total = sum(team_b_score)
            # Google Output
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
            embed=discord.Embed(
                title="Here are the teams:",
                url="http://football.richardbignell.co.uk",
                color=discord.Color.dark_green()
            )
            embed.add_field(name="TeamA (" 
                            + str(team_a_total) 
                            + "):", value=team_a, 
                            inline=True)
            embed.add_field(name="TeamB (" 
                            + str(team_b_total) 
                            + "):", value=team_b, 
                            inline=True)
            embed.set_thumbnail(url="attachment://football.png")
            embed.set_footer(text="Enter on the website if you prefer using the link above")
            await ctx.send(file = file, embed=embed)
            # Wait for user to enter SAVE
            await ctx.send("Type *SAVE* to store the results.")
            await ctx.send("*You need to save in 10 seconds or this team will be lost*")
            def check(m):
                return m.content == "SAVE" and m.channel == ctx.channel
            try:
                msg = await self.bot.wait_for("message", 
                                              timeout=10.0, check=check)
            except asyncio.TimeoutError: 
                print("Teams command timeout!")
                await ctx.send("You didnt type SAVE in 10 seconds. Run !man again")
                return
            else:
                if date == next_wednesday and scorea == "-":
                    result = post.update_result(google_output)
                    print("Running update function")
                    await ctx.send(f"Teams Saved!")
                else:
                    result = post.append_result(google_output)
                    print("Running append function")
                    await ctx.send(f"Teams Saved!")
                return

    @commands.has_permissions(administrator=True)
    @commands.command()
    async def manall(self, ctx, *args):
        """Manual(Play List)"""
        file = discord.File("static/football.png")
        players = player()
        all_players = players.all_players()
        game_player_tally = []
        num = 1
        for row in all_players:
            '''Takes in row of all_players 
            and returns list of game_players with index and score'''
            game_player_tally.append((num,row[0],row[1]))
            num = num+1
        args_count = len(args) #Count the args to use in validation
        args = list(map(int, args)) #Convert all args in list to ints
        # def match(args):
        #     for i in args:
        #         if re.match("(^[0-9]{1,2}$)", i):
        #             return False #I think this needs to be True
        #     return True

        #If no args added then send all players so user can choose from list
        if not args: 
            await ctx.invoke(self.bot.get_command('allplayers'))
        elif args_count != 10:
            await ctx.send('You must enter 10 numbers')
        else:
            #Get current result data ready to update results
            result = results()
            scorea = result.scorea()
            date = result.date()
            team_a, team_b, team_a_score, team_b_score = [], [], [], []
            for i, p, s in game_player_tally:
                if i in args[:5]:
                    team_a.append(p)
                    team_a_score.append(s)
                elif i in args[5:]:
                    team_b.append(p)
                    team_b_score.append(s)
            team_a_total = sum(team_a_score)
            team_b_total = sum(team_b_score)
            # Google Output
            google_output = []
            google_output.append((next_wednesday))
            google_output.append(str("-"))
            google_output.append(str("-"))
            google_output.append(int(team_a_total))
            google_output.append(int(team_b_total))
            google_output.extend((team_a))
            google_output.extend((team_b))
            print(google_output)
            team_a = "\n".join(item for item in team_a)
            team_b = "\n".join(item for item in team_b)
            # Embed Message
            embed=discord.Embed(
                title="Here are the teams:",
                url="http://football.richardbignell.co.uk",
                color=discord.Color.dark_green()
            )
            embed.add_field(name="TeamA (" 
                            + str(team_a_total) 
                            + "):", value=team_a, 
                            inline=True)
            embed.add_field(name="TeamB (" 
                            + str(team_b_total) 
                            + "):", value=team_b, 
                            inline=True)
            embed.set_thumbnail(url="attachment://football.png")
            embed.set_footer(text="Enter on the website if you prefer using the link above")
            await ctx.send(file = file, embed=embed)
            # Wait for user to enter SAVE
            await ctx.send("Type *SAVE* to store the results.")
            await ctx.send("*You need to save in 10 seconds or this team will be lost*")
            def check(m):
                return m.content == "SAVE" and m.channel == ctx.channel
            try:
                msg = await self.bot.wait_for("message", 
                                              timeout=10.0, check=check)
            except asyncio.TimeoutError: 
                print("Teams command timeout!")
                await ctx.send("You didnt type SAVE in 10 seconds. Run !man again")
                return
            else:
                if date == next_wednesday and scorea == "-":
                    result = post.update_result(google_output)
                    print("Running update function")
                    await ctx.send(f"Teams Saved!")
                else:
                    result = post.append_result(google_output)
                    print("Running append function")
                    await ctx.send(f"Teams Saved!")
                return

def setup(bot):
    bot.add_cog(AdminCommands(bot))