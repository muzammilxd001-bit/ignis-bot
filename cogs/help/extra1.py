import discord
from discord.ext import commands


class extra1(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    """Extra Commands"""

    def help_custom(self):
        emoji = "<:setting:1348340711862571069>"
        label = "Extra+"
        description = "Show You Commands Of Extra"
        return emoji, label, description

    @commands.group()
    async def __Extra__(self, ctx: commands.Context):
        """`botinfo` , `team` , `uptime` , `stats` , `invite` , `vote` , `serverinfo` , `userinfo` , `roleinfo` , `status` , `emoji` , `user` , `role` , `channel` , `boosts`, `steal` , `removeemoji` , `createsticker` , `unbanall` , `joined-at` , `ping` , `yt` , `reminder start` , `reminder delete` , `github` , `vcinfo` , `channelinfo` , `note` , `notes` , `trashnotes` , `badges` , `list boosters` , `list inrole` , `list emojis` , `list bots` , `list admins` , `list invoice` , `list mods` , `list early` , `list activedeveloper` , `list createpos` , `list roles` , `ignore` , `ignore channel` , `ignore channel add` , `ignore channel remove` , `banner user` , `banner server`\n\n
        __Encryption__\n `h encode` , `encode base85` , `encode ascii85` ,`encode base64` , `encode rot13` , `encode base32` , `encode hex` , `h decode` , `decode base85` , `decode base64` , `decode hex` , `decode ascii85` , `decode base32` , `decode rot13`
        """
