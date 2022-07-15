import sqlite3

from discord.ext import commands
import discord


class aMarkovBot(commands.Bot):
    def __init__(self, logger):
        super().__init__("am:")
        self.logger = logger
        self.conn = sqlite3.connect('log.db')
        self.cursor = self.conn.cursor()

        initial_extensions = (
            'extensions.listener',
            'extensions.config'
            # 'extensions.help',
            # 'extensions.log_management'
        )

        for extension in initial_extensions:
            try:
                self.load_extension(extension)
            except Exception as e:
                self.logger.error(f'E (Loading extension {extension}): {e}')

        @self.event
        async def on_ready():
            self.logger.success(f'{self.user} has connected to Discord!')
            await self.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="you 👀"))
