import discord
from discord.ext import commands


class games1(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    """Games/Fun commands"""

    def help_custom(self):
          emoji = '<:games:1348326482241523742>'
          label = "Games/Fun"
          description = "Show You Commands Of Games"
          return emoji, label, description

    @commands.group()
    async def __Games__(self, ctx: commands.Context):
        """ `chess` , `hangman` , `typerace` , `rps` , `reaction` , `tick-tack-toe` , `wordle` , `2048` , `memory-game` , `number-slider` , `battleship` , `country-guesser`\n\n
        __Fun__\n `tickle` , `kiss` , `hug` , `slap` , `pat` , `feed` , `pet` , `howgay` , `slots` , ` HowCute` , `meme` , `cat` , `iplookup` , `nitro`"""