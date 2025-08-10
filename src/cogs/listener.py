import random

from discord import Message, command  # pyright: ignore[reportUnknownVariableType]
from discord.commands.context import ApplicationContext
from discord.ext.commands import Cog
from discord.utils import escape_mentions

from bot import aMarkovBot
from markovify import get_text
from loguru import logger

from sql import schema


class Listener(Cog):
    def __init__(self, bot: aMarkovBot):
        self.bot: aMarkovBot = bot

    def __get_markov(self, guild_id: int, should_escape_mentions: bool, equal_chance: bool) -> str:
        logger.trace("firing message!")
        log = schema.fetch_log(guild_id, self.bot.conn)

        if should_escape_mentions:
            log = [escape_mentions(message) for message in log]

        return get_text(
            "\n".join(log),
            random.randint(10, 50),  # TODO: Configure OR fine tune?
            equal_chance,
            100,
        )

    @Cog.listener()
    async def on_message(self, message: Message):
        if not message.author.bot and message.guild is not None:
            logger.trace(
                f"""valid message received content: {message.content}
                id: {message.id}
                author: {message.author.name} ({message.author.id})"""
            )

            con = self.bot.conn

            config = schema.fetch_config(message.guild.id, con)

            if config is None:
                return

            (id, probability, enabled, should_escape_mentions, equal_chance) = config

            schema.create_message(message, con)

            if enabled:
                rolled = random.uniform(0.0, 100.0)
                if rolled < float(probability):
                    await message.reply(content=self.__get_markov(id, should_escape_mentions, equal_chance))

    @command(description="Triggers a markov response.")
    async def trigger(
        self,
        ctx: ApplicationContext,
    ):
        res = schema.fetch_config(ctx.guild_id, self.bot.conn)

        if res is None:
            await ctx.respond("Bot is not initialized in this server", ephemeral=True)
            return

        id, probability, enabled, escape_mentions, equal_chance = res

        await ctx.respond(self.__get_markov(id, escape_mentions, equal_chance))


def setup(bot: aMarkovBot):
    bot.add_cog(Listener(bot))
