import discord
import json
from discord.ext import commands
from core import Ignis, Cog, Context
from utils.Tools import *


class Errors(Cog):
    def __init__(self, client: Ignis):
        self.client = client
        with open('data/ignore.json', 'r') as heck:
            self.ignore_data = json.load(heck)
        with open('data/blacklist.json', 'r') as f:
            self.blacklist_data = json.load(f)

    @commands.Cog.listener()
    async def on_command_error(self, ctx: Context, error):
        if isinstance(error, commands.CommandNotFound):
            return

        # Check for NoPrivateMessage error
        if isinstance(error, commands.NoPrivateMessage):
            hacker = discord.Embed(color=0x2b2d31, description="You Can't Use My Commands In Dm(s)")
            hacker.set_author(name=ctx.author, icon_url=ctx.author.avatar.url if ctx.author.avatar else ctx.author.default_avatar.url)
            hacker.set_thumbnail(url=ctx.author.avatar.url if ctx.author.avatar else ctx.author.default_avatar.url)
            await ctx.reply(embed=hacker, delete_after=20)
            return

        # Check for Blacklist-related errors
        if isinstance(error, commands.CheckFailure):
            if str(ctx.author.id) in self.blacklist_data["ids"]:
                bl = discord.Embed(description="You are blacklisted from using my commands.\nReason could be excessive use or spamming commands.\nJoin our [Support Server](https://discord.com/invite/JJkF4jjVAE) to appeal.", color=discord.Colour(0x2b2d31))
                await ctx.reply(embed=bl, mention_author=False, delete_after=8)
                return

        # Check for Ignore-related errors
        if str(ctx.channel.id) in self.ignore_data["ids"]:
            await ctx.reply(embed=discord.Embed(description="This Channel is in the ignored channel list. Try my commands in another channel.", color=discord.Colour(0x2b2d31)), delete_after=8)


            return

        # Other Error Handling
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send_help(ctx.command)
            ctx.command.reset_cooldown(ctx)
            return

        if isinstance(error, commands.TooManyArguments):
            await ctx.send_help(ctx.command)
            ctx.command.reset_cooldown(ctx)
            return

        if isinstance(error, commands.CommandOnCooldown):
            hacker = discord.Embed(color=0x2b2d31, description=f"{ctx.author.name} is on cooldown retry after {error.retry_after:.2f} second(s)")
            hacker.set_author(name=f"{ctx.author}", icon_url=ctx.author.avatar.url if ctx.author.avatar else ctx.author.default_avatar.url)
            hacker.set_thumbnail(url=ctx.author.avatar.url if ctx.author.avatar else ctx.author.default_avatar.url)
            await ctx.reply(embed=hacker, delete_after=10)
            return

        if isinstance(error, commands.MaxConcurrencyReached):
            hacker = discord.Embed(color=0x2b2d31, description="This Command is already going on, let it finish and retry after")
            hacker.set_author(name=ctx.author, icon_url=ctx.author.avatar.url if ctx.author.avatar else ctx.author.default_avatar.url)
            hacker.set_thumbnail(url=ctx.author.avatar.url if ctx.author.avatar else ctx.author.default_avatar.url)
            await ctx.reply(embed=hacker, delete_after=10)
            ctx.command.reset_cooldown(ctx)
            return

        if isinstance(error, commands.MissingPermissions):
            member = ctx.author if isinstance(ctx.author, discord.Member) else ctx.guild.get_member(ctx.author.id)
            missing = [perm.replace("_", " ").replace("guild", "server").title() for perm in error.missing_permissions]
            fmt = ", and ".join(missing) if len(missing) > 1 else "".join(missing)
            
            hacker = discord.Embed(color=0xff0000, description=f"<:cross:1348326385386651748> | You lack `{fmt}` permission(s) to run `{ctx.command.name}` command!")
            
            if ctx.channel.permissions_for(ctx.guild.me).send_messages:
                await ctx.reply(embed=hacker, delete_after=6)
            else:
                await ctx.author.send(embed=hacker)
            
            ctx.command.reset_cooldown(ctx)
            return

        if isinstance(error, commands.BadArgument):
            await ctx.send_help(ctx.command)
            ctx.command.reset_cooldown(ctx)
            return

        if isinstance(error, commands.BotMissingPermissions):
            missing = ", ".join(error.missing_perms)
            await ctx.send(f'I need the **{missing}** to run the **{ctx.command.name}** command!', delete_after=10)
            return

        if isinstance(error, discord.Forbidden):
            await ctx.author.send("I don't have permission to send messages in that channel.")
            return

      #  await ctx.send(f"An error occurred: {error}")
