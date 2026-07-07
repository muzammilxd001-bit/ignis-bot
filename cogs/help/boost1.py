import discord
from discord.ext import commands


class boost1(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    """BoostMessage commands"""

    def help_custom(self):
        emoji = "<:boost:1348326410682372126>"
        label = "BoostMessage"
        description = "Show You BoostMessage Commands"
        return emoji, label, description

    @commands.group()
    async def __BoostMessage__(self, ctx: commands.Context):
        """`boostrole add` , `boostrole remove` , `boostrole config` , `boostrole reset` , `boost channel add` , `boost channel remove` , `boost channel` , `boost embed` , `boost image` , `boost message` , `boost ping` , `boost test` , `boost thumbnail` , `boost autodel` , `boost`"""
