import discord
import requests
import aiohttp
import datetime
import random
from discord.ext import commands
from random import randint
from utils.Tools import *
from core import Cog, Ignis, Context
#14
#snipe | editsnipe | tickle | kiss | hug | slap | pat | feed | pet | howgay | slots | HowCute | meme | cat

from pathlib import Path
import json

PICKUP_LINES = json.loads(Path("data/pikup.json").read_text("utf8"))


def RandomColor():
    randcolor = discord.Color(random.randint(0x2b2d31, 0x2b2d31))
    return randcolor


class Fun(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    async def add_role(self, *, role: int, member: discord.Member):
        if member.guild.me.guild_permissions.manage_roles:
            role = discord.Object(id=int(role))
            await member.add_roles(role, reason="Ignis | Role Added ")

    async def remove_role(self, *, role: int, member: discord.Member):
        if member.guild.me.guild_permissions.manage_roles:
            role = discord.Object(id=int(role))
            await member.remove_roles(role, reason="Ignis | Role Removed")

    @blacklist_check()
    @ignore_check()
    @commands.command(name="tickle",
                      help="Tickle mentioned user .",
                      usage="Tickle <member>")
    async def tickle(self, ctx, user: discord.Member = None):
        if user is None:
            await ctx.send("")
        else:
            r = requests.get("https://nekos.life/api/v2/img/tickle")
            res = r.json()
            embed = discord.Embed(
                timestamp=datetime.datetime.utcnow(),
                description=f"{ctx.author.mention} tickle {user.mention}",
                color=0x2b2d31)
            embed.set_image(url=res['url'])
            embed.set_footer(text=f"{ctx.guild.name}")
            await ctx.send(embed=embed)

    @blacklist_check()
    @ignore_check()
    @commands.command(name="kiss",
                      help="Kiss mentioned user .",
                      usage="Kiss <member>")
    async def kiss(self, ctx, user: discord.Member = None):
        if user is None:
            await ctx.send("")
        else:
            r = requests.get("https://nekos.life/api/v2/img/kiss")
            res = r.json()
            embed = discord.Embed(
                timestamp=datetime.datetime.utcnow(),
                description=f"{ctx.author.mention} kisses {user.mention}",
                color=0x2b2d31)
            embed.set_image(url=res['url'])
            embed.set_footer(text=f"{ctx.guild.name}")
            await ctx.send(embed=embed)

    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.command(name="hug",
                      help="hug mentioned user .",
                      usage="hug <member>")
    @blacklist_check()
    @ignore_check()
    async def hug(self, ctx, user: discord.Member = None):
        if user is None:
            await ctx.send("")
        else:
            r = requests.get("https://nekos.life/api/v2/img/hug")
            res = r.json()
            embed = discord.Embed(
                timestamp=datetime.datetime.utcnow(),
                color=0x2b2d31,
                description=f"{ctx.author.mention} hugged {user.mention}",
            )
            embed.set_image(url=res['url'])
            embed.set_footer(text=f"{ctx.guild.name}")
            await ctx.send(embed=embed)

    @commands.command(name="slap",
                      help="Slap mentioned user .",
                      usage="Slap <member>")
    @blacklist_check()
    @ignore_check()
    async def slap(self, ctx, user: discord.Member = None):
        if user is None:
            await ctx.send("")
        else:
            r = requests.get("https://nekos.life/api/v2/img/slap")
            res = r.json()
            embed = discord.Embed(
                timestamp=datetime.datetime.utcnow(),
                color=0x2b2d31,
                description=f"{ctx.author.mention} slapped {user.mention}",
            )
            embed.set_image(url=res['url'])
            embed.set_footer(text=f"{ctx.guild.name}")
            await ctx.send(embed=embed)

    @commands.command(name="pat",
                      help="pat mentioned user .",
                      usage="pat <member>")
    @blacklist_check()
    @ignore_check()
    async def pat(self, ctx, user: discord.Member = None):
        if user is None:
            await ctx.send("")
        else:
            r = requests.get("https://nekos.life/api/v2/img/pat")
            res = r.json()
            embed = discord.Embed(
                timestamp=datetime.datetime.utcnow(),
                color=0x2b2d31,
                description=f"{ctx.author.mention} patted {user.mention}",
            )
            embed.set_image(url=res['url'])
            embed.set_footer(text=f"{ctx.guild.name}")
            await ctx.send(embed=embed)
            
    @commands.command(name="feed",
                      help="Feed mentioned user .",
                      usage="Feed <member>")
    @blacklist_check()
    @ignore_check()
    async def feed(self, ctx, user: discord.Member = None):
        if user is None:
            await ctx.send("")
        else:
            r = requests.get("https://nekos.life/api/v2/img/feed")
            res = r.json()
            embed = discord.Embed(
                timestamp=datetime.datetime.utcnow(),
                description=f"{ctx.author.mention} feeds {user.mention}",
                color=0x2b2d31)
            embed.set_image(url=res['url'])
            embed.set_footer(text=f"{ctx.guild.name}")
            await ctx.send(embed=embed)

    @commands.command(name="pet", usage="Pet <member>")
    @blacklist_check()
    @ignore_check()
    async def pet(self, ctx, user: discord.Member = None):
        if user is None:
            await ctx.send("")
        else:
            r = requests.get("https://nekos.life/api/v2/img/pat")
            res = r.json()
            embed = discord.Embed(
                timestamp=datetime.datetime.utcnow(),
                description=f"{ctx.author.mention} pets {user.mention}",
                color=0x2b2d31)
            embed.set_image(url=res['url'])
            embed.set_footer(text=f"{ctx.guild.name}")
            await ctx.send(embed=embed)

    @commands.command(
        name="gay",
        help="Check someone's gay percentage",
        usage="gay [user]"
    )
    @blacklist_check()
    @ignore_check()
    async def gay(self, ctx, member: discord.Member = None):
        """Check someone's fabulousness level"""
        
        # Whitelisted users (IDs)
        WHITELIST = [
            870179991462236170,
            912422872411160667,
            806624430322483220,
            1196530292199014432
        ]
        
        member = member or ctx.author  # Default to author if no member mentioned
        
        embed = discord.Embed(color=0x2b2d31)
        
        # Whitelist check
        if member.id in WHITELIST:
            embed.description = f"**{member.display_name}** is not gay (He is Your Father) ❤️"
            embed.set_footer(text="Special exception")
            return await ctx.send(embed=embed)
        
        # Generate random percentage (0-100)
        percentage = random.randint(0, 100)
        
        # Set embed content
        embed.description = f"**{member.display_name}** is **{percentage}% gay** 🏳️‍🌈"
        embed.set_footer(text=f"Requested by {ctx.author.display_name}")
        
        await ctx.send(embed=embed)


    @commands.command(name="slots")
    @blacklist_check()
    async def slots(self, ctx):
        emojis = "🍎🍊🍐🍋🍉🍇🍓🍒"
        a = random.choice(emojis)
        b = random.choice(emojis)
        c = random.choice(emojis)
        slotmachine = f"[ {a} {b} {c} ]\n{ctx.author.mention}"
        if (a == b == c):
            await ctx.send(embed=discord.Embed(
                title="Slot machine",
                description=f"{slotmachine} All Matching! You Won!",
                color=0x2b2d31))
        elif (a == b) or (a == c) or (b == c):
            await ctx.send(embed=discord.Embed(
                title="Slot machine",
                description=f"{slotmachine} 2 Matching! You Won!",
                color=0x2b2d31))
        else:
            await ctx.send(embed=discord.Embed(
                title="Slot machine",
                description=f"{slotmachine} No Matches! You Lost!",
                color=0x2b2d31))

    @commands.command(name="howcute",
                      aliases=['cute', 'sexy', 'howsexy', 'howhorny'],
                      help="check someone cute percentage",
                      usage="Howcute <person>")
    @blacklist_check()
    async def howgay(self, ctx, member: discord.Member):  # Notice member: discord.Member
      embed = discord.Embed(color=0x2b2d31)
      responses = [
          '50', '75', '25', '1', '3', '5', '10', '65', '60', '85', '30', '40',
          '45', '80', '100', '150', '1000', '5000', '100000'
      ]
      embed.description = f'**{member.display_name} is {random.choice(responses)}% cute** 🥵'
      embed.set_footer(text=f'How cute are you? - {ctx.author.name}')
      await ctx.send(embed=embed)

    @commands.command(name="meme", help="give you a meme", usage="meme")
    @blacklist_check()
    @ignore_check()
    async def meme(self, ctx):
        embed = discord.Embed(title="""Take some memes""", color=0x2b2d31)
        async with aiohttp.ClientSession() as cs:
            async with cs.get(
                    'https://www.reddit.com/r/dankmemes/new.json?sort=hot'
            ) as r:
                res = await r.json()
                embed.set_image(url=res['data']['children'][random.randint(
                    0, 25)]['data']['url'])
                embed.set_footer(text=f'Random Meme:')
                await ctx.send(embed=embed)

    @commands.command(name="cat", usage="cat")
    @blacklist_check()
    @ignore_check()
    async def cat(self, ctx):
        embed = discord.Embed(title="""Here's a cat""", color=0x2b2d31)
        async with aiohttp.ClientSession() as cs:
            async with cs.get('http://aws.random.cat/meow') as r:
                res = await r.json()
                embed.set_image(url=res['file'])
                embed.set_footer(text=f'Random Cats:')
                await ctx.send(embed=embed)

    @commands.command(name="iplookup",
                             aliases=['ip', 'ipl'],
                             help="shows info about an ip",
                             usage="Iplookup [ip]")
    @blacklist_check()
    @ignore_check()
    async def iplookup(self, ctx, *, ip):
        async with aiohttp.ClientSession() as a:
            async with a.get(f"http://ipwhois.app/json/{ip}") as b:
                c = await b.json()
                try:
                    coordj = ''.join(f"{c['latitude']}" + ", " +
                                     f"{c['longitude']}")
                    embed = discord.Embed(
                        title="IP: {}".format(ip),
                        description=
                        f"```txt\n\nLocation Info:\nIP: {ip}\nIP Type: {c['type']}\nCountry, Country code: {c['country']} ({c['country_code']})\nPhone Number Prefix: {c['country_phone']}\nRegion: {c['region']}\nCity: {c['city']}\nCapital: {c['country_capital']}\nLatitude: {c['latitude']}\nLongitude: {c['longitude']}\nLat/Long: {coordj} \n\nTimezone Info:\nTimezone: {c['timezone']}\nTimezone Name: {c['timezone_name']}\nTimezone (GMT): {c['timezone_gmt']}\nTimezone (GMT) offset: {c['timezone_gmtOffset']}\n\nContractor/Hosting Info:\nASN: {c['asn']}\nISP: {c['isp']}\nORG: {c['org']}\n\nCurrency:\nCurrency type: {c['currency']}\nCurrency Code: {c['currency_code']}\nCurrency Symbol: {c['currency_symbol']}\nCurrency rates: {c['currency_rates']}\nCurrency type (plural): {c['currency_plural']}```",
                        color=0x2b2d31)
                    embed.set_footer(
                        text='Thanks For Using Ignis',
                        icon_url=
                        "https://media.discordapp.net/attachments/1349834275410939904/1355756857246879845/ignis1.png"
                    )
                    await ctx.send(embed=embed)
                except KeyError:
                    embed = discord.Embed(
                        description=
                        "KeyError has occured, perhaps this is a bogon IP address, or invalid IP address?",
                        color=0x2b2d31)
                    await ctx.send(embed=embed)


############################

    @commands.command(name="pickupline")
    @blacklist_check()
    @ignore_check()
    async def pickupline(self, ctx: Context) -> None:
        """
        Gives you a random pickup line.
        Note that most of them are very cheesy.
        """
        random_line = random.choice(PICKUP_LINES["lines"])
        embed = discord.Embed(
            title=":cheese: Your pickup line :cheese:",
            description=random_line["line"],
            color=ctx.author.color,
        )
        embed.set_thumbnail(
            url=random_line.get("image", PICKUP_LINES["placeholder"]))
        await ctx.send(embed=embed)