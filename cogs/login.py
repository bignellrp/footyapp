from discord.ext import commands

class Login(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        """Adds a message to the log when the bot logs in."""
        print(f"{self.bot.user.name} logged in successfully")

def setup(bot):
    bot.add_cog(Login(bot))