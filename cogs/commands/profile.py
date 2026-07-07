import json
from utils import *
import discord
from discord.ext import commands
import requests
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont


def getBDG(userid):
    with open("data/bdg.json", "r") as config:
        data = json.load(config)
    if str(userid) not in data["users"]:
        defaultConfig = {
            "owner": False,
            "developer": False,
            "staff": False,
            "early": False,
            "partner": False,
            "vip": False,
            "friends": False,
            "bug": False,
            "sponsors": False,
            "family": True,
        }
        updateBDG(userid, defaultConfig)
        return defaultConfig
    return data["users"][str(userid)]


def updateBDG(userid, data):
    with open("data/bdg.json", "r") as config:
        config = json.load(config)
    config["users"][str(userid)] = data
    newdata = json.dumps(config, indent=4, ensure_ascii=False)
    with open("data/bdg.json", "w") as config:
        config.write(newdata)


class Profile(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(
        name="badges",
        help="Check what premium badges a user have.",
        aliases=["badge", "profile", "pr"],
        usage="Badges [user]",
        with_app_command=True,
    )
    @blacklist_check()
    @ignore_check()
    async def profile(self, ctx, mem: discord.Member = None):
        if mem is None:
            mem = ctx.author
        message = await ctx.send(
            embed=discord.Embed(
                description="**<a:loading:1349238953450147924> | Loading user info**"
            )
        )
        background_image = Image.open("img/bg.png").convert("RGBA")
        font = ImageFont.truetype("ignis.ttf", 40)
        draw = ImageDraw.Draw(background_image)
        draw.text((60, 510), f"{mem.name}", font=font)
        avatar_url = mem.avatar.url if mem.avatar else mem.default_avatar.url
        response = requests.get(avatar_url)
        avatar_image = Image.open(BytesIO(response.content)).convert("RGBA")
        avatar_image = avatar_image.resize((340, 340))
        background_image.paste(avatar_image, (50, 70), avatar_image)
        data = getBDG(mem.id)
        selected_images = []
        text = []

        cord = [
            (560, 125),
            (1000, 125),
            (560, 260),
            (1000, 260),
            (560, 390),
            (1000, 390),
            (560, 530),
            (1000, 530),
            (560, 665),
            (1000, 665),
        ]
        if data["owner"] == True:
            selected_images += [
                "https://cdn.discordapp.com/emojis/1253658307806236722.jpg?v=1&size=48"
            ]
            text += ["Owner"]
        if data["developer"] == True:
            selected_images += [
                "https://cdn.discordapp.com/emojis/1253658492808593518.jpg?v=1&size=48"
            ]
            text += ["Developer"]
        if data["early"] == True:
            selected_images += [
                "https://cdn.discordapp.com/emojis/1253662457621250058.jpg?v=1&size=48"
            ]
            text += ["Early Supporter"]
        if data["staff"] == True:
            selected_images += [
                "https://cdn.discordapp.com/emojis/1253658901556101180.jpg?v=1&size=48"
            ]
            text += ["Staff"]
        if data["bug"] == True:
            selected_images += [
                "https://cdn.discordapp.com/emojis/1253661201674801182.jpg?v=1&size=48"
            ]
            text += ["Bug Hunter"]
        if data["vip"] == True:
            selected_images += [
                "https://cdn.discordapp.com/emojis/1253663009050726411.jpg?v=1&size=48"
            ]
            text += ["VIP"]
        if data["sponsors"] == True:
            selected_images += [
                "https://cdn.discordapp.com/emojis/1253658645829517323.jpg?v=1&size=48"
            ]
            text += ["Sponsors"]
        if data["partner"] == True:
            selected_images += [
                "https://cdn.discordapp.com/emojis/1253659491413659699.jpg?v=1&size=48"
            ]
            text += ["Partner"]
        if data["friends"] == True:
            selected_images += [
                "https://cdn.discordapp.com/emojis/1253658530628636672.jpg?v=1&size=48"
            ]
            text += ["Friends"]
        if data["family"] == True:
            selected_images += [
                "https://cdn.discordapp.com/emojis/1253658414211403808.jpg?v=1&size=48"
            ]
            text += ["Family"]
        locations = [
            (430, 105),
            (870, 105),
            (430, 240),
            (870, 240),
            (430, 370),
            (870, 370),
            (430, 510),
            (870, 510),
            (430, 645),
            (870, 645),
        ]

        def add_image(url):
            selected_images.append(url)

        for i, image_url in enumerate(selected_images):
            response = requests.get(image_url)
            img = Image.open(BytesIO(response.content))
            img = img.resize((90, 90))
            background_image.paste(img, locations[i])

        for lol, coordinates in zip(text, cord):
            draw.text(coordinates, f"{lol}", font=font)
        badges = ""
        if mem.public_flags.hypesquad:
            badges += "** ◇ Hypesquad**\n"
        elif mem.public_flags.hypesquad_balance:
            badges += (
                "** ◇ <:Hypesquad_Balance:1356221383213842594> HypeSquad Balance**\n"
            )

        elif mem.public_flags.hypesquad_bravery:
            badges += "** ◇ <:hypesquad3:1356221454261424241> HypeSquad Bravery**\n"
        elif mem.public_flags.hypesquad_brilliance:
            badges += "** ◇ <:hypesquad:1356221525388169297> Hypesquad Brilliance**\n"
        if mem.public_flags.early_supporter:
            badges += "** ◇ <:EarlySupporter:1356221575850102825> Early Supporter**\n"
        elif mem.public_flags.verified_bot_developer:
            badges += "** ◇ <a:VerifiedBotDeveloper:1356221604014587904> Verified Bot Developer**\n"
        elif mem.public_flags.active_developer:
            badges += "** ◇ <a:bot:1356221656468553781> Active Developer**\n"
        if badges == "":
            badges = "None"
        embed2 = discord.Embed(title=f"** ◇ {mem.name}'s Profile**", color=mem.color)
        embed2.add_field(
            name="**__Account Info__**",
            value=f"** ◇ Account Created at **: <t:{round(mem.created_at.timestamp())}:R>\n** ◇ Joined at : <t:{round(mem.joined_at.timestamp())}:R>**",
            inline=False,
        )
        embed2.add_field(name="**User Badges:**", value=f"{badges}", inline=False)
        # embed2.add_field(
        #   name="**Bot Badges:**",
        #   value="**Here**",
        #   inline=False)
        embed2.set_thumbnail(
            url=mem.avatar.url if mem.avatar else mem.default_avatar.url
        )

        buffer = BytesIO()
        background_image.save(buffer, format="PNG")
        buffer.seek(0)
        file = discord.File(buffer, filename="itz_your_ray_op.png")
        embed2.set_image(url="attachment://itz_your_ray_op.png")
        await message.edit(embed=embed2, attachments=[file])

    @commands.group(name="bdg", invoke_without_command=True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.max_concurrency(1, per=commands.BucketType.default, wait=False)
    @blacklist_check()
    @ignore_check()
    async def _autorole(self, ctx):
        if ctx.subcommand_passed is None:
            await ctx.send_help(ctx.command)
            ctx.command.reset_cooldown(ctx)

    @_autorole.command(name="remove")
    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.max_concurrency(1, per=commands.BucketType.default, wait=False)
    @commands.is_owner()
    @blacklist_check()
    @ignore_check()
    async def bdg_remove(self, ctx, user: discord.Member, *, badge: str):
        userid = user.id
        data = getBDG(user.id)
        badge = badge.lower()
        tick_emoji = "<:tick:1348326381611647046>"
        if badge in ["dev", "developer", "devp"]:
            data["developer"] = False
            updateBDG(user.id, data)
            embed = discord.Embed(
                description=f"{tick_emoji} | Successfully removed `developer` badge from {user.mention}"
            )
            await ctx.send(embed=embed)
        elif badge in ["owner"]:
            data["owner"] = False
            updateBDG(user.id, data)
            embed = discord.Embed(
                description=f"{tick_emoji} | Successfully removed `owner` badge from {user.mention}"
            )
            await ctx.send(embed=embed)
        elif badge in ["staff"]:
            data["staff"] = False
            updateBDG(userid, data)
            embed = discord.Embed(
                description=f"{tick_emoji} | Successfully removed `staff` badge from {user.mention}"
            )
            await ctx.send(embed=embed)
        elif badge in ["sponsors", "sponsor"]:
            data["sponsors"] = False
            updateBDG(userid, data)
            embed = discord.Embed(
                description=f"{tick_emoji} | Successfully removed `sponsor` badge from {user.mention}"
            )
            await ctx.send(embed=embed)
        elif badge in ["friend", "friends"]:
            data["friends"] = False
            updateBDG(userid, data)
            embed = discord.Embed(
                description=f"{tick_emoji} | Successfully removed `friend` badge from {user.mention}"
            )
            await ctx.send(embed=embed)
        elif badge in ["bug", "hunter"]:
            data["bug"] = False
            updateBDG(userid, data)
            embed = discord.Embed(
                description=f"{tick_emoji} | Successfully removed `bug hunter` badge from {user.mention}"
            )
            await ctx.send(embed=embed)
        elif badge in ["vip"]:
            data["vip"] = False
            updateBDG(userid, data)
            embed = discord.Embed(
                description=f"{tick_emoji} | Successfully removed `vip` badge from {user.mention}"
            )
            await ctx.send(embed=embed)
        elif badge in ["early"]:
            data["early"] = False
            updateBDG(userid, data)
            embed = discord.Embed(
                description=f"{tick_emoji} | Successfully removed `early` badge from {user.mention}"
            )
            await ctx.send(embed=embed)
        elif badge in ["partner"]:
            data["partner"] = False
            updateBDG(userid, data)
            embed = discord.Embed(
                description=f"{tick_emoji} | Successfully removed `partner` badge from {user.mention}"
            )
            await ctx.send(embed=embed)
        elif badge in ["all"]:
            data["developer"] = False
            data["owner"] = False
            data["staff"] = False
            data["sponsors"] = False
            data["friends"] = False
            data["bug"] = False
            data["vip"] = False
            data["early"] = False
            data["partner"] = False
            updateBDG(user.id, data)
            embed = discord.Embed(
                description=f"{tick_emoji} | Successfully removed all badges from {user.mention}"
            )
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(
                description="<:cross:1348326385386651748>** | No badge found!**"
            )
            await ctx.send(embed=embed)

    @_autorole.command(name="add")
    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.max_concurrency(1, per=commands.BucketType.default, wait=False)
    @commands.is_owner()
    @blacklist_check()
    @ignore_check()
    async def bdg_add(self, ctx, user: discord.Member, badge: str):
        userid = user.id
        data = getBDG(userid)
        badge = badge.lower()
        tick_emoji = "<:tick:1348326381611647046>"
        if badge in ["dev", "developer", "devp"]:
            data["developer"] = True
            updateBDG(userid, data)
            embed = discord.Embed(
                description=f"{tick_emoji} | Successfully added `developer` badge to {user.mention}"
            )
            await ctx.send(embed=embed)
        elif badge in ["owner"]:
            data["owner"] = True
            updateBDG(userid, data)
            embed = discord.Embed(
                description=f"{tick_emoji} | Successfully added `owner` badge to {user.mention}"
            )
            await ctx.send(embed=embed)
        elif badge in ["staff"]:
            data["staff"] = True
            updateBDG(userid, data)
            embed = discord.Embed(
                description=f"{tick_emoji} | Successfully added `staff` badge to {user.mention}"
            )
            await ctx.send(embed=embed)
        elif badge in ["sponsors", "sponsor"]:
            data["sponsors"] = True
            updateBDG(userid, data)
            embed = discord.Embed(
                description=f"{tick_emoji} | Successfully added `sponsor` badge to {user.mention}"
            )
            await ctx.send(embed=embed)
        elif badge in ["friend", "friends"]:
            data["friends"] = True
            updateBDG(userid, data)
            embed = discord.Embed(
                description=f"{tick_emoji} | Successfully added `friend` badge to {user.mention}"
            )
            await ctx.send(embed=embed)
        elif badge in ["bug", "hunter"]:
            data["bug"] = True
            updateBDG(userid, data)
            embed = discord.Embed(
                description=f"{tick_emoji} | Successfully added `bug hunter` badge to {user.mention}"
            )
            await ctx.send(embed=embed)
        elif badge in ["vip"]:
            data["vip"] = True
            updateBDG(userid, data)
            embed = discord.Embed(
                description=f"{tick_emoji} | Successfully added `vip` badge to {user.mention}"
            )
            await ctx.send(embed=embed)
        elif badge in ["early"]:
            data["early"] = True
            updateBDG(userid, data)
            embed = discord.Embed(
                description=f"{tick_emoji} | Successfully added `early` badge to {user.mention}"
            )
            await ctx.send(embed=embed)
        elif badge in ["partner"]:
            data["partner"] = True
            updateBDG(userid, data)
            embed = discord.Embed(
                description=f"{tick_emoji} | Successfully added `partner` badge to {user.mention}"
            )
            await ctx.send(embed=embed)
        elif badge in ["all"]:
            data["developer"] = True
            data["owner"] = True
            data["staff"] = True
            data["sponsors"] = True
            data["friends"] = True
            data["bug"] = True
            data["vip"] = True
            data["early"] = True
            data["partner"] = True
            updateBDG(userid, data)
            embed = discord.Embed(
                description=f"{tick_emoji} | Successfully added all badges to {user.mention}"
            )
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(
                description="<:cross:1348326385386651748> **| No badge found!**"
            )
            await ctx.send(embed=embed)
