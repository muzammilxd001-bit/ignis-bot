import os
import discord
import aiohttp
from discord.ext import commands, tasks
from discord.colour import Color
import json
import random
from discord.ui import Button, View

# from utils.checks import getConfig, updateConfig


class Join(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        try:

            #  data = getConfig(guild.id)
            # key = "".join(random.choice("aAbBcCdDeE1234567890nNmMkKiIuUyY") for _ in range(6))
            # data['backupkey'] = key
            # updateConfig(guild.id, data)
            embed = discord.Embed(
                description="Thank you for adding me to your server!\n・ My default prefix is `.`\n・ You can use the `.help` command to get list of commands\n・ Our [Support Server](https://discord.gg/nakhre) or our team offers detailed information & guides for commands\n・ Feel free to join our Support Server https://discord.gg/nakhre if you need help/support for anything related to the bot",
                color=0x2B2D31,
            )
            skidgod = Button(
                label="Support Server",
                style=discord.ButtonStyle.link,
                url="https://discord.gg/nakhre",
            )
            docs = Button(
                label="Invite Me",
                style=discord.ButtonStyle.link,
                url="https://discord.com/api/oauth2/authorize?client_id=1355539303475712032&permissions=4398046511103&scope=applications.commands+bot%20applications.commands",
            )
            docs1 = Button(
                label="Vote Me",
                style=discord.ButtonStyle.link,
                url="https://discord.gg/nakhre",
            )
            view = View()
            view.add_item(skidgod)
            view.add_item(docs)
            view.add_item(docs1)
            if guild.icon:
                embed.set_author(name=f"{guild.name}", icon_url=guild.icon.url)
            if guild.owner and guild.owner.avatar:
                embed.set_thumbnail(url=guild.owner.avatar.url)

            try:
                await guild.owner.send(embed=embed, view=view)
            except discord.Forbidden:
                pass  # Can't DM owner

        except Exception as e:
            print(f"Error in on_guild_join (join.py): {e}")
