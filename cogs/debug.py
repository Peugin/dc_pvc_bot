import discord
from discord import app_commands
from discord.ext import commands

from utils import point_utils


class Debug(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command()
    async def debug(self, ctx: commands.Context):
        point_utils.update_point(ctx.author.id, 100)


# Cog 載入 Bot 中
async def setup(bot: commands.Bot):
    await bot.add_cog(Debug(bot))
    print('除錯指令載入完成')
