import discord
import json
from discord.ext import commands
from utils.Tools import blacklist_check, ignore_check

class Media(commands.Cog):
    def __init__(self, client):
        self.client = client

    async def ensure_media_config(self, guild_id):
        # Ensure data/media.json exists and has default structure
        try:
            with open("data/media.json", "r") as f:
                media = json.load(f)
        except FileNotFoundError:
            media = {}

        if str(guild_id) not in media:
            media[str(guild_id)] = {"channel": []}

        with open("data/media.json", "w") as f:
            json.dump(media, f, indent=4)

    @commands.Cog.listener()
    async def on_ready(self):
        for guild in self.client.guilds:
            await self.ensure_media_config(guild.id)

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        await self.ensure_media_config(guild.id)

    @commands.group(invoke_without_command=True)
    @blacklist_check()
    @ignore_check()
    async def media(self, ctx):
        prefix = ctx.prefix
        em = discord.Embed(
            title=f"media Commands",
            description=f"`{prefix}media`\nConfigures the media only channels!\n\n`{prefix}media setup`\nSetups media only channels in the server.\n\n`{prefix}media remove`\nRemoves the media only channels in the server.\n\n`{prefix}media config`\nShows the configured media only channels for the server.\n\n`{prefix}media reset`\nRemoves all the channels from media only channels for the server.  ", color=0x2b2d31)
        await ctx.send(embed=em)

    @media.command(name="setup", description="Setups media only channels for the server")
    @commands.has_permissions(administrator=True)
    @blacklist_check()
    @ignore_check()
    async def setup(self, ctx, *, channel: discord.TextChannel):
        with open("data/media.json", "r") as f:
            media = json.load(f)

        media[str(ctx.guild.id)]["channel"].append(channel.id)

        with open("data/media.json", "w") as f:
            json.dump(media, f, indent=4)

        await ctx.send(f"<:tick:1348326381611647046> | Successfully added {channel.mention} in media only channels.")

    @media.command(name="remove", description="Removes media only channels for the server")
    @commands.has_permissions(administrator=True)
    @blacklist_check()
    @ignore_check()
    async def remove(self, ctx, *, channel: discord.TextChannel):
        with open("data/media.json", "r") as f:
            media = json.load(f)

        media[str(ctx.guild.id)]["channel"].remove(channel.id)

        with open("data/media.json", "w") as f:
            json.dump(media, f, indent=4)

        await ctx.send(f"<:tick:1348326381611647046> | Successfully removed {channel.mention} from media only channels.")

    @media.command(name="config", aliases=["settings", "show"], description="Shows the configured media only channels for the server")
    @commands.has_permissions(administrator=True)
    @blacklist_check()
    @ignore_check()
    async def config(self, ctx):
        with open("data/media.json", "r") as f:
            media = json.load(f)

        chan = media.get(str(ctx.guild.id), {}).get("channel", [])

        channel = list([self.client.get_channel(id).mention for id in chan])

        embed = discord.Embed(title=f"Media Only Channels for {ctx.guild.name}", color=0x2b2d31)
        num = 0
        for i in channel:
            num += 1
            i = i.replace("['']", "")
            embed.add_field(name=f"{num}", value=i, inline=True)

        embed.set_footer(text=f"Requested by {ctx.author.name}", icon_url=ctx.author.avatar)

        await ctx.send(embed=embed)

    @media.command(name="reset", description="Removes all the channels from media only channels for the server")
    @blacklist_check()
    @ignore_check()
    @commands.has_permissions(administrator=True)
    async def reset(self, ctx):
        with open("data/media.json", "r") as f:
            media = json.load(f)

        media[str(ctx.guild.id)]["channel"] = []

        with open("data/media.json", "w") as f:
            json.dump(media, f, indent=4)

        await ctx.send("<:tick:1348326381611647046> | Successfully removed all the media only channels.")

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return

        with open("data/media.json", "r") as f:
            media = json.load(f)

        channel = media.get(str(message.guild.id), {}).get("channel", [])

        if message.channel.id in channel and not message.attachments:
            await message.delete()
            await message.channel.send("This channel is configured for media only. You are only allowed to send media files.", delete_after=1)
