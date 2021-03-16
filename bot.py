from discord.ext import commands


class aMarkovBot(commands.Bot):
    def __init__(self):
        super().__init__("am:")

        initial_extensions = (
            'extensions.listener',
            'extensions.config',
            'extensions.help'
        )

        for extension in initial_extensions:
            try:
                self.load_extension(extension)
            except Exception as e:
                print(f'E (Loading extension {extension}): {e}')

        @self.event
        async def on_ready():
            print(f'{self.user} has connected to Discord!')
