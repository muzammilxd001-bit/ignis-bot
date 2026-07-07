import discord
from discord.ext import commands


class general1(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    """General Commands"""

    def help_custom(self):
        emoji = "<:earth:1348327194342199409>"
        label = "General"
        description = "Show You Commands Of General"
        return emoji, label, description

    @commands.group()
    async def __General__(self, ctx: commands.Context):
        """`afk`, `gafk` , `avatar` , `banner` , `servericon` , `membercount` , `poll` , `hack` , `token` , `users` , `italicize` , `strike` , `quote` , `code` , `bold` , `censor` , `underline` , `gender` , `wizz` , `pikachu` , `shorten` , `urban` , `rickroll` , `hash` , `snipe` , `roleall` , `embed`"""
