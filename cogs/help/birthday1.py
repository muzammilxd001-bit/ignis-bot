import discord
from discord.ext import commands


class fun1(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    """Birthday Commands"""

    def help_custom(self):
        emoji = "<:circle2:1348326520581521469>"
        label = "Birthday"
        description = "Show You Commands Of Birthday"
        return emoji, label, description

    @commands.group()
    async def __Birthday__(self, ctx: commands.Context):
        """`birthday`, `birthdaysetup`, , `setbirthday` , `removebirthday` , `listbirthdays`"""
