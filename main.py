import os

import dotenv
from discord.ext import commands

bot = commands.Bot("1dr#")

bot.run(os.getenv("discord"))