import discord
import asyncio
import datetime
import re
import typing
import typing 
from typing import *
from utils.Tools import *
from core import Cog, Ignis, Context
from discord.ext.commands import Converter
from discord.ext import commands
from discord.ui import Button, View
from typing import Union, Optional
from utils import Paginator, DescriptionEmbedPaginator, FieldPagePaginator, TextPaginator
from typing import Union, Optional
from io import BytesIO
import requests
import aiohttp
import datetime



time_regex = re.compile(r"(?:(\d{1,5})(h|s|m|d))+?")
time_dict = {"h": 3600, "s": 1, "m": 60, "d": 86400}


def convert(argument):
  args = argument.lower()
  matches = re.findall(time_regex, args)
  time = 0
  for key, value in matches:
    try:
      time += time_dict[value] * float(key)
    except KeyError:
      raise commands.BadArgument(
        f"{value} is an invalid time key! h|m|s|d are valid arguments")
    except ValueError:
      raise commands.BadArgument(f"{key} is not a number!")
  return round(time)

async def do_removal(ctx, limit, predicate, *, before=None, after=None):
    if limit > 2000:
        return await ctx.error(f"Too many messages to search given ({limit}/2000)")

    if before is None:
        before = ctx.message
    else:
        before = discord.Object(id=before)

    if after is not None:
        after = discord.Object(id=after)

    try:
        deleted = await ctx.channel.purge(limit=limit, before=before, after=after, check=predicate)
    except discord.Forbidden as e:
        return await ctx.error("I do not have permissions to delete messages.")
    except discord.HTTPException as e:
        return await ctx.error(f"Error: {e} (try a smaller search?)")

    spammers = Counter(m.author.display_name for m in deleted)
    deleted = len(deleted)
    messages = [f'<:tick:1348326381611647046> | {deleted} message{" was" if deleted == 1 else "s were"} removed.']
    if deleted:
        messages.append("")
        spammers = sorted(spammers.items(), key=lambda t: t[1], reverse=True)
        messages.extend(f"**{name}**: {count}" for name, count in spammers)

    to_send = "\n".join(messages)

    if len(to_send) > 2000:
        await ctx.send(f"<:tick:1348326381611647046> | Successfully removed {deleted} messages.", delete_after=10)
    else:
        await ctx.send(to_send, delete_after=10)




class mod(commands.Cog):

  def __init__(self, bot):
    self.bot = bot
    self.color = 0x2b2d31
    self.bot.sniped_messages = {}

  def convert(self, time):
    pos = ["s", "m", "h", "d"]

    time_dict = {"s": 1, "m": 60, "h": 3600, "d": 3600 * 24}
    unit = time[-1]
    if unit not in pos:
      return -1
    try:
      val = int(time[:-1])
    except:
      return -2
    return val * time_dict[unit]



  @commands.hybrid_group(name="gban",
                  help="",
                  invoke_without_command=True,
                  usage="gban add/remove")
  @blacklist_check()
  @ignore_check()
  @commands.cooldown(1, 4, commands.BucketType.user)
  @commands.max_concurrency(1, per=commands.BucketType.default, wait=False)
  @commands.guild_only()
  @commands.has_permissions(administrator=True)
  async def _mod(self, ctx):
      if ctx.subcommand_passed is None:
          await ctx.send_help(ctx.command)
          ctx.command.reset_cooldown(ctx) 


  @_mod.command(name="add",
                  help="Add a user to Gban list",
                  usage="gban add <user>")
  @blacklist_check()
  @ignore_check()
  @commands.cooldown(1, 4, commands.BucketType.user)
  @commands.max_concurrency(1, per=commands.BucketType.default, wait=False)
  @commands.guild_only()
  @commands.has_permissions(administrator=True)
  async def mod_add(self, ctx, user: discord.User):
      data = getExtra(ctx.guild.id)
      wled = data["mods"]
      if ctx.author == ctx.guild.owner or ctx.author.top_role.position > ctx.guild.me.top_role.position:
          if len(wled) == 100:
              ray = discord.Embed(
                     title=self.bot.user.name,
                   description=
                       "<:arrow_right:1348340445708816494> You are trying to add more users than what it's allowed in [Trusted Mods]!",
                    color=self.color)
              ray.set_author(name="Unsuccessful Operation!",
                          icon_url=ctx.author.avatar.url if ctx.author.avatar
                          else ctx.author.default_avatar.url)
              await ctx.reply(embed=ray, mention_author=False)
          else:
              if str(user.id) in wled:
                  ray1 = discord.Embed(color=self.color)
                  ray1.add_field(
                    name="<:tick:1348326381611647046> Successful Operations",
                        value="No successful operation!",
                     inline=False)
                  ray1.add_field(
                    name="<:cross:1348326385386651748> Unsuccessful",
                     value=
                      f"""<:arrow_right:1348340445708816494> `{user}` <:cross:1348326385386651748>
                                                                <:arrow_right:1348340445708816494> *Already exists!*""",
                      inline=False)
                  ray1.set_author(
                    name="Gban Addition Result:",
                    icon_url=ctx.author.avatar.url if ctx.author.avatar else ctx.author.default_avatar.url)
                  await ctx.reply(embed=ray1, mention_author=False)
              else:
                  wled.append(str(user.id))
                  updateExtra(ctx.guild.id, data)
                  ray4 = discord.Embed(color=self.color)
                  ray4.add_field(
                        name="<:tick:1348326381611647046> Successful ",
                           value=f"<:arrow_right:1348340445708816494> `{user}`",
                              inline=False)
                  ray4.add_field(
                              name="<:cross:1348326385386651748> Unsuccessful",
                        value="All operations were successful!",
                       inline=False)
                  ray4.set_author(
                        name="Gban Addition Result:",
                          icon_url=ctx.author.avatar.url
                      if ctx.author.avatar else ctx.author.default_avatar.url)
                  await ctx.reply(embed=ray4, mention_author=False)

      else:
          ray5 = discord.Embed(
        description=
        """```yaml\n - You must have Administrator permission.\n - Your top role should be above my top role.```""",
        color=self.color)
          ray5.set_author(name=f"{ctx.author.name}",
                         icon_url=ctx.author.avatar.url
                       if ctx.author.avatar else ctx.author.default_avatar.url)
          await ctx.reply(embed=ray5, mention_author=False)    





  @_mod.command(name="remove",
                  help="Remove a user from Gban list",
                  usage="gban remove <user>")
  @blacklist_check()
  @ignore_check()
  @commands.cooldown(1, 4, commands.BucketType.user)
  @commands.max_concurrency(1, per=commands.BucketType.default, wait=False)
  @commands.guild_only()
  @commands.has_permissions(administrator=True)
  async def mod_remove(self, ctx, user: discord.User):
      data = getExtra(ctx.guild.id)
      wled = data["mods"]
      if ctx.author == ctx.guild.owner or ctx.author.top_role.position > ctx.guild.me.top_role.position:
          if str(user.id) in wled:
              wled.remove(str(user.id))
              updateExtra(ctx.guild.id, data)
              ray = discord.Embed(color=self.color)
              ray.add_field(
                name="<:tick:1348326381611647046> Successful",
                 value=f"<:arrow_right:1348340445708816494> `{user}`",
                inline=False)
              ray.add_field(
               name="<:cross:1348326385386651748> Unsuccessful",
               value="All operations were successful!",
               inline=False)
              ray.set_author(
               name="Gban Removal Result:",
               icon_url=ctx.author.avatar.url
               if ctx.author.avatar else ctx.author.default_avatar.url)
              await ctx.reply(embed=ray, mention_author=False)

          else:
              ray1 = discord.Embed(color=self.color)
              ray1.add_field(
                    name="<:tick:1348326381611647046> Successful",
                        value="No successful operation!",
                     inline=False)
              ray1.add_field(
                    name="<:cross:1348326385386651748> Unsuccessful",
                     value=
                      f"""<:arrow_right:1348340445708816494> `{user}` <:cross:1348326385386651748>
                                                                <:arrow_right:1348340445708816494> *Already not exists!*""",
                      inline=False)
              ray1.set_author(
                    name="Gban Removal Result:",
                    icon_url=ctx.author.avatar.url if ctx.author.avatar else ctx.author.default_avatar.url)
              await ctx.reply(embed=ray1, mention_author=False)



      else:
          ray5 = discord.Embed(
             description=
        """```yaml\n - You must have Administrator permission.\n - Your top role should be above my top role.```""",
             color=self.color)
          ray5.set_author(name=f"{ctx.author.name}",
                         icon_url=ctx.author.avatar.url
                       if ctx.author.avatar else ctx.author.default_avatar.url)
          await ctx.reply(embed=ray5, mention_author=False)   







  @_mod.command(name="show",
                  help="Shows list of Gban users in the server.",
                  usage="gban show")
  @blacklist_check()
  @ignore_check()
  @commands.cooldown(1, 4, commands.BucketType.user)
  @commands.max_concurrency(1, per=commands.BucketType.default, wait=False)
  @commands.guild_only()
  @commands.has_permissions(administrator=True)
  async def mod_show(self, ctx):   
        data = getExtra(ctx.guild.id)
        wled = data["mods"]
        if len(wled) == 0:
            ray = discord.Embed(
           color=self.color,
           title=self.bot.user.name,
        description=
        f"<:cross:1348326385386651748> | There aren\'t any Gban users for this server"
      )
            await ctx.reply(embed=ray, mention_author=False)
        else:
            entries = [
        f"`{no}` | <@!{idk}> | ID: [{idk}](https://discord.com/users/{idk})"
        for no, idk in enumerate(wled, start=1)
      ]
            Paginator = Paginator(source=DescriptionEmbedPaginator(
        entries=entries,
        title=f"Gban Users of {ctx.guild.name} - {len(wled)}",
        description="",
        color=self.color),
                            ctx=ctx)
            await Paginator.paginate()



  @_mod.command(name="reset",
                  help="removes every user from Gban database",
                  aliases=["clear"],
                  usage="gban reset")
  @blacklist_check()
  @ignore_check()
  @commands.cooldown(1, 4, commands.BucketType.user)
  @commands.max_concurrency(1, per=commands.BucketType.default, wait=False)
  @commands.guild_only()
  @commands.has_permissions(administrator=True)
  async def mod_reset(self, ctx):
        data = getExtra(ctx.guild.id)
        if ctx.author == ctx.guild.owner or ctx.author.top_role.position > ctx.guild.me.top_role.position:
            data = getExtra(ctx.guild.id)
            data["mods"] = []
            updateExtra(ctx.guild.id, data)
            ray = discord.Embed(
        color=self.color,
        title=self.bot.user.name,
        description=
        f"<:tick:1348326381611647046> | Successfully Cleared Gban Database For **{ctx.guild.name}**"
      )
            await ctx.reply(embed=ray, mention_author=False)
        else:
            ray5 = discord.Embed(
        description=
        """```yaml\n - You must have Administrator permission.\n - Your top role should be above my top role.```""",
        color=self.color)
            ray5.set_author(name=f"{ctx.author.name}",
                         icon_url=ctx.author.avatar.url
                       if ctx.author.avatar else ctx.author.default_avatar.url)
            await ctx.reply(embed=ray5, mention_author=False)




  @_mod.command(name="role",
                  help="Add a role to Gban role",
                  usage="gban role")
  @blacklist_check()
  @ignore_check()
  @commands.cooldown(1, 4, commands.BucketType.user)
  @commands.max_concurrency(1, per=commands.BucketType.default, wait=False)
  @commands.guild_only()
  @commands.has_permissions(administrator=True)
  async def mod_role(self, ctx,  *,role: discord.Role):
        data = getExtra(ctx.guild.id)
        data["modrole"] = role.id
        if ctx.author == ctx.guild.owner or ctx.author.top_role.position > ctx.guild.me.top_role.position:
            updateExtra(ctx.guild.id, data)
            ray4 = discord.Embed(
        color=self.color,
        title=self.bot.user.name,
        description=
        f"<:tick:1348326381611647046> | {role.mention} Has Been Added To Gban Role For {ctx.guild.name}"
      )
            await ctx.reply(embed=ray4, mention_author=False)
        else:
            ray5 = discord.Embed(
        description=
        """```yaml\n - You must have Administrator permission.\n - Your top role should be above my top role.```""",
        color=self.color)

            ray5.set_author(name=f"{ctx.author.name}",
                           icon_url=ctx.author.avatar.url
                       if ctx.author.avatar else ctx.author.default_avatar.url)
            await ctx.reply(embed=ray5, mention_author=False)


  @commands.command(description="Changes the icon for the role .")
  @commands.has_permissions(administrator=True)
  @commands.bot_has_guild_permissions(manage_roles=True)
  async def roleicon(self, ctx: commands.Context, role: discord.Role, *, icon: Union[discord.Emoji, discord.PartialEmoji, str]=None):
        if role.position >= ctx.guild.me.top_role.position:
            em = discord.Embed(description=f"| {role.mention} role is higher than my role, move it to the top!", color=self.color)
        if ctx.author.top_role.position <= role.position:
            em = discord.Embed(description=f"| {role.mention} has the same or higher position from your top role!", color=self.color)
            return await ctx.send(embed=em, delete_after=15)
        if icon is None:
            c = False
            url = None
            for xd in ctx.message.attachments:
                url = xd.url
                c = True
            if c:
                try:
                    async with aiohttp.request("GET", url) as r:
                        img = await r.read()
                        await role.edit(display_icon=img)
                    em = discord.Embed(description=f"<:tick:1348326381611647046> | Successfully changed icon of {role.mention}", color=self.color)
                except:
                    return await ctx.reply("Failed to change the icon of the role")
            else:
                await role.edit(display_icon=None)
                em = discord.Embed(description=f"<:tick:1348326381611647046> | Successfully removed icon from {role.mention}", color=self.color)
            return await ctx.reply(embed=em, mention_author=False)
        if isinstance(icon, discord.Emoji) or isinstance(icon, discord.PartialEmoji):
            png = f"https://cdn.discordapp.com/emojis/{icon.id}.png"
            try:
              async with aiohttp.request("GET", png) as r:
                img = await r.read()
            except:
              return await ctx.reply("Failed to change the icon of the role")
            await role.edit(display_icon=img)
            em = discord.Embed(description=f"<:tick:1348326381611647046> | Successfully changed the icon for {role.mention} to {icon}", color=self.color)
            return await ctx.reply(embed=em, mention_author=False)
        else:
            if not icon.startswith("https://"):
                return await ctx.reply("Give a valid link")
            try:
              async with aiohttp.request("GET", icon) as r:
                img = await r.read()
            except:
              return await ctx.reply("An error occured while changing the icon for the role")
            await role.edit(display_icon=img)
            em = discord.Embed(description=f"<:tick:1348326381611647046> | Successfully changed the icon for {role.mention}", color=self.color)
            return await ctx.reply(embed=em, mention_author=False)



  @commands.group(name="role",invoke_without_command=True)
  @blacklist_check()
  @ignore_check()
  @commands.cooldown(1, 5, commands.BucketType.user)
  @commands.max_concurrency(1, per=commands.BucketType.default, wait=False)
  @commands.guild_only()
  @blacklist_check()
  async def role(
    self,
    ctx,
    member: discord.Member, *,role: discord.Role):


    if ctx.author == ctx.guild.owner or member.guild_permissions.manage_roles:
      if role not in member.roles:
        try:
          ray1 = discord.Embed(
            description=
            f"<:tick:1348326381611647046> | Changed roles for {member.name}, Added {role.name}",
            color=self.color)
          await member.add_roles(role,
                                 reason=f"{ctx.author} (ID: {ctx.author.id})")
          await ctx.send(embed=ray1)
        except:
          pass
      elif role in member.roles:
        try:
          ray = discord.Embed(
            description=
            f"<:tick:1348326381611647046> | Changed roles for {member.name}, Removed {role.name}",
            color=self.color)
          await member.remove_roles(
            role, reason=f"{ctx.author} (ID: {ctx.author.id})")
          await ctx.send(embed=ray)
        except:
          pass
    else:
      error = discord.Embed(color=self.color,
                            description=f"""
<:cross:1348326385386651748> You need to give permissions to {self.bot.user.name} For use this command!
       <:arrow_right:1348340445708816494> to use this command you have to give us this permission:
       `Role Command` or drag my role to the top for the role that you want to use
       """)
      error.set_author(name="Permission Error",
                       icon_url=ctx.author.avatar.url
                       if ctx.author.avatar else ctx.author.default_avatar.url)

      await ctx.send(embed=error)


  @role.command(help="Give a role to member for particular time .")
  @commands.bot_has_permissions(manage_roles=True)
  @blacklist_check()
  @ignore_check()
  @commands.has_permissions(administrator=True)
  async def temp(self, ctx, role: discord.Role, time, *, user: discord.Member):
    '''Temporarily give a role to any member'''
    if role == ctx.author.top_role:
      embed = discord.Embed(
        description=
        f"<:cross:1348326385386651748> | {role} has the same position as your top role!",
        color=self.color)
      return await ctx.send(embed=embed)
    else:
      if role.position >= ctx.guild.me.top_role.position:
        embed1 = discord.Embed(
          description=
          f"<:cross:1348326385386651748> | {role} is higher than my role, move my role above {role}.",
          color=self.color)
        return await ctx.send(embed=embed1)
    seconds = convert(time)
    await user.add_roles(role, reason=None)
    ray = discord.Embed(
      description=
      f"<:tick:1348326381611647046> | Successfully added {role.mention} to {user.mention} .",
      color=self.color)
    await ctx.send(embed=ray)
    await asyncio.sleep(seconds)
    await user.remove_roles(role)



  @role.command(help="Delete a role in the server .")
  @blacklist_check()
  @ignore_check()
  @commands.has_permissions(administrator=True)
  @commands.bot_has_permissions(manage_roles=True)
  async def delete(self, ctx,*, role: discord.Role):
    '''Deletes the role from server'''
    if role == ctx.author.top_role:
      embed = discord.Embed(
        description=
        f"<:cross:1348326385386651748> | {role} has the same position as your top role!",
        color=self.color)
      return await ctx.send(embed=embed)
    else:
      if role.position >= ctx.guild.me.top_role.position:
        embed1 = discord.Embed(
          description=
          f"<:cross:1348326385386651748> | {role} is higher than my role, move my role above {role}.",
          color=self.color)
        return await ctx.send(embed=embed1)
    if role is None:
      embed2 = discord.Embed(
        description=
        f"<:cross:1348326385386651748> | No role named {role} found in this server .",
        color=self.color)
      return await ctx.send(embed=embed2)
    await role.delete()
    ray = discord.Embed(
      description=
      f"<:tick:1348326381611647046> | Successfully deleted {role}",
      color=self.color)
    await ctx.send(embed=ray)

  @role.command(help="Create a role in the server .")
  @blacklist_check()
  @ignore_check()
  @commands.has_permissions(administrator=True)
  @commands.bot_has_permissions(manage_roles=True)
  async def create(self, ctx, *, name):
    '''Creates a role in the server'''
    if ctx.author == ctx.guild.owner or ctx.guild.me.top_role <= ctx.author.top_role:
      ray = discord.Embed(
        description=
        f"<:tick:1348326381611647046> | Successfully created role with the name {name}",
        color=self.color)
      await ctx.guild.create_role(name=name, color=discord.Color.default())
      await ctx.send(embed=ray)
    else:
      ray5 = discord.Embed(
        description=
        """```diff\n - You must have Administrator permission.\n - Your top role should be above my top role. \n```""",
        color=self.color)
      ray5.set_author(name=f"{ctx.author.name}",
                         icon_url=ctx.author.avatar.url
                       if ctx.author.avatar else ctx.author.default_avatar.url)

      await ctx.send(embed=ray5)

  @role.command(help="Renames a role in the server .")
  @blacklist_check()
  @ignore_check()
  @commands.has_permissions(administrator=True)
  @commands.bot_has_permissions(manage_roles=True)
  async def rename(self, ctx, role: discord.Role, *, newname):
    '''Renames any role '''
    if ctx.author == ctx.guild.owner or ctx.guild.me.top_role <= ctx.author.top_role:
      await role.edit(name=newname)
      await ctx.send(
        f"<:tick:1348326381611647046> | Role {role.name} has been renamed to {newname}"
      )
    elif role is None:
      embed2 = discord.Embed(
        description=
        f"<:cross:1348326385386651748> | No role named {role} found in this server .",
        color=self.color)
      return await ctx.send(embed=embed2)
    else:
      ray5 = discord.Embed(
        description=
        """```diff\n - You must have Administrator permission.\n - Your top role should be above my top role. \n```""",
        color=self.color)
      ray5.set_author(name=f"{ctx.author.name}",
                         icon_url=ctx.author.avatar.url
                       if ctx.author.avatar else ctx.author.default_avatar.url)

      await ctx.send(embed=ray5)

  @role.command(name="humans", help="Gives a role to all the humans in the server .")
  @commands.cooldown(1, 10, commands.BucketType.user)
  @commands.max_concurrency(1, per=commands.BucketType.default, wait=False)
  @commands.guild_only()
  @commands.has_permissions(administrator=True)
  async def role_humans(self, ctx, *,role: discord.Role):
    if ctx.author == ctx.guild.owner or ctx.author.top_role.position > ctx.guild.me.top_role.position:
        button = Button(label="Yes",
                    style=discord.ButtonStyle.green,
                    emoji="<:tick:1348326381611647046>")
        button1 = Button(label="No",
                     style=discord.ButtonStyle.red,
                     emoji="<:cross:1348326385386651748>")
        async def button_callback(interaction: discord.Interaction):
            a = 0
            if interaction.user == ctx.author:
                if interaction.guild.me.guild_permissions.ban_members:
                    embed1 = discord.Embed(
                     color=self.color,
                    description=f"Adding {role.mention} to all humans .")
                    await interaction.response.edit_message(
                     embed=embed1, view=None)
                    for ray in interaction.guild.members:
                      if ray.bot != True and role not in ray.roles:
                        try:
                          await ray.add_roles(role,reason="Role Humans Command Executed By: {}".format(ctx.author))
                          a += 1  
                        except Exception as e:
                          print(e)


                    await interaction.channel.send(
                           content=f"<:tick:1348326381611647046> | Successfully Added {role.mention} To {a} Human(s) .")
                else:
                    await interaction.response.edit_message(
                        content=
                          "I am missing permission.\ntry giving me permissions and retry",
                            embed=None,
                               view=None)
            else:
                await interaction.response.send_message("This Is Not For You Dummy!",
                                                embed=None,
                                                view=None,
                                                ephemeral=True)
        async def button1_callback(interaction: discord.Interaction):
            if interaction.user == ctx.author:
                embed2 = discord.Embed(
                     color=self.color,
                    description=f"Ok I will Not Give {role.mention} To Any Humans .")
                await interaction.response.edit_message( embed=embed2, view=None)
            else:
                await interaction.response.send_message("This Is Not For You Dummy!",
                                                embed=None,
                                                view=None,
                                                ephemeral=True)
        test = [member for member in ctx.guild.members if all([not member.bot, not role in member.roles])]
        if len(test) == 0:
            return await ctx.reply(embed=discord.Embed(description=f"| {role.mention} is already given to all the members of the server .", color=self.color))
        else:
            embed = discord.Embed(
                color=self.color,
                  description=f'**Are you sure you want to give {role.mention} to {len(test)} members**')
            view = View()
            button.callback = button_callback
            button1.callback = button1_callback
            view.add_item(button)
            view.add_item(button1)
            await ctx.reply(embed=embed, view=view, mention_author=False)



    else:
        ray5 = discord.Embed(
        description=
        """```yaml\n - You must have Administrator permission.\n - Your top role should be above my top role.```""",
        color=self.color)
        ray5.set_author(name=f"{ctx.author.name}",
                         icon_url=ctx.author.avatar.url
                       if ctx.author.avatar else ctx.author.default_avatar.url)

        await ctx.send(embed=ray5, mention_author=False)                    





  @role.command(name="bots", description="Gives a role to all the bots in the server .")
  @commands.cooldown(1, 10, commands.BucketType.user)
  @commands.max_concurrency(1, per=commands.BucketType.default, wait=False)
  @commands.guild_only()
  @commands.has_permissions(administrator=True)
  async def role_bots(self, ctx, *,role: discord.Role):
    '''Gives a role to all the Bots in the server .'''
    if ctx.author == ctx.guild.owner or ctx.author.top_role.position > ctx.guild.me.top_role.position:
        button = Button(label="Yes",
                    style=discord.ButtonStyle.green,
                    emoji="<:tick:1348326381611647046>")
        button1 = Button(label="No",
                     style=discord.ButtonStyle.red,
                     emoji="<:cross:1348326385386651748>")
        async def button_callback(interaction: discord.Interaction):
            a = 0
            if interaction.user == ctx.author:
                if interaction.guild.me.guild_permissions.ban_members:
                    embed1 = discord.Embed(
                     color=self.color,
                    description=f"Adding {role.mention} to all bots .")
                    await interaction.response.edit_message(
                     embed=embed1, view=None)
                    for ray in interaction.guild.members:
                      if ray.bot and role not in ray.roles:
                        try:
                          await ray.add_roles(role,reason="Role Bots Command Executed By: {}".format(ctx.author))
                          a += 1  
                        except Exception as e:
                          print(e)

                    await interaction.channel.send(
            content=f"<:tick:1348326381611647046> | Successfully Added {role.mention} To {a} Bot(s) .")
                else:
                    await interaction.response.edit_message(
                         content=
                           "I am missing permission.\ntry giving me permissions and retry",
                              embed=None,
                                  view=None)
            else:
                await interaction.response.send_message("This Is Not For You Dummy!",
                                                embed=None,
                                                view=None,
                                                ephemeral=True)

        async def button1_callback(interaction: discord.Interaction):
            if interaction.user == ctx.author:
                embed2 = discord.Embed(
                     color=self.color,
                    description=f"Ok I will Not Give {role.mention} To Any Bots .")
                await interaction.response.edit_message(
          embed=embed2, view=None)
            else:
                await interaction.response.send_message("This Is Not For You Dummy!",
                                                embed=None,
                                                view=None,
                                                ephemeral=True)
        test = [member for member in ctx.guild.members if all([member.bot, not role in member.roles])]
        if len(test) == 0:
            return await ctx.reply(embed=discord.Embed(description=f"| {role.mention} is already given to all the bots of the server .", color=self.color))
        else:
            embed = discord.Embed(
                color=self.color,
                  description=f'**Are you sure you want to give {role.mention} to {len(test)} bots**')
            view = View()
            button.callback = button_callback
            button1.callback = button1_callback
            view.add_item(button)
            view.add_item(button1)
            await ctx.reply(embed=embed, view=view, mention_author=False)
    else:
        ray5 = discord.Embed(
        description=
        """```yaml\n - You must have Administrator permission.\n - Your top role should be above my top role.```""",
        color=self.color)
        ray5.set_author(name=f"{ctx.author.name}",
                         icon_url=ctx.author.avatar.url
                       if ctx.author.avatar else ctx.author.default_avatar.url)

        await ctx.send(embed=ray5, mention_author=False)








  @role.command(name="unverified", description="Gives a role to all the unverified members in the server .")
  @commands.cooldown(1, 10, commands.BucketType.user)
  @commands.max_concurrency(1, per=commands.BucketType.default, wait=False)
  @commands.guild_only()
  @commands.has_permissions(administrator=True)
  async def role_unverified(self, ctx,*,role: discord.Role):
    '''Gives a role to all unverified members.'''
    if ctx.author == ctx.guild.owner or ctx.author.top_role.position > ctx.guild.me.top_role.position:
        button = Button(label="Yes",
                    style=discord.ButtonStyle.green,
                    emoji="<:tick:1348326381611647046>")
        button1 = Button(label="No",
                     style=discord.ButtonStyle.red,
                     emoji="<:cross:1348326385386651748>")
        async def button_callback(interaction: discord.Interaction):
            a = 0
            if interaction.user == ctx.author:
                if interaction.guild.me.guild_permissions.ban_members:
                  embed1 = discord.Embed(
                     color=self.color,
                    description=f"Adding {role.mention} to all unverified members .")
                  await interaction.response.edit_message(
                     embed=embed1, view=None)
                  for ray in interaction.guild.members:
                    if ray.avatar is None and role not in ray.roles:
                      try:
                        await ray.add_roles(role,reason="Role Unverified Command Executed By: {}".format(ctx.author))
                        a += 1 
                      except Exception as e:
                        print(e)

                  await interaction.channel.send(
            content=f"<:tick:1348326381611647046> | Successfully Added {role.mention} To {a} Unverified Member(s) .")
                else:
                    await interaction.response.edit_message(
                         content=
                           "I am missing permission.\ntry giving me permissions and retry",
                              embed=None,
                                  view=None)
            else:
                await interaction.response.send_message("This Is Not For You Dummy!",
                                                embed=None,
                                                view=None,
                                                ephemeral=True)

        async def button1_callback(interaction: discord.Interaction):
            if interaction.user == ctx.author:
                embed2 = discord.Embed(
                     color=self.color,
                    description=f"Ok I will Not Give {role.mention} To Any Unverified Members .")
                await interaction.response.edit_message(
          embed=embed2, view=None)
            else:
                await interaction.response.send_message("This Is Not For You Dummy!",
                                                embed=None,
                                                view=None,
                                                ephemeral=True)
        embed = discord.Embed(
      color=self.color,
      description=f'**Are you sure you want to give {role.mention} to all unverified members in this guild?**')
        view = View()
        button.callback = button_callback
        button1.callback = button1_callback
        view.add_item(button)
        view.add_item(button1)
        await ctx.reply(embed=embed, view=view, mention_author=False)
    else:
        ray5 = discord.Embed(
        description=
        """```yaml\n - You must have Administrator permission.\n - Your top role should be above my top role.```""",
        color=self.color)
        ray5.set_author(name=f"{ctx.author.name}",
                         icon_url=ctx.author.avatar.url
                       if ctx.author.avatar else ctx.author.default_avatar.url)

        await ctx.send(embed=ray5, mention_author=False)     



  @role.command(name="all", description="Gives a role to all the members in the server .")
  @commands.cooldown(1, 10, commands.BucketType.user)
  @commands.max_concurrency(1, per=commands.BucketType.default, wait=False)
  @commands.guild_only()
  @commands.has_permissions(administrator=True)
  async def role_all(self, ctx,*,role: discord.Role):
    '''Gives a role to all the members of a server.'''
    if ctx.author == ctx.guild.owner or ctx.author.top_role.position > ctx.guild.me.top_role.position:
        button = Button(label="Yes",
                    style=discord.ButtonStyle.green,
                    emoji="<:tick:1348326381611647046>")
        button1 = Button(label="No",
                     style=discord.ButtonStyle.red,
                     emoji="<:cross:1348326385386651748>")
        async def button_callback(interaction: discord.Interaction):
            a = 0
            if interaction.user == ctx.author:
                if interaction.guild.me.guild_permissions.ban_members:
                  embed1 = discord.Embed(
                     color=self.color,
                    description=f"Adding {role.mention} to all members .")
                  await interaction.response.edit_message(
                     embed=embed1, view=None)
                  for ray in interaction.guild.members:
                    try:
                        await ray.add_roles(role,reason="Role All Command Executed By: {}".format(ctx.author))
                        a += 1  
                    except Exception as e:
                        print(e)


                  await interaction.channel.send(
            content=f"<:tick:1348326381611647046> | Successfully Added {role.mention} To {a} Member(s) .")
                else:
                    await interaction.response.edit_message(
                         content=
                           "I am missing permission.\ntry giving me permissions and retry",
                              embed=None,
                                  view=None)
            else:
                await interaction.response.send_message("This Is Not For You Dummy!",
                                                embed=None,
                                                view=None,
                                                ephemeral=True)

        async def button1_callback(interaction: discord.Interaction):
            if interaction.user == ctx.author:
                embed2 = discord.Embed(
                     color=self.color,
                    description=f"Ok I will Not Give {role.mention} To Anyone .")
                await interaction.response.edit_message(
                 embed=embed2, view=None)
            else:
                await interaction.response.send_message("This Is Not For You Dummy!",
                                                embed=None,
                                                view=None,
                                                ephemeral=True)
        test = [member for member in ctx.guild.members if role not in member.roles]
        if len(test) == 0:
            return await ctx.reply(embed=discord.Embed(description=f"| {role.mention} is already given to all the members of the server .", color=self.color))
        else:
            embed = discord.Embed(
                color=self.color,
                  description=f'**Are you sure you want to give {role.mention} to {len(test)} members**')
            view = View()
            button.callback = button_callback
            button1.callback = button1_callback
            view.add_item(button)
            view.add_item(button1)
            await ctx.reply(embed=embed, view=view, mention_author=False)
    else:
        ray5 = discord.Embed(
        description=
        """```yaml\n - You must have Administrator permission.\n - Your top role should be above my top role.```""",
        color=self.color)
        ray5.set_author(name=f"{ctx.author.name}",
                         icon_url=ctx.author.avatar.url
                       if ctx.author.avatar else ctx.author.default_avatar.url)

        await ctx.send(embed=ray5, mention_author=False)   

  @commands.hybrid_command(name="mute",
                             description="Timeouts someone for specific time.",
                             usage="mute <member> <time>",
                             aliases=["timeout", "stfu"])
  @commands.cooldown(1, 20, commands.BucketType.member)
  @commands.max_concurrency(1, per=commands.BucketType.default, wait=False)
  @commands.guild_only()
  @blacklist_check()
  @ignore_check()
  @commands.has_permissions(manage_messages=True)
  async def _mute(self, ctx, member: discord.Member, duration):
        ok = duration[:-1]
        tame = self.convert(duration)
        till = duration[-1]
        if tame == -1:
            ray3 = discord.Embed(
                color=0x2b2d31,
                description=
                f"<:cross:1348326385386651748> | You didnt didnt gave time with correct unit\nExamples:\n{ctx.prefix}mute {ctx.author} 10m\n{ctx.prefix}mute {ctx.author} 5hr",
                timestamp=ctx.message.created_at)
            await ctx.reply(embed=ray3, mention_author=False)
        elif tame == -2:
            ray4 = discord.Embed(
                color=0x2b2d31,
                description=
                f"<:cross:1348326385386651748> | Time must be an integer!",
                timestamp=ctx.message.created_at)
            await ctx.reply(embed=ray4, mention_author=False)
        else:
            if till.lower() == "d":
                t = datetime.timedelta(seconds=tame)
                ray = discord.Embed(
                    color=0x2b2d31,
                    description=
                    " <:tick:1348326381611647046> | Successfully Muted {0.mention} For {1} Day(s)"
                    .format(member, ok),
                    timestamp=ctx.message.created_at)
            elif till.lower() == "m":
                t = datetime.timedelta(seconds=tame)
                ray = discord.Embed(
                    color=0x2b2d31,
                    description=
                    " <:tick:1348326381611647046> | Successfully Muted {0.mention} For {1} Minute(s)"
                    .format(member, ok),
                    timestamp=ctx.message.created_at)
            elif till.lower() == "s":
                t = datetime.timedelta(seconds=tame)
                ray = discord.Embed(
                    color=0x2b2d31,
                    description=
                    " <:tick:1348326381611647046> | Successfully Muted {0.mention} For {1} Second(s)"
                    .format(member, ok),
                    timestamp=ctx.message.created_at)
            elif till.lower() == "h":
                t = datetime.timedelta(seconds=tame)
                ray = discord.Embed(
                    color=0x2b2d31,
                    description=
                    "<:tick:1348326381611647046> | Successfully Muted {0.mention} For {1} Hour(s)"
                    .format(member, ok),
                    timestamp=ctx.message.created_at)
        try:
            if member.guild_permissions.administrator:
                ray1 = discord.Embed(
                    color=0x2b2d31,
                    description=
                    "<:cross:1348326385386651748> | I can\'t mute administrators",
                    timestamp=ctx.message.created_at)
                await ctx.reply(embed=ray1)
            else:
                await member.timeout(discord.utils.utcnow() + t,
                                     reason="Command Used By: {0}".format(
                                         ctx.author))
                await ctx.send(embed=ray)
        except:
            print("an error occured")  

  @commands.group(invoke_without_command=True, aliases=["purge", "cln", "cl", "cn"], description="Clears the messages")
  @commands.has_permissions(manage_messages=True)
  async def clear(self, ctx, Choice: Union[discord.Member, int], Amount: int = None):
        """
        An all in one purge command.
        Choice can be a Member or a number
        """
        await ctx.message.delete()

        if isinstance(Choice, discord.Member):
            search = Amount or 5
            return await do_removal(ctx, search, lambda e: e.author == Choice)

        elif isinstance(Choice, int):
            return await do_removal(ctx, Choice, lambda e: True)



  @clear.command(description="Clears the messages containing embeds")
  @commands.has_permissions(manage_messages=True)
  async def embeds(self, ctx, search=100):
        """Removes messages that have embeds in them."""
        await ctx.message.delete()
        await do_removal(ctx, search, lambda e: len(e.embeds))


  @clear.command(description="Clears the messages containing files")
  @commands.has_permissions(manage_messages=True)
  async def files(self, ctx, search=100):
        """Removes messages that have attachments in them."""

        await ctx.message.delete()
        await do_removal(ctx, search, lambda e: len(e.attachments))

  @clear.command(description="Clears the messages containg images")
  @commands.has_permissions(manage_messages=True)
  async def images(self, ctx, search=100):
        """Removes messages that have embeds or attachments."""

        await ctx.message.delete()
        await do_removal(ctx, search, lambda e: len(e.embeds) or len(e.attachments))


  @clear.command(name="all", description="Clears all messages")
  @commands.has_permissions(manage_messages=True)
  async def _remove_all(self, ctx, search=100):
        """Removes all messages."""

        await ctx.message.delete()
        await do_removal(ctx, search, lambda e: True)

  @clear.command(description="Clears the messages of a specific user")
  @commands.has_permissions(manage_messages=True)
  async def user(self, ctx, member: discord.Member, search=100):
        """Removes all messages by the member."""

        await ctx.message.delete()
        await do_removal(ctx, search, lambda e: e.author == member)



  @clear.command(description="Clears the messages containing a specifix string")
  @commands.has_permissions(manage_messages=True)
  async def contains(self, ctx, *, string: str):
        """Removes all messages containing a substring.
        The substring must be at least 3 characters long.
        """

        await ctx.message.delete()
        if len(string) < 3:
            await ctx.error("The substring length must be at least 3 characters.")
        else:
            await do_removal(ctx, 100, lambda e: string in e.content)

  @clear.command(name="bot", aliases=["bots","b"], description="Clears the messages sent by bot")
  @commands.has_permissions(manage_messages=True)
  async def _bot(self, ctx, prefix=None, search=100):
        """Removes a bot user's messages and messages with their optional prefix."""

        await ctx.message.delete()

        def predicate(m):
            return (m.webhook_id is None and m.author.bot) or (prefix and m.content.startswith(prefix))

        await do_removal(ctx, search, predicate)

  @clear.command(name="emoji", aliases=["emojis"], description="Clears the messages having emojis")
  @commands.has_permissions(manage_messages=True)
  async def _emoji(self, ctx, search=100):
        """Removes all messages containing custom emoji."""

        await ctx.message.delete()
        custom_emoji = re.compile(r"<a?:[a-zA-Z0-9\_]+:([0-9]+)>")

        def predicate(m):
            return custom_emoji.search(m.content)

        await do_removal(ctx, search, predicate)

  @clear.command(name="reactions", description="Clears the reaction from the messages")
  @commands.has_permissions(manage_messages=True)
  async def _reactions(self, ctx, search=100):
        """Removes all reactions from messages that have them."""

        await ctx.message.delete()

        if search > 2000:
            return await ctx.send(f"Too many messages to search for ({search}/2000)")

        total_reactions = 0
        async for message in ctx.history(limit=search, before=ctx.message):
            if len(message.reactions):
                total_reactions += sum(r.count for r in message.reactions)
                await message.clear_reactions()

        await ctx.success(f"<:tick:1348326381611647046> | Successfully removed {total_reactions} reactions.")

  @commands.hybrid_command(
    name="prefix",
    aliases=["setprefix", "prefixset"],
    help="Allows you to change prefix of the bot for this server")
  @blacklist_check()
  @ignore_check()
  @commands.has_permissions(administrator=True)
  @commands.cooldown(1, 10, commands.BucketType.user)
  @commands.max_concurrency(1, per=commands.BucketType.default, wait=False)
  @commands.guild_only()
  async def _prefix(self, ctx: commands.Context, prefix):
    data = getConfig(ctx.guild.id)
    if ctx.author == ctx.guild.owner or ctx.author.top_role.position > ctx.guild.me.top_role.position:
      data["prefix"] = str(prefix)
      updateConfig(ctx.guild.id, data)
      await ctx.reply(embed=discord.Embed(
        description=
        f"<:tick:1348326381611647046> | Successfully Changed Prefix For **{ctx.guild.name}**\nNew Prefix for **{ctx.guild.name}** is : `{prefix}`\nUse `{prefix}help` For More info .",
        color=self.color))
    else:
      ray5 = discord.Embed(
        description=
        """```diff\n - You must have Administrator permission.\n - Your top role should be above my top role. \n```""",
        color=self.color)
      ray5.set_author(name=f"{ctx.author.name}",
                         icon_url=ctx.author.avatar.url
                       if ctx.author.avatar else ctx.author.default_avatar.url)

      await ctx.send(embed=ray5)
