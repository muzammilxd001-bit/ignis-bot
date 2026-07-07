import discord
from discord.ext import commands
from utils.Tools import *
import json


class Vanityroles(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.group(name="vanityroles",
                    description="Setups vanity roles for the server .",
                    help="Setups vanity roles for the server .",
                    aliases=['vr'])
    @blacklist_check()
    @commands.has_permissions(administrator=True)
    async def __vr(self, ctx):
        if ctx.subcommand_passed is None:
            await ctx.send_help(ctx.command)
            ctx.command.reset_cooldown(ctx)

    @__vr.command(name="setup",
                  description="Setups vanity role for the server .",
                  help="Setups vanity role for the server .")
    @blacklist_check()
    @commands.has_permissions(administrator=True)
    async def _setup(self, ctx, vanity, role: discord.Role,
                     channel: discord.TextChannel):
        with open("data/vanity.json", "r") as f:
            idk = json.load(f)
            if ctx.author == ctx.guild.owner or ctx.guild.me.top_role <= ctx.author.top_role:
                if role.permissions.administrator or role.permissions.ban_members or role.permissions.kick_members:
                    embed1 = discord.Embed(
                        description=
                        "<:cross:1348326385386651748> | Please Select Role That Dont Have Any Type Of Dangerous Permissions.",
                        color=0x2b2d31)
                    await ctx.send(embed=embed1)
                else:
                    pop = {
                        "vanity": vanity,
                        "role": role.id,
                        "channel": channel.id
                    }
                    idk[str(ctx.guild.id)] = pop
                    embed = discord.Embed(color=0x2b2d31)
                    embed.set_author(
                        name=f"Vanity Roles Config For {ctx.guild.name}",
                        icon_url=f"{ctx.author.avatar}")
                    embed.add_field(
                        name="<:arrow_right:1348340445708816494> Vanity",
                        value=f"{vanity}",
                        inline=False)
                    embed.add_field(
                        name="<:arrow_right:1348340445708816494> Role",
                        value=f"{role.mention}",
                        inline=False)
                    embed.add_field(
                        name="<:arrow_right:1348340445708816494> Channel",
                        value=f"{channel.mention}",
                        inline=False)
                    await ctx.send(embed=embed)
                    with open("data/vanity.json", "w") as f:
                        json.dump(idk, f, indent=4)
            else:
                ray5 = discord.Embed(
                    description=
                    """```diff\n - You must have Administrator permission.\n - Your top role should be above my top role. \n```""",
                    color=0x2b2d31)
                ray5.set_author(name=f"{ctx.author.name}",
                                   icon_url=f"{ctx.author.avatar}")
                await ctx.reply(embed=ray5, mention_author=False)

    @__vr.command(name="reset",
                  description="reset vanity role for the server .",
                  help="reset vanity role for the server .")
    @blacklist_check()
    @commands.has_permissions(administrator=True)
    async def ___reset(self, ctx):
        with open("data/vanity.json", "r") as f:
            jnl = json.load(f)
            if ctx.author == ctx.guild.owner or ctx.guild.me.top_role <= ctx.author.top_role:
                if str(ctx.guild.id) not in jnl:
                    embed1 = discord.Embed(
                        description=
                        "<:cross:1348326385386651748> | This server don't have any vanity roles setupped yet .",
                        color=0x2b2d31)
                    await ctx.reply(embed=embed1, mention_author=False)
                else:
                    jnl.pop(str(ctx.guild.id))
                    await ctx.reply(
                        f"Vanity Role System Removed For This Guild.",
                        mention_author=False)
                    with open('data/vanity.json', 'w') as f:
                        json.dump(jnl, f, indent=4)
            else:
                ray5 = discord.Embed(
                    description=
                    """```diff\n - You must have Administrator permission.\n - Your top role should be above my top role. \n```""",
                    color=0x2b2d31)
                ray5.set_author(name=f"{ctx.author.name}",
                                   icon_url=f"{ctx.author.avatar}")
                await ctx.reply(embed=ray5, mention_author=False)

    @__vr.command(name="show",
                  description="shows vanity role config for the server .",
                  help="shows vanity role config for the server .")
    @blacklist_check()
    @commands.has_permissions(administrator=True)
    async def config(self, ctx):
        with open("data/vanity.json", "r") as f:
            jnl = json.load(f)
        if str(ctx.guild.id) not in jnl:
            embed1 = discord.Embed(
                description=
                "<:cross:1348326385386651748> | This server don't have any vanity roles setupped yet .",
                color=0x2b2d31)
            await ctx.reply(embed=embed1, mention_author=False)
        elif str(ctx.guild.id) in jnl:
            vanity = jnl[str(ctx.guild.id)]["vanity"]
            role = jnl[str(ctx.guild.id)]["role"]
            channel = jnl[str(ctx.guild.id)]["channel"]
            lundchannel = self.bot.get_channel(channel)
            Ignisrole = ctx.guild.get_role(role)
            embed = discord.Embed(color=0x2b2d31)

            embed.add_field(name="<:arrow_right:1348340445708816494> Vanity",
                            value=f"{vanity}",
                            inline=False)
            embed.add_field(name="<:arrow_right:1348340445708816494> Role",
                            value=f"{Ignisrole.mention}",
                            inline=False)
            embed.add_field(name="<:arrow_right:1348340445708816494> Channel",
                            value=f"{lundchannel.mention}",
                            inline=False)
            embed.set_author(name=f"Vanity Role Config For {ctx.guild.name}",
                             icon_url=f"{ctx.author.avatar}")
            await ctx.send(embed=embed, mention_author=False)




    @commands.Cog.listener()
    async def on_presence_update(self, before, after):
        # Load configuration data from JSON file
        with open("data/vanity.json", "r") as f:
            config_data = json.load(f)

        # Check if guild ID is in the configuration
        guild_id = str(before.guild.id)
        if guild_id not in config_data:
            return

        # Retrieve configuration for the guild
        vanity = config_data[guild_id]["vanity"]
        role_id = config_data[guild_id]["role"]
        channel_id = config_data[guild_id]["channel"]

        # Check if the member went from online to another state
        if before.status == discord.Status.offline:
            return

        # Retrieve channel and role objects
        channel = self.bot.get_channel(channel_id)
        role = after.guild.get_role(role_id)

        # Check if the member is a bot or if guilds are different
        if after.bot or before.guild.id != after.guild.id:
            return

        # Check if activity changed
        if before.activity == after.activity:
            return

        # Vanity role assignment
        if vanity in str(after.activity).lower() and role not in after.roles:
            await after.add_roles(role, reason=f"Added {vanity} In Status")
            embed = discord.Embed(
                color=0x030404,
                description=f"{after.mention} Thanks for representing Vanity {vanity} in your status <a:white_heart:1263167235866890352>",
                timestamp=discord.utils.utcnow()
            )
            embed.set_author(name=after.name, icon_url=after.display_avatar.url)
            embed.set_footer(text="Thanks For Choosing This Server.")
            await channel.send(embed=embed)

        # Vanity role removal
        elif vanity not in str(after.activity).lower() and role in after.roles:
            await after.remove_roles(role, reason=f"Removed {vanity} From Status")
            embed = discord.Embed(
                color=0x030404,
                description=f"{after.mention} Removed Vanity {vanity} From Their Status <a:cry:1349242877326393385>",
                timestamp=discord.utils.utcnow()
            )
            embed.set_author(name=after.name, icon_url=after.display_avatar.url)
            embed.set_footer(text="Thanks For Choosing This Server.")
            await channel.send(embed=embed)