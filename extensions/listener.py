import json

from discord.ext import commands
from .intermediate.serverhandler import accumulate, FileReturner

class Listener(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.Cog.listener()
    async def on_message(self, ctx):
        if not ctx.author.bot: 
            log_wrapper, json_wrapper = accumulate(ctx.guild.id)
            d_config = json.loads(json_wrapper.read())
            if d_config['on']:
                if d_config['channel'] == ctx.channel.id:
                    t_log = log_wrapper.read()
                    t_log += f'\n{ctx.content}'
                    
                    log_wrapper.write(t_log)


def setup(bot):
    bot.add_cog(Listener(bot))