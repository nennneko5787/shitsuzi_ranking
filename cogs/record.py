import json
from typing import Dict

import aiofiles
import discord
from discord.ext import commands

class RecordCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.records: Dict[int, int] = {}

    async def cog_load(self):
        async with aiofiles.open("records.json") as f:
            data = json.loads(await f.read())
            self.records = {int(k): v for k, v in data.items()}

    @commands.Cog.listener()
    async def on_guild_channel_create(self, channel: discord.TextChannel):
        if channel.name != "1day-chat":
            return

        def check(m):
            return m.author.id == 1178247997465837588 and m.channel == channel

        await self.bot.wait_for("message", check=check)

        def check(m):
            return m.channel == channel

        message = await self.bot.wait_for("message", check=check)
        if not message.author.id in self.records:
            self.records[message.author.id] = 0
        self.records[message.author.id] += 1

        async with aiofiles.open("records.json", "w+") as f:
            await f.write(json.dumps(self.records))

        await channel.send(f"{message.author.mention} さんが**{self.records[message.author.id]}**回目のコインロール獲得です！")

async def setup(bot: commands.Bot):
    await bot.add_cog(RecordCog(bot))