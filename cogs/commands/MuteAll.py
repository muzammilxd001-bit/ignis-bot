import discord
from discord.ext import commands
import datetime

class MuteAll(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(name="setupmuterole", description="Sets up a 'Muted' role with the necessary permissions.", usage="setupmuterole")
    @commands.has_permissions(manage_roles=True)
    async def setup_mute_role(self, ctx):
        # Check if the role already exists
        muted_role = discord.utils.get(ctx.guild.roles, name="Muted")
        if muted_role:
            await ctx.send("The 'Muted' role already exists.")
            return

        # Create the role
        try:
            muted_role = await ctx.guild.create_role(name="Muted", permissions=discord.Permissions(send_messages=False))
            await ctx.send(f"Created 'Muted' role with ID {muted_role.id}.")
            
            # Set the role permissions
            for channel in ctx.guild.channels:
                await channel.set_permissions(muted_role, send_messages=False)

            await ctx.send("Role 'Muted' created and permissions set.")
        except Exception as e:
            await ctx.send(f"An error occurred while creating the role: {str(e)}")

    @commands.command(name="muteall", description="Timeouts all members by adding the 'Muted' role.", usage="muteall")
    @commands.cooldown(1, 20, commands.BucketType.guild)
    @commands.max_concurrency(1, per=commands.BucketType.guild, wait=False)
    @commands.guild_only()
    @commands.has_permissions(manage_roles=True)
    async def _muteall(self, ctx):
        muted_role = discord.utils.get(ctx.guild.roles, name="Muted")
        if not muted_role:
            await ctx.send("Muted role not found. Please create a 'Muted' role using `!setupmuterole`.")
            return

        members_muted = []
        for member in ctx.guild.members:
            if not member.bot and not member.guild_permissions.administrator:
                try:
                    await member.add_roles(muted_role, reason=f"Command used by {ctx.author}")
                    members_muted.append(member.mention)
                except Exception as e:
                    await ctx.send(f"Failed to mute {member.mention}: {str(e)}")

        muted_list = "\n".join(members_muted) if members_muted else "None"
        embed = discord.Embed(
            color=0x2b2d31,
            description=f"<:tick:1348326381611647046> | Successfully muted all members.\n\nMuted Members:\n{muted_list}",
            timestamp=ctx.message.created_at
        )
        await ctx.send(embed=embed)

    @commands.command(name="unmuteall", description="Unmutes all members by removing the 'Muted' role.", usage="unmuteall")
    @commands.cooldown(1, 20, commands.BucketType.guild)
    @commands.max_concurrency(1, per=commands.BucketType.guild, wait=False)
    @commands.guild_only()
    @commands.has_permissions(manage_roles=True)
    async def _unmuteall(self, ctx):
        muted_role = discord.utils.get(ctx.guild.roles, name="Muted")
        if not muted_role:
            await ctx.send("Muted role not found.")
            return

        members_unmuted = []
        for member in ctx.guild.members:
            if not member.bot and not member.guild_permissions.administrator:
                try:
                    await member.remove_roles(muted_role, reason=f"Command used by {ctx.author}")
                    members_unmuted.append(member.mention)
                except Exception as e:
                    await ctx.send(f"Failed to unmute {member.mention}: {str(e)}")

        unmuted_list = "\n".join(members_unmuted) if members_unmuted else "None"
        embed = discord.Embed(
            color=0x2b2d31,
            description=f"<:tick:1348326381611647046> | Successfully unmuted all members.\n\nUnmuted Members:\n{unmuted_list}",
            timestamp=ctx.message.created_at
        )
        await ctx.send(embed=embed)

async def setup(client):
    await client.add_cog(MuteAll(client))
