import json, sys, os
import discord
from discord.ext import commands
from core import Context
import aiohttp
from discord.ui import Select, View, Button
import time
from typing import Any


class NotVoter(commands.CheckFailure):
    pass


async def check_voter(mem, bot_id: int):
    topgg_token = os.environ.get("TOPGG_TOKEN", "")
    if not topgg_token:
        return "okay"
    async with aiohttp.ClientSession(headers={"Authorization": topgg_token}) as session:
        async with session.get(
                f"https://top.gg/api/bots/{bot_id}/check?userId={str(mem)}"
        ) as response:
            vote = await response.json()
            if vote.get("voted") == 1:
                return "okay"
            return "not okay"


def is_voter():
    async def predicate(ctx: Context):
        topgg_token = os.environ.get("TOPGG_TOKEN", "")
        if not topgg_token:
            return True
        bot_id = ctx.bot.user.id if ctx.bot.user else 0
        async with aiohttp.ClientSession(headers={"Authorization": topgg_token}) as session:
            async with session.get(
                    f"https://top.gg/api/bots/{bot_id}/check?userId={str(ctx.author.id)}"
            ) as response:
                vote = await response.json()
                if vote.get("voted") == 1 or ctx.author.id in ctx.bot.owner_ids:
                    return True
                raise NotVoter()
    return commands.check(predicate)


def DotEnv(query: str):
    return os.getenv(query)


def updateDB(guildID, data):
    with open("data/database.json", "r") as config:
        config = json.load(config)
    config["guilds"][str(guildID)] = data
    newdata = json.dumps(config, indent=4, ensure_ascii=False)
    with open("data/database.json", "w") as config:
        config.write(newdata)


def updateDB1(guildID, data):
    with open("data/bst.json", "r") as config:
        config = json.load(config)
    config["guilds"][str(guildID)] = data
    newdata = json.dumps(config, indent=4, ensure_ascii=False)
    with open("data/bst.json", "w") as config:
        config.write(newdata)


def getExtra(guildID):
    with open("data/extra.json", "r") as config:
        data = json.load(config)
    if str(guildID) not in data["guilds"]:
        defaultConfig = {
            "owners": [],
            "antiSpam": False,
            "antiLink": False,
            "antiinvites": False,
            "punishment": "mute",
            "whitelisted": [],
            "channel": None,
            "mods": [],
            "modrole": None,
            "ignorechannels": []
        }
        updateExtra(guildID, defaultConfig)
        return defaultConfig
    return data["guilds"][str(guildID)]


def updateExtra(guildID, data):
    with open("data/extra.json", "r") as config:
        config = json.load(config)
    config["guilds"][str(guildID)] = data
    newdata = json.dumps(config, indent=4, ensure_ascii=False)
    with open("data/extra.json", "w") as config:
        config.write(newdata)


def getDB1(guildID):
    with open("data/bst.json", "r") as config:
        data = json.load(config)
    if str(guildID) not in data["guilds"]:
        defaultConfig = {
            "boost": {
                "autodel": 0,
                "channel": [],
                "color": "",
                "embed": False,
                "footer": "",
                "image": "",
                "message": "<<boost.user_mention>> Thank you for boosting <<boost.server_name>>",
                "ping": False,
                "title": "",
                "thumbnail": ""
            },
            "boost1": {
                "role": []
            }
        }
        updateDB1(guildID, defaultConfig)
        return defaultConfig
    return data["guilds"][str(guildID)]


import json


def getDB(guildID):
    with open("data/database.json", "r") as config:
        try:
            data = json.load(config)
        except json.JSONDecodeError:
            data = {}

    if "guilds" not in data:
        data["guilds"] = {}

    if str(guildID) not in data["guilds"]:
        defaultConfig = {
            "welcome": {
                "autodel": 0,
                "channel": [],
                "color": "",
                "embed": False,
                "footer": "",
                "image": "",
                "message": "<<user.mention>> Welcome To <<server.name>>",
                "ping": False,
                "title": "",
                "thumbnail": ""
            },
            "goodbye": {
                "autodel": 0,
                "channel": [],
                "color": "",
                "embed": False,
                "footer": "",
                "image": "",
                "message": "<<user.mention>> has left <<server.name>>",
                "ping": False,
                "title": "",
                "thumbnail": ""
            },
            "vcrole": {
                "humans": "",
                "bots": ""
            },
            "nightmode": {
                "status": False,
                "time": None,
                "channel": None
            }
        }
        updateDB(guildID, defaultConfig)
        return defaultConfig
    return data["guilds"][str(guildID)]


def getConfig(guildID):
    with open("config.json", "r") as config:
        try:
            data = json.load(config)
        except json.JSONDecodeError:
            data = {}

    if "guilds" not in data:
        data["guilds"] = {}

    if str(guildID) not in data["guilds"]:
        defaultConfig = {
            "antiSpam": False,
            "antiLink": False,
            "antiInvite": False,
            "whitelisted": [],
            "extraowners": [],
            "bypass_antispam": [],
            "bypass_antilink": [],
            "panic_main_role": [],
            "panic_mode": False,
            "panic_punishment": [],
            "punishment": "ban",
            "prefix": ".",
            "staff": None,
            "vip": None,
            "girl": None,
            "guest": None,
            "frnd": None,
            "owner": None,
            "coown": None,
            "headadmin": None,
            "admin": None,
            "mod": None,
            "gmod": None,
            "gadmin": None,
            "headmod": None,
            "wlrole": None
        }
        updateConfig(guildID, defaultConfig)
        return defaultConfig
    return data["guilds"][str(guildID)]


def updateConfig(guildID, data):
    with open("config.json", "r") as config:
        try:
            cfg = json.load(config)
        except json.JSONDecodeError:
            cfg = {"guilds": {}}
    cfg.setdefault("guilds", {})[str(guildID)] = data
    with open("config.json", "w") as config:
        json.dump(cfg, config, indent=4, ensure_ascii=False)


def blacklist_check():
    async def predicate(ctx: Context):
        try:
            with open("data/blacklist.json", "r") as f:
                data = json.load(f)
            blacklisted = data.get("users", [])
            if ctx.author.id in blacklisted:
                embed = discord.Embed(
                    title="Blacklisted",
                    description="You are blacklisted from using this bot.",
                    color=0x000000)
                await ctx.send(embed=embed)
                return False
        except (FileNotFoundError, json.JSONDecodeError):
            pass
        return True
    return commands.check(predicate)


def ignore_check():
    async def predicate(ctx: Context):
        try:
            with open("data/ignore.json", "r") as f:
                data = json.load(f)
            guild_data = data.get(str(ctx.guild.id), {}) if ctx.guild else {}
            ignored_channels = guild_data.get("channels", [])
            ignored_users = guild_data.get("users", [])
            if ctx.channel.id in ignored_channels or ctx.author.id in ignored_users:
                return False
        except (FileNotFoundError, json.JSONDecodeError):
            pass
        return True
    return commands.check(predicate)


def getanti(guildID):
    """Get antinuke settings for a guild from anti.json"""
    try:
        with open("data/anti.json", "r") as f:
            data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        data = {"guilds": {}}
    if "guilds" not in data:
        data["guilds"] = {}
    if str(guildID) not in data["guilds"]:
        defaultConfig = {
            "status": False,
            "punishment": "ban",
            "whitelisted": [],
            "limits": {
                "ban": 3, "kick": 3, "channel": 3,
                "role": 3, "webhook": 3, "bot": 1
            }
        }
        data["guilds"][str(guildID)] = defaultConfig
        with open("data/anti.json", "w") as f:
            json.dump(data, f, indent=4)
        return defaultConfig
    return data["guilds"][str(guildID)]


def add_user_to_blacklist(user_id: int):
    """Add a user ID to the blacklist file"""
    try:
        with open("data/blacklist.json", "r") as f:
            data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        data = {"users": []}
    if user_id not in data.get("users", []):
        data.setdefault("users", []).append(user_id)
        with open("data/blacklist.json", "w") as f:
            json.dump(data, f, indent=4)


class Timer:
    """Simple context manager timer"""
    def __init__(self):
        self._start = None
        self._end = None

    def __enter__(self):
        self._start = time.perf_counter()
        return self

    def __exit__(self, *args):
        self._end = time.perf_counter()

    @property
    def elapsed(self) -> float:
        if self._end is None:
            return time.perf_counter() - self._start
        return self._end - self._start

    @property
    def elapsed_ms(self) -> float:
        return self.elapsed * 1000
