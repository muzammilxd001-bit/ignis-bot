import discord
from discord.ext import commands


class invites1(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    """Invites Commands"""

    def help_custom(self):
        emoji = "<:atom:1348326466210889821>"
        label = "Invites"
        description = "Show You Commands Of Invites"
        return emoji, label, description

    @commands.group()
    async def __Invites__(self, ctx: commands.Context):
        """`invites`, `addinvites`, `resetinvites`, `removeinvites`, `resetserverinvites`, `setinvitechannellog`,"""
