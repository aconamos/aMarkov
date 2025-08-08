import sqlite3
import discord
import loguru


bot_intents = discord.Intents.default()
bot_intents.message_content = True


class aMarkovBot(discord.Bot):
    def __init__(self, logger, connection):
        super().__init__(intents=bot_intents)
        self.logger: loguru.Logger = logger
        self.conn: sqlite3.Connection = connection
        self.cursor = self.conn.cursor()

        initial_extensions = (
            "cogs.listener",
            # "cogs.config",
            # 'cogs.help',
            # 'cogs.log_management'
        )

        for extension in initial_extensions:
            try:
                self.load_extension(extension)
            except Exception as e:
                self.logger.error(f"E (Loading extension {extension}): {e}")

        @self.listen()
        async def on_ready():
            self.logger.success(f"{self.user} has connected to Discord!")
            await self.change_presence(
                activity=discord.Activity(
                    type=discord.ActivityType.watching, name="you 👀"
                )
            )
