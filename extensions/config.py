import json

from discord.ext import commands
from .intermediate.serverhandler import accumulate, FileReturner

class Config(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.command(help="Turns the bot on and off. Specify anything other than 'act' or nothing and it will return the state of the bot without modifying anything.", aliases=['Toggle'])
    async def toggle(self, ctx, mode='act'):
        json_wrapper = accumulate(ctx.guild.id)[1]
        d_config = json.loads(json_wrapper.read())
        if mode == 'act':
            d_config['on'] = not d_config['on']
            json_wrapper.write(json.dumps(d_config, indent=2))
        await ctx.message.reply(f"Bot is {'disabled' if d_config['on'] == False else 'enabled'}.")


    @commands.command(help="Sets the channel in which the bot will listen and speak to the one the command was sent in.", aliases=['Setchannel', 'SetChannel', 'set_channel'])
    async def setchannel(self, ctx):
        json_wrapper = accumulate(ctx.guild.id)[1]
        d_config = json.loads(json_wrapper.read())
        channel = ctx.channel.id
        d_config['channel'] = channel
        json_wrapper.write(json.dumps(d_config, indent=2))
        await ctx.message.reply(f'Bot has been set to channel id {channel}.')


    @commands.command(help="Set probability for the bot to send a message after a server member sends a message. Specify anything other than 'act' or nothing and it will return the state of the bot without modifying anything.", aliases=['Setprobability', 'SetProbability', 'set_probability'])
    async def setprobability(self, ctx, probability, mode='act'):
        json_wrapper = accumulate(ctx.guild.id)[1]
        d_config = json.loads(json_wrapper.read())
        if int(probability) < 1 or int(probability) > 100:
            await ctx.message.reply('Error: You set a probability higher than 100 or lower than 1!')
        else:
            d_config['probability'] = probability
            json_wrapper.write(json.dumps(d_config, indent=2))
            await ctx.message.reply(f'Probability successfully set to {probability}.')


def setup(bot):
    bot.add_cog(Config(bot))