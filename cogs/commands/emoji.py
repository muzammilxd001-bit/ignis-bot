import contextlib
from traceback import format_exception
import discord
from discord.ext import commands
import io
import textwrap
import datetime
import sys
from discord.ui import Button, View
import psutil
import time
import datetime
import platform
from utils.Tools import *
import os
import logging
from discord.ext import commands
import motor.motor_asyncio
from pymongo import MongoClient
from discord.ext.commands import BucketType, cooldown
import requests
import motor.motor_asyncio as mongodb
from typing import *
from utils import *
import re

from core import Cog, Ignis, Context
from typing import Optional
from discord import app_commands
EMOJI_REGEX = r'<(?P<animated>a?):(?P<name>[a-zA-Z0-9_]{2,32}):(?P<id>[0-9]{18,22})>'
class emojis(commands.Cog, description="Emoji related commands!"):
    def __init__(self, bot):
        self.bot = bot

    @commands.cooldown(2, 10, commands.BucketType.user)
    @blacklist_check()
    @ignore_check()
    @commands.command(help="Enlarge an emoji.")
    async def enlarge(self, ctx, emoji: Union[discord.Emoji, discord.PartialEmoji, str] = None):
        prefix = ctx.clean_prefix

        if emoji is None:
            ctx.command.reset_cooldown(ctx)
            return await ctx.reply(embed=discord.Embed(
                title="❌ Invalid Usage!",
                description=f"Please enter an emoji to enlarge.\nCorrect Usage: `{prefix}enlarge <emoji>`",
                color=discord.Color.red()
            ))

        if isinstance(emoji, (discord.Emoji, discord.PartialEmoji)):
            return await ctx.reply(emoji.url)

        # If the emoji is a default Discord emoji (like 😀, 🚀)
        await ctx.reply(embed=discord.Embed(
            title="❌ Error",
            description="This emoji is not a custom emoji, so I cannot enlarge it!",
            color=discord.Color.red()
        ))


    @commands.command(help="Steal emojis!", aliases=['steal-emoji', 'stwalemoji'])
    @commands.has_permissions(manage_emojis=True)
    @commands.bot_has_permissions(manage_emojis=True)
    @blacklist_check()
    @ignore_check()
    @commands.cooldown(7, 15, commands.BucketType.user)

  #  @commands.max_concurrency(1, per=commands.BucketType.default, wait=False)

    @commands.guild_only()
    async def steal(self, ctx, emojis: commands.Greedy[Union[discord.PartialEmoji, discord.Emoji]] = None):
        ref = ctx.message.reference
        prefix = ctx.clean_prefix
        
        if ref:
            msg = await ctx.fetch_message(ref.message_id)
            emojis = re.findall(EMOJI_REGEX, msg.content)
            stolen_emojis = ""
            fail_emojis = ""
            s = await ctx.send(f"stealing please wait... ")
            for emoji in emojis:
                name = emoji[1]
                ext = "gif" if emoji[0] else "png"
                image_url = f"https://cdn.discordapp.com/emojis/{emoji[2]}.{ext}"
                
                async with ClientSession() as session:
                   async with session.get(image_url) as resp:
                        image = await resp.read()
                        try:
                        
                           op = await ctx.guild.create_custom_emoji(name=name, image=image)
                           stolen_emojis += f"{op}"
                        except Exception:
                           fail_emojis += f"`{op.name}` "
                      
        
            await s.edit(content=f" | Successfully stole emoji(s), {stolen_emojis}{' and failed to steal '+fail_emojis if len(fail_emojis) > 0 else ''}",embed=None,view=None)
            return
        else:
            if emojis is None:
                return await ctx.reply(embed=error_embed(
                f" Invalid Usage!",
                f"Please enter some emojis to steal.\n\n**Example:** ?steal  ..."
            ))
        uploaded_emojis = ""
        failed_emojis = ""

        m = await ctx.reply(f"stealing please wait... ")

        for emoji in emojis:
            if isinstance(emoji, discord.PartialEmoji):
                try:
                    emo = await ctx.guild.create_custom_emoji(
                        name=emoji.name,
                        image=await emoji.read(),
                        reason=f"steal command used by {ctx.author} ({ctx.author.id})"
                    )
                    uploaded_emojis += f"{emo} "
                except Exception:
                    failed_emojis += f"`{emoji.name}` "
            else:
                view = Confirm(context=ctx)
                await m.edit(
                    content="",
                    embed=success_embed(
                        "Is this the emoji you wanted?",
                        f"The name `{emoji.name}` corresponds to this emote, do u want to steal this?"
                    ).set_image(url=emoji.url),
                    view=view
                )
                await view.wait()
                if view.value is None:
                    await m.edit(
                        content="",
                        embed=error_embed(
                            "You didn't respond in time.",
                            f"Skipped this emoji. stealing other emojis... "
                        ),
                        view=None
                    )
                elif not view.value:
                    await m.edit(
                        content="",
                        embed=success_embed(
                            f" Alright!",
                            "Skipped that emote."
                        ),
                        view=None
                    )
                else:
                    await m.edit(
                        content="",
                        embed=discord.Embed(
                            title=f" Ok, stealing...",
                            color=MAIN_COLOR),
                        view=None
                    )
                    try:
                        emo = await ctx.guild.create_custom_emoji(
                            name=emoji.name,
                            image=await emoji.read(),
                            reason=f"steal command used by {ctx.author} ({ctx.author.id})"
                        )
                        uploaded_emojis += f"{emo} "
                    except Exception:
                        failed_emojis += f"`{emoji.name}` "

        await m.edit(
            content=f"I have stealed {uploaded_emojis}{' and failed to steal '+failed_emojis if len(failed_emojis) > 0 else ''}",embed=None,view=None)
                


            
