import discord
from discord.ext import commands


class pfps1(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    """Pfp Commands"""

    def help_custom(self):
        emoji = "<:atom:1348326466210889821>"
        label = "Pfp"
        description = "Show You Commands Of Pfp"
        return emoji, label, description

    @commands.group()
    async def __Pfp__(self, ctx: commands.Context):
        """`pic`, `boys` , `girls`, `couples`, `anime`"""
