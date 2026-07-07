import json
import discord
from discord.ext import commands
from utils.Tools import *
from core import Cog, Ignis, Context
from discord.ui import View, Button, Select

# Utility functions for JSON operations
def read_db():
    try:
        with open('data/voice.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def write_db(data):
    with open('data/voice.json', 'w') as f:
        json.dump(data, f, indent=4)

class VoiceControlView(View):
    def __init__(self, channel_id, creator_id):
        super().__init__(timeout=None)
        self.channel_id = channel_id
        self.creator_id = creator_id
        
    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        if interaction.user.id != self.creator_id:
            await interaction.response.send_message("❌ Only the channel creator can use these controls!", ephemeral=True)
            return False
        return True
    
    @discord.ui.button(label="Trust User", style=discord.ButtonStyle.green, emoji="✅", row=2)
    async def trust_user(self, interaction: discord.Interaction, button: Button):
        """Add a user to the trusted list"""
        db = read_db()
        guild_data = db.get(str(interaction.guild.id), {})  # Remove the extra comma here
        channel_data = guild_data.get("temp_channels", {}).get(str(self.channel_id), {})
        
        # Get all server members not already trusted
        trusted_users = channel_data.get("trusted_users", [])
        members = [m for m in interaction.guild.members 
                  if m.id not in trusted_users 
                  and m.id != self.creator_id
                  and not m.bot]
        
        if not members:
            await interaction.response.send_message("No members available to trust!", ephemeral=True)
            return
            
        options = [
            discord.SelectOption(label=member.display_name, value=str(member.id))
            for member in members[:25]  # Discord limit of 25 options
        ]
        
        select = Select(placeholder="Select member to trust", options=options)
        
        async def select_callback(interaction: discord.Interaction):
            member_id = int(select.values[0])
            member = interaction.guild.get_member(member_id)
            
            if member:
                # Update database
                if "trusted_users" not in channel_data:
                    channel_data["trusted_users"] = []
                if member_id not in channel_data["trusted_users"]:
                    channel_data["trusted_users"].append(member_id)
                    db[str(interaction.guild.id)]["temp_channels"][str(self.channel_id)] = channel_data
                    write_db(db)
                    
                # Update channel permissions
                channel = interaction.guild.get_channel(self.channel_id)
                if channel:
                    await channel.set_permissions(member, connect=True)
                
                await interaction.response.send_message(
                    f"✅ {member.mention} can now join your locked channel!",
                    ephemeral=True
                )
        
        select.callback = select_callback
        view = View()
        view.add_item(select)
        await interaction.response.send_message("Select member to trust:", view=view, ephemeral=True)
    
    @discord.ui.button(label="Untrust User", style=discord.ButtonStyle.red, emoji="❌", row=2)
    async def untrust_user(self, interaction: discord.Interaction, button: Button):
        """Remove a user from the trusted list"""
        db = read_db()
        guild_data = db.get(str(interaction.guild.id), {})  # Remove the extra comma here
        channel_data = guild_data.get("temp_channels", {}).get(str(self.channel_id), {})
        trusted_users = channel_data.get("trusted_users", [])
        
        if not trusted_users:
            await interaction.response.send_message("No trusted users to remove!", ephemeral=True)
            return
            
        # Get member objects for trusted users
        options = []
        for user_id in trusted_users[:25]:  # Discord limit of 25 options
            member = interaction.guild.get_member(user_id)
            if member:
                options.append(discord.SelectOption(
                    label=member.display_name,
                    value=str(user_id)
                ))
        
        if not options:
            await interaction.response.send_message("No trusted users found!", ephemeral=True)
            return
            
        select = Select(placeholder="Select member to untrust", options=options)
        
        async def select_callback(interaction: discord.Interaction):
            member_id = int(select.values[0])
            member = interaction.guild.get_member(member_id)
            
            if member_id in channel_data.get("trusted_users", []):
                # Update database
                channel_data["trusted_users"].remove(member_id)
                db[str(interaction.guild.id)]["temp_channels"][str(self.channel_id)] = channel_data
                write_db(db)
                
                # Update channel permissions
                channel = interaction.guild.get_channel(self.channel_id)
                if channel:
                    await channel.set_permissions(member, overwrite=None)  # Remove specific permission
                
                await interaction.response.send_message(
                    f"❌ {member.mention} can no longer join your locked channel!",
                    ephemeral=True
                )
        
        select.callback = select_callback
        view = View()
        view.add_item(select)
        await interaction.response.send_message("Select member to untrust:", view=view, ephemeral=True)

    
    @discord.ui.button(label="Lock", style=discord.ButtonStyle.gray, emoji="🔒")
    async def lock(self, interaction: discord.Interaction, button: Button):
        channel = interaction.guild.get_channel(self.channel_id)
        if channel:
            # Get trusted users from database
            db = read_db()
            trusted_users = db.get(str(interaction.guild.id), {}).get("temp_channels", {}).get(str(self.channel_id), {}).get("trusted_users", [])
            
            # Deny connect for everyone except trusted users
            await channel.set_permissions(interaction.guild.default_role, connect=False)
            
            # Ensure trusted users keep access
            for user_id in trusted_users:
                member = interaction.guild.get_member(user_id)
                if member:
                    await channel.set_permissions(member, connect=True)
            
            await interaction.response.send_message("🔒 Channel locked (trusted users can still join)!", ephemeral=True)
    
    @discord.ui.button(label="Unlock", style=discord.ButtonStyle.gray, emoji="🔓")
    async def unlock(self, interaction: discord.Interaction, button: Button):
        channel = interaction.guild.get_channel(self.channel_id)
        if channel:
            # Allow everyone to connect
            await channel.set_permissions(interaction.guild.default_role, connect=True)
            
            # Clear individual user overrides (optional)
            db = read_db()
            trusted_users = db.get(str(interaction.guild.id), {}).get("temp_channels", {}).get(str(self.channel_id), {}).get("trusted_users", [])
            for user_id in trusted_users:
                member = interaction.guild.get_member(user_id)
                if member:
                    await channel.set_permissions(member, overwrite=None)
            
            await interaction.response.send_message("🔓 Channel unlocked for everyone!", ephemeral=True)
    
    @discord.ui.button(label="Hide", style=discord.ButtonStyle.gray, emoji="👻")
    async def hide(self, interaction: discord.Interaction, button: Button):
        channel = interaction.guild.get_channel(self.channel_id)
        if channel:
            await channel.set_permissions(interaction.guild.default_role, view_channel=False)
            await interaction.response.send_message("👻 Channel hidden!", ephemeral=True)
    
    @discord.ui.button(label="Unhide", style=discord.ButtonStyle.gray, emoji="👀")
    async def unhide(self, interaction: discord.Interaction, button: Button):
        channel = interaction.guild.get_channel(self.channel_id)
        if channel:
            await channel.set_permissions(interaction.guild.default_role, view_channel=True)
            await interaction.response.send_message("👀 Channel unhidden!", ephemeral=True)
    
    @discord.ui.button(label="Kick", style=discord.ButtonStyle.red, emoji="👢")
    async def kick(self, interaction: discord.Interaction, button: Button):
        channel = interaction.guild.get_channel(self.channel_id)
        if channel:
            options = [
                discord.SelectOption(label=member.display_name, value=str(member.id))
                for member in channel.members if member.id != self.creator_id
            ]
            if not options:
                await interaction.response.send_message("No members to kick!", ephemeral=True)
                return
                
            select = Select(placeholder="Select member to kick", options=options)
            
            async def select_callback(interaction: discord.Interaction):
                member_id = int(select.values[0])
                member = interaction.guild.get_member(member_id)
                if member:
                    await member.move_to(None)
                    await interaction.response.send_message(f"👢 {member.display_name} has been kicked!", ephemeral=True)
            
            select.callback = select_callback
            view = View()
            view.add_item(select)
            await interaction.response.send_message("Select member to kick:", view=view, ephemeral=True)
    
    @discord.ui.button(label="Limit", style=discord.ButtonStyle.blurple, emoji="👥")
    async def limit(self, interaction: discord.Interaction, button: Button):
        options = [
            discord.SelectOption(label="No limit", value="0"),
            discord.SelectOption(label="2 users", value="2"),
            discord.SelectOption(label="3 users", value="3"),
            discord.SelectOption(label="5 users", value="5"),
            discord.SelectOption(label="10 users", value="10")
        ]
        
        select = Select(placeholder="Set user limit", options=options)
        
        async def select_callback(interaction: discord.Interaction):
            channel = interaction.guild.get_channel(self.channel_id)
            if channel:
                limit = int(select.values[0])
                await channel.edit(user_limit=limit)
                msg = "Removed user limit" if limit == 0 else f"Set user limit to {limit}"
                await interaction.response.send_message(f"👥 {msg}!", ephemeral=True)
        
        select.callback = select_callback
        view = View()
        view.add_item(select)
        await interaction.response.send_message("Set user limit:", view=view, ephemeral=True)

class J2C(commands.Cog):
    """Join-to-Create voice channel system commands"""
    
    def __init__(self, client: Ignis):
        self.client = client
    
    @commands.hybrid_group(name="j2c", invoke_without_command=True)
    @blacklist_check()
    @ignore_check()
    @commands.guild_only()
    async def j2c_group(self, ctx: Context):
        """Join-to-Create voice channel system"""
        await ctx.send_help(ctx.command)

    @j2c_group.command(name="setup", help="Sets up the J2C system in your server")
    @commands.cooldown(1, 7, commands.BucketType.user)
    @commands.max_concurrency(1, per=commands.BucketType.default, wait=False)
    async def setup_j2c(self, ctx: commands.Context):
        guild = ctx.guild
        db = read_db()
        
        # Create J2C category if it doesn't exist
        category = discord.utils.get(guild.categories, name="J2C")
        if not category:
            category = await guild.create_category("J2C")
        
        # Create control text channel if it doesn't exist
        control_channel = discord.utils.get(guild.text_channels, name="vc-controls")
        if not control_channel:
            overwrites = {
                guild.default_role: discord.PermissionOverwrite(send_messages=False),
                guild.me: discord.PermissionOverwrite(send_messages=True)
            }
            control_channel = await guild.create_text_channel(
                "vc-controls",
                category=category,
                overwrites=overwrites
            )
            
            # Send instructions message
            embed = discord.Embed(
                title="Voice Channel Controls",
                description="When you create a temporary voice channel, your controls will appear here.",
                color=0x2b2d31
            )
            await control_channel.send(embed=embed)
        
        # Create J2C voice channel if it doesn't exist
        existing_channel = discord.utils.get(guild.voice_channels, name="Join to Create")
        if not existing_channel:
            new_channel = await guild.create_voice_channel("Join to Create", category=category)
            db[str(guild.id)] = {
                "j2c_channel": new_channel.id,
                "control_channel": control_channel.id,
                "temp_channels": {}
            }
            write_db(db)
            await ctx.reply(embed=discord.Embed(
                description="<:tick:1348326381611647046> | J2C system setup successfully with control channel!",
                color=0x2b2d31), mention_author=False)
        else:
            await ctx.reply(embed=discord.Embed(
                description="<:cross:1348326385386651748> | J2C system already exists.",
                color=0x2b2d31), mention_author=False)

    @j2c_group.command(name="config", help="Configure J2C settings")
    @commands.has_permissions(manage_guild=True)
    async def config_j2c(self, ctx: Context):
        """Configure J2C settings"""
        db = read_db()
        guild_data = db.get(str(ctx.guild.id), {})
        
        if not guild_data:
            return await ctx.reply("J2C system is not setup yet! Use `j2c setup` first.")
        
        embed = discord.Embed(
            title="J2C Configuration",
            description="Current J2C system settings",
            color=0x2b2d31
        )
        
        j2c_channel = ctx.guild.get_channel(guild_data.get("j2c_channel", 0))
        control_channel = ctx.guild.get_channel(guild_data.get("control_channel", 0))
        temp_channels = len(guild_data.get("temp_channels", {}))
        
        embed.add_field(name="Join-to-Create Channel", value=j2c_channel.mention if j2c_channel else "Not found", inline=True)
        embed.add_field(name="Control Channel", value=control_channel.mention if control_channel else "Not found", inline=True)
        embed.add_field(name="Active Temp Channels", value=str(temp_channels), inline=True)
        
        await ctx.reply(embed=embed)

    @j2c_group.command(name="reset", help="Reset the J2C system (deletes all temp channels)")
    @commands.has_permissions(administrator=True)
    async def reset_j2c(self, ctx: Context):
        """Reset the J2C system"""
        db = read_db()
        guild_data = db.get(str(ctx.guild.id), {})
        
        if not guild_data:
            return await ctx.reply("J2C system is not setup yet! Use `j2c setup` first.")
        
        # Confirm with user
        view = ConfirmView(ctx.author)
        msg = await ctx.reply(
            "⚠️ This will delete ALL temporary voice channels and reset the system. Continue?",
            view=view
        )
        
        await view.wait()
        if not view.value:
            return await msg.edit(content="J2C reset cancelled.", view=None)
        
        # Delete all temp channels
        temp_channels = guild_data.get("temp_channels", {})
        deleted = 0
        
        for channel_id in list(temp_channels.keys()):
            channel = ctx.guild.get_channel(int(channel_id))
            if channel:
                try:
                    await channel.delete()
                    deleted += 1
                except:
                    pass
        
        # Reset database entry
        db[str(ctx.guild.id)] = {
            "j2c_channel": guild_data["j2c_channel"],
            "control_channel": guild_data["control_channel"],
            "temp_channels": {}
        }
        write_db(db)
        
        await msg.edit(
            content=f"✅ J2C system reset complete. Deleted {deleted} temporary voice channels.",
            view=None
        )

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        guild = member.guild
        db = read_db()
        guild_data = db.get(str(guild.id), {})
        j2c_channel_id = guild_data.get("j2c_channel")
        control_channel_id = guild_data.get("control_channel")

        if not j2c_channel_id or not control_channel_id:
            return

        j2c_channel = guild.get_channel(j2c_channel_id)
        control_channel = guild.get_channel(control_channel_id)

        # User joined the J2C channel
        if after.channel == j2c_channel and before.channel != j2c_channel:
            category = discord.utils.get(guild.categories, name="J2C") or await guild.create_category("J2C")
            
            # Check if user is still in voice (prevent race condition)
            if not member.voice or not member.voice.channel:
                return

            # Create personal VC
            try:
                new_channel = await guild.create_voice_channel(
                    f"{member.name}'s VC",
                    category=category,
                    user_limit=5
                )
                
                # Move user with error handling
                try:
                    await member.move_to(new_channel)
                except discord.HTTPException as e:
                    if e.code == 40032:  # User not in voice
                        await new_channel.delete()
                        return
                    raise

                # Send control panel
                view = VoiceControlView(new_channel.id, member.id)
                msg = await control_channel.send(
                    f"🎚️ **Voice Channel Controls** for {member.mention}'s channel",
                    view=view
                )
                
                # Update DB
                if "temp_channels" not in db[str(guild.id)]:
                    db[str(guild.id)]["temp_channels"] = {}
                db[str(guild.id)]["temp_channels"][str(new_channel.id)] = {
                    "creator": member.id,
                    "control_message": msg.id,
                    "trusted_users": []  # Initialize empty trusted users list
                }

                write_db(db)

            except Exception as e:
                print(f"Error creating VC: {e}")
                if 'new_channel' in locals():
                    await new_channel.delete()

        # User left a temp channel
        if before.channel and before.channel != j2c_channel:
            temp_channels = db[str(guild.id)].get("temp_channels", {})
            if str(before.channel.id) in temp_channels:
                # Handle empty channel cleanup
                if len(before.channel.members) == 0:
                    try:
                        await before.channel.delete()
                        # Delete control message
                        try:
                            msg = await control_channel.fetch_message(temp_channels[str(before.channel.id)]["control_message"])
                            await msg.delete()
                        except:
                            pass
                        # Update DB
                        del temp_channels[str(before.channel.id)]
                        write_db(db)
                    except:
                        pass

class ConfirmView(View):
    def __init__(self, author: discord.Member):
        super().__init__(timeout=30)
        self.value = None
        self.author = author
    
    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        return interaction.user == self.author
    
    @discord.ui.button(label="Confirm", style=discord.ButtonStyle.green)
    async def confirm(self, interaction: discord.Interaction, button: Button):
        self.value = True
        self.stop()
    
    @discord.ui.button(label="Cancel", style=discord.ButtonStyle.red)
    async def cancel(self, interaction: discord.Interaction, button: Button):
        self.value = False
        self.stop()

async def setup(client: Ignis):
    await client.add_cog(J2C(client))