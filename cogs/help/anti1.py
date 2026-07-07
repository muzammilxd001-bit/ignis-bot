import discord
from discord.ext import commands


class anti1(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    """AntiNuke Commands"""

    def help_custom(self):
        emoji = "<:thunder:1348326374493917214>"
        label = "AntiNuke"
        description = "Show You Commands Of Antinuke"
        return emoji, label, description

    @commands.group()
    async def __Antinuke__(self, ctx: commands.Context):
        """`antinuke` , `antinuke enable` , `antinuke disable` , `whitelist` , `whitelist @user` , `unwhitelist` , `whitelisted` , `whitelist reset` , `extraowner` , `extraowner set` , `extraowner view` , `extraowner reset`, `nightmode` , `nightmode enable` , `nightmode disable`\n\n__**Emergency Situation**__\n`emergency` , `emergency enable` , `emergency disable` , `emergency role` , `emergency role add` , `emergency role remove` , `emergency role list` , `emergency authorise` , `emergency authorise add` , `emergency authorise remove` , `emergency authorise list`\n`emergency-situation (emgs)`"""
