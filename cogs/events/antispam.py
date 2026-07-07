import discord
from discord.ext import commands
import datetime
import re
import json
from core import Ignis, Cog
from utils.Tools import getConfig


class AntiSpam(Cog):
    def __init__(self, client: Ignis):
        self.client = client
        self.spam_cd_mapping = commands.CooldownMapping.from_cooldown(4, 7, commands.BucketType.member)
        self.spam_punish_cooldown_cd_mapping = commands.CooldownMapping.from_cooldown(1, 10, commands.BucketType.member)

    @commands.Cog.listener()    
    async def on_message(self, message):
      if not message.guild:
        return
      mem = message.author
      invite_regex = re.compile(r"(?:https?://)?discord(?:app)?\.(?:com/invite|gg)/[a-zA-Z0-9]+/?")
      link_regex = re.compile(r"http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+")
      invite_matches = invite_regex.findall(message.content)
      link_matches = link_regex.findall(message.content)
      data = getConfig(message.guild.id)
      antiSpam = data["antiSpam"]
      antiLink = data["antiLink"]
      wled = data["whitelisted"]
      wlrole = data['wlrole']  
      ray = message.guild.get_member(message.author.id)
      wlroles = message.guild.get_role(wlrole)
      try:
                if antiSpam is True:
                  if mem.guild_permissions.administrator or str(message.author.id) in wled or wlroles in ray.roles:
                    return
                  bucket = self.spam_cd_mapping.get_bucket(message)
                  retry = bucket.update_rate_limit()

                  if retry:
                    #punish_cd_bucket = self.spam_punish_cooldown_cd_mapping.get_bucket(message)
                 #   if not punish_cd_bucket.update_rate_limit():
                      if data["punishment"] == "kick":
                        now = discord.utils.utcnow()
                        await message.author.timeout(now + datetime.timedelta(minutes=15), reason="Ignis | Anti Spam")
                        ray = discord.Embed(color=0x2b2d31,description=f"<:tick:1348326381611647046> | Successfully Muted {message.author} For Spamming")
                        ray.set_author(name=f"{message.author}", icon_url=f"{message.author.avatar}")
                        ray.set_thumbnail(url =f"{message.author.avatar}")
                        await message.channel.send(embed=ray)

                      if data["punishment"] == "ban":
                        now = discord.utils.utcnow()
                        await message.author.timeout(now + datetime.timedelta(minutes=15), reason="Ignis | Anti Spam")
                        ray1 = discord.Embed(color=0x2b2d31,description=f"<:tick:1348326381611647046> | Successfully Muted {message.author} For Spamming")
                        ray1.set_author(name=f"{message.author}", icon_url=f"{message.author.avatar}")
                        ray1.set_thumbnail(url =f"{message.author.avatar}")
                        await message.channel.send(embed=ray1)

                      if data["punishment"] == "none":
                        now = discord.utils.utcnow()
                        await message.author.timeout(now + datetime.timedelta(minutes=15), reason="Ignis | Anti Spam")
                        ray2 = discord.Embed(color=0x2b2d31,description=f"<:tick:1348326381611647046> | Successfully Muted {message.author} For Spamming")
                        ray2.set_author(name=f"{message.author}", icon_url=f"{message.author.avatar}")
                        ray2.set_thumbnail(url =f"{message.author.avatar}")
                        await message.channel.send(embed=ray2)

                if antiLink is True:
                    if mem.guild_permissions.administrator or str(message.author.id) in wled or wlroles in ray.roles:
                        return
                    if invite_matches:
                        await message.delete()

                        if data["punishment"] == "kick":
                            await message.author.timeout(now + datetime.timedelta(minutes=15), reason="Ignis | Anti Discord Invites")
                            ray3 = discord.Embed(color=0x2b2d31,description=f"<:tick:1348326381611647046> | Successfully Muted {message.author} For Sending Discord Server Invites")
                            ray3.set_author(name=f"{message.author}", icon_url=f"{message.author.avatar}")
                            ray3.set_thumbnail(url =f"{message.author.avatar}")
                            await message.channel.send(embed=ray3)

                        if data["punishment"] == "ban":
                            await message.author.timeout(now + datetime.timedelta(minutes=15), reason="Ignis | Anti Discord Invites")
                            ray4 = discord.Embed(color=0x2b2d31,description=f"<:tick:1348326381611647046> | Successfully Muted {message.author} For Sending Discord Server Invites")
                            ray4.set_author(name=f"{message.author}", icon_url=f"{message.author.avatar}")
                            ray4.set_thumbnail(url =f"{message.author.avatar}")
                            await message.channel.send(embed=ray4)

                        if data["punishment"] == "none":
                             now = discord.utils.utcnow()
                             await message.author.timeout(now + datetime.timedelta(minutes=15), reason="Ignis | Anti Discord Invites")
                             ray5 = discord.Embed(color=0x2b2d31,description=f"<:tick:1348326381611647046> | Successfully Muted {message.author} For Sending Discord Server Invites")
                             ray5.set_author(name=f"{message.author}", icon_url=f"{message.author.avatar}")
                             ray5.set_thumbnail(url =f"{message.author.avatar}")
                             await message.channel.send(embed=ray5)
                    if link_matches:
                        if data["punishment"] == "kick":
                          await message.author.timeout(now + datetime.timedelta(minutes=15), reason="Ignis | Anti Link")
                          ray6 = discord.Embed(color=0x2b2d31,description=f"<:tick:1348326381611647046> | Successfully Muted {message.author} For Sending Links")
                          ray6.set_author(name=f"{message.author}", icon_url=f"{message.author.avatar}")
                          ray6.set_thumbnail(url =f"{message.author.avatar}") 
                          await message.channel.send(embed=ray6)



                        if data["punishment"] == "ban":
                          await message.author.timeout(now + datetime.timedelta(minutes=15), reason="Ignis | Anti Link")
                          ray7 = discord.Embed(color=0x2b2d31,description=f"<:tick:1348326381611647046> | Successfully Muted {message.author} For Sending Links")
                          ray7.set_author(name=f"{message.author}", icon_url=f"{message.author.avatar}")
                          ray7.set_thumbnail(url =f"{message.author.avatar}")  
                          await message.channel.send(embed=ray7)

                        if data["punishment"] == "none":
                          now = discord.utils.utcnow()
                          await message.author.timeout(now + datetime.timedelta(minutes=15), reason="Ignis | Anti Link")
                          ray8 = discord.Embed(color=0x2b2d31,description=f"<:tick:1348326381611647046> | Successfully Muted {message.author} For Sending Links")
                          ray8.set_author(name=f"{message.author}", icon_url=f"{message.author.avatar}")
                          ray8.set_thumbnail(url =f"{message.author.avatar}") 
                          await message.channel.send(embed=ray8)
                    else:
                      return
      except Exception as error:
                print(error)