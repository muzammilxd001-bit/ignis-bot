import discord
from discord.ext import commands
from utils.Tools import *
import json
import os
from core import Cog, Ignis, Context

class Marriage(Cog):
    """Marriage system for your Discord server."""

    def __init__(self, client: Ignis):
        self.client = client
        self.marriages = {}
        self.proposals = {}
        self.load_marriages()

    def load_marriages(self):
        try:
            if os.path.exists("data/marriages.json"):
                with open("data/marriages.json", "r") as f:
                    self.marriages = json.load(f)
        except json.JSONDecodeError:
            self.marriages = {}

    def save_marriages(self):
        with open("data/marriages.json", "w") as f:
            json.dump(self.marriages, f, indent=4)

    @commands.command(
        name="propose",
        help="Propose to another member."
    )
    @blacklist_check()
    @ignore_check()
    @commands.cooldown(1, 30, commands.BucketType.user)
    @commands.guild_only()
    async def propose(self, ctx: commands.Context, member: discord.Member):
        if member.id == ctx.author.id:
            await ctx.reply("You can't propose to yourself!", mention_author=False)
            return

        if str(ctx.author.id) in self.marriages:
            await ctx.reply("You are already married!", mention_author=False)
            return

        if str(member.id) in self.marriages:
            await ctx.reply(f"{member.mention} is already married!", mention_author=False)
            return

        self.proposals[(ctx.author.id, member.id)] = ctx.guild.id
        await ctx.reply(f"{member.mention}, {ctx.author.mention} has proposed to you! Type `.accept @{ctx.author.display_name}` to accept the proposal or `.decline @{ctx.author.display_name}` to decline.", mention_author=False)

    @commands.command(
        name="accept",
        help="Accept a marriage proposal."
    )
    @blacklist_check()
    @ignore_check()
    @commands.cooldown(1, 30, commands.BucketType.user)
    @commands.guild_only()
    async def accept(self, ctx: commands.Context, proposer: discord.Member):
        if (proposer.id, ctx.author.id) not in self.proposals:
            await ctx.reply("No proposal found!", mention_author=False)
            return

        guild_id = self.proposals.pop((proposer.id, ctx.author.id))
        if guild_id != ctx.guild.id:
            await ctx.reply("This proposal is not from this server!", mention_author=False)
            return

        if str(proposer.id) in self.marriages or str(ctx.author.id) in self.marriages:
            await ctx.reply("One of you is already married!", mention_author=False)
            return

        self.marriages[str(proposer.id)] = ctx.author.id
        self.marriages[str(ctx.author.id)] = proposer.id
        self.save_marriages()

        await ctx.reply(f"{ctx.author.mention} and {proposer.mention} are now married! <a:tada:1349242523800830003>", mention_author=False)

    @commands.command(
        name="decline",
        help="Decline a marriage proposal."
    )
    @blacklist_check()
    @ignore_check()
    @commands.cooldown(1, 30, commands.BucketType.user)
    @commands.guild_only()
    async def decline(self, ctx: commands.Context, proposer: discord.Member):
        if (proposer.id, ctx.author.id) not in self.proposals:
            await ctx.reply("No proposal found!", mention_author=False)
            return

        self.proposals.pop((proposer.id, ctx.author.id))
        await ctx.reply(f"{ctx.author.mention} has declined the proposal from {proposer.mention} <a:cry:1349242877326393385>", mention_author=False)

    @commands.command(
        name="marriage",
        help="Check your marriage status."
    )
    @blacklist_check()
    @ignore_check()
    @commands.cooldown(1, 30, commands.BucketType.user)
    @commands.guild_only()
    async def marriage(self, ctx: commands.Context, member: discord.Member = None):
        member = member or ctx.author
        if str(member.id) in self.marriages:
            spouse_id = self.marriages[str(member.id)]
            spouse = self.client.get_user(spouse_id)
            if spouse:
                await ctx.reply(f"{member.mention} is married to {spouse.mention}.", mention_author=False)
            else:
                await ctx.reply(f"{member.mention} is single <a:cry:1349242877326393385> (sed life) ", mention_author=False)

    @commands.command(
        name="divorce",
        help="Divorce your current spouse."
    )
    @blacklist_check()
    @ignore_check()
    @commands.cooldown(1, 30, commands.BucketType.user)
    @commands.guild_only()
    async def divorce(self, ctx: commands.Context):
        if str(ctx.author.id) not in self.marriages:
            await ctx.reply("You are not married!", mention_author=False)
            return

        spouse_id = self.marriages.pop(str(ctx.author.id))
        self.marriages.pop(str(spouse_id), None)
        self.save_marriages()

        spouse = self.client.get_user(spouse_id)
        if spouse:
            await ctx.reply(f"{ctx.author.mention} is now divorced from {spouse.mention}.", mention_author=False)
        else:
            await ctx.reply(f"{ctx.author.mention} is now divorced.", mention_author=False)

async def setup(client: Ignis):
    await client.add_cog(Marriage(client))
