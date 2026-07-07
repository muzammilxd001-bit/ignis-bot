import discord
from discord.ext import commands


class all(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    """Extra Commands"""

    def help_custom(self):
        emoji = "<:mail2:1263546290109812820>"
        label = "Extra Commands"
        description = "Show Extra Commands Of Bot"
        return emoji, label, description

    @commands.group()
    async def __Extraa__(self, ctx: commands.Context):
        """`setupj2c`, `joindm enable`, `joindm disable`, `joindm message`, `autosnipe`, `birthdaysetup`, `setbirthday`, `removebirthday`, `listbirthdays`, `birthday`, `ignore` `propose` , `accept` , `decline` , `marrige` , `divorce`, `media`, `media setup`, `media remove`, `media config`, `media reset`, `audit` , `role` , `role temp` , `role remove` , `role delete` , `role create` , `role rename` , `enlarge` , `vanityroles setup` , `vanityroles show` , `vanityroles reset`, `verification enable` , `verification disable` , `verification config`, `yt setup` , `ytconfig` , `ytremove`, `nsfw` , ||`nsfw 4k` , `nsfw pussy` , `nsfw boobs` , `nsfw lewd` , `nsfw lesbian` , `nsfw blowjob` , `nsfw cum` , `nsfw gasm` , `nsfw hentai`||"""
