import random
import threading
from functools import wraps

import discord
from discord import app_commands
from discord.ext import commands

from utils import point_utils

# 定義賭博的機率和對應的點數變化
gamble_outcomes = {
    "lose_all": -1,
    "lose_10": -0.1,
    "lose_20": -0.2,
    "lose_90": -0.9,
    "gain_10": 0.1,
    "gain_50": 0.5,
    "gain_100": 1.0,
    "gain_900": 9.0,
}

gamble_probabilities = [1, 30, 15, 6, 35, 8, 3, 2]  # 對應賭博結果的機率（總和應該為100）

lock_dict = {}

def lock(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        user_id = args[1]
        if user_id not in lock_dict:
            lock_dict[user_id] = threading.Lock()
            with lock_dict[user_id]:
                return func(self, *args, **kwargs)
        else:
            print("請稍後再試")

    return wrapper

class Gamble(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    # @app_commands.command(name="賭博", description="點數有機率 -10%, -20%, -90%, -100%, +10%, +50%, +100%, +300%")
    # async def gamble_slash(self, interaction: discord.Interaction):
    #     # 回覆使用者的訊息
    #     await interaction.response.send_message("Hello, world!")

    @commands.command(aliases=["賭"])
    async def 賭博(self, ctx: commands.Context, count=1):
        return await self._exec_gamble(ctx, ctx.author.id, count= count)

    @point_utils.transaction
    @lock
    async def _exec_gamble(self, ctx_or_interaction, user_id, count):
        point = point_utils.get_point(user_id)

        if point is not None and point <= 0:
            return await self.__send_replay(ctx_or_interaction, "你目前沒有積分紀錄。")

        message = f"原始的賭博積分：{point} 你的賭博的結果如下：\n"

        for i in range(count):
            gamble_result = random.choices(list(gamble_outcomes.keys()), weights=gamble_probabilities, k=1)[0]
            point_change = gamble_outcomes[gamble_result]
            change_amount = int(point * point_change)
            point += change_amount

            message += f"第 {i + 1} 次: **{gamble_result}**，變動 {change_amount} 點。\n"

        updated_points = max(point, 0)
        point_utils.update_point(user_id, updated_points)
        return await self.__send_replay(ctx_or_interaction, message + f"連賭結束，目前積分: {updated_points} 點。")

    async def __send_replay(self, ctx_or_interaction, message: str):
        if isinstance(ctx_or_interaction, commands.Context):
            return await ctx_or_interaction.reply(message)
        elif isinstance(ctx_or_interaction, discord.Interaction):
            return await ctx_or_interaction.response.send_message(message)


# Cog 載入 Bot 中
async def setup(bot: commands.Bot):
    await bot.add_cog(Gamble(bot))
    print('賭博指令載入完成')

# message = f"原始的賭博積分：{point} 你的賭博的結果如下：\n"
#
# for i in range(count):
#     gamble_result = random.choices(list(gamble_outcomes.keys()), weights=gamble_probabilities, k=1)[0]
#     point_change = gamble_outcomes[gamble_result]
#     change_amount = int(point * point_change)
#     point += change_amount
#
#     message += f"第 {i + 1} 次: **{gamble_result}**，變動 {change_amount} 點。\n"
#
# updated_points = max(point, 0)
# point_utils.update_point(user_id, updated_points)
# await self.__send_replay(ctx_or_interaction, message + f"連賭結束，目前積分: {updated_points} 點。")

# message = await self.__send_replay(ctx_or_interaction, f"原始的賭博積分：{point} 你的賭博的結果如下：\n")
#
# for i in range(count):
#     gamble_result = random.choices(list(gamble_outcomes.keys()), weights=gamble_probabilities, k=1)[0]
#     point_change = gamble_outcomes[gamble_result]
#     change_amount = int(point * point_change)
#     point += change_amount
#
#     message = await message.edit(content=message.content + "\n" + f"第 {i + 1} 次: **{gamble_result}**，變動 {change_amount} 點。\n")
#
# updated_points = max(point, 0)
# point_utils.update_point(user_id, updated_points)
# await message.edit(content=message.content + f"連賭結束，目前積分: {updated_points} 點。")
