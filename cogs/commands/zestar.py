import os
import discord
from discord.ext import commands
import requests
import sys
from utils.Tools import getConfig, add_user_to_blacklist, getanti
import setuptools
from itertools import cycle
from collections import Counter
import threading
import datetime
import logging
from core import Ignis, Cog
import time
import asyncio
import aiohttp
import tasksio
from discord.ui import View, Button
import json
from discord.ext import tasks
import random

logging.basicConfig(
    level=logging.INFO,
    format="\x1b[38;5;197m[\x1b[0m%(asctime)s\x1b[38;5;197m]\x1b[0m -> \x1b[38;5;197m%(message)s\x1b[0m",
    datefmt="%H:%M:%S",
)

proxies = open("proxies.txt").read().split("\n")
proxs = cycle(proxies)
proxies = {"http": "http://" + next(proxs)}


class Zestar(Cog):
    def __init__(self, client: Ignis):
        self.client = client
        self.spam_control = commands.CooldownMapping.from_cooldown(
            10, 12.0, commands.BucketType.user
        )

    @commands.Cog.listener()
    async def on_message(self, message):
        button = Button(
            label="Invite Me",
            url="https://discord.com/api/oauth2/authorize?client_id=1355539303475712032&permissions=4398046511103&scope=applications.commands+bot",
        )
        button1 = Button(label="Support Server", url="https://discord.gg/nakhre")
        button2 = Button(label="Vote Me", url="https://discord.gg/nakhre")
        try:

            with open("data/blacklist.json", "r") as f:
                data2 = json.load(f)
            with open("data/ignore.json", "r") as heck:
                Igniss = json.load(heck)
                Ignis = "<@1355539303475712032>"
                try:
                    data = getConfig(message.guild.id)
                    anti = getanti(message.guild.id)
                    prefix = data["prefix"]
                    wled = data["whitelisted"]
                    punishment = data["punishment"]
                    wlrole = data["wlrole"]
                    guild = message.guild
                    ray = guild.get_member(message.author.id)
                    wlroles = guild.get_role(wlrole)
                except Exception:
                    pass
                guild = message.guild
                if message.mention_everyone:
                    if (
                        str(message.author.id) in wled
                        or anti == "off"
                        or wlroles in ray.roles
                    ):
                        pass
                    else:
                        if punishment == "ban":
                            await message.guild.ban(
                                message.author,
                                reason="Mentioning Everyone | Not Whitelisted",
                            )
                        elif punishment == "kick":
                            await message.guild.kick(
                                message.author,
                                reason="Mentioning Everyone | Not Whitelisted",
                            )
                        elif punishment == "none":
                            return

                elif (
                    message.content == Ignis
                    or message.content == "<@1355539303475712032>"
                ):
                    if str(message.author.id) in data2["ids"]:
                        embed = discord.Embed(
                            title="<:cross:1348326385386651748> Blacklisted",
                            description="You Are Blacklisted From Using My Commands.\nIf You Think That It Is A Mistake, You Can't Appeal In Our Support Server By Clicking [here](https://discord.gg/nakhre)",
                        )
                        await message.reply(embed=embed, mention_author=False)
                    if str(message.channel.id) in Igniss["ids"]:
                        await message.reply(
                            f"My all commands are disabled for {message.channel.mention}",
                            mention_author=True,
                            delete_after=10,
                        )

                    else:

                        embed = discord.Embed(
                            description=f"# <a:hello:1348887579361280061> Hello {message.author.mention}\n\n> <:arrow_right:1348340445708816494> Don't Know **The Prefix: ``{prefix}``**\n> <:arrow_right:1348340445708816494> If You Don't Know Where to Start Type :``{prefix}help`` \n> <:arrow_right:1348340445708816494> If you continue to have problems, consider asking for help **[Click Here](https://discord.gg/nakhre)** \n> <:arrow_right:1348340445708816494> If Bot is not Responding Type : ``{prefix}ping``",
                            color=0x2B2D31,
                        )
                        embed.set_image(
                            url="https://media.discordapp.net/attachments/1349834275410939904/1355756769292320923/ignis.png"
                        )
                        embed.set_footer(
                            icon_url="https://media.discordapp.net/attachments/1349834275410939904/1355756857246879845/ignis1.png",
                        )
                        view = View()
                        view.add_item(button)
                        view.add_item(button1)
                        view.add_item(button2)

                        await message.reply(
                            embed=embed,
                            delete_after=20,
                            mention_author=False,
                            view=view,
                        )
                else:
                    return
        except Exception as error:
            if isinstance(error, discord.Forbidden):
                return
