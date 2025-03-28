from datetime import datetime
from zoneinfo import ZoneInfo

import discord
from discord.ext import commandz tasks

class OneDayChatCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        
    @tasks.loop(seconds=1)
    async def dayChat(self):
        pass # いつかじっそうするめんどうすぎる

async def setup(bot: commands.Bot):
    await bot.add_cog(OneDayChatCog(bot))