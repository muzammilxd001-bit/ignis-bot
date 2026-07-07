import json
import discord
from discord.ext import commands
from utils.Tools import *
from core import Cog, Ignis, Context

# Utility functions for JSON operations
def read_db(filename):
    try:
        with open(filename, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def write_db(filename, data):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)

class invites(Cog):
    """Track invites in your server and who invited whom!"""

    def __init__(self, client: Ignis):
        self.client = client
        self.invites = {}

    @commands.Cog.listener()
    async def on_ready(self):
        for guild in self.client.guilds:
            try:
                # Check if the bot has "Manage Server" permission
                if guild.me.guild_permissions.manage_guild:
                    self.invites[guild.id] = await guild.invites()
                else:
                    print(f"Skipping {guild.name} ({guild.id}): Missing 'Manage Server' permission.")
            except discord.Forbidden:
                print(f"Skipping {guild.name} ({guild.id}): Bot lacks permission to fetch invites.")
            except discord.HTTPException as e:
                print(f"Skipping {guild.name} ({guild.id}): HTTP Exception - {e}")


    @commands.Cog.listener()
    async def on_member_join(self, member):
        db = read_db('data/invites.json')
        log_db = read_db('data/invite_logs.json')
        guild = member.guild
        new_invites = await guild.invites()
        
        # Check if the guild and member are in the database
        if str(guild.id) not in db:
            db[str(guild.id)] = {}
        if str(member.id) not in db[str(guild.id)]:
            db[str(guild.id)][str(member.id)] = {"invites": 0}

        invites_count = db[str(guild.id)][str(member.id)]["invites"]
        old_invites = self.invites.get(guild.id, [])

        for invite in new_invites:
            for old_invite in old_invites:
                if invite.code == old_invite.code and invite.uses > old_invite.uses:
                    inviter = invite.inviter
                    if str(guild.id) not in db:
                        db[str(guild.id)] = {}
                    if str(member.id) not in db[str(guild.id)]:
                        db[str(guild.id)][str(member.id)] = {"invited_by": inviter.id}
                    if str(inviter.id) not in db[str(guild.id)]:
                        db[str(guild.id)][str(inviter.id)] = {"invites": 0}
                    db[str(guild.id)][str(inviter.id)]["invites"] += 1
                    write_db('data/invites.json', db)
                    self.invites[guild.id] = new_invites

                    # Send log message
                    log_channel_id = log_db.get(str(guild.id), {}).get("log_channel")
                    if log_channel_id:
                        log_channel = guild.get_channel(log_channel_id)
                        if log_channel:
                            await log_channel.send(
                                embed=discord.Embed(
                                    description=f"{member.mention} joined using {inviter.mention}'s invite and now have {invites_count} invites.",
                                    color=0x2b2d31
                                )
                            )
                    try:
                        await member.send(f"Welcome to {guild.name}! You were invited by {inviter.name} and now have {invites_count} invites.")
                    except discord.Forbidden:
                        pass
                    break

    @commands.command(
        name="invites",
        help="Check the number of invites a member has.")
    @blacklist_check()
    @ignore_check()
    @commands.cooldown(1, 7, commands.BucketType.user)
    @commands.guild_only()
    async def _invites(self, ctx: commands.Context, member: discord.Member = None):
        db = read_db('data/invites.json')
        guild_id = str(ctx.guild.id)
        member = member or ctx.author
        if guild_id in db and str(member.id) in db[guild_id] and "invites" in db[guild_id][str(member.id)]:
            invites = db[guild_id][str(member.id)]["invites"]
            await ctx.reply(embed=discord.Embed(
                description=f"{member.name} has {invites} invites.",
                color=0x2b2d31), mention_author=False)
        else:
            await ctx.reply(embed=discord.Embed(
                description=f"{member.name} has no invite information.",
                color=0x2b2d31), mention_author=False)

    @commands.command(
        name="addinvites",
        aliases=["add-invites"],
        help="Add invites to a member.")
    @blacklist_check()
    @ignore_check()
    @commands.has_permissions(administrator=True)
    @commands.guild_only()
    async def _addinvites(self, ctx: commands.Context, member: discord.Member, amount: int):
        db = read_db('data/invites.json')
        guild_id = str(ctx.guild.id)
        if guild_id not in db:
            db[guild_id] = {}
        if str(member.id) not in db[guild_id]:
            db[guild_id][str(member.id)] = {"invites": 0}
        db[guild_id][str(member.id)]["invites"] += amount
        write_db('data/invites.json', db)
        await ctx.reply(embed=discord.Embed(
            description=f"Added {amount} invites to {member.name}.",
            color=0x2b2d31), mention_author=False)

    @commands.command(
        name="resetinvites",
        aliases=["reset-invites"],
        help="Reset invites of a member.")
    @blacklist_check()
    @ignore_check()
    @commands.has_permissions(administrator=True)
    @commands.guild_only()
    async def _resetinvites(self, ctx: commands.Context, member: discord.Member):
        db = read_db('data/invites.json')
        guild_id = str(ctx.guild.id)
        if guild_id in db and str(member.id) in db[guild_id] and "invites" in db[guild_id][str(member.id)]:
            db[guild_id][str(member.id)]["invites"] = 0
            write_db('data/invites.json', db)
            await ctx.reply(embed=discord.Embed(
                description=f"Reset invites of {member.name}.",
                color=0x2b2d31), mention_author=False)
        else:
            await ctx.reply(embed=discord.Embed(
                description=f"{member.name} has no invite information to reset.",
                color=0x2b2d31), mention_author=False)

    @commands.command(
        name="removeinvites",
        aliases=["remove-invites"],
        help="Remove a number of invites from a member.")
    @blacklist_check()
    @ignore_check()
    @commands.has_permissions(administrator=True)
    @commands.guild_only()
    async def _removeinvites(self, ctx: commands.Context, member: discord.Member, amount: int):
        db = read_db('data/invites.json')
        guild_id = str(ctx.guild.id)
        if guild_id in db and str(member.id) in db[guild_id] and "invites" in db[guild_id][str(member.id)]:
            db[guild_id][str(member.id)]["invites"] = max(0, db[guild_id][str(member.id)]["invites"] - amount)
            write_db('data/invites.json', db)
            await ctx.reply(embed=discord.Embed(
                description=f"Removed {amount} invites from {member.name}.",
                color=0x2b2d31), mention_author=False)
        else:
            await ctx.reply(embed=discord.Embed(
                description=f"{member.name} has no invite information to remove.",
                color=0x2b2d31), mention_author=False)

    @commands.command(
        name="resetserverinvites",
        aliases=["reset-server-invites"],
        help="Reset all invites of all members in the server.")
    @blacklist_check()
    @ignore_check()
    @commands.has_permissions(administrator=True)
    @commands.guild_only()
    async def _resetserverinvites(self, ctx: commands.Context):
        db = read_db('data/invites.json')
        guild_id = str(ctx.guild.id)
        if guild_id in db:
            for member_id in db[guild_id]:
                if "invites" in db[guild_id][member_id]:
                    db[guild_id][member_id]["invites"] = 0
            write_db('data/invites.json', db)
            await ctx.reply(embed=discord.Embed(
                description=f"All invites have been reset.",
                color=0x2b2d31), mention_author=False)

    @commands.command(
        name="setinvitechannellog",
        aliases=["set-invite-channel"],
        help="Set the channel where invite logs will be posted.")
    @blacklist_check()
    @ignore_check()
    @commands.has_permissions(administrator=True)
    @commands.guild_only()
    async def _setinvitelog(self, ctx: commands.Context, channel: discord.TextChannel):
        log_db = read_db('data/invite_logs.json')
        log_db[str(ctx.guild.id)] = {"log_channel": channel.id}
        write_db('data/invite_logs.json', log_db)
        await ctx.reply(embed=discord.Embed(
            description=f"Invite logs will be posted in {channel.mention}.",
            color=0x2b2d31), mention_author=False)

async def setup(client: Ignis):
    await client.add_cog(invites(client))
