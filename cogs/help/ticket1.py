import discord
from discord.ext import commands


class ticket1(commands.Cog):

  def __init__(self, bot):
    self.bot = bot

  """Ticket commands"""

  def help_custom(self):
    emoji = '<:mail:1348340617935065240>'
    label = "Ticket"
    description = "Show You Ticket Commands"
    return emoji, label, description

  @commands.group()
  async def __Ticket__(self, ctx: commands.Context):
    """`ticket setup`, `ticket delete`, `ticket reopen` `ticket edit`"""
