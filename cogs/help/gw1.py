import discord
from discord.ext import commands


class gw1(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    """Giveaway Commands"""

    def help_custom(self):
        emoji = "<:gift:1348326523043840120>"
        label = "Giveaway"
        description = "Show You Commands Of Giveaway"
        return emoji, label, description

    @commands.group()
    async def __Giveaway__(self, ctx: commands.Context):
        """`gstart <time> <winner> <prize>` , `greroll <message id>` , `gend <message id>`"""
