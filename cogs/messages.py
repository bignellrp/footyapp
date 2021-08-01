from discord.ext import commands
from services.get_players import _get_players_table, _fetch_players_table
from services.update_sheet import _update_playing_status, _modify_playing_status

class Messages(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return
        if message.content.startswith('👍'):
            print("Player is in:", message.author.name)
            _update_playing_status(message.author.name)
            _,_,_,_,player_count,_ = _get_players_table(_fetch_players_table())
            msg = f'You are on the team {message.author.mention}. There are {player_count} places remaining'
            await message.channel.send(msg)
        if message.content.startswith('👎'):
            print("Player is out:", message.author.name)
            _modify_playing_status(message.author.name)
            _,_,_,_,player_count,_ = _get_players_table(_fetch_players_table())
            msg = f'Now we have {player_count} places left. Hopefully see you next week {message.author.mention}'
            await message.channel.send(msg)

def setup(bot):
    bot.add_cog(Messages(bot))