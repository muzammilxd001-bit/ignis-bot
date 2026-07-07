import discord
from discord.ext import commands


class Leveling1(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    """Leveling Commands"""

    def help_custom(self):
        emoji = "<:up:1348326392537808928>"
        label = "Leveling"
        description = "Show You Commands Of Leveling"
        return emoji, label, description

    @commands.group()
    async def __leveling__(self, ctx: commands.Context):
        """`level help`, `level`, `setuplevelchannel`, `setlevel`, `resetlevel`, `addlevel`, `leaderboard`"""
