import discord
from discord.ext import commands
from discord.utils import get
import os
from utils.Tools import *
from typing import Optional, Union
from discord.ext.commands import Context
from utils import Paginator, DescriptionEmbedPaginator, FieldPagePaginator, TextPaginator
from utils import *


class Voice(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        
        
        
    def has_permission_or_admin(permission: str):
        async def predicate(ctx):
            perms = ctx.author.guild_permissions
            return perms.administrator or getattr(perms, permission, False)
        return commands.check(predicate)





    @commands.group(name="voice", invoke_without_command=True, aliases=['vc'])
    @blacklist_check()
    @ignore_check()
    async def vc(self, ctx: commands.Context):
        if ctx.subcommand_passed is None:
            await ctx.send_help(ctx.command)
            ctx.command.reset_cooldown(ctx)

    @vc.command(name="kick",
                help="Dissconnect a member from a voice channel .",
                usage="voice kick <member>")
    @has_permission_or_admin("move_members")
    @commands.cooldown(1, 10, commands.BucketType.user)
    @blacklist_check()
    @ignore_check()
    @commands.max_concurrency(1, per=commands.BucketType.default, wait=False)
    async def _kick(self, ctx, *, member: discord.Member):
        if member.voice is None:
            ray5 = discord.Embed(
                title="Ignis",
                description=
                f"{str(member)} Is not connected in any of the voice channel",
                color=0x2b2d31)
            ray5.set_author(name=f"{ctx.author}",
                               icon_url=f"{ctx.author.avatar}")
            ray5.set_thumbnail(url=f"{ctx.author.avatar}")
            return await ctx.reply(embed=ray5)
        ch = member.voice.channel.mention
        await member.edit(voice_channel=None,
                          reason=f"Disconnected by {str(ctx.author)}")
        ray = discord.Embed(
            title="Ignis",
            description=f"{str(member)} has been disconnected from {ch}",
            color=0x2b2d31)
        ray.set_author(name=f"{ctx.author}",
                          icon_url=f"{ctx.author.avatar}")
        ray.set_thumbnail(url=f"{ctx.author.avatar}")
        return await ctx.reply(embed=ray)

    @vc.command(name="kickall",
                help="Dissconnect all member from a voice channel .",
                usage="voice kick all")
    @commands.has_permissions(administrator=True)
    @commands.cooldown(1, 10, commands.BucketType.user)
    @blacklist_check()
    @ignore_check()
    @commands.max_concurrency(1, per=commands.BucketType.default, wait=False)
    async def _kickall(self, ctx):
        if ctx.author.voice is None:
            ray5 = discord.Embed(
                title="Ignis",
                description=
                f"You are not connected in any of the voice channel",
                color=0x2b2d31)
            ray5.set_author(name=f"{ctx.author.name}",
                               icon_url=f"{ctx.author.avatar}")
            ray5.set_thumbnail(url=f"{ctx.author.avatar}")
            return await ctx.reply(embed=ray5)
        count = 0
        ch = ctx.author.voice.channel.mention
        for member in ctx.author.voice.channel.members:
            await member.edit(
                voice_channel=None,
                reason=f"Disconnected Command Executed By {str(ctx.author)}")
            count += 1
        ray = discord.Embed(
            title="Ignis",
            description=f"Disconnected {count} members from {ch}",
            color=0x2b2d31)
        ray.set_author(name=f"{ctx.author}",
                          icon_url=f"{ctx.author.avatar}")
        ray.set_thumbnail(url=f"{ctx.author.avatar}")
        return await ctx.reply(embed=ray)

    @vc.command(name="mute",
                help="mute a member in voice channel .",
                usage="voice mute <member>")
    @has_permission_or_admin("mute_members")
    @commands.cooldown(1, 10, commands.BucketType.user)
    @blacklist_check()
    @ignore_check()
    @commands.max_concurrency(1, per=commands.BucketType.default, wait=False)
    async def _mute(self, ctx, *, member: discord.Member):
        if member.voice is None:
            error = discord.Embed(
                title="Ignis",
                description=
                f"{str(member)} Is not connected in any of the voice channel",
                color=0x2b2d31)
            error.set_author(name=f"{ctx.author}",
                             icon_url=f"{ctx.author.avatar}")
            error.set_thumbnail(url=f"{ctx.author.avatar}")
            return await ctx.reply(embed=error)
        if member.voice.mute == True:
            ray5 = discord.Embed(
                title="Ignis",
                description=
                f"{str(member)} Is already muted in the voice channel",
                color=0x2b2d31)
            ray5.set_author(name=f"{ctx.author}",
                               icon_url=f"{ctx.author.avatar}")
            ray5.set_thumbnail(url=f"{ctx.author.avatar}")
            return await ctx.reply(embed=ray5)
        ch = member.voice.channel.mention
        ray = discord.Embed(
            title="Ignis",
            description=f"{str(member)} has been muted in {ch}",
            color=0x2b2d31)
        ray.set_author(name=f"{ctx.author}",
                          icon_url=f"{ctx.author.avatar}")
        ray.set_thumbnail(url=f"{ctx.author.avatar}")
        await member.edit(mute=True, reason=f"Muted by {str(ctx.author)}")
        return await ctx.reply(embed=ray)

    @vc.command(name="unmute",
                help="unmute a member in voice channel .",
                usage="voice unmute <member>")
    @has_permission_or_admin("mute_members")
    @commands.cooldown(1, 10, commands.BucketType.user)
    @blacklist_check()
    @ignore_check()
    @commands.max_concurrency(1, per=commands.BucketType.default, wait=False)
    async def vcunmute(self, ctx, *, member: discord.Member):
        if member.voice is None:
            error = discord.Embed(
                title="Ignis",
                description=
                f"{str(member)} Is not connected in any of the voice channel",
                color=0x2b2d31)
            error.set_author(name=f"{ctx.author}",
                             icon_url=f"{ctx.author.avatar}")
            error.set_thumbnail(url=f"{ctx.author.avatar}")
            return await ctx.reply(embed=error)
        if member.voice.mute == False:
            ray5 = discord.Embed(
                title="Ignis",
                description=
                f"{str(member)} Is already unmuted in the voice channel",
                color=0x2b2d31)
            ray5.set_author(name=f"{ctx.author}",
                               icon_url=f"{ctx.author.avatar}")
            ray5.set_thumbnail(url=f"{ctx.author.avatar}")
            return await ctx.reply(embed=ray5)
        ch = member.voice.channel.mention
        ray = discord.Embed(
            title="Ignis",
            description=f"{str(member)} has been unmuted in {ch}",
            color=0x2b2d31)
        ray.set_author(name=f"{ctx.author}",
                          icon_url=f"{ctx.author.avatar}")
        ray.set_thumbnail(url=f"{ctx.author.avatar}")
        await member.edit(mute=False, reason=f"Unmuted by {str(ctx.author)}")
        return await ctx.reply(embed=ray)

    @vc.command(name="muteall",
                help="mute all member in a voice channel .",
                usage="voice muteall")
    @commands.has_permissions(administrator=True)
    @commands.cooldown(1, 10, commands.BucketType.user)
    @blacklist_check()
    @ignore_check()
    @commands.max_concurrency(1, per=commands.BucketType.default, wait=False)
    async def _muteall(self, ctx):
        if ctx.author.voice is None:
            error = discord.Embed(
                title="Ignis",
                description=
                f"You are not connected in any of the voice channel",
                color=0x2b2d31)
            error.set_author(name=f"{ctx.author}",
                             icon_url=f"{ctx.author.avatar}")
            error.set_thumbnail(url=f"{ctx.author.avatar}")
            return await ctx.reply(embed=error)
        count = 0
        ch = ctx.author.voice.channel.mention
        for member in ctx.author.voice.channel.members:
            if member.voice.mute == False:
                await member.edit(
                    mute=True,
                    reason=
                    f"voice muteall Command Executed by {str(ctx.author)}")
                count += 1
        ray = discord.Embed(title="Ignis",
                               description=f"Muted {count} members in {ch}",
                               color=0x2b2d31)
        ray.set_author(name=f"{ctx.author}",
                          icon_url=f"{ctx.author.avatar}")
        ray.set_thumbnail(url=f"{ctx.author.avatar}")
        return await ctx.reply(embed=ray)

    @vc.command(name="unmuteall",
                help="unmute all member in a voice channel .",
                usage="voice unmuteall")
    @commands.has_permissions(administrator=True)
    @commands.cooldown(1, 10, commands.BucketType.user)
    @blacklist_check()
    @ignore_check()
    @commands.max_concurrency(1, per=commands.BucketType.default, wait=False)
    async def _unmuteall(self, ctx):
        if ctx.author.voice is None:
            error = discord.Embed(
                title="Ignis",
                description=
                f"You are not connected in any of the voice channel",
                color=0x2b2d31)
            error.set_author(name=f"{ctx.author}",
                             icon_url=f"{ctx.author.avatar}")
            error.set_thumbnail(url=f"{ctx.author.avatar}")
            return await ctx.reply(embed=error)
        count = 0
        ch = ctx.author.voice.channel.mention
        for member in ctx.author.voice.channel.members:
            if member.voice.mute == True:
                await member.edit(
                    mute=False,
                    reason=
                    f"voice unmuteall Command Executed by {str(ctx.author)}")
                count += 1
        ray = discord.Embed(title="Ignis",
                               description=f"Unmuted {count} members in {ch}",
                               color=0x2b2d31)
        ray.set_author(name=f"{ctx.author}",
                          icon_url=f"{ctx.author.avatar}")
        ray.set_thumbnail(url=f"{ctx.author.avatar}")
        return await ctx.reply(embed=ray)

    @vc.command(name="deafen",
                help="deafen a member in a voice channel .",
                usage="voice deafen <member>")
    @has_permission_or_admin("deafen_members")
    @commands.cooldown(1, 10, commands.BucketType.user)
    @blacklist_check()
    @ignore_check()
    @commands.max_concurrency(1, per=commands.BucketType.default, wait=False)
    async def _deafen(self, ctx, *, member: discord.Member):
        if member.voice is None:
            error = discord.Embed(
                title="Ignis",
                description=
                f"{str(member)} Is not connected in any of the voice channel",
                color=0x2b2d31)
            error.set_author(name=f"{ctx.author}",
                             icon_url=f"{ctx.author.avatar}")
            error.set_thumbnail(url=f"{ctx.author.avatar}")
            return await ctx.reply(embed=error)
        if member.voice.deaf == True:
            ray5 = discord.Embed(
                title="Ignis",
                description=
                f"{str(member)} Is already deafen in the voice channel",
                color=0x2b2d31)
            ray5.set_author(name=f"{ctx.author}",
                               icon_url=f"{ctx.author.avatar}")
            ray5.set_thumbnail(url=f"{ctx.author.avatar}")
            return await ctx.reply(embed=ray5)
        ch = member.voice.channel.mention
        ray = discord.Embed(
            title="Ignis",
            description=f"{str(member)} has been Deafen in {ch}",
            color=0x2b2d31)
        ray.set_author(name=f"{ctx.author}",
                          icon_url=f"{ctx.author.avatar}")
        ray.set_thumbnail(url=f"{ctx.author.avatar}")
        await member.edit(deafen=True, reason=f"Deafen by {str(ctx.author)}")
        return await ctx.reply(embed=ray)

    @vc.command(name="undeafen",
                help="undeafen a member in a voice channel .",
                usage="voice undeafen <member>")
    @has_permission_or_admin("deafen_members")
    @commands.cooldown(1, 10, commands.BucketType.user)
    @blacklist_check()
    @ignore_check()
    @commands.max_concurrency(1, per=commands.BucketType.default, wait=False)
    async def _undeafen(self, ctx, *, member: discord.Member):
        if member.voice is None:
            error = discord.Embed(
                title="Ignis",
                description=
                f"{str(member)} Is not connected in any of the voice channel",
                color=0x2b2d31)
            error.set_author(name=f"{ctx.author}",
                             icon_url=f"{ctx.author.avatar}")
            error.set_thumbnail(url=f"{ctx.author.avatar}")
            return await ctx.reply(embed=error)
        if member.voice.deaf == False:
            ray5 = discord.Embed(
                title="Ignis",
                description=
                f"{str(member)} Is already undeafen in the voice channel",
                color=0x2b2d31)
            ray5.set_author(name=f"{ctx.author}",
                               icon_url=f"{ctx.author.avatar}")
            ray5.set_thumbnail(url=f"{ctx.author.avatar}")
            return await ctx.reply(embed=ray5)
        ch = member.voice.channel.mention
        ray = discord.Embed(
            title="Ignis",
            description=f"{str(member)} has been undeafen in {ch}",
            color=0x2b2d31)
        ray.set_author(name=f"{ctx.author}",
                          icon_url=f"{ctx.author.avatar}")
        ray.set_thumbnail(url=f"{ctx.author.avatar}")
        await member.edit(deafen=False,
                          reason=f"Undeafen by {str(ctx.author)}")
        return await ctx.reply(embed=ray)

    @vc.command(name="deafenall",
                help="deafen all member in a voice channel .",
                usage="voice deafenall")
    @commands.has_permissions(administrator=True)
    @commands.cooldown(1, 10, commands.BucketType.user)
    @blacklist_check()
    @ignore_check()
    @commands.max_concurrency(1, per=commands.BucketType.default, wait=False)
    async def _deafenall(self, ctx):
        if ctx.author.voice is None:
            error = discord.Embed(
                title="Ignis",
                description=
                f"You are not connected in any of the voice channel",
                color=0x2b2d31)
            error.set_author(name=f"{ctx.author}",
                             icon_url=f"{ctx.author.avatar}")
            error.set_thumbnail(url=f"{ctx.author.avatar}")
            return await ctx.reply(embed=error)
        count = 0
        ch = ctx.author.voice.channel.mention
        for member in ctx.author.voice.channel.members:
            if member.voice.deaf == False:
                await member.edit(
                    deafen=True,
                    reason=
                    f"voice deafenall Command Executed by {str(ctx.author)}")
                count += 1
        ray = discord.Embed(title="Ignis",
                               description=f"Deafened {count} members in {ch}",
                               color=0x2b2d31)
        ray.set_author(name=f"{ctx.author}",
                          icon_url=f"{ctx.author.avatar}")
        ray.set_thumbnail(url=f"{ctx.author.avatar}")
        return await ctx.reply(embed=ray)

    @vc.command(name="undeafenall",
                help="undeafen all member in a voice channel .",
                usage="voice undeafenall")
    @commands.has_permissions(administrator=True)
    @commands.cooldown(1, 10, commands.BucketType.user)
    @blacklist_check()
    @ignore_check()
    @commands.max_concurrency(1, per=commands.BucketType.default, wait=False)
    async def _undeafall(self, ctx):
        if ctx.author.voice is None:
            error = discord.Embed(
                title="Ignis",
                description=
                f"You are not connected in any of the voice channel",
                color=0x2b2d31)
            error.set_author(name=f"{ctx.author}",
                             icon_url=f"{ctx.author.avatar}")
            error.set_thumbnail(url=f"{ctx.author.avatar}")
            return await ctx.reply(embed=error)
        count = 0
        ch = ctx.author.voice.channel.mention
        for member in ctx.author.voice.channel.members:
            if member.voice.deaf == True:
                await member.edit(
                    deafen=False,
                    reason=
                    f"voice undeafenall Command Executed by {str(ctx.author)}")
                count += 1
        ray = discord.Embed(
            title="Ignis",
            description=f"Undeafened {count} members in {ch}",
            color=0x2b2d31)
        ray.set_author(name=f"{ctx.author}",
                          icon_url=f"{ctx.author.avatar}")
        ray.set_thumbnail(url=f"{ctx.author.avatar}")
        return await ctx.reply(embed=ray)

    @vc.command(name="moveall",
                help="Moves all the members from the voice channel .",
                usage="voice moveall <voice channel>")
    @commands.has_permissions(administrator=True)
    @commands.cooldown(1, 10, commands.BucketType.user)
    @blacklist_check()
    @ignore_check()
    @commands.max_concurrency(1, per=commands.BucketType.default, wait=False)
    async def _moveall(self, ctx, *, channel: discord.VoiceChannel):
        if ctx.author.voice is None:
            error = discord.Embed(
                title="Ignis",
                description=
                f"You are not connected in any of the voice channel",
                color=0x2b2d31)
            error.set_author(name=f"{ctx.author}",
                             icon_url=f"{ctx.author.avatar}")
            error.set_thumbnail(url=f"{ctx.author.avatar}")
            return await ctx.reply(embed=error)
        try:
            ch = ctx.author.voice.channel.mention
            nch = channel.mention
            count = 0
            for member in ctx.author.voice.channel.members:
                await member.edit(
                    voice_channel=channel,
                    reason=
                    f"voice moveall Command Executed by {str(ctx.author)}")
                count += 1
            ray = discord.Embed(
                title="Ignis",
                description=f"{count} Members Moved From {ch} to {nch}",
                color=0x2b2d31)
            ray.set_author(name=f"{ctx.author}",
                              icon_url=f"{ctx.author.avatar}")
            ray.set_thumbnail(url=f"{ctx.author.avatar}")
            await ctx.reply(embed=ray)
        except:
            ray1 = discord.Embed(
                title="Ignis",
                description=f"Invalid Voice channel provided",
                color=0x2b2d31)
            ray1.set_author(name=f"{ctx.author}",
                               icon_url=f"{ctx.author.avatar}")
            ray1.set_thumbnail(url=f"{ctx.author.avatar}")
            await ctx.reply(embed=ray1)
            
    @vc.command(name="pull",
                help="Pulls specified members to your voice channel",
                usage="voice pull <member1> [member2] ...")
    @has_permission_or_admin("move_members")
    @commands.cooldown(1, 10, commands.BucketType.user)
    @blacklist_check()
    @ignore_check()
    @commands.max_concurrency(1, per=commands.BucketType.default, wait=False)
    async def _pull(self, ctx, members: commands.Greedy[discord.Member]):
        if ctx.author.voice is None:
            error = discord.Embed(
                title="Ignis",
                description="You are not connected to any voice channel",
                color=0x2b2d31)
            error.set_author(name=f"{ctx.author}",
                            icon_url=f"{ctx.author.avatar}")
            error.set_thumbnail(url=f"{ctx.author.avatar}")
            return await ctx.reply(embed=error)
        
        if not members:
            error = discord.Embed(
                title="Ignis",
                description="Please specify at least one member to pull",
                color=0x2b2d31)
            return await ctx.reply(embed=error)
        
        success = []
        failed = []
        
        for member in members:
            try:
                await member.edit(
                    voice_channel=ctx.author.voice.channel,
                    reason=f"Voice pull command executed by {ctx.author}"
                )
                success.append(member.mention)
            except Exception as e:
                failed.append(f"{member.mention} ({str(e)})")
        
        embed = discord.Embed(
            title="Ignis - Voice Pull Results",
            color=0x2b2d31)
        embed.set_author(name=ctx.author, icon_url=ctx.author.avatar)
        
        if success:
            embed.add_field(
                name="✅ Successfully Pulled",
                value="\n".join(success) or "None",
                inline=False)
        
        if failed:
            embed.add_field(
                name="❌ Failed to Pull",
                value="\n".join(failed) or "None",
                inline=False)
        
        await ctx.reply(embed=embed)

    @vc.command(name="push",
                help="Pushes specified members to another voice channel",
                usage="voice push <voice_channel> <member1> [member2] ...")
    @has_permission_or_admin("move_members")
    @commands.cooldown(1, 10, commands.BucketType.user)
    @blacklist_check()
    @ignore_check()
    @commands.max_concurrency(1, per=commands.BucketType.default, wait=False)
    async def _push(self, ctx, channel: discord.VoiceChannel, members: commands.Greedy[discord.Member]):
        if not members:
            error = discord.Embed(
                title="Ignis",
                description="Please specify at least one member to push",
                color=0x2b2d31)
            return await ctx.reply(embed=error)
        
        success = []
        failed = []
        
        for member in members:
            try:
                await member.edit(
                    voice_channel=channel,
                    reason=f"Voice push command executed by {ctx.author}"
                )
                success.append(member.mention)
            except Exception as e:
                failed.append(f"{member.mention} ({str(e)})")
        
        embed = discord.Embed(
            title="Ignis - Voice Push Results",
            description=f"Target Channel: {channel.mention}",
            color=0x2b2d31)
        embed.set_author(name=ctx.author, icon_url=ctx.author.avatar)
        
        if success:
            embed.add_field(
                name="✅ Successfully Pushed",
                value="\n".join(success) or "None",
                inline=False)
        
        if failed:
            embed.add_field(
                name="❌ Failed to Push",
                value="\n".join(failed) or "None",
                inline=False)
        
        await ctx.reply(embed=embed)


################################################################


    @commands.group(name="vcrole", invoke_without_command=True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.max_concurrency(1, per=commands.BucketType.default, wait=False)
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    @blacklist_check()
    @ignore_check()
    async def _vcrole(self, ctx):
        if ctx.subcommand_passed is None:
            await ctx.send_help(ctx.command)
            ctx.command.reset_cooldown(ctx)

    @_vcrole.group(name="humans",
                   aliases=["human"],
                   help="Setups vcroles for human users .",
                   invoke_without_command=True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.max_concurrency(1, per=commands.BucketType.default, wait=False)
    @blacklist_check()
    @ignore_check()
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def _humans(self, ctx):
        if ctx.subcommand_passed is None:
            await ctx.send_help(ctx.command)
            ctx.command.reset_cooldown(ctx)

    @_vcrole.group(name="bots",
                   aliases=['bot'],
                   help="Setups vcroles for bots .",
                   invoke_without_command=True)
    @blacklist_check()
    @ignore_check()
    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.max_concurrency(1, per=commands.BucketType.default, wait=False)
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def _bots(self, ctx):
        if ctx.subcommand_passed is None:
            await ctx.send_help(ctx.command)
            ctx.command.reset_cooldown(ctx)

    @_humans.command(name="add",
                     help="Add role to list of vcroles for human users.")
    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.max_concurrency(1, per=commands.BucketType.default, wait=False)
    @blacklist_check()
    @ignore_check()
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def _addhumans(self, ctx, role: discord.Role):
        data = getDB(ctx.guild.id)
        if ctx.author == ctx.guild.owner or ctx.author.top_role.position > ctx.guild.me.top_role.position:
            if role.position >= ctx.guild.me.top_role.position:
                await ctx.send(embed=discord.Embed(
                    color=0x2b2d31,
                    description=
                    "My top role is below {}. Kindly move my role above and try the command again."
                    .format(role.mention)))
            elif data["vcrole"]["humans"] == role.id:
                embed = discord.Embed(
                    description=
                    "<:cross:1348326385386651748> | {} is already in human vcroles ."
                    .format(role.mention),
                    color=0x2b2d31)
                await ctx.reply(embed=embed, mention_author=False)
            else:
                data["vcrole"]["humans"] = role.id
                updateDB(ctx.guild.id, data)
                ray = discord.Embed(
                    description=
                    "<:tick:1348326381611647046> | {} has been added to human vcroles ."
                    .format(role.mention),
                    color=0x2b2d31)
                await ctx.send(embed=ray, mention_author=False)
        else:
            ray5 = discord.Embed(
                description=
                """```yaml\n - You must have Administrator permission.\n - Your top role should be above my top role.```""",
                color=0x2b2d31)
            ray5.set_author(name=f"{ctx.author.name}",
                               icon_url=f"{ctx.author.avatar}")

            await ctx.send(embed=ray5)

    @_bots.command(name="add",
                   help="Add role to list of vcroles for bot users .")
    @blacklist_check()
    @ignore_check()
    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.max_concurrency(1, per=commands.BucketType.default, wait=False)
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def _addbots(self, ctx, role: discord.Role):
        data = getDB(ctx.guild.id)
        if ctx.author == ctx.guild.owner or ctx.author.top_role.position > ctx.guild.me.top_role.position:
            if role.position >= ctx.guild.me.top_role.position:
                await ctx.send(embed=discord.Embed(
                    color=0x2b2d31,
                    description=
                    "My top role is below {}. Kindly move my role above and try the command again."
                    .format(role.mention)))
            elif data["vcrole"]["bots"] == role.id:
                embed = discord.Embed(
                    description=
                    "<:cross:1348326385386651748> | {} is already in bot vcroles ."
                    .format(role.mention),
                    color=0x2b2d31)
                await ctx.reply(embed=embed, mention_author=False)
            else:
                data["vcrole"]["bots"] = role.id
                updateDB(ctx.guild.id, data)
                ray = discord.Embed(
                    description=
                    "<:tick:1348326381611647046> | {} has been added to bot vcroles ."
                    .format(role.mention),
                    color=0x2b2d31)
                await ctx.send(embed=ray, mention_author=False)
        else:
            ray5 = discord.Embed(
                description=
                """```yaml\n - You must have Administrator permission.\n - Your top role should be above my top role.```""",
                color=0x2b2d31)
            ray5.set_author(name=f"{ctx.author.name}",
                               icon_url=f"{ctx.author.avatar}")
            await ctx.send(embed=ray5)

    @_humans.command(name="remove",
                     help="Remove a role from vcroles for human users .")
    @blacklist_check()
    @ignore_check()
    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.max_concurrency(1, per=commands.BucketType.default, wait=False)
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def _removehumans(self, ctx, role: discord.Role):
        data = getDB(ctx.guild.id)
        if ctx.author == ctx.guild.owner or ctx.author.top_role.position > ctx.guild.me.top_role.position:
            if role.position >= ctx.guild.me.top_role.position:
                await ctx.send(embed=discord.Embed(
                    color=0x2b2d31,
                    description=
                    "My top role is below {}. Kindly move my role above and try the command again."
                    .format(role.mention)))
            elif role.id != data["vcrole"]["humans"]:
                embed = discord.Embed(
                    description=
                    "<:cross:1348326385386651748> | {} is not in human vcroles ."
                    .format(role.mention),
                    color=0x2b2d31)
                await ctx.reply(embed=embed)
            elif role.id == data["vcrole"]["humans"]:
                data["vcrole"]["humans"] = ""
                updateDB(ctx.guild.id, data)
                ray = discord.Embed(
                    description=
                    "<:tick:1348326381611647046> | {} has been removed from human vcroles."
                    .format(role.mention),
                    color=0x2b2d31)
                await ctx.send(embed=ray)
        else:
            ray5 = discord.Embed(
                description=
                """```yaml\n - You must have Administrator permission.\n - Your top role should be above my top role.```""",
                color=0x2b2d31)
            ray5.set_author(name=f"{ctx.author.name}",
                               icon_url=f"{ctx.author.avatar}")

            await ctx.send(embed=ray5)

    @_bots.command(name="remove",
                   help="Remove a role from vcroles for bot users .")
    @blacklist_check()
    @ignore_check()
    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.max_concurrency(1, per=commands.BucketType.default, wait=False)
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def _removebots(self, ctx, role: discord.Role):
        data = getDB(ctx.guild.id)
        if ctx.author == ctx.guild.owner or ctx.author.top_role.position > ctx.guild.me.top_role.position:
            if role.position >= ctx.guild.me.top_role.position:
                await ctx.send(embed=discord.Embed(
                    color=0x2b2d31,
                    description=
                    "My top role is below {}. Kindly move my role above and try the command again."
                    .format(role.mention)))
            elif role.id != data["vcrole"]["bots"]:
                embed = discord.Embed(
                    description=
                    "<:cross:1348326385386651748> | {} is not in bot vcroles.".
                    format(role.mention),
                    color=0x2b2d31)
                await ctx.reply(embed=embed)
            elif role.id == data["vcrole"]["bots"]:
                data["vcrole"]["bots"] = ""
                updateDB(ctx.guild.id, data)
                ray = discord.Embed(
                    description=
                    "<:tick:1348326381611647046> | {} has been removed from bot vcroles."
                    .format(role.mention),
                    color=0x2b2d31)
                await ctx.send(embed=ray)
        else:
            ray5 = discord.Embed(
                description=
                """```yaml\n - You must have Administrator permission.\n - Your top role should be above my top role.```""",
                color=0x2b2d31)
            ray5.set_author(name=f"{ctx.author.name}",
                               icon_url=f"{ctx.author.avatar}")

            await ctx.send(embed=ray5)

    @_vcrole.command(name="config", help="Get vcroles config for the server.")
    @blacklist_check()
    @ignore_check()
    @commands.has_permissions(administrator=True)
    async def _config(self, ctx):
        data = getDB(ctx.guild.id)
        embed = discord.Embed(color=0x2b2d31,
                              title=f"{ctx.guild.name} **VC Roles Settings**")
        if data["vcrole"]["humans"] != "":
            hr = data["vcrole"]["humans"]
            hr1 = get(ctx.guild.roles, id=hr)
            embed.add_field(name="__Humans__", value=f"{hr1.mention}")
        else:
            embed.add_field(name="__Humans__", value=f"Not Set")
        if data["vcrole"]["bots"] != "":
            br = data["vcrole"]["bots"]
            br1 = get(ctx.guild.roles, id=br)
            embed.add_field(name="__Bots__", value=br1.mention)
        else:
            embed.add_field(name="__Bots__", value="Not Set")
        await ctx.send(embed=embed)

    @_vcrole.command(name="reset", help="Clear vcroles config for the server.")
    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.max_concurrency(1, per=commands.BucketType.default, wait=False)
    @commands.guild_only()
    @blacklist_check()
    @ignore_check()
    @commands.has_permissions(administrator=True)
    async def _reset(self, ctx):
        data = getDB(ctx.guild.id)
        if ctx.author == ctx.guild.owner or ctx.author.top_role.position > ctx.guild.me.top_role.position:
            if data["vcrole"]["humans"] == "" and data["vcrole"]["bots"] == "":
                embed = discord.Embed(
                    description=
                    "<:cross:1348326385386651748> | This server don't have any vcroles setupped .",
                    color=0x2b2d31)
                await ctx.send(embed=embed)
            else:
                data["vcrole"]["bots"] = ""
                data["vcrole"]["humans"] = ""
                updateDB(ctx.guild.id, data)
                ray = discord.Embed(
                    description=
                    "<:tick:1348326381611647046> | Succesfully cleared all vcroles for this server .",
                    color=0x2b2d31)
                await ctx.send(embed=ray)
        else:
            ray5 = discord.Embed(
                description=
                """```yaml\n - You must have Administrator permission.\n - Your top role should be above my top role.```""",
                color=0x2b2d31)
            ray5.set_author(name=f"{ctx.author.name}",
                               icon_url=f"{ctx.author.avatar}")
            await ctx.send(embed=ray5)
