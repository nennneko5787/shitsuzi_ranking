import json
import io
from typing import Dict

import aiofiles
import discord
from discord.ext import commands
from PIL import Image, ImageDraw, ImageFont

class RecordCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.records: Dict[int, int] = {}

    async def cog_load(self):
        async with aiofiles.open("records.json") as f:
            data = json.loads(await f.read())
            self.records = {int(k): v for k, v in data.items()}

    @commands.command()
    async def ranking(self, ctx: commands.Context):
        sortedRecords = sorted(self.records.items(), key=lambda x: x[1], reverse=True)[:5]
    
        # ユーザー名を取得
        users = []
        for user_id, count in sortedRecords:
            try:
                user = await ctx.guild.fetch_member(user_id)
                users.append((user.name, count))
            except:
                users.append((str(user_id), count))
    
        # 画像作成
        width, height = 600, 300
        img = Image.new("RGB", (width, height), color=(255, 255, 255))
        draw = ImageDraw.Draw(img)
        font = ImageFont.truetype("arial.ttf", 24)  # フォントは環境に合わせて変更
    
        title_font = ImageFont.truetype("arial.ttf", 28)
        draw.text((width // 2 - 120, 20), "🏆 コインロールランキング TOP5 🏆", font=title_font, fill=(0, 0, 0))
    
        y_offset = 80
        for i, (name, count) in enumerate(users):
            draw.text((50, y_offset), f"{i+1}位: {name} - {count}回", font=font, fill=(0, 0, 0))
            y_offset += 40
    
        # バッファに保存
        buffer = io.BytesIO()
        img.save(buffer, format="PNG")
        buffer.seek(0)
    
        file = discord.File(fp=buffer, filename="ranking.png")
        await ctx.reply(file=file, silent=True)

    @commands.Cog.listener()
    async def on_guild_channel_create(self, channel: discord.TextChannel):
        if channel.name != "1day-chat":
            return

        def check(m):
            return m.author.id == 1362354606923059322 and m.channel == channel

        message = await self.bot.wait_for("message", check=check)

        before = message.created_at.timestamp()

        def check(m):
            return m.channel == channel

        message = await self.bot.wait_for("message", check=check)
        if not message.author.id in self.records:
            self.records[message.author.id] = 0
        self.records[message.author.id] += 1

        async with aiofiles.open("records.json", "w+") as f:
            await f.write(json.dumps(self.records))

        between = message.created_at.timestamp() - before
        await channel.send(f"{message.author.mention} さんが**{self.records[message.author.id]}**回目のコインロール獲得です！")
        await channel.send(f"タイム: {between}秒")

async def setup(bot: commands.Bot):
    await bot.add_cog(RecordCog(bot))