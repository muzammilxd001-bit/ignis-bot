import discord
from discord.ext import commands


class nsfw1(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    """NSFW commands"""

    def help_custom(self):
        emoji = "<:nsfw:1348340604559560816>"
        label = "Nsfw"
        description = ""
        return emoji, label, description

    @commands.group()
    async def __Nsfw__(self, ctx: commands.Context):
        """`nsfw` , `nsfw 4k` , `nsfw pussy` , `nsfw boobs` , `nsfw lewd` , `nsfw lesbian` , `nsfw blowjob` , `nsfw cum` , `nsfw gasm` , `nsfw hentai`"""
