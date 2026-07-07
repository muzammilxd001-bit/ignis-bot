import discord
from discord.ext import commands


class VoiceChannelManager1(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    """JoinToCreate Commands"""

    def help_custom(self):
        emoji = "<:speak1:1348340478264873034>"
        label = "Join To Create"
        description = "Show You Commands Of Join To Create"
        return emoji, label, description

    @commands.group()
    async def __JoinToCreate__(self, ctx: commands.Context):
        """`j2c setup`"""
