from discord.ext import commands, tasks
import asyncio
import datetime as dt

class Login(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        """Adds a message to the log when the bot logs in."""
        print(f"{self.bot.user.name} logged in successfully")
    #     self.msg1.start()
    
    # # Message 1
    # # https://stackoverflow.com/questions/63769685/discord-py-how-to-send-a-message-everyday-at-a-specific-time
    # @tasks.loop(hours=24)
    # async def msg1(self):
    #     message_channel = self.bot.get_channel(868980424955801681)
    #     await message_channel.send("Hello this is your helpful footybot")

    # @msg1.before_loop
    # async def before_msg1(self):
    #     for _ in range(60*60*24):  # loop the whole day
    #         if dt.datetime.now().hour == 19+10:  # 24 hour format
    #             print('It is time')
    #             return
    #         await asyncio.sleep(1)# wait a second before looping again. You can make it more 

def setup(bot):
    bot.add_cog(Login(bot))