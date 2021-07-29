import discord
from discord.ext import commands

class Welcome(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self,member):
        # Customise the message below to what you want to send new users!
        newUserMessage = """
        Welcome to the Footapp channel.
        Weekly poll will ask who is playing.
        Poll will be sent on Sunday morning.
        Games are played at 6:30pm at Goals.
        Normally pitch 10.
        Pay for your share via the Goals app.
        """
        print("Recognised that a member called " + member.name + " joined")
        try: 
            await self.bot.send_message(member, newUserMessage)
            print("Sent message to " + member.name)
        except:
            print("Couldn't message " + member.name)
        embed=discord.Embed(
            title="Welcome "+member.name+"!",
            description="We're so glad you're here!",
            color=discord.Color.green()
        )
            
        role = discord.utils.get(member.server.roles, name="name-of-your-role") #  Gets the member role as a `role` object
        await self.bot.add_roles(member, role) # Gives the role to the user
        print("Added role '" + role.name + "' to " + member.name)

    @commands.Cog.listener()
    async def on_member_leave(self,member):
        print("Recognised that a member called " + member.name + " left")
        embed=discord.Embed(
            title="😢 Goodbye "+member.name+"!",
            description="Until we meet again old friend.", # A description isn't necessary, you can delete this line if you don't want a description.
            color=discord.Color.red() # There are lots of colors, you can check them here: https://discordpy.readthedocs.io/en/latest/api.html?highlight=discord%20color#discord.Colour
        )

def setup(bot):
    bot.add_cog(Welcome(bot))