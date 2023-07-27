from discord.ext import commands
from services.get_spread import player
import services.post_spread as post
from services.lookup import lookup
from services.get_oscommand import GITBRANCH, IFBRANCH

class Messages(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        '''If branch is dev then use the dev channel id
        This prevents the two bots conflicting with each other'''
        ##Rewite to use lookup
        prod = False
        if prod:
            CHANNEL_ID = lookup("channel_id")
        else:
            CHANNEL_ID = lookup("channel_id_dev")
        CHANNEL_ID = int(CHANNEL_ID) #Wasnt matching channel.id as a string
        '''If message starts with thumbsup then 
        add the player to the playing list'''
        if message.author == self.bot.user:
            return
        if message.content.startswith('👍') and message.channel.id == CHANNEL_ID:
            try:
                players = player()
                count = players.player_count()
                if count > 0:
                    post.update_playing_status(message.author.display_name)
                    print("Player is in:", message.author.display_name)
                    players = player()
                    count = players.player_count()
                    msg = f'You are on the team {message.author.display_name}. There are {count} places remaining'
                    await message.channel.send(msg)
                else:
                    msg = "Sorry there are no places left this week."
                    await message.channel.send(msg)
            except:
                print("Couldn't find player", message.author.display_name)
                msg = f"Couldn't find player {message.author.display_name}."
                await message.channel.send(msg)
        if message.content.startswith('👎') and message.channel.id == CHANNEL_ID:
            '''If message starts with thumbsdown then 
            remove the player to the playing list'''
            try:
                post.modify_playing_status(message.author.display_name)
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