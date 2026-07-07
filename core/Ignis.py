from __future__ import annotations
from discord.ext import commands
import discord
import aiohttp
import colorama
from colorama import Fore
import json
import jishaku, time
import asyncio
import typing
import os
from utils.config import OWNER_IDS, EXTENSIONS, No_Prefix
from utils import getConfig, updateConfig, DotEnv
from .Context import Context
from discord.ext import commands, tasks


class Ignis(commands.AutoShardedBot):

    def __init__(self, *arg, **kwargs):
        self.topgg_token = os.environ.get("TOPGG_TOKEN", "")
        intents = discord.Intents.all()
        intents.presences = False
        intents.members = True
        super().__init__(
            command_prefix=self.get_prefix,
            case_insensitive=True,
            intents=intents,
            status=discord.Status.dnd,
            strip_after_prefix=True,
            owner_ids=OWNER_IDS,
            allowed_mentions=discord.AllowedMentions(
                everyone=False, replied_user=False, roles=False),
            shard_count=2)

    async def on_ready(self):
        print(Fore.RED + "Connected as {}".format(self.user))

    async def on_connect(self):
        await self.change_presence(
            status=discord.Status.dnd,
            activity=discord.Activity(
                type=discord.ActivityType.listening, name=".help | .inv"))

        if self.topgg_token:
            try:
                headers = {"Authorization": self.topgg_token}
                async with aiohttp.ClientSession(headers=headers) as session:
                    bot_id = self.user.id if self.user else 0
                    async with session.post(
                            f"https://top.gg/api/bots/{bot_id}/stats",
                            json={
                                "server_count": len(self.guilds),
                                "shard_count": len(self.shards)
                            }) as r:
                        if r.status == 200:
                            print(Fore.LIGHTBLUE_EX + "Ignis On Top GG")
                        else:
                            print(Fore.YELLOW + f"Top.gg update returned {r.status}")
            except Exception as e:
                print(Fore.YELLOW + f"Top.gg stats update failed: {e}")

    async def send_raw(self, channel_id: int, content: str,
                       **kwargs) -> typing.Optional[discord.Message]:
        await self.http.send_message(channel_id, content, **kwargs)

    async def invoke_help_command(self, ctx: Context) -> None:
        return await ctx.send_help(ctx.command)

    async def fetch_message_by_channel(
            self, channel: discord.TextChannel,
            messageID: int) -> typing.Optional[discord.Message]:
        async for msg in channel.history(
                limit=1,
                before=discord.Object(messageID + 1),
                after=discord.Object(messageID - 1),
        ):
            return msg

    async def get_prefix(self, message: discord.Message):
        if not message.guild:
            return commands.when_mentioned_or('.')(self, message)
        data = getConfig(message.guild.id)
        prefix = data.get("prefix", ".")
        with open('info.json', 'r') as f:
            p = json.load(f)
        if message.author.id in p.get("np", []):
            return commands.when_mentioned_or(prefix, '')(self, message)
        else:
            return commands.when_mentioned_or(prefix)(self, message)

    async def on_message_edit(self, before, after):
        ctx: Context = await self.get_context(after, cls=Context)
        if before.content != after.content:
            if after.guild is None or after.author.bot:
                return
            if ctx.command is None:
                return
            if isinstance(ctx.channel, discord.Thread):
                return
            await self.invoke(ctx)
