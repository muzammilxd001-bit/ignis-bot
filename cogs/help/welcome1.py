import discord
from discord.ext import commands


class welcome1(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    """Welcome commands"""

    def help_custom(self):
        emoji = "<:web_eart2:1348326507134713876>"
        label = "Welcomer"
        description = "Show You Commands Of Welcome"
        return emoji, label, description

    @commands.group()
    async def __Welcomer__(self, ctx: commands.Context):
        """`autorole bots add` , `autorole bots remove` , `autorole bots` , `autorole config` , `autorole humans add` , `autorole humans remove` , `autorole humans` , `autorole reset all` , `autorole reset bots` , `autorole reset humans` , `autorole reset` , `autorole`, `greet autodel` , `greet channel add` , `greet channel remove`, `greet channel` , `greet embed` , `greet image` , `greet message` , `greet ping` , `greet test` , `greet thumbnail` , `greet`"""
