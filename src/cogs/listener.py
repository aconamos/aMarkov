import json
import random

from discord import ChannelType, Message
import discord
from discord.ext import commands
from discord.utils import escape_mentions
from serverhandler import get_json_wrapper

from bot import aMarkovBot
from markovify import get_text


class Listener(commands.Cog):
    def __init__(self, bot):
        self.bot: aMarkovBot = bot

    @discord.Cog.listener()
    async def on_message(self, message: Message):
        # ctx = await self.bot.get_context(
        # message
        # )
        self.bot.logger.debug(message)

        if not message.author.bot and message.guild is not None:
            if message.channel.type == ChannelType.text:
                # SQL Connection
                cur = self.bot.cursor
                con = self.bot.conn
                cur.execute(
                    f"CREATE TABLE if not exists S{message.guild.id} (ID INT PRIMARY KEY NOT NULL, CHANNEL_ID INT NOT NULL, CONTENT TEXT NOT NULL)"
                )
                con.commit()

                # Get configuration
                json_wrapper = get_json_wrapper(message.guild.id)
                d_config = json.loads(json_wrapper.read())

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
