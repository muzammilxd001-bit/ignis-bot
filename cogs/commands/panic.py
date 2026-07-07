from discord.ext import commands
from utils.Tools import *
import discord
from core import Cog, Ignis, Context
import datetime


class PanicMode(Cog):
    """Advanced server lockdown system"""

    def __init__(self, client: Ignis):
        self.client = client

    def is_owner_or_extra_owner(self, ctx: commands.Context):
        """Check if user is server owner or extra owner"""
        data = getConfig(ctx.guild.id)
        return (ctx.author == ctx.guild.owner or 
                str(ctx.author.id) in data.get("extraowners", []))

    @commands.command(name="panicmode",
                     help="Panic mode control center | Shows guide when used without arguments")
    @blacklist_check()
    @ignore_check()
    @commands.has_permissions(administrator=True)
    async def panicmode_control(self, ctx: commands.Context, action: str = None):
        if action is None:
            # Show comprehensive guide
            data = getConfig(ctx.guild.id)
            embed = discord.Embed(
                title="🚨 Panic Mode Control Center",
                description=(
                    "**Complete Protection System Against Raids**\n\n"
                    "🔹 **Setup Required Before Use:**\n"
                    "1. First set your protected role with `mainrole @Role`\n"
                    "2. Configure punishment type with `panicsetup punishment <ban/quarantine>`\n\n"
                    "🔹 **Activation Commands:**\n"
                    "• `panicmode enable` - Activates full protection\n"
                    "• `panicmode disable` - Deactivates panic mode\n\n"
                    "🔹 **What Happens During Panic Mode:**\n"
                    "✓ Protected role moved to top position\n"
                    "✓ All dangerous permissions disabled\n"
                    "✓ Anti-invite automatically enabled\n"
                    "✓ New members automatically punished\n"
                    "✓ Channel/role creation blocked\n\n"
                    "🔹 **Current Status:**\n"
                    f"• Panic Mode: `{'ACTIVE' if data.get('panic_mode') else 'INACTIVE'}`\n"
                    f"• Protected Role: {'<@&' + str(data.get('panic_main_role')) + '>' if data.get('panic_main_role') else '`NOT SET`'}\n"
                    f"• Punishment Type: `{data.get('panic_punishment', 'Not configured')}`"
                ),
                color=0x2b2d31)
            embed.set_footer(text="Only server owners/extra owners can configure these settings")
            return await ctx.send(embed=embed)
            
        if not self.is_owner_or_extra_owner(ctx):
            embed = discord.Embed(
                description="<:cross:1348326385386651748> | Only server owner or extra owners can control panic mode",
                color=0x2b2d31)
            return await ctx.send(embed=embed)
            
        action = action.lower()
        data = getConfig(ctx.guild.id)
        
        if action == "enable":
            # Verify main role is set
            main_role_id = data.get("panic_main_role")
            if not main_role_id:
                embed = discord.Embed(
                    description="<:cross:1348326385386651748> | No main role set! Use `mainrole @Role` first",
                    color=0x2b2d31)
                return await ctx.send(embed=embed)
                
            main_role = ctx.guild.get_role(main_role_id)
            if not main_role:
                embed = discord.Embed(
                    description="<:cross:1348326385386651748> | Main role not found! Please reconfigure",
                    color=0x2b2d31)
                return await ctx.send(embed=embed)

            try:
                # 1. Move main role to top
                await main_role.edit(position=len(ctx.guild.roles)-1)
                
                # 2. Disable dangerous permissions
                for role in ctx.guild.roles:
                    if role != main_role and role != ctx.guild.default_role:
                        try:
                            await role.edit(permissions=discord.Permissions(
                                send_messages=False,
                                manage_messages=False,
                                manage_roles=False,
                                manage_channels=False,
                                administrator=False
                            ))
                        except:
                            continue
                
                # 3. Enable protections
                data["antiInvite"] = True
                data["panic_mode"] = True
                updateConfig(ctx.guild.id, data)
                
                embed = discord.Embed(
                    title="🚨 PANIC MODE ACTIVATED",
                    description=(
                        f"**Full protection enabled!**\n\n"
                        f"• Protected role moved to top: {main_role.mention}\n"
                        f"• Dangerous permissions revoked\n"
                        f"• Anti-invite system engaged\n"
                        f"• New join protection active\n"
                        f"• Channel/Role creation blocked"
                    ),
                    color=0xff0000)
                await ctx.send(embed=embed)
                
            except discord.Forbidden:
                embed = discord.Embed(
                    description="<:cross:1348326385386651748> | Bot needs administrator permissions",
                    color=0x2b2d31)
                await ctx.send(embed=embed)
                
        elif action == "disable":
            if not data.get("panic_mode", False):
                embed = discord.Embed(
                    description="<:cross:1348326385386651748> | Panic mode isn't active",
                    color=0x2b2d31)
                return await ctx.send(embed=embed)
                
            data["panic_mode"] = False
            data["antiInvite"] = False
            updateConfig(ctx.guild.id, data)
            
            embed = discord.Embed(
                title="🟢 PANIC MODE DEACTIVATED",
                description="All protections have been lifted\nServer returned to normal operation",
                color=0x00ff00)
            await ctx.send(embed=embed)
            
        else:
            embed = discord.Embed(
                description="<:cross:1348326385386651748> | Invalid action. Use `enable` or `disable`",
                color=0x2b2d31)
            await ctx.send(embed=embed)

    @commands.command(name="mainrole",
                     help="Set the main protected role for panic mode")
    @blacklist_check()
    @ignore_check()
    @commands.has_permissions(administrator=True)
    async def set_panic_role(self, ctx: commands.Context, role: discord.Role):
        if not self.is_owner_or_extra_owner(ctx):
            embed = discord.Embed(
                description="<:cross:1348326385386651748> | Only server owner or extra owners can set main role",
                color=0x2b2d31)
            return await ctx.send(embed=embed)
            
        data = getConfig(ctx.guild.id)
        data["panic_main_role"] = role.id
        updateConfig(ctx.guild.id, data)
        
        embed = discord.Embed(
            description=f"<:tick:1348326381611647046> | {role.mention} is now the protected role for panic mode",
            color=0x2b2d31)
        await ctx.send(embed=embed)

    @commands.command(name="panicsetup",
                     help="Configure panic mode settings")
    @blacklist_check()
    @ignore_check()
    @commands.has_permissions(administrator=True)
    async def panic_setup(self, ctx: commands.Context, setting: str = None, value: str = None):
        if setting is None:
            # Show setup guide
            data = getConfig(ctx.guild.id)
            embed = discord.Embed(
                title="⚙️ Panic Mode Setup Guide",
                description=(
                    "**Required Configuration:**\n\n"
                    "1. `mainrole @Role` - Set your main role\n"
                    "2. `panicsetup punishment <ban/quarantine>` - Set join punishment\n\n"
                    f"Current Protected Role: {'<@&' + str(data.get('panic_main_role')) + '>' if data.get('panic_main_role') else '`NOT SET`'}"
                ),
                color=0x2b2d31)
            return await ctx.send(embed=embed)
            
        if not self.is_owner_or_extra_owner(ctx):
            embed = discord.Embed(
                description="<:cross:1348326385386651748> | Only server owner or extra owners can configure panic mode",
                color=0x2b2d31)
            return await ctx.send(embed=embed)
            
        data = getConfig(ctx.guild.id)
        setting = setting.lower()
        
        if setting == "punishment":
            if value.lower() not in ["ban", "quarantine"]:
                embed = discord.Embed(
                    description="<:cross:1348326385386651748> | Invalid punishment. Use `ban` or `quarantine`",
                    color=0x2b2d31)
                return await ctx.send(embed=embed)
                
            data["panic_punishment"] = value.lower()
            updateConfig(ctx.guild.id, data)
            
            embed = discord.Embed(
                description=f"<:tick:1348326381611647046> | New join punishment set to: `{value.lower()}`",
                color=0x2b2d31)
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(
                description="<:cross:1348326385386651748> | Invalid setting. Use `punishment`",
                color=0x2b2d31)
            await ctx.send(embed=embed)

    @Cog.listener()
    async def on_member_join(self, member: discord.Member):
        data = getConfig(member.guild.id)
        if data.get("panic_mode", False):
            punishment = data.get("panic_punishment", "kick")
            
            try:
                if punishment == "ban":
                    await member.ban(reason="Panic mode auto-ban")
                elif punishment == "quarantine":
                    try:
                        await member.edit(communication_disabled_until=datetime.datetime.utcnow() + datetime.timedelta(days=7))
                    except:
                        await member.kick(reason="Panic mode auto-kick (quarantine failed)")
                else:  # Default to kick
                    await member.kick(reason="Panic mode auto-kick")
                    
            except discord.Forbidden:
                pass

    @Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author.bot or self.is_owner_or_extra_owner(message):
            return

        data = getConfig(message.guild.id)
        if data.get("panic_mode", False) and data.get("antiInvite", False):
            if any(x in message.content.lower() for x in ["discord.gg/", "discord.com/invite/"]):
                try:
                    await message.delete()
                    embed = discord.Embed(
                        title="⚠️ Invite Blocked",
                        description=f"{message.author.mention}, invites are blocked during panic mode",
                        color=0xff0000)
                    await message.channel.send(embed=embed, delete_after=10)
                    
                    # Timeout the user
                    try:
                        await message.author.timeout(
                            datetime.timedelta(hours=1),
                            reason="Posted invite during panic mode"
                        )
                    except:
                        pass
                        
                except discord.Forbidden:
                    pass

    @Cog.listener()
    async def on_guild_channel_create(self, channel):
        data = getConfig(channel.guild.id)
        if data.get("panic_mode", False):
            try:
                await channel.delete(reason="Panic mode auto-delete")
            except:
                pass

    @Cog.listener()
    async def on_guild_role_create(self, role):
        data = getConfig(role.guild.id)
        if data.get("panic_mode", False):
            try:
                await role.delete(reason="Panic mode auto-delete")
            except:
                pass