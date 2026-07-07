import discord
from discord.ext import commands


class owner2(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    """Premium commands"""

    def help_custom(self):
        emoji = "<a:diamond:1348872355031683084>"
        label = "Premium"
        description = "Show You Commands Of Premium"
        return emoji, label, description

    @commands.group()
    async def __Premium__(self, ctx: commands.Context):
        """**WE GIVE YOU ALL PREMIUM FEATURES FOR FREE!!. BUT YOU CAN DONATE US FOR MORE INFO JOIN OUR [SUPPORT SERVER](https://discord.gg/nakhre)**"""
