import discord
from discord.ext import commands


class marrige1(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    """Marrige Commands"""

    def help_custom(self):
        emoji = "<:heart:1348340513719193612>"
        label = "Marrige"
        description = "Show You Commands Of Marrige"
        return emoji, label, description

    @commands.group()
    async def __Marrige__(self, ctx: commands.Context):
        """`propose` , `accept` , `decline` , `marrige` , `divorce`"""
