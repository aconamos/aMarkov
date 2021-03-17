import json

from discord.ext import commands
from .intermediate.serverhandler import accumulate

class Config(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.command()
    async def toggle(self, ctx, mode='act'):
        """

        """
        f_config = accumulate(ctx.guild.id)[1]
        d_config = json.load(f_config)
        if mode == 'act':
            """
            Send Message
            """
            d_config['on'] = not d_config['on']

        await ctx.message.reply(f"Bot is {'disabled' if d_config['on'] == False else 'enabled'}!")
        json.dump(d_config, f_config)


def setup(bot):
    bot.add_cog(Config(bot))