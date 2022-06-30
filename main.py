from os import getenv
from dotenv import load_dotenv
from loguru import logger

import bot

load_dotenv()

@logger.catch
def main():
    TOKEN = getenv('TOKEN')

    client = bot.aMarkovBot(logger)

    client.run(TOKEN)
    

main()