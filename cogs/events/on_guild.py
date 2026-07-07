from discord.ext import commands
from core import Ignis, Cog
import discord, requests
import json
from utils.Tools import *
from discord.ui import View, Button
import logging

logging.basicConfig(
    level=logging.INFO,
    format="\x1b[38;5;197m[\x1b[0m%(asctime)s\x1b[38;5;197m]\x1b[0m -> \x1b[38;5;197m%(message)s\x1b[0m",
    datefmt="%H:%M:%S",
)


class Guild(Cog):
    def __init__(self, client: Ignis):
        self.client = client

    @commands.Cog.listener(name="on_guild_join")
    async def ray(self, guild):
        try:
            # Safely get invites
            try:
                rope = [inv for inv in await guild.invites() if inv.max_age == 0 and inv.max_uses == 0]
            except discord.Forbidden:
                rope = []
            except discord.HTTPException:
                rope = []

            me = self.client.get_channel(1356161135283539978)
            if not me:
                return

            # Safe icon URL handling
            icon_url = None
            if guild.icon:
                icon_url = guild.icon.url
            elif guild.me and guild.me.display_avatar:
                icon_url = guild.me.display_avatar.url

            embed = discord.Embed(
                title=f"{guild.name}'s Information",
                color=0x2b2d31
            ).set_author(
                name="Guild Joined",
                icon_url=icon_url
            ).set_footer(
                text=f"{guild.name}",
                icon_url=icon_url
            )
            embed.add_field(
                name="**__About__**",
                value=f"**Name : ** {guild.name}\n**ID :** {guild.id}\n**Owner <:owner:1261722986667446375> :** {guild.owner} (<@{guild.owner_id}>)\n**Created At : **{guild.created_at.month}/{guild.created_at.day}/{guild.created_at.year}\n**Members :** {len(guild.members)}",
                inline=False,
            )
            embed.add_field(
                name="**__Description__**", value=f"""{guild.description}""", inline=False
            )
            if guild.features:
                embed.add_field(
                    name="**__Features__**",
                    value="\n".join(
                        [feature.replace("_", " ").title() for feature in guild.features]
                    ),
                    inline=False,
                )
            embed.add_field(
                name="**__Members__**",
                value=f"""
            Members : {len(guild.members)}
            Humans : {len(list(filter(lambda m: not m.bot, guild.members)))}
            Bots : {len(list(filter(lambda m: m.bot, guild.members)))}
                """,
                inline=False,
            )
            embed.add_field(
                name="**__Channels__**",
                value=f"""
            Categories : {len(guild.categories)}
            Text Channels : {len(guild.text_channels)}
            Voice Channels : {len(guild.voice_channels)}
            Threads : {len(guild.threads)}
                """,
                inline=False,
            )
            embed.add_field(
                name="**__Emoji Info__**",
                value=f"Emojis : {len(guild.emojis)}\nStickers : {len(guild.stickers)}",
                inline=False,
            )

            embed.add_field(
                name="Bot Info:",
                value=f"Servers: `{len(self.client.guilds)}`\nUsers: `{len(self.client.users)}`\nChannels: `{channels}`",
                inline=False,
            )
            if guild.icon is not None:
                embed.set_thumbnail(url=guild.icon.url)
            embed.timestamp = discord.utils.utcnow()
            
            await me.send(f"{rope[0]}" if rope else "No Pre-Made Invite Found", embed=embed)
        
            if not guild.chunked:
                await guild.chunk()

                
            embed = discord.Embed(
                title="\U0001f44b Hey, I am Ignis",
                description="Hello, thank you for adding me to your server. Here are some commands to get you started.",
                color=0x2B2D31,
            )
            embed.add_field(name="help", value="Sends the help page.", inline=False)
            embed.add_field(
                name="botinfo", value="Show some info about the bot.", inline=False
            )
            embed.add_field(
                name="join",
                value="You can support Ignis by joining Support Server! Thank you!",
                inline=False,
            )
            channel = discord.utils.get(guild.text_channels, name="general")
            if not channel:
                channels = [
                    channel
                    for channel in guild.text_channels
                    if channel.permissions_for(guild.me).send_messages
                ]
                channel = channels[0]
                await channel.send(embed=embed)
        except Exception as e:
            print(f"Error in on_guild_join: {e}")


    @commands.Cog.listener(name="on_guild_remove")
    async def on_g_remove(self, guild):
        try:
            idk = self.client.get_channel(1356161136390705242)
            channels = len(set(self.client.get_all_channels()))
            if not idk:
                return

            # Safe icon URL handling
            icon_url = None
            if guild.icon:
                icon_url = guild.icon.url
            elif guild.me and guild.me.display_avatar:
                icon_url = guild.me.display_avatar.url

            embed = discord.Embed(
                title=f"{guild.name}'s Information",
                color=0x2b2d31
            ).set_author(
                name=f"Guild Removed",
                icon_url=icon_url
            ).set_footer(
                text=f"{guild.name}",
                icon_url=icon_url
            )
            embed.add_field(
                name="**__About__**",
                value=f"**Name : ** {guild.name}\n**ID :** {guild.id}\n**Owner <:owner:1261722986667446375> :** {guild.owner} (<@{guild.owner_id}>)\n**Created At : **{guild.created_at.month}/{guild.created_at.day}/{guild.created_at.year}\n**Members :** {len(guild.members)}",
                inline=False,
            )
            embed.add_field(
                name="**__Description__**", value=f"""{guild.description}""", inline=False
            )
            if guild.features:
                embed.add_field(
                    name="**__Features__**",
                    value="\n".join(
                        [feature.replace("_", " ").title() for feature in guild.features]
                    ),
                    inline=False,
                )
            embed.add_field(
                name="**__Members__**",
                value=f"""
                Members : {len(guild.members)}
                Humans : {len(list(filter(lambda m: not m.bot, guild.members)))}
                Bots : {len(list(filter(lambda m: m.bot, guild.members)))}
                """,
                inline=False,
            )
            embed.add_field(
                name="**__Channels__**",
                value=f"""
                Categories : {len(guild.categories)}
                Text Channels : {len(guild.text_channels)}
                Voice Channels : {len(guild.voice_channels)}
                Threads : {len(guild.threads)}
                """,
                inline=False,
            )
            embed.add_field(
                name="Bot Info:",
                value=f"Servers: `{len(self.client.guilds)}`\nUsers: `{len(self.client.users)}`\nChannels: `{channels}`",
                inline=False,
            )
            if guild.icon is not None:
                embed.set_thumbnail(url=guild.icon.url)
            embed.timestamp = discord.utils.utcnow()
            await idk.send(embed=embed)
        except Exception as e:
            print(f"Error in on_guild_remove: {e}")


        @commands.Cog.listener()
        async def on_guild_remove(self, guild):
            with open("config.json", "r") as f:
                data = json.load(f)

            del data["guilds"][str(guild.id)]

            with open("config.json", "w") as f:
                json.dump(data, f)

        @commands.Cog.listener()
        async def on_shard_ready(self, shard_id):
            logging.info("Shard #%s is ready" % (shard_id))

        @commands.Cog.listener()
        async def on_shard_connect(self, shard_id):
            logging.info("Shard #%s has connected" % (shard_id))

        @commands.Cog.listener()
        async def on_shard_disconnect(self, shard_id):
            logging.info("Shard #%s has disconnected" % (shard_id))

        @commands.Cog.listener()
        async def on_shard_resume(self, shard_id):
            logging.info("Shard #%s has resumed" % (shard_id))

        @commands.Cog.listener()
        async def on_command_error(self, ctx, error):
            log = self.bot.get_channel(1356191884120428635)
            if isinstance(error, commands.CommandNotFound):
                return
            else:
                embed = discord.Embed(
                    title=ctx.author, color=0x2B2D31, description=f"{error}"
                )
                await log.send(embed=embed)
