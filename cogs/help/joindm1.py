import discord
from discord.ext import commands


class joindm1(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    """Join Dm Commands"""

    def help_custom(self):
        emoji = "<:msg:1348326387873873960>"
        label = "Join Dm"
        description = "Show You Commands Of Join Dm"
        return emoji, label, description

    @commands.group()
    async def __JoinDM__(self, ctx: commands.Context):
        """`joindm enable`, `joindm disable`, `joindm message`"""
