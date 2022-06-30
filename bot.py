from discord.ext import commands


class aMarkovBot(commands.Bot):
    def __init__(self, logger):
        super().__init__("am:")
        self.logger = logger

        initial_extensions = (
            'extensions.listener',
            'extensions.config',
            'extensions.help',
            'extensions.log_management'
        )

        for extension in initial_extensions:
            try:
                self.load_extension(extension)
            except Exception as e:
                self.logger.error(f'E (Loading extension {extension}): {e}')

        @self.event
        async def on_ready():
            self.logger.success(f'{self.user} has connected to Discord!')
