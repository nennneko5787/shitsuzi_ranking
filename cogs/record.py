import discord
from discord.ext import commands

class RecordCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_guild_channel_create(channel: discord.TextChannel):
        if channel.name != "1day-chat":
            return

        def check(m):
            return m.author.id == 1178247997465837588 and m.channel == channel

        await self.bot.wait_for("message", check=check)

        def check(m):
            return m.channel == channel

        message = await self.bot.wait_for("message", check=check)

        await channel.send(f"{message.author.mention} さんがコインロールを手に入れました！")

async def setup(bot: commands.Bot):
    await bot.add_cog(RecordCog(bot))