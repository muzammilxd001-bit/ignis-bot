import discord
from traceback import format_exception
from discord.ext import commands
from difflib import get_close_matches
import io
import textwrap
import datetime
import sys
from contextlib import suppress
from core import Context
from core.Ignis import Ignis
from core.Cog import Cog
from utils import Paginator
from utils.Tools import getConfig
from itertools import chain
import psutil
import time
import datetime
import platform
import os
import logging
import motor.motor_asyncio
from pymongo import MongoClient
import requests
import motor.motor_asyncio as mongodb
from typing import *
from utils import *
import json
from utils import help as vhelp
from utils import DescriptionEmbedPaginator, FieldPagePaginator, TextPaginator

from core import Cog, Ignis, Context
from typing import Optional
from discord import app_commands
start_time = time.time()



def datetime_to_seconds(thing: datetime.datetime):
    current_time = datetime.datetime.fromtimestamp(time.time())
    return round(
        round(time.time()) +
        (current_time - thing.replace(tzinfo=None)).total_seconds())




class HelpCommand(commands.HelpCommand):

  async def on_help_command_error(self, ctx, error):
    serverCount = len(self.client.guilds)
    users = sum(g.member_count for g in self.client.guilds
                    if g.member_count != None)

    total_members = sum(g.member_count for g in self.client.guilds
                            if g.member_count != None)
    Ignis = [
      commands.CommandOnCooldown, commands.CommandNotFound,
      discord.HTTPException, commands.CommandInvokeError
    ]
    if not type(error):
      await self.context.reply(f"Unknown Error Occurred\n{error.original}",
                               mention_author=False)
    else:
      if type(error) == commands.CommandOnCooldown:
        return

        return await super().on_help_command_error(ctx, error)

  async def command_not_found(self, string: str) -> None:
    with open('data/blacklist.json', 'r') as f:
      data = json.load(f)
    if str(self.context.author.id) in data["ids"]:
      embed = discord.Embed(
        title="<:cross:1348326385386651748> Blacklisted",
        description=
        "You Are Blacklisted From Using My Commands.",
        color=0x2b2d31)
      await self.context.reply(embed=embed, mention_author=False)
    else:

      if string in ("security", "anti", "antinuke"):
        cog = self.context.bot.get_cog("Antinuke")
        with suppress(discord.HTTPException):
          await self.send_cog_help(cog)
      else:
        msg = f"Command `{string}` is not found...\n"
        piyush = await self.context.bot.fetch_user(870179991462236170)
        cmds = (str(cmd) for cmd in self.context.bot.walk_commands())
        mtchs = get_close_matches(string, cmds)
        if mtchs:
          for okaay, okay in enumerate(mtchs, start=1):
            msg += f"Did You Mean: \n`[{okaay}]`. `{okay}`\n"
        embed1 = discord.Embed(
          color=0x2b2d31,
          title=f"Command `{string}` is not found...\n",
          description=f"Did You Mean: \n`[{okaay}]`. `{okay}`\n")

        return None

  async def send_bot_help(self, mapping):
    await self.context.typing()
    with open('data/ignore.json', 'r') as heck:
      Igniss = json.load(heck)
    with open('data/blacklist.json', 'r') as f:
      bled = json.load(f)
    if str(self.context.author.id) in bled["ids"]:
      embed = discord.Embed(
        title="<:cross:1348326385386651748> Blacklisted",
        description=
        "You Are Blacklisted From Using My Commands.",
        color=0x2b2d31)
      return await self.context.reply(embed=embed, mention_author=False)
    elif str(self.context.channel.id) in Igniss["ids"]:
      return None
    data = getConfig(self.context.guild.id)
    prefix = data["prefix"]
    
    
    filtered = await self.filter_commands(self.context.bot.walk_commands(),sort=True)

    loading_message = await self.context.reply(embed=discord.Embed(color=0x2b2d31,description="<a:loading:1515039450214699099> **Loading Help command...**"))
    await asyncio.sleep(2)
    
    embed = discord.Embed(
       description=
      f"<a:blackdot:1514219180600328293> **Prefix For This Server: `{prefix}`**\n<a:blackdot:1514219180600328293> **My Total Featurs : {len(set(self.context.bot.walk_commands()))}**\n<a:blackdot:1514219180600328293> **Type `?antinuke enable` to get started up**",
      color= 0x2b2d31)
    embed.set_thumbnail(url=self.context.bot.user.display_avatar.url)

    embed.set_footer(
     icon_url=self.context.bot.user.display_avatar.url)

    embed.add_field(name="**__Main Featurs__**",
                    value=""" <:welcome:1516977918704746636> Welcome\n<:raid:1516973887735206001> Raidmode\n<:antinuke:1516973595937607690> Antinuke\n<:automod:1516766258983469167> Automod\n<a:Giveaway:1516864573024501872> Giveaway\n<a:Music:1516973200850817156> Music\n<:bell:1348326441279819906> Logging\n<:moderation:1516863523043541174> Moderation\n<:up:1348326392537808928> Leveling\n<:atom:1348326466210889821> Invites\n<:booster:1514212145347428483> Boost\n<:Ticket:1514212547631386717> Ticket\n<:automod:1516766258983469167> Automod\n<:Verified:1514211869957685319> Verification\n<:lock:1348340492647010436> Encryption """,
                    inline=True)
    embed.add_field(
        name="**__Extra Featurs__**",
        value=f""" <:earth:1348327194342199409> Gereral\n<:setting:1348340711862571069> Extra\n<:cricle1:1348326512482455603> Vanity Roles\n<:speak1:1348340478264873034> Join To Create\n<:atom:1348326466210889821> PFPs\n<:games:1348326482241523742> Games/Fun\n<:mail1:1348340613636165712> Media\n<:mic:1348326446216515604> Voice/VC Roles\n<:msg:1348326387873873960> Join DM\n<:tv:1348340581964976239> Server\n<:circle2:1348326520581521469> Birthday\n<:heart:1348340513719193612> Marrige\n """,
        inline=True)  
    embed.add_field(
        name="__Stats__",
        value=f"""<a:online:1509176312580018328> **Ping** - {int(self.context.bot.latency * 1000)} ms """,
        inline=False)
    embed.set_author(name=self.context.author.name,
                     icon_url=self.context.author.display_avatar.url)
    embed.set_image(url="https://media.discordapp.net/attachments/1348879432567488563/1348880653395169302/Ignis1.gif")
    embed.timestamp = discord.utils.utcnow()

    # Create the invite button
    invite_button = discord.ui.Button(
        style=discord.ButtonStyle.link,
        # emoji='<a:985:1151531674207789189>',
        label="Invite Me",
url="https://discord.com/oauth2/authorize?client_id=1375349766124470332&integration_type=0&scope=applications.commands"
    )
    support_button = discord.ui.Button(
        style=discord.ButtonStyle.link,
        # emoji='<a:999:1151531721381134377>',
        label="Support Server",
      url="https://dsc.gg/chillstation"
    )
    Vote_button = discord.ui.Button(
        style=discord.ButtonStyle.link,
        # emoji='<a:982:1142461636389650542>',
        label="Vote Me",
      url="https://dsc.gg/chillstation"
    )    

    view = vhelp.View(mapping=mapping, ctx=self.context, homeembed=embed, ui=2)
    view.add_item(invite_button)
    view.add_item(support_button)
   # view.add_item(Vote_button)    
    await loading_message.delete()
    await self.context.send(embed=embed, mention_author=True, view=view)

  async def send_command_help(self, command):
    with open('data/ignore.json', 'r') as heck:
      Igniss = json.load(heck)
    with open('data/blacklist.json', 'r') as f:
      data = json.load(f)
    if str(self.context.author.id) in data["ids"]:
      embed = discord.Embed(
        title="<:cross:1348326385386651748> Blacklisted",
        description=
        "You Are Blacklisted From Using My Commands.",
        color=0x2b2d31)
      await self.context.reply(embed=embed, mention_author=False)
    elif str(self.context.channel.id) in Igniss["ids"]:
      return None
    else:
      ray = f">>> {command.help}" if command.help else '>>> No Help Provided...'
      embed = discord.Embed(
        description=
        f"""```yaml\n- [] = optional argument\n- <> = required argument\n- Do NOT Type These When Using Commands !```\n{ray}""",
        color=0x2b2d31)
      alias = ' | '.join(command.aliases)

      embed.add_field(name="**Aliases**",
                      value=f"{alias}" if command.aliases else "No Aliases",
                      inline=False)
      embed.add_field(name="**Usage**",
                      value=f"`{self.context.prefix}{command.signature}`\n")
      embed.set_author(name=f"{command.cog.qualified_name.title()}",
                       icon_url=self.context.bot.user.display_avatar.url)
      await self.context.reply(embed=embed, mention_author=False)

  def get_command_signature(self, command: commands.Command) -> str:
    parent = command.full_parent_name
    if len(command.aliases) > 0:
      aliases = ' | '.join(command.aliases)
      fmt = f'[{command.name} | {aliases}]'
      if parent:
        fmt = f'{parent}'
      alias = f'[{command.name} | {aliases}]'
    else:
      alias = command.name if not parent else f'{parent} {command.name}'
    return f'{alias} {command.signature}'

  def common_command_formatting(self, embed_like, command):
    embed_like.title = self.get_command_signature(command)
    if command.description:
      embed_like.description = f'{command.description}\n\n{command.help}'
    else:
      embed_like.description = command.help or 'No help found...'

  async def send_group_help(self, group):
    with open('data/blacklist.json', 'r') as f:
      idk = json.load(f)
    with open('data/ignore.json', 'r') as heck:
      Igniss = json.load(heck)
    if str(self.context.author.id) in idk["ids"]:
      embed = discord.Embed(
        title="<:cross:1348326385386651748> Blacklisted",
        description=
        "You Are Blacklisted From Using My Commands.",
        color=0x2b2d31)
      await self.context.reply(embed=embed, mention_author=False)
    elif str(self.context.channel.id) in Igniss["ids"]:
      return None
    else:
      entries = [(
        f"`{self.context.prefix}{cmd.qualified_name}`",
        f"{cmd.short_doc if cmd.short_doc else 'No Description Provided...'}\n\n"
      ) for cmd in group.commands]
    Paginator = Paginator(source=FieldPagePaginator(
      entries=entries,
      title=f"{group.qualified_name} Commands",
      description="```yaml\n- [] = optional argument\n- <> = required argument\n- Do NOT Type These When Using Commands !```",
      color=0x2b2d31,
      per_page=10),
                          ctx=self.context)
    await Paginator.paginate()

  async def send_cog_help(self, cog):
    with open('data/blacklist.json', 'r') as f:
      data = json.load(f)
    with open('data/ignore.json', 'r') as heck:
      Igniss = json.load(heck)
    if str(self.context.author.id) in data["ids"]:
      embed = discord.Embed(
        title="<:cross:1348326385386651748> Blacklisted",
        description=
        "You Are Blacklisted From Using My Commands.",
        color=0x2b2d31)
      return await self.context.reply(embed=embed, mention_author=False)
    elif str(self.context.channel.id) in Igniss["ids"]:
      return None
    #await self.context.typing()
    entries = [(
      f"`{self.context.prefix}{cmd.qualified_name}`",
      f"{cmd.short_doc if cmd.short_doc else 'No Description Provided...'}\n\n"
    ) for cmd in cog.get_commands()]
    Paginator = Paginator(source=FieldPagePaginator(
      entries=entries,
      title=f"{cog.qualified_name.title()} ({len(cog.get_commands())})",
      description="```yaml\n- [] = optional argument\n- <> = required argument\n- Do NOT Type These When Using Commands !```\n\n",
      color=0x2b2d31,
      per_page=10),
                          ctx=self.context)
    await Paginator.paginate()


class Help(Cog, name="help"):

  def __init__(self, client: Ignis):
    self._original_help_command = client.help_command
    attributes = {
      'name':
      "help",
      'aliases': ['h'],
      'cooldown':
      commands.CooldownMapping.from_cooldown(1, 5, commands.BucketType.user),
      'help':
      'Shows help about bot, a command or a category'
    }
    client.help_command = HelpCommand(command_attrs=attributes)
    client.help_command.cog = self

  async def cog_unload(self):
    self.help_command = self._original_help_command