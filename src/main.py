import sqlite3
import sys
import bot

from os import getenv
from dotenv import load_dotenv
from loguru import logger
from sql import schema

load_dotenv()


@logger.catch(message="Couldn't initialize bot!")
def main():
    logger.remove()
    logger.add(sys.stdout, level="TRACE")

    TOKEN = getenv("TOKEN")

    if TOKEN is None:
        raise Exception("Missing TOKEN in environment!")

    connection = sqlite3.connect("data/amarkov.db")
    schema.write_schema(connection)

    client = bot.aMarkovBot(connection)

    client.run(TOKEN)


main()
