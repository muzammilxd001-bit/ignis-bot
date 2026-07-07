import discord,datetime ; from discord.ext import commands
from utils.Tools import *

# Contact For Paid Bots <@870179991462236170>
class AmanView(discord.ui.View):
  def __init__(self, ctx: commands.Context, timeout = 60):
      super().__init__(timeout=timeout)
      self.ctx = ctx



  async def interaction_check(self, interaction: discord.Interaction):
      if interaction.user.id != self.ctx.author.id and interaction.user.id not in [870179991462236170]:
          await interaction.response.send_message("Opps , Looks like you are not the author of the command .", ephemeral=True)
          return False
      return True

class Ignis(AmanView):
  def __init__(self, ctx: commands.Context):
      super().__init__(ctx, timeout=60)
      self.value = None

  @discord.ui.button(label="Yes", custom_id='yes', style=discord.ButtonStyle.green)
  async def png(self, interaction, button):
      self.value = 'yes'
      self.stop()

  @discord.ui.button(label="No", custom_id='stop', style=discord.ButtonStyle.danger)
  async def cancel(self, interaction, button):
      self.value = 'stop'
      self.stop()

      
  
def getLogging(guildID):
    with open("data/logging.json", "r") as config:
        data = json.load(config)
    if str(guildID) not in data["guilds"]:
        defaultConfig = {
            "mod": None,
            "role": None,
            "message": None,
            "member": None,
            "channel": None,
            "server": None,
            "voice": None
        }
        updateLogging(guildID, defaultConfig)
        return defaultConfig
    return data["guilds"][str(guildID)]


def updateLogging(guildID, data):
    with open("data/logging.json", "r") as config:
        config = json.load(config)
    config["guilds"][str(guildID)] = data
    newdata = json.dumps(config, indent=4, ensure_ascii=False)
    with open("data/logging.json", "w") as config:
        config.write(newdata) 
        
class Logging(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.color = 0x2b2d31


    @commands.group(name="logging",invoke_without_command=True,help="Shows the logging's help menu")
    @blacklist_check()
    @ignore_check()
    async def logging(self, ctx):
        listem = discord.Embed(title="Logging Command", colour=self.color,description="```yaml\n- [] = optional argument\n- <> = required argument\n- Do NOT Type These When Using Commands !```")
        listem.add_field(name="logconfig", value="Get logging config of this server", inline=False)
        listem.add_field(name="logreset", value="Resets all loggings of this server.", inline=False)
        listem.add_field(name="memberlog <channel>", value="Log when someone joins/leaves/nickname/role update etc..", inline=False)
        listem.add_field(name="msglog <channel>", value="Log message deleted/ edited / bulk deleted.", inline=False)
        listem.add_field(name="serverlog <channel>", value="Log server updates like emoji update , icon change, etc.", inline=False)
        listem.add_field(name="rolelog <channel>", value="Log create/ edit/ delete roles.", inline=False)
        listem.add_field(name="modlog <channel>", value="Log mod actions in the server.", inline=False)
        listem.add_field(name="channellog <channel>", value="Log create/ edit/ delete channel", inline=False)
        listem.add_field(name="logall <channel>", value="Configures logging settings for various events in the server in one channel.", inline=False)
        listem.set_author(name=f"{str(ctx.author)}", icon_url=ctx.author.display_avatar.url)
        listem.timestamp = discord.utils.utcnow()
        listem.set_footer(text="Ignis • Page 1/1", icon_url="https://storage.googleapis.com/replit/images/1697368882447_77d962c64daa5462b2333fa30dc91247.gif")
        await ctx.send(embed=listem)




    @commands.command(name="logconfig", invoke_without_command=True,help="Shows the logging Configuration of this server.",usage="logconfig")
    @blacklist_check()
    @ignore_check()
    @commands.has_permissions(administrator=True)  
    async def logconfig(self, ctx):
        data = getLogging(ctx.guild.id)
        embed = discord.Embed(title="Logging Configuration", color=0x2b2d31)
        if data["message"] is None:
          embed.add_field(name="Message Logs", value="None", inline=False)
        else:
          embed.add_field(name="Message Logs", value=f"<#{data['message']}>",inline=False)
        if data["member"] is None:
           embed.add_field(name="Member Logs", value="None", inline=False)
        else:
          embed.add_field(name="Member Logs", value=f"<#{data['member']}>",inline=False)          
        if data["role"] is None:
           embed.add_field(name="Role Logs", value="None", inline=False)
        else:
          embed.add_field(name="Role Logs", value=f"<#{data['role']}>",inline=False)  
        if data["server"] is None:
           embed.add_field(name="Server Logs", value="None", inline=False)
        else:
          embed.add_field(name="Server Logs", value=f"<#{data['server']}>",inline=False)
        if data["mod"] is None:
           embed.add_field(name="Moderator Logs", value="None", inline=False)
        else:
          embed.add_field(name="Moderator Logs", value=f"<#{data['mod']}>",inline=False)  
        if data["channel"] is None:
           embed.add_field(name="Channel Logs", value="None", inline=False)
        else:
          embed.add_field(name="Channel Logs", value=f"<#{data['channel']}>",inline=False)
        embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar.url)
        embed.timestamp = discord.utils.utcnow()
        embed.set_thumbnail(url=self.bot.user.avatar.url)
        await ctx.send(embed=embed)

          
     #########################################################################################
    @commands.command(name="logall",help="Configures logging settings for various events in the server in one channel.",usage="logall <channel>")
    @blacklist_check()
    @ignore_check()
    @commands.has_permissions(administrator=True)
    async def lok(self, ctx, channel: discord.TextChannel = None):
      view = Ignis(ctx)
      if channel is None:
        await ctx.send_help(ctx.command)
        return
      if ctx.author == ctx.guild.owner or ctx.author.top_role.position > ctx.guild.me.top_role.position:
        embed = discord.Embed(description=f"Are you sure to set {channel.mention} for all type of logging in this server?",color=self.color)
        msg = await ctx.send(embed=embed,view=view)
        await view.wait()
        if view.value == 'stop':
          return await msg.edit(embed=discord.Embed(description=f"Okay I will not make {channel.mention} for all type of logging in this server.",color=self.color),view=None)        
        data = getLogging(ctx.guild.id)
        data["message"] = str(channel.id)
        data["mod"] = str(channel.id)
        data["role"] = str(channel.id)
        data["member"] = str(channel.id)
        data["server"] = str(channel.id)
        data["channel"] = str(channel.id)
        updateLogging(ctx.guild.id, data)
        await msg.edit(embed=discord.Embed(description=f"<:tick:1348326381611647046> | Successfully all logs for {ctx.guild.name} and set {channel.mention} for all type of logging in this server.",color=self.color),view=None)
      else:
        lol = discord.Embed(description="""```yaml\n - You must have Administrator permission.\n - Your top role should be above my top role.```""",color=self.color)
        lol.set_author(name=ctx.author,icon_url=ctx.author.avatar.url if ctx.author.avatar else ctx.author.default_avatar.url)
        await ctx.send(embed=lol) 


    @commands.command(name="logreset",help="Resets all loggings of this server.",usage="logreset")
    @blacklist_check()
    @ignore_check()
    @commands.has_permissions(administrator=True)
    async def loki(self, ctx):
      view = Ignis(ctx)
      if ctx.author == ctx.guild.owner or ctx.author.top_role.position > ctx.guild.me.top_role.position:
        embed = discord.Embed(description="Are you sure you want to reset all the logging of this server?",color=self.color)
        msg = await ctx.send(embed=embed,view=view)
        await view.wait()
        if view.value == 'stop':
          return await msg.edit(embed=discord.Embed(description="Okay i will not reset the configuration of logging in this server.",color=self.color),view=None)        
        data = getLogging(ctx.guild.id)
        if data["message"] is not None:
          data["message"] = None
        else:
          pass
        if data["mod"] is not None:
          data["mod"] = None
        else:
          pass
        if data["role"] is not None:
            data["role"] = None
        else:
            pass
        if data["channel"] is not None:
          data["channel"] = None
        else:
          pass
        if data["member"] is not None:
          data["member"] = None
        else:
          pass
        if data["server"] is not None:
          data["server"] = None
        else:
          pass
        updateLogging(ctx.guild.id, data)
        await msg.edit(embed=discord.Embed(description="<:tick:1348326381611647046> | Successfully reset all the logging of this server.",color=self.color),view=None)
      else:
        lol = discord.Embed(description="""```yaml\n - You must have Administrator permission.\n - Your top role should be above my top role.```""",color=self.color)
        lol.set_author(name=ctx.author,icon_url=ctx.author.avatar.url if ctx.author.avatar else ctx.author.default_avatar.url)
        await ctx.send(embed=lol) 
 ############################################################################       
    @commands.command(name="msglog", aliases=['messagelogs'],help="Log message deleted/ edited / bulk deleted.",usage="msglog <channel>")
    @blacklist_check()
    @ignore_check()
    @commands.has_permissions(administrator=True)
    async def msglogs(self, ctx, channel: discord.TextChannel = None):
        data = getLogging(ctx.guild.id)
        ch= data["message"]
        if ctx.author == ctx.guild.owner or ctx.author.top_role.position > ctx.guild.me.top_role.position:
            if channel is None:
              await ctx.send_help(ctx.command)
              return
            if str(channel.id) == ch:
                embed = discord.Embed(
                     color=self.color,
                    description=f"<:cross:1348326385386651748> | Log message deleted/ edited / bulk deleted is already enabled for {ctx.guild.name} in {channel.mention}.")
                return await ctx.reply(embed=embed)
            else:
                data["message"] = str(channel.id)
                updateLogging(ctx.guild.id, data)
                hacker = discord.Embed(
                        description=
                        f"<:tick:1348326381611647046> | Successfully setuped message logs for {ctx.guild.name} and set {channel.mention} for logging Of deleted/ edited / bulk deleted messages .",
                        color=self.color)
                await ctx.send(embed=hacker,view=None)

        else:
            hacker5 = discord.Embed(
                description=
                """```yaml\n - You must have Administrator permission.\n - Your top role should be above my top role.```""",
                color=self.color)
            hacker5.set_author(name=ctx.author,
                               icon_url=ctx.author.avatar.url if ctx.author.avatar else ctx.author.default_avatar.url)

            await ctx.send(embed=hacker5)                   











    





    @commands.command(name="rolelog", aliases=['rolelogs'], help="Log create/ edit/ delete roles.",usage="rolelog <channel>")
    @blacklist_check()
    @ignore_check()
    @commands.has_permissions(administrator=True)
    async def _rolelogs(self, ctx, channel: discord.TextChannel = None):
      data = getLogging(ctx.guild.id)
      ch= data["role"]
      if ctx.author == ctx.guild.owner or ctx.author.top_role.position > ctx.guild.me.top_role.position:
          if channel is None:
            await ctx.send_help(ctx.command)
            return
          if str(channel.id) == ch:
              embed = discord.Embed(
                   color=self.color,
                  description=f"<:cross:1348326385386651748> | Logging of create/ edit/ delete roles is already enabled for {ctx.guild.name} in {channel.mention}.")
              return await ctx.reply(embed=embed)
          else:
              data["role"] = str(channel.id)
              updateLogging(ctx.guild.id, data)
              hacker = discord.Embed(
                      description=
                      f"<:tick:1348326381611647046> | Successfully setuped role logs for {ctx.guild.name} and set {channel.mention} for logging Of create/ edit/ delete roles .",
                      color=self.color)
              await ctx.send(embed=hacker,view=None)

      else:
        hacker5 = discord.Embed(description="""```yaml\n - You must have Administrator permission.\n - Your top role should be above my top role.```""",color=self.color)
        hacker5.set_author(name=ctx.author,icon_url=ctx.author.avatar.url if ctx.author.avatar else ctx.author.default_avatar.url)

        await ctx.send(embed=hacker5)


    @commands.command(name="modlog", aliases=['modlogs'], help="Log mod actions in the server.",usage="modlog <channel>")
    @blacklist_check()
    @ignore_check()
    @commands.has_permissions(administrator=True)
    async def _modogs(self, ctx, channel: discord.TextChannel = None):
      data = getLogging(ctx.guild.id)
      ch= data["mod"]
      if ctx.author == ctx.guild.owner or ctx.author.top_role.position > ctx.guild.me.top_role.position:
          if channel is None:
            await ctx.send_help(ctx.command)
            return
          if str(channel.id) == ch:
              embed = discord.Embed(color=self.color,description=f"<:cross:1348326385386651748> | Logging of mod actions in the server is already enabled for {ctx.guild.name} in {channel.mention}.")
              return await ctx.reply(embed=embed)
          else:
              data["mod"] = str(channel.id)
              updateLogging(ctx.guild.id, data)
              hacker = discord.Embed(description=f"<:tick:1348326381611647046> | Successfully setuped mod logs for {ctx.guild.name} and set {channel.mention} for logging Of mod actions in the server .",color=self.color)
              await ctx.send(embed=hacker,view=None)

      else:
        hacker5 = discord.Embed(description="""```yaml\n - You must have Administrator permission.\n - Your top role should be above my top role.```""",color=self.color)
        hacker5.set_author(name=ctx.author,icon_url=ctx.author.avatar.url if ctx.author.avatar else ctx.author.default_avatar.url)

        await ctx.send(embed=hacker5) 






    @commands.command(name="memberlog", aliases=['memberlogs'], help="Log when someone joins/leaves/nickname/role update etc..",usage="memberlog <channel>")
    @commands.has_permissions(administrator=True)
    @blacklist_check()
    @ignore_check()
    async def _memberogs(self, ctx, channel: discord.TextChannel = None):
      data = getLogging(ctx.guild.id)
      ch= data["member"]
      if ctx.author == ctx.guild.owner or ctx.author.top_role.position > ctx.guild.me.top_role.position:
          if channel is None:
            await ctx.send_help(ctx.command)
            return
          if str(channel.id) == ch:
              embed = discord.Embed(color=self.color,description=f"<:cross:1348326385386651748> | Logging of when someone joins/leaves/nickname/role update etc is already enabled for {ctx.guild.name} in {channel.mention}.")
              return await ctx.reply(embed=embed)
          else:
              data["member"] = str(channel.id)
              updateLogging(ctx.guild.id, data)
              hacker = discord.Embed(description=f"<:tick:1348326381611647046> | Successfully setuped member logs for {ctx.guild.name} and set {channel.mention} for logging when someone joins/leaves/nickname/role update etc .",color=self.color)
              await ctx.send(embed=hacker,view=None)

      else:
        hacker5 = discord.Embed(description="""```yaml\n - You must have Administrator permission.\n - Your top role should be above my top role.```""",color=self.color)
        hacker5.set_author(name=ctx.author,icon_url=ctx.author.avatar.url if ctx.author.avatar else ctx.author.default_avatar.url)
        await ctx.send(embed=hacker5) 


    @commands.command(name="channellog", aliases=['channellogs'], help="Log create/ edit/ delete channel.",usage="channellog <channel>")
    @blacklist_check()
    @ignore_check()
    @commands.has_permissions(administrator=True)
    async def _channellogs(self, ctx, channel: discord.TextChannel = None):
      data = getLogging(ctx.guild.id)
      ch= data["channel"]
      if ctx.author == ctx.guild.owner or ctx.author.top_role.position > ctx.guild.me.top_role.position:
          if channel is None:
            await ctx.send_help(ctx.command)
            return
          if str(channel.id) == ch:
              embed = discord.Embed(color=self.color,description=f"<:cross:1348326385386651748> | Logging of create/ edit/ delete channel is already enabled for {ctx.guild.name} in {channel.mention}.")
              return await ctx.reply(embed=embed)
          else:
              data["channel"] = str(channel.id)
              updateLogging(ctx.guild.id, data)
              hacker = discord.Embed(description=f"<:tick:1348326381611647046> | Successfully setuped channel logs for {ctx.guild.name} and set {channel.mention} for logging of create/ edit/ delete channel.",color=self.color)
              await ctx.send(embed=hacker,view=None)

      else:
        hacker5 = discord.Embed(description="""```yaml\n - You must have Administrator permission.\n - Your top role should be above my top role.```""",color=self.color)
        hacker5.set_author(name=ctx.author,icon_url=ctx.author.avatar.url if ctx.author.avatar else ctx.author.default_avatar.url)
        await ctx.send(embed=hacker5)  






    @commands.command(name="serverlog", aliases=['serverlogs'], help="Log server updates like emoji update , icon change, etc.",usage="serverlog <channel>")
    @blacklist_check()
    @ignore_check()
    @commands.has_permissions(administrator=True)
    async def _serverlogs(self, ctx, channel: discord.TextChannel = None):
      data  = getLogging(ctx.guild.id)
      ch= data["server"]
      if ctx.author == ctx.guild.owner or ctx.author.top_role.position > ctx.guild.me.top_role.position:
          if channel is None:
            await ctx.send_help(ctx.command)
            return
          if str(channel.id) == ch:
              embed = discord.Embed(color=self.color,description=f"<:cross:1348326385386651748> | Logging of server updates like emoji update , icon change, etc is already enabled for {ctx.guild.name} in {channel.mention}.")
              return await ctx.reply(embed=embed)
          else:
              data["server"] = str(channel.id)
              updateLogging(ctx.guild.id, data)
              hacker = discord.Embed(description=f"<:tick:1348326381611647046> | Successfully setuped server logs for {ctx.guild.name} and set {channel.mention} for logging of server updates like emoji update , icon change, etc .",color=self.color)
              await ctx.send(embed=hacker,view=None)

      else:
        hacker5 = discord.Embed(description="""```yaml\n - You must have Administrator permission.\n - Your top role should be above my top role.```""",color=self.color)
        hacker5.set_author(name=ctx.author,icon_url=ctx.author.avatar.url if ctx.author.avatar else ctx.author.default_avatar.url)
        await ctx.send(embed=hacker5)


    # oi ka dekh rha h vai thodi coding sikh naki skidding
    ##############EVENTS#################
    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        await self.bot.wait_until_ready()
        if not member.guild:
            return
        if not member.guild.me.guild_permissions.view_audit_log:
            return
        data = getLogging(member.guild.id)
        ch = data["member"]
        if ch is not None:
            c = member.guild.get_channel(int(ch))
            if c is None:
                return 
            em = discord.Embed(title="A member joined the server", description=f"Username: {str(member)}\nUser id: {member.id}\nAccount created at: <t:{round(member.created_at.timestamp())}:R>", color=self.color)
            if member.bot:
                async for entry in member.guild.audit_logs(limit=1, after=datetime.datetime.utcnow() - datetime.timedelta(minutes=2), action=discord.AuditLogAction.bot_add):
                    em.title = "A bot added to the server"
                    adder = entry.user
                    em.add_field(name="Bot added by:", value=f"{str(adder)} - [{adder.id}] {adder.mention}")
            em.set_author(name=str(member), icon_url=member.display_avatar.url)
            em.set_footer(text="Joined", icon_url=member.guild.me.display_avatar.url)
            em.timestamp = datetime.datetime.utcnow()
            em.set_thumbnail(url=member.display_avatar.url)
            await c.send(embed=em)
            return


######################################
    @commands.Cog.listener()
    async def on_member_remove(self, member: discord.Member):
        await self.bot.wait_until_ready()
        
        if not member or not member.guild:
            return
            
        try:
            # Check if bot has permission to view audit logs
            if not member.guild.me or not member.guild.me.guild_permissions.view_audit_log:
                return

            kick = False
            kicked_by = None
            kick_reason = None

            try:
                async for entry in member.guild.audit_logs(limit=1, after=datetime.datetime.utcnow() - datetime.timedelta(seconds=3), action=discord.AuditLogAction.kick):
                    if entry.target == member and (datetime.datetime.utcnow() - entry.created_at.replace(tzinfo=None)).total_seconds() <= 10:
                        kick = True
                        kicked_by = entry.user
                        kick_reason = entry.reason
            except discord.Forbidden:
                pass

            data = getLogging(member.guild.id)
            logging_channel_id = data.get("member")

            if logging_channel_id:
                logging_channel = member.guild.get_channel(int(logging_channel_id))
                if logging_channel:
                    # Leave embed
                    leave_embed = discord.Embed(
                        title="A member left the server",
                        description=f"Username: {member}\nUser id: {member.id}\nAccount created at: <t:{round(member.created_at.timestamp())}:R>",
                        color=self.color
                    )
                    leave_embed.set_author(name=str(member), icon_url=member.display_avatar.url if member.display_avatar else None)
                    leave_embed.set_footer(text="Left", icon_url=member.guild.me.display_avatar.url if member.guild.me.display_avatar else None)
                    leave_embed.timestamp = datetime.datetime.utcnow()
                    if member.display_avatar:
                        leave_embed.set_thumbnail(url=member.display_avatar.url)

                    await logging_channel.send(embed=leave_embed)

                    # Kick embed if applicable
                    if kick and kicked_by:
                        kick_embed = discord.Embed(
                            title="A member got kicked from the server",
                            description=f"Username: {member}\nUser id: {member.id}\nAccount created at: <t:{round(member.created_at.timestamp())}:R>",
                            color=self.color
                        )
                        kick_embed.add_field(name="Kicked by:", value=f"{kicked_by} - [{kicked_by.id}] {kicked_by.mention}")
                        if kick_reason:
                            kick_embed.add_field(name="Reason:", value=kick_reason)
                        kick_embed.set_author(name=str(member), icon_url=member.display_avatar.url if member.display_avatar else None)
                        kick_embed.set_footer(text="Kicked", icon_url=member.guild.me.display_avatar.url if member.guild.me.display_avatar else None)
                        kick_embed.timestamp = datetime.datetime.utcnow()
                        if member.display_avatar:
                            kick_embed.set_thumbnail(url=member.display_avatar.url)

                        await logging_channel.send(embed=kick_embed)

        except Exception as e:
            print(f"Error in on_member_remove: {e}")


################################


    @commands.Cog.listener()
    async def on_member_update(self, before: discord.Member, after: discord.Member) -> None:
        await self.bot.wait_until_ready()
        if not after.guild:  # Checking if the update occurred in a guild
            return
        if not after.guild.me.guild_permissions.view_audit_log:  # Checking bot's permissions
            return

        data = getLogging(after.guild.id)
        ch = data["member"]  # Fetching the logging channel ID from data

        if ch is not None:
            c = after.guild.get_channel(int(ch))  # Fetching the logging channel object from ID

            if c is None:
                return

            async for entry in after.guild.audit_logs(limit=1, after=datetime.datetime.now() - datetime.timedelta(seconds=3), action=discord.AuditLogAction.member_update):
                # Checking if the update action was related to member updates
                if entry.target == after:  # Checking if the member being updated is the same as 'after'

                    em = discord.Embed(title="A member updated", color=self.color)
                    em.set_author(name=f"{str(after)}", icon_url=after.display_avatar.url)
                    em.set_footer(text="UPDATED", icon_url=after.guild.me.display_avatar.url)
                    em.timestamp = datetime.datetime.utcnow()
                    em.set_thumbnail(url=after.display_avatar.url)

                    if after.nick != before.nick:
                        em.description = f"Nickname changed:\n`{before.nick}` to `{after.nick}`"
                        em.add_field(name="Nick changed by:", value=f"{str(entry.user)} - [{entry.user.id}] {entry.user.mention}")
                        em.title = "A member's nickname changed"
                        await c.send(embed=em)  # Sending the embed to the logging channel
                        return

            # Checking for role changes
            if len(after.roles) != len(before.roles):
                check = False
                em = discord.Embed(title="A member's role changed", color=self.color)
                em.set_author(name=f"{str(after)}", icon_url=after.display_avatar.url)
                em.set_footer(text="UPDATED", icon_url=after.guild.me.display_avatar.url)
                em.timestamp = datetime.datetime.utcnow()
                em.set_thumbnail(url=after.display_avatar.url)

                # Fetching the audit log for role updates
                async for role_entry in after.guild.audit_logs(limit=1, after=datetime.datetime.now() - datetime.timedelta(seconds=3), action=discord.AuditLogAction.member_role_update):
                    if role_entry.target == after:
                        # Finding the added or removed role
                        added_roles = [role for role in after.roles if role not in before.roles]
                        removed_roles = [role for role in before.roles if role not in after.roles]

                        if added_roles:
                            em.add_field(name="Role Added:", value=", ".join([f"{role.mention} - [{role.id}]" for role in added_roles]))
                            check = True

                        if removed_roles:
                            em.add_field(name="Role Removed:", value=", ".join([f"{role.mention} - [{role.id}]" for role in removed_roles]))
                            check = True

                        em.add_field(name="Top role changed?", value="Yes" if after.top_role != before.top_role else "No")

                        if role_entry.reason:
                            em.add_field(name="Reason", value=role_entry.reason)

                        if check:
                            await c.send(embed=em)  # Sending the embed to the logging channel
                            return



       



##############BAN##############


    @commands.Cog.listener()
    async def on_member_ban(self, guild: discord.Guild, member: discord.Member):
        await self.bot.wait_until_ready()
        if not guild or not guild.me.guild_permissions.view_audit_log:
            return

        data = getLogging(guild.id)
        ch = data["mod"]
        if ch is None:
            return

        mod_channel = guild.get_channel(int(ch))
        if mod_channel is None:
            return

        async for entry in guild.audit_logs(limit=1,
                                            after=datetime.datetime.utcnow() -
                                            datetime.timedelta(minutes=2),
                                            action=discord.AuditLogAction.ban):
            m = entry.user
            if not m.guild:
                return

            em = discord.Embed(title="A member got banned from the server", description=f"Username: {str(member)}\nUser id: {member.id}\nAccount created at: <t:{round(member.created_at.timestamp())}:R>", color=self.color)
            em.add_field(name="Banned by:", value=f"{str(m)} - [{m.id}] {m.mention}")
            if entry.reason:
                em.add_field(name="Reason:", value=entry.reason)
            em.set_author(name=str(member), icon_url=member.display_avatar.url)
            em.set_footer(text="Banned", icon_url=member.guild.me.display_avatar.url)
            em.timestamp = datetime.datetime.utcnow()
            em.set_thumbnail(url=member.display_avatar.url)

            await mod_channel.send(embed=em)
            return
     


##################UNBAN################

    @commands.Cog.listener()
    async def on_member_unban(self, guild: discord.Guild, member: discord.Member):
        await self.bot.wait_until_ready()
        if not guild or not guild.me.guild_permissions.view_audit_log:
            return

        data = getLogging(guild.id)
        ch = data["mod"]
        if ch is None:
            return

        mod_channel = guild.get_channel(int(ch))
        if mod_channel is None:
            return

        async for entry in guild.audit_logs(limit=1,
                                            after=datetime.datetime.utcnow() -
                                            datetime.timedelta(minutes=2),
                                            action=discord.AuditLogAction.unban):
            m = entry.user
            if not m.guild:
                return

            em = discord.Embed(title="A member got unbanned from the server", description=f"Username: {str(member)}\nUser id: {member.id}\nAccount created at: <t:{round(member.created_at.timestamp())}:R>", color=self.color)
            em.add_field(name="Unbanned by:", value=f"{str(m)} - [{m.id}] {m.mention}")
            if entry.reason:
                em.add_field(name="Reason:", value=entry.reason)
            em.set_author(name=str(member), icon_url=member.display_avatar.url)
            em.set_footer(text="Unbanned", icon_url=guild.me.display_avatar.url)
            em.timestamp = datetime.datetime.utcnow()
            em.set_thumbnail(url=member.display_avatar.url)

            await mod_channel.send(embed=em)
            return
     


    @commands.Cog.listener()
    async def on_guild_role_create(self, role: discord.Role) -> None:
        await self.bot.wait_until_ready()
        guild = role.guild
        if not guild or not guild.me.guild_permissions.view_audit_log:
            return

        data = getLogging(guild.id)
        ch = data["role"]
        if ch is None:
            return

        mod_channel = guild.get_channel(int(ch))
        if mod_channel is None:
            return

        async for entry in guild.audit_logs(limit=1,
                                            after=datetime.datetime.utcnow() -
                                            datetime.timedelta(minutes=2),
                                            action=discord.AuditLogAction.role_create):
            m = entry.user
            if not m.guild:
                return

            em = discord.Embed(title="Role Created", description=f"Role {role.mention} Created by {entry.user.mention}", color=self.color)
            em.add_field(name="Name", value=f"{role.name}")
            em.add_field(name="Colour", value=f"{role.color}")
            em.add_field(name="Mentionable", value=role.mentionable)
            em.add_field(name="Hoist", value=role.hoist)
            em.add_field(name="Position", value=role.position + 1)
            role_perm = ', '.join([str(p[0]).replace("_", " ").title() for p in role.permissions if p[1]])
            if role_perm is None:
                role_perm = "No Permissions"
            em.add_field(name="Permissions", value=role_perm)
            if entry.reason:
                em.add_field(name="Reason:", value=entry.reason)
            em.set_author(name=str(entry.user), icon_url=entry.user.display_avatar.url)
            em.set_footer(text="Created", icon_url=guild.me.display_avatar.url)
            em.timestamp = datetime.datetime.utcnow()
            em.set_thumbnail(url=entry.user.display_avatar.url)

            await mod_channel.send(embed=em)
            return

    @commands.Cog.listener()
    async def on_guild_role_delete(self, role: discord.Role) -> None:
        await self.bot.wait_until_ready()
        guild = role.guild
        if not guild or not guild.me.guild_permissions.view_audit_log:
            return

        data = getLogging(guild.id)
        ch = data["role"]
        if ch is None:
            return

        mod_channel = guild.get_channel(int(ch))
        if mod_channel is None:
            return

        async for entry in guild.audit_logs(limit=1,
                                            after=datetime.datetime.utcnow() -
                                            datetime.timedelta(minutes=2),
                                            action=discord.AuditLogAction.role_delete):
            m = entry.user
            if not m.guild:
                return

            em = discord.Embed(title="Role Deleted", description=f"Role `{role.name}` Deleted by {entry.user.mention}", color=self.color)
            em.add_field(name="Name", value=f"{role.name}")
            em.add_field(name="Colour", value=f"{role.color}")
            em.add_field(name="Mentionable", value=role.mentionable)
            em.add_field(name="Hoist", value=role.hoist)
            em.add_field(name="Members", value=len(role.members))
            role_perm = ', '.join([str(p[0]).replace("_", " ").title() for p in role.permissions if p[1]])
            if role_perm is None:
                role_perm = "No Permissions"
            em.add_field(name="Permissions", value=role_perm)
            if entry.reason:
                em.add_field(name="Reason:", value=entry.reason)
            em.set_author(name=str(entry.user), icon_url=entry.user.display_avatar.url)
            em.set_footer(text="Deleted", icon_url=guild.me.display_avatar.url)
            em.timestamp = datetime.datetime.utcnow()
            em.set_thumbnail(url=entry.user.display_avatar.url)

            await mod_channel.send(embed=em)
            return







    @commands.Cog.listener()
    async def on_guild_role_update(self, before: discord.Role, after: discord.Role) -> None:
          await self.bot.wait_until_ready()
          guild = after.guild
          if not guild or not guild.me.guild_permissions.view_audit_log:
              return

          data = getLogging(guild.id)
          ch = data["role"]
          if ch is None:
              return

          mod_channel = guild.get_channel(int(ch))
          if mod_channel is None:
              return

          async for entry in guild.audit_logs(limit=1,
                                              after=datetime.datetime.utcnow() -
                                              datetime.timedelta(minutes=2),
                                              action=discord.AuditLogAction.role_update):
              m = entry.user
              if not m.guild:
                  return

              # Check if the role's properties actually changed
              if before.name == after.name and \
                 before.color == after.color and \
                 before.hoist == after.hoist and \
                 before.mentionable == after.mentionable and \
                 before.permissions.value == after.permissions.value and \
                 before.icon == after.icon:
                  return  # Exit if only position changed

              em = discord.Embed(title="Role Updated", description=f"Role {after.mention} Updated by {entry.user.mention}", color=self.color)
              if before.name != after.name:
                  em.add_field(name="Name changed", value=f"`{before.name}` to `{after.name}`")
              if before.color != after.color:
                  em.add_field(name="Color changed", value=f"{before.color} to {after.color}")
              if before.hoist != after.hoist:
                  em.add_field(name="Hoist changed", value=f'{"False" if after.hoist == True else "True"} to {after.hoist}')
              if before.mentionable != after.mentionable:
                  em.add_field(name="Mentionable changed", value=f'{"False" if after.mentionable == True else "True"} to {after.mentionable}')
              if before.permissions.value != after.permissions.value:
                  all_perm = []
                  b_perm = {}
                  a_perm = {}
                  given_perm = []
                  removed_perm = []
                  for i in before.permissions:
                      b_perm[i[0]] = i[1]
                      all_perm.append(i[0])
                  for i in after.permissions:
                      a_perm[i[0]] = i[1]
                  for i in all_perm:
                      if a_perm[i] != b_perm[i]:
                          if a_perm[i] == True:
                              given_perm.append(i)
                          else:
                              removed_perm.append(i)
                  if len(given_perm) > 0:
                      des = ', '.join([str(p).replace("_", " ").title() for p in given_perm])
                      em.add_field(name="Permissions given", value=des)
                  if len(removed_perm) > 0:
                      des1 = ', '.join([str(p).replace("_", " ").title() for p in removed_perm])
                      em.add_field(name="Permissions removed", value=des1)
              if before.icon != after.icon:
                  if before.icon is None:
                      d = f"None to [New Icon]({after.icon.url})"
                  elif after.icon is None:
                      d = f"[Old Icon]({before.icon.url}) to None"
                  else:
                      d = f"[Old Icon]({before.icon.url}) to [New Icon]({after.icon.url})"
                  em.add_field(name="Role icon changed", value=d)
              if entry.reason:
                  em.add_field(name="Reason:", value=entry.reason)
              em.set_author(name=str(entry.user), icon_url=entry.user.display_avatar.url)
              em.set_footer(text="Updated", icon_url=guild.me.display_avatar.url)
              em.timestamp = datetime.datetime.utcnow()
              em.set_thumbnail(url=entry.user.display_avatar.url)

              await mod_channel.send(embed=em)
              return



    @commands.Cog.listener()
    async def on_guild_channel_create(self, channel: discord.abc.GuildChannel) -> None:
        await self.bot.wait_until_ready()
        guild = channel.guild
        if not guild or not guild.me.guild_permissions.view_audit_log:
            return

        data = getLogging(guild.id)
        ch = data["channel"]
        if ch is None:
            return

        mod_channel = guild.get_channel(int(ch))
        if mod_channel is None:
            return

        async for entry in guild.audit_logs(limit=1,
                                            after=datetime.datetime.utcnow() -
                                            datetime.timedelta(minutes=2),
                                            action=discord.AuditLogAction.channel_create):
            m = entry.user
            if not m.guild:
                return

            em = None
            if isinstance(channel, discord.TextChannel):
                em = discord.Embed(title="Text Channel Created", description=f"Text Channel {channel.mention} Created by {entry.user.mention}", color=self.color)
            elif isinstance(channel, discord.VoiceChannel):
                em = discord.Embed(title="Voice Channel Created", description=f"Voice Channel {channel.mention} Created by {entry.user.mention}", color=self.color)
            elif isinstance(channel, discord.CategoryChannel):
                em = discord.Embed(title="Category Created", description=f"Category Channel {channel.mention} Created by {entry.user.mention}", color=self.color)
            elif isinstance(channel, discord.StageChannel):
                em = discord.Embed(title="Stage Channel Created", description=f"Stage Channel {channel.mention} Created by {entry.user.mention}", color=self.color)

            if em is not None:
                em.add_field(name="Name", value=f"{channel.name}")
                em.add_field(name="Position", value=channel.position + 1)
                overwrite = channel.overwrites_for(guild.default_role)
                em.add_field(name="Private?", value=f'{"Yes" if not overwrite.view_channel else "No"}')
                em.add_field(name="Permissions synced?", value=f'{"Yes" if channel.permissions_synced else "No"}')
                if isinstance(channel, (discord.VoiceChannel, discord.StageChannel)):
                    em.add_field(name="Bitrate", value=channel.bitrate / 1000)
                if channel.category:
                    em.add_field(name="Category", value=f"{channel.category.name} - [{channel.category_id}")
                if entry.reason:
                    em.add_field(name="Reason:", value=entry.reason)
                em.set_author(name=f"{str(entry.user)}", icon_url=entry.user.display_avatar.url)
                em.set_footer(text="Created", icon_url=guild.me.display_avatar.url)
                em.timestamp = datetime.datetime.utcnow()
                em.set_thumbnail(url=entry.user.display_avatar.url)

                await mod_channel.send(embed=em)
                return

    @commands.Cog.listener()
    async def on_guild_channel_delete(self, channel: discord.abc.GuildChannel) -> None:
        await self.bot.wait_until_ready()
        guild = channel.guild
        if not guild or not guild.me.guild_permissions.view_audit_log:
            return

        data = getLogging(guild.id)
        ch = data["channel"]
        if ch is None:
            return

        mod_channel = guild.get_channel(int(ch))
        if mod_channel is None:
            return

        async for entry in guild.audit_logs(limit=1,
                                            after=datetime.datetime.utcnow() -
                                            datetime.timedelta(minutes=2),
                                            action=discord.AuditLogAction.channel_delete):
            m = entry.user
            if not m.guild:
                return

            em = None
            if isinstance(channel, discord.TextChannel):
                em = discord.Embed(title="Text Channel Deleted", description=f"Text Channel {channel.mention} Deleted by {entry.user.mention}", color=self.color)
            elif isinstance(channel, discord.VoiceChannel):
                em = discord.Embed(title="Voice Channel Deleted", description=f"Voice Channel {channel.mention} Deleted by {entry.user.mention}", color=self.color)
            elif isinstance(channel, discord.CategoryChannel):
                em = discord.Embed(title="Category Deleted", description=f"Category Channel {channel.mention} Deleted by {entry.user.mention}", color=self.color)
            elif isinstance(channel, discord.StageChannel):
                em = discord.Embed(title="Stage Channel Deleted", description=f"Stage Channel {channel.mention} Deleted by {entry.user.mention}", color=self.color)

            if em is not None:
                em.add_field(name="Name", value=f"{channel.name}")
                em.add_field(name="Position", value=channel.position + 1)
                overwrite = channel.overwrites_for(guild.default_role)
                em.add_field(name="Permissions synced?", value=f'{"Yes" if channel.permissions_synced else "No"}')
                if isinstance(channel, (discord.VoiceChannel, discord.StageChannel)):
                    em.add_field(name="Bitrate", value=f"{channel.bitrate/1000} kbps")
                if channel.category:
                    em.add_field(name="Category", value=f"{channel.category.name} - [{channel.category_id}")
                if entry.reason:
                    em.add_field(name="Reason:", value=entry.reason)
                em.set_author(name=f"{str(entry.user)}", icon_url=entry.user.display_avatar.url)
                em.set_footer(text="Deleted", icon_url=guild.me.display_avatar.url)
                em.timestamp = datetime.datetime.utcnow()
                em.set_thumbnail(url=entry.user.display_avatar.url)

                await mod_channel.send(embed=em)
                return


    @commands.Cog.listener()
    async def on_message_edit(self, before: discord.Message, after: discord.Message):
        if before.author.bot:
            return

        guild = after.guild
        if not guild or not guild.me.guild_permissions.view_audit_log:
            return

        data = getLogging(guild.id)
        ch = data["message"]
        if ch is None:
            return

        mod_channel = guild.get_channel(int(ch))
        if mod_channel is None:
            return

        em = discord.Embed(description=f":scroll: Message sent by {after.author.mention} edited in {after.channel.mention} [Jump to message]({after.jump_url})", color=self.color)
        em.add_field(name="Before", value=f"```{before.content}```", inline=False)
        em.add_field(name="After", value=f"```{after.content}```", inline=False)
        em.set_author(name=f"{str(after.author)}", icon_url=after.author.display_avatar.url)
        em.set_footer(text="Edited", icon_url=guild.me.display_avatar.url)
        em.timestamp = datetime.datetime.utcnow()

        await mod_channel.send(embed=em)
        return

    @commands.Cog.listener()
    async def on_message_delete(self, message: discord.Message):
        if message.author.bot:
            return

        guild = message.guild
        if not guild or not guild.me.guild_permissions.view_audit_log:
            return

        data = getLogging(guild.id)
        ch = data["message"]
        if ch is None:
            return

        mod_channel = guild.get_channel(int(ch))
        if mod_channel is None:
            return

        async for entry in guild.audit_logs(limit=1, after=datetime.datetime.utcnow() - datetime.timedelta(minutes=1), action=discord.AuditLogAction.message_delete):
            em = discord.Embed(description=f":put_litter_in_its_place: Message sent by {message.author.mention} deleted in {message.channel.mention}", color=self.color)
            url = None
            for x in message.attachments:
                url = x.url
            if message.content == "":
                content = "***Content Unavailable***"
            else:
                content = message.content
            em.add_field(name="__Content__:", value=f"{content}", inline=False)
            x = datetime.datetime.now() - datetime.timedelta(seconds=5)
            if entry.user is not None and entry.target.id == message.author.id and x.timestamp() <= entry.created_at.timestamp():
                em.add_field(name="**Deleted By:**", value=f"{entry.user.mention} (ID: {entry.user.id})")
            if url is not None:
                if url.startswith("http") or url.startswith("http"):
                    em.set_image(url=url)
            em.set_author(name=f"{str(message.author)}", icon_url=message.author.display_avatar.url)
            em.set_footer(text="Deleted", icon_url=guild.me.display_avatar.url)
            em.timestamp = datetime.datetime.utcnow()

            await mod_channel.send(embed=em)
            return



    @commands.Cog.listener()
    async def on_guild_channel_update(self, before: discord.abc.GuildChannel, after: discord.abc.GuildChannel) -> None:
        if not after.guild or not after.guild.me.guild_permissions.view_audit_log:
            return

        data = getLogging(after.guild.id)
        ch = data["channel"]
        if ch is None:
            return

        mod_channel = after.guild.get_channel(int(ch))
        if mod_channel is None:
            return

        async for entry in after.guild.audit_logs(limit=1, after=datetime.datetime.utcnow() - datetime.timedelta(minutes=2), action=discord.AuditLogAction.channel_update):
            em = discord.Embed(title=f"{type(after).__name__} Updated", description=f"{type(after).__name__} {after.mention} Updated by {entry.user.mention}", color=self.color)
            if isinstance(after, discord.TextChannel):
                em.title = "Text Channel Updated"
            elif isinstance(after, discord.VoiceChannel):
                em.title = "Voice Channel Updated"
            elif isinstance(after, discord.CategoryChannel):
                em.title = "Category Updated"
            elif isinstance(after, discord.StageChannel):
                em.title = "Stage Channel Updated"

            if before.name != after.name:
                em.add_field(name="Name changed", value=f"`{before.name}` to `{after.name}`")

            if isinstance(after, discord.TextChannel) and isinstance(before, discord.TextChannel):
                if before.topic != after.topic:
                    em.add_field(name="Channel's topic updated", value=f"`{before.topic}` to `{after.topic}`")
                if before.slowmode_delay != after.slowmode_delay:
                    em.add_field(name="Slowmode delay updated", value=f"`{before.slowmode_delay} Seconds` to `{after.slowmode_delay} Seconds`")
                if before.nsfw != after.nsfw:
                    em.add_field(name="NSFW State updated", value=f'{"Yes to No" if before.nsfw else "No to Yes"}')

            if isinstance(after, discord.VoiceChannel) and isinstance(before, discord.VoiceChannel):
                if before.slowmode_delay != after.slowmode_delay:
                    em.add_field(name="Bitrate updated", value=f"`{before.bitrate/1000} kbps` to `{after.bitrate/1000} kbps`")
                if before.user_limit != after.user_limit:
                    em.add_field(name="User Limit updated", value=f"`{before.user_limit} users` to `{after.user_limit} users`")

            if entry.reason:
                em.add_field(name="Reason:", value=entry.reason)

            em.set_author(name=str(entry.user), icon_url=entry.user.display_avatar.url)
            em.set_footer(text="Updated", icon_url=after.guild.me.display_avatar.url)
            em.timestamp = datetime.datetime.utcnow()
            em.set_thumbnail(url=entry.user.display_avatar.url)

            await mod_channel.send(embed=em)
            return



    @commands.Cog.listener()
    async def on_guild_update(self, before: discord.Guild, after: discord.Guild) -> None:
        if not after.me.guild_permissions.view_audit_log:
            return

        data = getLogging(after.id)
        ch = data["server"]
        if ch is None:
            return

        mod_channel = after.get_channel(int(ch))
        if mod_channel is None:
            return

        async for entry in after.audit_logs(limit=1, after=datetime.datetime.utcnow() - datetime.timedelta(minutes=2), action=discord.AuditLogAction.guild_update):
            em = discord.Embed(title="Server Updated", description=f"Server Updated by {entry.user.mention}", color=self.color)

            if before.name != after.name:
                em.add_field(name="Server Name changed", value=f"`{before.name}` to `{after.name}`")

            if before.icon != after.icon:
                if before.icon is None:
                    d = f"None to [New Icon]({after.icon.url})"
                elif after.icon is None:
                    d = f"[Old Icon]({before.icon.url}) to None"
                else:
                    d = f"[Old Icon]({before.icon.url}) to [New Icon]({after.icon.url})"
                em.add_field(name="Guild icon changed", value=d)

            if before.banner != after.banner:
                if before.banner is None:
                    d = f"None to [New Banner]({after.banner.url})"
                elif after.icon is None:
                    d = f"[Old Banner]({before.banner.url}) to None"
                else:
                    d = f"[Old Banner]({before.banner.url}) to [New Banner]({after.banner.url})"
                em.add_field(name="Guild Banner changed", value=d)

            if before.owner_id != after.owner_id:
                em.add_field(name="Ownership Transfered", value=f"From: {before.owner.mention} - [{before.owner_id}\nTo: {after.owner.mention} - [{after.owner_id}]")

            if before.description != after.description:
                em.add_field(name="Server's Description Updated", value=f"`{str(before.description)}` to `{str(after.description)}`")

            if before.verification_level != after.verification_level:
                em.add_field(name="Server Verification Updated", value=f"`{str(before.verification_level)}` to `{str(after.verification_level)}`")

            if before.default_notifications != after.default_notifications:
                em.add_field(name="Default Notification Level Updated", value=f"`{str(before.default_notifications)}` to `{str(after.default_notifications)}`")

            if before.explicit_content_filter != after.explicit_content_filter:
                em.add_field(name="Explicit Content Filter Updated", value=f"`{str(before.explicit_content_filter)}` to `{str(after.explicit_content_filter)}`")

            if before.system_channel != after.system_channel:
                if before.system_channel is None:
                    bmen = "None"
                else:
                    bmen = before.system_channel.mention
                if after.system_channel is None:
                    amen = "None"
                else:
                    amen = after.system_channel.mention
                em.add_field(name="Server's System Channel Updated", value=f"{bmen} to {amen}")

            if before.rules_channel != after.rules_channel:
                if before.rules_channel is None:
                    bmen = "None"
                else:
                    bmen = before.rules_channel.mention
                if after.rules_channel is None:
                    amen = "None"
                else:
                    amen = after.rules_channel.mention
                em.add_field(name="Server's Rules Channel Updated", value=f"{bmen} to {amen}")

            if before.afk_channel != after.afk_channel:
                if before.afk_channel is None:
                    bmen = "None"
                else:
                    bmen = before.afk_channel.mention
                if after.afk_channel is None:
                    amen = "None"
                else:
                    amen = after.afk_channel.mention
                em.add_field(name="Afk Channel Updated", value=f"{bmen} to {amen}")

            if before.afk_timeout != after.afk_timeout:
                em.add_field(name="Afk Timeout Updated", value=f"`{int(before.afk_timeout)} Minutes` to `{int(after.afk_timeout)} Minutes`")

            if entry.reason:
                em.add_field(name="Reason:", value=entry.reason)

            em.set_author(name=str(entry.user), icon_url=entry.user.display_avatar.url)
            em.set_footer(text="Updated", icon_url=after.me.display_avatar.url)
            em.timestamp = datetime.datetime.utcnow()
            em.set_thumbnail(url=entry.user.display_avatar.url)

            await mod_channel.send(embed=em)
            return