import discord
from discord.ext import commands
from services.update_sheet import _add_new_player, _remove_player

class Welcome(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self,member):
        # Embed Message to send to new users
        embed=discord.Embed(
            title="Welcome "+member.name+"!",
            description="""Thank you for joining.
                Weekly poll will ask who is playing.
                Poll will be sent on Sunday morning.
                Games are played at 6:30pm at Goals.
                Normally pitch 10.
                Pay for your share via the
                [Goals App](https://www.goalsfootball.co.uk/goals-app/)""",
            color=discord.Color.green()
        )
        embed.set_thumbnail(
            url="https://e7.pngegg.com/pngimages/347/591/png-clipart-football-team-sport-ball-white-sport-thumbnail.png"
        )
        print("Recognised that a member called " + member.name + " joined")
        try: 
            await member.send(embed=embed)
            _add_new_player(member.name) #Running add new player func
            print('Added new player with a generic score of 77: {}'.format(member.name))
        except:
            print("Couldn't message " + member.name)
            
        role = discord.utils.get(member.guild.roles, name="player")
        await member.add_roles(role)
        print("Added role '" + role.name + "' to " + member.name)

    @commands.Cog.listener()
    async def on_member_remove(self,member):
        print("Recognised that a member called " + member.name + " left")
        try: 
            _remove_player(member.name) #Running add new player func
            print("Removed player " + member.name)
        except:
            print("Couldn't remove " + member.name)

def setup(bot):
    bot.add_cog(Welcome(bot))