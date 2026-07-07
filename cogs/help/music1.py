import discord
from discord.ext import commands


class music1(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    """Music commands"""

    def help_custom(self):
        emoji = "<:music:1348340499647430777>"
        label = "Music"
        description = "Show You Commands Of Music"
        return emoji, label, description

    @commands.group()
    async def __Music__(self, ctx: commands.Context):
        """`play` , `connect` , `disconnect` , `stop` , `skip`   ,  `pause` ,  `resume` , `bassboost`  , `move` , `volume` , `nowplaying` , `shuffle` , `pull` , `queue` , `queue clear` , `seek`"""
