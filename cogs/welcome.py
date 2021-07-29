import discord
from discord.ext import commands

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
                Pay for your share via the Goals app.""",
            url="https://www.goalsfootball.co.uk/goals-app/",
            color=discord.Color.green()
        )
        print("Recognised that a member called " + member.name + " joined")
        try: 
            await member.send(embed=embed)
            print("Sent message to " + member.name)
        except:
            print("Couldn't message " + member.name)
            
        role = discord.utils.get(member.guild.roles, name="player")
        await member.add_roles(role)
        print("Added role '" + role.name + "' to " + member.name)

    @commands.Cog.listener()
    async def on_member_remove(self,member):
        print("Recognised that a member called " + member.name + " left")
        embed=discord.Embed(
            title="😢 Goodbye "+member.name+"!",
            description="You are welcome back anytime!",
            color=discord.Color.red()
        )
        try: 
            await member.send(embed=embed)
            print("Sent message to " + member.name)
        except:
            print("Couldn't message " + member.name)

def setup(bot):
    bot.add_cog(Welcome(bot))