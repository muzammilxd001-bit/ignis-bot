import json
import discord
from discord.ext import commands
from utils.Tools import *
from core import Cog, Ignis, Context
import os

class Leveling(Cog):
    """Leveling system for your Discord server."""

    def __init__(self, client: Ignis):
        self.client = client
        self.levels = {}
        self.levelup_channel_id = None
        self.load_levels()

    def load_levels(self):
        try:
            if os.path.exists("data/levels.json"):
                with open("data/levels.json", "r") as f:
                    self.levels = json.load(f)
        except json.JSONDecodeError:
            self.levels = {}

    def save_levels(self):
        with open("data/levels.json", "w") as f:
            json.dump(self.levels, f)

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.client.user:
            return

        if str(message.guild.id) not in self.levels:
            self.levels[str(message.guild.id)] = {}

        if str(message.author.id) not in self.levels[str(message.guild.id)]:
            self.levels[str(message.guild.id)][str(message.author.id)] = {"level": 1, "xp": 0}

        user_data = self.levels[str(message.guild.id)][str(message.author.id)]
        user_data["xp"] += 1

        if user_data["xp"] >= user_data["level"] * 10:
            user_data["xp"] = 0
            user_data["level"] += 1
            if self.levelup_channel_id:
                channel = self.client.get_channel(self.levelup_channel_id)
                if channel:
                    await channel.send(f'Congratulations {message.author.mention}, you have reached level {user_data["level"]}!')

        self.save_levels()

    @commands.hybrid_command(
        name="setlevelupchannel",
        help="Sets the channel for level-up notifications.")
    @blacklist_check()
    @ignore_check()
    @commands.has_permissions(administrator=True)
    @commands.cooldown(1, 30, commands.BucketType.user)
    @commands.max_concurrency(1, per=commands.BucketType.default, wait=False)
    @commands.guild_only()
    async def set_levelup_channel(self, ctx: commands.Context, channel: discord.TextChannel):
        self.levelup_channel_id = channel.id
        await ctx.reply(f'Level up channel set to {channel.mention}', mention_author=False)

    @commands.hybrid_command(
        name="addlevel",
        help="Adds levels to a member.")
    @blacklist_check()
    @ignore_check()
    @commands.has_permissions(administrator=True)
    @commands.cooldown(1, 30, commands.BucketType.user)
    @commands.max_concurrency(1, per=commands.BucketType.default, wait=False)
    @commands.guild_only()
    async def add_level(self, ctx: commands.Context, member: discord.Member, amount: int):
        if str(ctx.guild.id) not in self.levels:
            self.levels[str(ctx.guild.id)] = {}

        if str(member.id) not in self.levels[str(ctx.guild.id)]:
            self.levels[str(ctx.guild.id)][str(member.id)] = {"level": 1, "xp": 0}

        self.levels[str(ctx.guild.id)][str(member.id)]["level"] += amount
        await ctx.reply(f'{member.mention} has been given {amount} levels.', mention_author=False)
        self.save_levels()

    @commands.hybrid_command(
        name="setlevel",
        help="Sets the level of a member.")
    @blacklist_check()
    @ignore_check()
    @commands.has_permissions(administrator=True)
    @commands.cooldown(1, 30, commands.BucketType.user)
    @commands.max_concurrency(1, per=commands.BucketType.default, wait=False)
    @commands.guild_only()
    async def set_level(self, ctx: commands.Context, member: discord.Member, level: int):
        if str(ctx.guild.id) not in self.levels:
            self.levels[str(ctx.guild.id)] = {}

        self.levels[str(ctx.guild.id)][str(member.id)] = {"level": level, "xp": 0}
        await ctx.reply(f'{member.mention} is now set to level {level}.', mention_author=False)
        self.save_levels()

    @commands.hybrid_command(
        name="resetlevel",
        help="Resets the level of a member to 1.")
    @blacklist_check()
    @ignore_check()
    @commands.has_permissions(administrator=True)
    @commands.cooldown(1, 30, commands.BucketType.user)
    @commands.max_concurrency(1, per=commands.BucketType.default, wait=False)
    @commands.guild_only()
    async def reset_level(self, ctx: commands.Context, member: discord.Member):
        if str(ctx.guild.id) not in self.levels:
            self.levels[str(ctx.guild.id)] = {}

        if str(member.id) in self.levels[str(ctx.guild.id)]:
            self.levels[str(ctx.guild.id)][str(member.id)] = {"level": 1, "xp": 0}
            await ctx.reply(f'{member.mention} has been reset to level 1.', mention_author=False)
            self.save_levels()

    @commands.hybrid_command(
        name="level",
        help="Displays your current level and XP in the server.")
    @blacklist_check()
    @ignore_check()
    @commands.cooldown(1, 30, commands.BucketType.user)
    @commands.max_concurrency(1, per=commands.BucketType.default, wait=False)
    @commands.guild_only()
    async def my_level(self, ctx: commands.Context):
        if str(ctx.guild.id) in self.levels and str(ctx.author.id) in self.levels[str(ctx.guild.id)]:
            user_data = self.levels[str(ctx.guild.id)][str(ctx.author.id)]
            embed = discord.Embed(
                title=f"{ctx.author.display_name}'s Level",
                color=discord.Color.blue()
            )
            embed.add_field(name="Level", value=user_data["level"], inline=True)
            embed.add_field(name="XP", value=user_data["xp"], inline=True)
            embed.set_thumbnail(url=ctx.author.avatar.url)
            await ctx.reply(embed=embed, mention_author=False)
        else:
            await ctx.reply(f'{ctx.author.mention}, you have no levels or XP recorded in this server.', mention_author=False)

    @commands.hybrid_command(
        name="leaderboard",
        help="Displays the top 10 members in the server based on levels.")
    @blacklist_check()
    @ignore_check()
    @commands.cooldown(1, 30, commands.BucketType.user)
    @commands.max_concurrency(1, per=commands.BucketType.default, wait=False)
    @commands.guild_only()
    async def leaderboard(self, ctx: commands.Context):
        if str(ctx.guild.id) not in self.levels:
            await ctx.reply("No leveling data found for this server.", mention_author=False)
            return

        guild_data = self.levels[str(ctx.guild.id)]
        sorted_data = sorted(guild_data.items(), key=lambda x: (x[1]['level'], x[1]['xp']), reverse=True)
        top_10 = sorted_data[:10]

        embed = discord.Embed(
            title="Leaderboard",
            description="Top 10 members based on levels and XP",
            color=discord.Color.gold()
        )

        for index, (user_id, user_data) in enumerate(top_10, start=1):
            user = self.client.get_user(int(user_id))
            if user:
                embed.add_field(    
                    name=f"{index}. {user.display_name}",
                    value=f"Level: {user_data['level']} XP: {user_data['xp']}",
                    inline=False
                )

        await ctx.reply(embed=embed, mention_author=False)

async def setup(client: Ignis):
    await client.add_cog(Leveling(client))
