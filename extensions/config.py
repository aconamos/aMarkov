import json

from discord.ext import commands
from .intermediate.serverhandler import accumulate, FileReturner

class Config(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.command()
    async def toggle(self, ctx, mode='act'):
        """

        """
        json_wrapper = accumulate(ctx.guild.id)[1]
        s_config = json_wrapper.read()
        d_config = json.loads(s_config)
        if mode == 'act':
            d_config['on'] = not d_config['on']

        await ctx.message.reply(f"Bot is {'disabled' if d_config['on'] == False else 'enabled'}!")
        s_config = json.dumps(d_config)
        json_wrapper.write(s_config)


def setup(bot):
    bot.add_cog(Config(bot))