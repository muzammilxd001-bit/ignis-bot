from __future__ import annotations
from discord.ext import commands
from utils.Tools import *
from discord import *
from utils.config import OWNER_IDS, No_Prefix
import json, discord
import typing
from utils import (
    Paginator,
    Paginator,
    DescriptionEmbedPaginator,
    FieldPagePaginator,
    TextPaginator,
)
from utils import (
    DescriptionEmbedPaginator,
    FieldPagePaginator,
    TextPaginator,
)

from typing import Optional


class Owner(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(name="slist", aliases=["serverlist"])
    @commands.is_owner()
    async def _slist(self, ctx):
        """List all servers the bot is in (sorted by member count)"""
        try:
            # Sort servers by member count (descending)
            servers = sorted(
                self.client.guilds,
                key=lambda g: g.member_count,
                reverse=True
            )

            # Prepare pagination entries
            entries = [
                f"`[{idx}]` | [{g.name}](https://discord.com/channels/{g.id}) - {g.member_count:,} members"
                for idx, g in enumerate(servers, start=1)
            ]

            # Create paginator
            paginator = Paginator(
                source=DescriptionEmbedPaginator(
                    entries=entries,
                    description="",
                    title=f"Server List - {len(servers)} servers",
                    color=0x2B2D31,
                    per_page=10
                ),
                ctx=ctx
            )

            await paginator.paginate()
            
        except Exception as e:
            error_embed = discord.Embed(
                title="Error",
                description=f"Failed to generate server list:\n```{str(e)}```",
                color=0xff0000
            )
            await ctx.send(embed=error_embed)

    @commands.command(name="sleave", help="Leaves a server by ID.")
    @commands.is_owner()
    async def sleave(self, ctx, server_id: int):
        guild = self.client.get_guild(server_id)
        if guild is None:
            await ctx.send("I am not in a server with that ID.")
            return

        try:
            await guild.leave()
            await ctx.send(
                f"Successfully left the server: **{guild.name}** ({guild.id})"
            )
        except discord.Forbidden:
            await ctx.send("I don't have permission to leave this server.")
        except discord.HTTPException as e:
            await ctx.send(f"An error occurred while trying to leave the server: {e}")
            

    @commands.command(name="reload", help="Reloads a specific cog or all cogs.")
    @commands.is_owner()
    async def reload(self, ctx, cog: str = None):
        if cog is None:
            # Reload all extensions
            reloaded_cogs = []
            for extension in list(self.client.extensions.keys()):
                try:
                    await self.client.reload_extension(extension)
                    reloaded_cogs.append(extension)
                except Exception as e:
                    return await ctx.reply(f"❌ Failed to reload `{extension}`\n`{str(e)}`")

            await ctx.reply(f"✅ Reloaded {len(reloaded_cogs)} cogs successfully!", mention_author=False)

        else:
            # Reload a specific cog
            cog_name = f"cogs.{cog}" if not cog.startswith("cogs.") else cog
            try:
                await self.client.reload_extension(cog_name)
                await ctx.reply(f"✅ Successfully reloaded `{cog_name}`!", mention_author=False)
            except Exception as e:
                await ctx.reply(f"❌ Failed to reload `{cog_name}`\n`{str(e)}`", mention_author=False)




    @commands.command(name="restart", help="Restarts the client.")
    @commands.is_owner()
    async def _restart(self, ctx: Context):
        await ctx.reply(
            "Restarting! <:tick:1348326381611647046> Please Wait It Takes 10 Second"
        )
        restart_program()

    @commands.command(name="shutdown", help="Shutdown the client.")
    @commands.is_owner()
    async def _shutdown(self, ctx: Context):
        await self.client.close()

    @commands.command(name="sync", help="Syncs all database files.")
    @commands.is_owner()
    async def _sync(self, ctx):
        # Send initial message
        sync_msg = await ctx.reply("🔄 Syncing all databases...", mention_author=False)
        results = []

        # List of all database files to sync
        databases = [
            ("data/anti.json", self._sync_anti),
            ("data/database.json", self._sync_database),
            ("data/bst.json", self._sync_bst),
            ("data/extra.json", self._sync_extra),
            ("config.json", self._sync_config),
            ("data/logging.json", self._sync_logging),
            ("data/blacklist.json", self._sync_blacklist),
            ("data/bdg.json", self._sync_badges),
            ("data/vanity.json", self._sync_vanity),
            ("data/ignore.json", self._sync_ignore)
        ]

        # Process each database
        for filename, sync_func in databases:
            try:
                result = await sync_func()
                results.append(f"✅ `{filename}` synced")
            except Exception as e:
                results.append(f"❌ `{filename}` sync failed: `{e}`")

        # Update sync message with all results
        await sync_msg.edit(content=f"🔄 **Sync Completed!**\n" + "\n".join(results))

    async def _sync_anti(self):
        with open("data/anti.json", "r") as f:
            anti_data = json.load(f)

        # Ensure proper structure
        if "guilds" not in anti_data:
            anti_data["guilds"] = {}

        for guild in self.client.guilds:
            if str(guild.id) not in anti_data["guilds"]:
                anti_data["guilds"][str(guild.id)] = "on"

        with open("data/anti.json", "w") as f:
            json.dump(anti_data, f, indent=4)

    async def _sync_database(self):
        with open("data/database.json", "r") as f:
            try:
                db_data = json.load(f)
            except (json.JSONDecodeError, FileNotFoundError):
                db_data = {"guilds": {}}

        # Ensure proper structure
        if "guilds" not in db_data:
            db_data["guilds"] = {}

        default_config = {
            "welcome": {
                "autodel": 0,
                "channel": [],
                "color": "",
                "embed": False,
                "footer": "",
                "image": "",
                "message": "<<user.mention>> Welcome To <<server.name>>",
                "ping": False,
                "title": "",
                "thumbnail": ""
            },
            "vcrole": {
                "bots": "",
                "humans": ""
            }
        }

        for guild in self.client.guilds:
            if str(guild.id) not in db_data["guilds"]:
                db_data["guilds"][str(guild.id)] = default_config
            else:
                # Merge existing config with default (preserving existing values)
                for key, value in default_config.items():
                    if key not in db_data["guilds"][str(guild.id)]:
                        db_data["guilds"][str(guild.id)][key] = value

        with open("data/database.json", "w") as f:
            json.dump(db_data, f, indent=4)

    async def _sync_bst(self):
        with open("data/bst.json", "r") as f:
            try:
                bst_data = json.load(f)
            except (json.JSONDecodeError, FileNotFoundError):
                bst_data = {"guilds": {}}

        # Ensure proper structure
        if "guilds" not in bst_data:
            bst_data["guilds"] = {}

        default_config = {
            "boost": {
                "autodel": 0,
                "channel": [],
                "color": "",
                "embed": False,
                "footer": "",
                "image": "",
                "message": "<<boost.user_mention>> Thank you for boosting <<boost.server_name>>",
                "ping": False,
                "title": "",
                "thumbnail": ""
            },
            "boost1": {
                "role": []
            }
        }

        for guild in self.client.guilds:
            if str(guild.id) not in bst_data["guilds"]:
                bst_data["guilds"][str(guild.id)] = default_config

        with open("data/bst.json", "w") as f:
            json.dump(bst_data, f, indent=4)

    async def _sync_extra(self):
        with open("data/extra.json", "r") as f:
            try:
                extra_data = json.load(f)
            except (json.JSONDecodeError, FileNotFoundError):
                extra_data = {"guilds": {}}

        # Ensure proper structure
        if "guilds" not in extra_data:
            extra_data["guilds"] = {}

        default_config = {
            "owners": [],
            "antiSpam": False,
            "antiLink": False,
            "antiinvites": False,
            "punishment": "mute",
            "whitelisted": [],
            "channel": None,
            "mods": [],
            "modrole": None,
            "ignorechannels": []
        }

        for guild in self.client.guilds:
            if str(guild.id) not in extra_data["guilds"]:
                extra_data["guilds"][str(guild.id)] = default_config

        with open("data/extra.json", "w") as f:
            json.dump(extra_data, f, indent=4)

    async def _sync_config(self):
        with open("config.json", "r") as f:
            try:
                config_data = json.load(f)
            except (json.JSONDecodeError, FileNotFoundError):
                config_data = {"guilds": {}}

        # Ensure proper structure
        if "guilds" not in config_data:
            config_data["guilds"] = {}

        default_config = {
            "antiSpam": False,
            "antiLink": False,
            "antiInvite": False,
            "whitelisted": [],
            "extraowners": [],
            "bypass_antispam": [],
            "bypass_antilink": [],
            "panic_main_role": [],
            "panic_mode": False,
            "panic_punishment": [],
            "punishment": "ban",
            "prefix": ".",
            "staff": None,
            "vip": None,
            "girl": None,
            "guest": None,
            "frnd": None,
            "owner": None,
            "coown": None,
            "headadmin": None,
            "admin": None,
            "mod": None,
            "gmod": None,
            "gadmin": None,
            "headmod": None,
            "wlrole": None
        }

        for guild in self.client.guilds:
            if str(guild.id) not in config_data["guilds"]:
                config_data["guilds"][str(guild.id)] = default_config

        with open("config.json", "w") as f:
            json.dump(config_data, f, indent=4)

    async def _sync_logging(self):
        with open("data/logging.json", "r") as f:
            try:
                logging_data = json.load(f)
            except (json.JSONDecodeError, FileNotFoundError):
                logging_data = {"guilds": {}}

        # Ensure proper structure
        if "guilds" not in logging_data:
            logging_data["guilds"] = {}

        default_config = {
            "logging": {
                "logall": False,
                "channel": [],
                "msglog": [],
                "memberlog": [],
                "serverlog": [],
                "rolelog": [],
                "channellog": [],
                "modlog": [],
                "voicelog": []
            }
        }

        for guild in self.client.guilds:
            if str(guild.id) not in logging_data["guilds"]:
                logging_data["guilds"][str(guild.id)] = default_config

        with open("data/logging.json", "w") as f:
            json.dump(logging_data, f, indent=4)

    async def _sync_blacklist(self):
        with open("data/blacklist.json", "r") as f:
            try:
                blacklist_data = json.load(f)
            except (json.JSONDecodeError, FileNotFoundError):
                blacklist_data = {"ids": []}

        # Ensure proper structure
        if "ids" not in blacklist_data:
            blacklist_data["ids"] = []

        with open("data/blacklist.json", "w") as f:
            json.dump(blacklist_data, f, indent=4)

    async def _sync_badges(self):
        with open("data/bdg.json", "r") as f:
            try:
                badges_data = json.load(f)
            except (json.JSONDecodeError, FileNotFoundError):
                badges_data = {}

        with open("data/bdg.json", "w") as f:
            json.dump(badges_data, f, indent=4)

    async def _sync_vanity(self):
        with open("data/vanity.json", "r") as f:
            try:
                vanity_data = json.load(f)
            except (json.JSONDecodeError, FileNotFoundError):
                vanity_data = {}

        with open("data/vanity.json", "w") as f:
            json.dump(vanity_data, f, indent=4)

    async def _sync_ignore(self):
        with open("data/ignore.json", "r") as f:
            try:
                ignore_data = json.load(f)
            except (json.JSONDecodeError, FileNotFoundError):
                ignore_data = {"ids": []}

        # Ensure proper structure
        if "ids" not in ignore_data:
            ignore_data["ids"] = []

        with open("data/ignore.json", "w") as f:
            json.dump(ignore_data, f, indent=4)
        
        
    @commands.group(
        name="blacklist", help="let's you add someone in blacklist", aliases=["bl"]
    )
    @commands.is_owner()
    async def blacklist(self, ctx):
        if ctx.invoked_subcommand is None:
            with open("data/blacklist.json") as file:
                blacklist = json.load(file)
                entries = [
                    f"`[{no}]` | <@!{mem}> (ID: {mem})"
                    for no, mem in enumerate(blacklist["ids"], start=1)
                ]
                Paginator = Paginator(
                    source=DescriptionEmbedPaginator(
                        entries=entries,
                        title=f"List of Blacklisted users of Ignis - {len(blacklist['ids'])}",
                        description="",
                        per_page=10,
                        color=0x2B2D31,
                    ),
                    ctx=ctx,
                )
                await Paginator.paginate()

    @blacklist.command(name="add")
    @commands.is_owner()
    async def blacklist_add(self, ctx: Context, member: discord.Member):
        try:
            with open("data/blacklist.json", "r") as bl:
                blacklist = json.load(bl)
                if str(member.id) in blacklist["ids"]:
                    embed = discord.Embed(
                        title="Error!",
                        description=f"{member.name} is already blacklisted",
                        color=discord.Colour(0x2B2D31),
                    )
                    await ctx.reply(embed=embed, mention_author=False)
                else:
                    add_user_to_blacklist(member.id)
                    embed = discord.Embed(
                        title="Blacklisted",
                        description=f"Successfully Blacklisted {member.name}",
                        color=discord.Colour(0x2B2D31),
                    )
                    with open("data/blacklist.json") as file:
                        blacklist = json.load(file)
                        embed.set_footer(
                            text=f"There are now {len(blacklist['ids'])} users in the blacklist"
                        )
                        await ctx.reply(embed=embed, mention_author=False)
        except:
            embed = discord.Embed(
                title="Error!",
                description=f"An Error Occurred",
                color=discord.Colour(0x2B2D31),
            )
            await ctx.reply(embed=embed, mention_author=False)

    @blacklist.command(name="remove")
    @commands.is_owner()
    async def blacklist_remove(self, ctx, member: discord.Member = None):
        try:
            remove_user_from_blacklist(member.id)
            embed = discord.Embed(
                title="User removed from blacklist",
                description=f"<:tick:1348326381611647046> | **{member.name}** has been successfully removed from the blacklist",
                color=0x2B2D31,
            )
            with open("data/blacklist.json") as file:
                blacklist = json.load(file)
                embed.set_footer(
                    text=f"There are now {len(blacklist['ids'])} users in the blacklist"
                )
                await ctx.reply(embed=embed, mention_author=False)
        except:
            embed = discord.Embed(
                title="Error!",
                description=f"**{member.name}** is not in the blacklist.",
                color=0x2B2D31,
            )
            embed.set_thumbnail(url=f"{self.client.user.display_avatar.url}")
            await ctx.reply(embed=embed, mention_author=False)

    @commands.command()
    @commands.is_owner()
    async def dm(self, ctx, user: discord.User, *, message: str):
        """DM the user of your choice"""
        try:
            await user.send(message)
            await ctx.send(
                f"<:tick:1348326381611647046> | Successfully Sent a DM to **{user}**"
            )
        except discord.Forbidden:
            await ctx.send(
                "This user might be having DMs blocked or it's a bot account..."
            )
            

    @commands.command(name="say", aliases=["echo"])
    @commands.is_owner()
    async def say(self, ctx, *, message: str = None):
        """
        Make the bot send a message (Owner Only)
        Usage: 
        - !say <message> [Sends message in current channel]
        - !say #channel <message> [Sends message in specified channel]
        """
        if message is None:
            embed = discord.Embed(
                description="<:cross:1348326385386651748> | Please provide a message to send",
                color=0x2b2d31
            )
            return await ctx.send(embed=embed)

        # Check for channel mention
        if ctx.message.channel_mentions:
            target_channel = ctx.message.channel_mentions[0]
            message = message.replace(target_channel.mention, "").strip()
        else:
            target_channel = ctx.channel

        try:
            # Delete the command message if possible
            try:
                await ctx.message.delete()
            except discord.Forbidden:
                pass

            # Send the message
            await target_channel.send(message)
            
            # Send confirmation to owner
            confirm_embed = discord.Embed(
                description=f"<:tick:1348326381611647046> | Successfully sent message to {target_channel.mention}",
                color=0x2b2d31
            )
            await ctx.author.send(embed=confirm_embed)  # DM confirmation

        except discord.Forbidden:
            error_embed = discord.Embed(
                description="<:cross:1348326385386651748> | I don't have permissions to send messages there",
                color=0x2b2d31
            )
            await ctx.send(embed=error_embed)
        except Exception as e:
            error_embed = discord.Embed(
                description=f"<:cross:1348326385386651748> | An error occurred: {str(e)}",
                color=0x2b2d31
            )
            await ctx.send(embed=error_embed)

    @commands.group()
    @commands.is_owner()
    async def change(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send_help(str(ctx.command))

    @change.command(name="nickname")
    @commands.is_owner()
    async def change_nickname(self, ctx, *, name: str = None):
        """Change nickname."""
        try:
            await ctx.guild.me.edit(nick=name)
            if name:
                await ctx.send(
                    f"<:tick:1348326381611647046> | Successfully changed nickname to **{name}**"
                )
            else:
                await ctx.send(
                    "<:tick:1348326381611647046> | Successfully cleared nickname"
                )
        except Exception as err:
            await ctx.send(err)

    @commands.command()
    @commands.is_owner()
    async def globalban(self, ctx, *, user: discord.User = None):
        if user is None:
            return await ctx.send("You need to define the user")
        for guild in self.client.guilds:
            for member in guild.members:
                if member == user:
                    await user.ban(reason="...")
