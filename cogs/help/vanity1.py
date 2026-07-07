import discord
from discord.ext import commands


class vanity1(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    """Vanityroles Commands"""

    def help_custom(self):
        emoji = "<:cricle1:1348326512482455603>"
        label = "Vanityroles"
        description = "Show You Commands Of Vanityroles"
        return emoji, label, description

    @commands.group()
    async def __Vanityroles__(self, ctx: commands.Context):
        """`vanityroles setup` , `vanityroles show` , `vanityroles reset`"""
