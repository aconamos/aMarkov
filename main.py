from os import getenv
from dotenv import load_dotenv

import bot

load_dotenv()
TOKEN = getenv('TOKEN')

client = bot.aMarkovBot()

client.run(TOKEN)