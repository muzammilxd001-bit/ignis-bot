import discord
from discord.ext import commands


class ai1(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    """Ai Commands"""

    def help_custom(self):
        emoji = "<:mail2:1263546290109812820>"
        label = "Ai"
        description = "Show You Commands Of Logging"
        return emoji, label, description

    @commands.group()
    async def __Ai__(self, ctx: commands.Context):
        """`setaichannel`"""
