import json
import random

from discord import ChannelType
from discord.ext import commands
from discord.utils import escape_mentions
from .intermediate.serverhandler import get_json_wrapper
from .intermediate.markovify import get_text

class Listener(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.Cog.listener()
    async def on_message(self, message):
        ctx = await self.bot.get_context(message) #im being dumb here and i just saw this code. i don't care. it works.
        if not ctx.author.bot:
            if not ctx.message.content.startswith(self.bot.command_prefix) and ctx.message.channel.type == ChannelType.text:
                # SQL Connection
                cur = self.bot.cursor
                con = self.bot.conn
                cur.execute(f'CREATE TABLE if not exists S{ctx.message.guild.id} (ID INT PRIMARY KEY NOT NULL, CHANNEL_ID INT NOT NULL, CONTENT TEXT NOT NULL)')
                con.commit()
                
                # Get configuration
                json_wrapper = get_json_wrapper(ctx.guild.id)
                d_config = json.loads(json_wrapper.read())
                
                if d_config['channel'] == ctx.channel.id:
                    # Insert text into database
                    text = ctx.message.content
                    if not text == '':
                        text = escape_mentions(text)
                        cur.execute(f'INSERT INTO S{ctx.message.guild.id} (ID, CHANNEL_ID, CONTENT) VALUES ({ctx.message.id},{ctx.message.channel.id},?)', (text,)) 
                        con.commit()
                        
                    # Reply
                    if d_config['on']:
                            probability = d_config['probability']
                            rolled = random.uniform(0.0, 100.0)
                            if rolled < float(probability):
                                c_log = cur.execute(f'SELECT CONTENT FROM S{ctx.message.guild.id} WHERE CHANNEL_ID = {ctx.message.channel.id}')
                                t_log = [row[0] for row in c_log]
                                await ctx.channel.send(get_text('\n'.join(t_log), random.randint(10, 50), d_config['equal_chance'], 100))


def setup(bot):
    bot.add_cog(Listener(bot))