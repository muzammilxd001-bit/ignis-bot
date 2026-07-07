import discord
from discord.ext import commands


class automod1(commands.Cog):

  def __init__(self, bot):
    self.bot = bot

  """AutoMod Commands"""

  def help_custom(self):
    emoji = '<:hammer:1348326417854890004>'
    label = "AutoMod"
    description = "Show You Commands Of AutoMod"
    return emoji, label, description

  @commands.group()
  async def __AutoMod__(self, ctx: commands.Context):
    """`automod` , `automod enable` , `automod disable` , `automod punishment` , `autmod config` , `automod logging` `automod ignore` , `automod ignore channel` , `automod ignore role` , `automod ignore show` , `automod ignore reset` , `automod unignore` , `automod unignore channel` , `automod unignore role`
    \n\n__**Blacklistword Commands**__\n`blacklistword` , `blacklistword add <word>` , `blacklistword remove <word>` , `blacklistword reset` , `blacklistword config` , `blacklistword bypass add <user/role>` , `blacklistword bypass remove <user/role>` , `blacklistword bypass show`"""