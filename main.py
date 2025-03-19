import os

import dotenv
from discord.ext import commands

bot = commands.Bot("1dr#")

@bot.event
async def setup_hook():
    await bot.load_extension("cogs.record")

bot.run(os.getenv("discord"))