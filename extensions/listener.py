import json
import random

from discord.ext import commands
from discord.utils import escape_mentions
from .intermediate.serverhandler import accumulate
from .intermediate.markovify import get_text

class Listener(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.Cog.listener()
    async def on_message(self, message):
        ctx = await self.bot.get_context(message)
        if not ctx.author.bot:
            if not ctx.message.content.startswith(self.bot.command_prefix):
                log_wrapper, json_wrapper = accumulate(ctx.guild.id)
                d_config = json.loads(json_wrapper.read())
                if d_config['channel'] == ctx.channel.id:
                    t_log = log_wrapper.read()
                    text = ctx.message.content
                    if not d_config['mentions']:
                        text = escape_mentions(text)
                    if not text == '':
                        t_log += f'\n{ctx.message.id}:{text}'
                    log_wrapper.write(t_log)
                    if d_config['on']:
                            probability = d_config['probability']
                            rolled = random.uniform(0.0, 100.0)
                            if rolled < float(probability):
                                await ctx.channel.send(get_text(t_log, random.randint(10, 50), d_config['equal_chance'], 100))


def setup(bot):
    bot.add_cog(Listener(bot))