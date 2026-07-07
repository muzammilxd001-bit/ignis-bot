import discord
from discord.ext import commands


class voice1(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    """Voice commands"""

    def help_custom(self):
        emoji = "<:mic:1348326446216515604>"
        label = "Voice/VC Roles/J2C"
        description = "Show You Commands Of Voice"
        return emoji, label, description

    @commands.group()
    async def __Voice__(self, ctx: commands.Context):
        """`voice` , `voice kick` , `voice kickall` , `voice mute` , `voice muteall` , `voice unmute` , `voice unmuteall` , `voice deafen` , `voice deafenall` , `voice undeafen` , `voice undeafenall` , `voice moveall`\n\n
        __VC Roles__\n `vcrole` , `vcrole bots add` , `vcrole bots remove` , `vcrole bots` , `vcrole config` , `vcrole humans add` , `vcrole humans remove` , `vcrole humans` , `vcrole reset`\n\n
        __Join To Create__\n `j2c setup` , `j2c config` , `j2c reset`"""
