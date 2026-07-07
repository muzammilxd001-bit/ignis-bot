import discord
import wavelink
from wavelink.ext import spotify
from discord.ext import commands
import logging
from typing import Any, Dict, Union, Optional
from discord.enums import try_enum
import os
import datetime
import datetime as dt
import datetime

import typing as t
import requests
import re
from discord.ext.commands.errors import CheckFailure
import asyncio
import os
from wavelink import Player
import async_timeout
from utils.Tools import *
from wavelink.filters import Karaoke, Timescale

class MusicFilters(commands.Cog):
    def __init__(self, bot):
        self.bot = bot



    @commands.group(name="nightcore",
                    invoke_without_command=True,
                    aliases=['nc'])
    @blacklist_check()
    @ignore_check()
    async def _nightcore(self, ctx):
        if ctx.subcommand_passed is None:
            await ctx.send_help(ctx.command)
            ctx.command.reset_cooldown(ctx)

    @_nightcore.command(name="enable", aliases=[("on")])
    @blacklist_check()
    @ignore_check()
    async def enable_nightcore(self, ctx: commands.Context):
        vc: wavelink.Player = ctx.voice_client

        if vc is None:
            ray = discord.Embed(
                description=
                "<:cross:1348326385386651748> | You are not connected to a voice channel.",
                color=0x2b2d31)
            ray.set_footer(text=f"Requested By {ctx.author}",
                              icon_url=f"{ctx.author.avatar}")
            ray.set_thumbnail(url = f"{ctx.author.avatar}")
            
            return await ctx.reply(embed=ray)
        
        # add nightcore filter
        nightcore_filter = wavelink.Filter(
            timescale=Timescale(rate=1.3),
            karaoke=Karaoke(level=1.0, mono_level=1.0, filter_band=220, filter_width=100)
        )
        
        await vc.set_filter(nightcore_filter, seek=True)
        ray4 = discord.Embed(
            description=
            "<:tick:1348326381611647046> | Successfully enabled `nightcore` filter.",
            color=0x2b2d31)

        await ctx.reply(embed=ray4)
