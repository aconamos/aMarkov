from os import getenv
from dotenv import load_dotenv
from loguru import logger

import sqlite3
import bot
import readline  # noqa: F401

load_dotenv()


@logger.catch(message="Couldn't initialize bot!")
def main():
    TOKEN = getenv("TOKEN")

    if TOKEN is None:
        raise Exception("Missing TOKEN in environment!")

    connection = sqlite3.connect("data/amarkov.db")

    client = bot.aMarkovBot(logger, connection)

    client.run(TOKEN)


main()
