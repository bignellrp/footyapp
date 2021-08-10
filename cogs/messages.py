from discord.ext import commands
from services.get_spread import player
from services.post_spread import _update_playing_status, _modify_playing_status #Could these be added to a class?

class Messages(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return
        if message.content.startswith('👍'):
            try:
                _update_playing_status(message.author.display_name)
                print("Player is in:", message.author.display_name)
                players = player()
                players = players.player_count() #Will this run the update?
                msg = f'You are on the team {message.author.display_name}. There are {players} places remaining'
                await message.channel.send(msg)
            except:
                print("Couldn't find player", message.author.display_name)
                msg = f"Couldn't find player {message.author.display_name}."
                await message.channel.send(msg)
        if message.content.startswith('👎'):
            try:
                _modify_playing_status(message.author.display_name)
                print("Player is out:", message.author.display_name)
                players = player()
                players = players.player_count()
                msg = f'Now we have {players} places left. Hopefully see you next week {message.author.display_name}'
                await message.channel.send(msg)
            except:
                print("Couldn't find player", message.author.display_name)
                msg = f"Couldn't find player {message.author.display_name}."
                await message.channel.send(msg)

def setup(bot):
    bot.add_cog(Messages(bot))