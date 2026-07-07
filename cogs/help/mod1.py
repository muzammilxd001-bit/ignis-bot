import discord
from discord.ext import commands


class mod1(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    """Moderation Commands"""

    def help_custom(self):
        emoji = "<:mod:1348326431737909260>"
        label = "Moderation"
        description = "Show You Commands Of Moderation"
        return emoji, label, description

    @commands.group()
    async def __Moderation__(self, ctx: commands.Context):
        """`purge` , `purge contains` , `purge startswith` , `purge invites` , `purge user <user>` , `mute <user>` , `unmute <user>` , `kick <user>` , `warn <user>` , `ban <user>` , `unban <user id>` , `clone` , `nick <user> <nick>` , `slowmode` , `unslowmode` , `clear <ammount>` , `clear all` , `clear bots` , `clear embeds` , `clear files` , `clear mentions` , `clear images` , `clear contains` , `clear reactions` , `nuke` , `lock` , `unlock` , `hide` , `unhide` , `hideall` ,` unhideall` , `audit` , `role` , `role temp` , `role remove` , `role delete` , `role create` , `role rename` , `enlarge` , `role humans` , `role bots` , `role all` , `removerole humans` , `roleicon`, `removerole bots` , `removerole all`"""
