import json
import random

from discord import ChannelType, Message
import discord
from discord.ext import commands
from discord.utils import escape_mentions
from serverhandler import get_json_wrapper

from bot import aMarkovBot
from markovify import get_text
from loguru import logger

from sql import schema


class Listener(commands.Cog):
    def __init__(self, bot):
        self.bot: aMarkovBot = bot

    @discord.Cog.listener()
    async def on_message(self, message: Message):
        if not message.author.bot and message.guild is not None:
            logger.trace(f"""
valid message received
content: {message.content}
id: {message.id}
author: {message.author.name} ({message.author.id})""")

            con = self.bot.conn

            res = con.execute(f"""
            SELECT *
            FROM servers
            WHERE
                id = {message.guild.id}
                ;
            """).fetchone()

            if res is None:
                logger.trace("server is not configured, not proceeding")
                return

            id, probability, enabled, mentioned, equal_chance = res

            logger.debug(f"""server configuration: 
{id}
{probability}
{enabled}
{mentioned}
{equal_chance}""")

            schema.create_message(message, con)

            return
            if message.channel.type == ChannelType.text:
                if d_config["channel"] == message.channel.id:
                    # Insert text into database
                    text = message.content
                    if not text == "":
                        text = escape_mentions(text)
                        cur.execute(
                            f"INSERT INTO S{message.guild.id} (ID, CHANNEL_ID, CONTENT) VALUES ({message.id},{message.channel.id},?)",
                            (text,),
                        )
                        con.commit()

                    # Reply
                    if d_config["on"]:
                        probability = d_config["probability"]
                        rolled = random.uniform(0.0, 100.0)
                        if rolled < float(probability):
                            c_log = cur.execute(
                                f"SELECT CONTENT FROM S{message.guild.id} WHERE CHANNEL_ID = {message.channel.id}"
                            )
                            t_log = [row[0] for row in c_log]
                            await message.channel.send(
                                get_text(
                                    "\n".join(t_log),
                                    random.randint(10, 50),
                                    d_config["equal_chance"],
                                    100,
                                )
                            )


def setup(bot):
    bot.add_cog(Listener(bot))
