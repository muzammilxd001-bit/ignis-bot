import os
import datetime
import random
import time
import math
from core.Ignis import Ignis
import colorama
from colorama import Fore
import asyncio, json
import jishaku, cogs
from discord.ext import commands, tasks
from utils.config import OWNER_IDS, No_Prefix
from utils.init_db import init_db
import discord
from discord import app_commands
import traceback
from discord.ext.commands import Context
from discord import Spotify
from discord import Embed
import json
from pathlib import Path


intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.presences = False


os.environ["JISHAKU_NO_DM_TRACEBACK"] = "True"
os.environ["JISHAKU_HIDE"] = "True"
os.environ["JISHAKU_NO_UNDERSCORE"] = "True"
os.environ["JISHAKU_FORCE_PAGINATOR"] = "True"


tkn = os.environ.get("DISCORD_TOKEN")
if not tkn:
    raise RuntimeError("DISCORD_TOKEN environment variable is not set!")

web = os.environ.get("COMMAND_LOG_WEBHOOK", "")


client = Ignis(application_id=int(os.environ.get("APPLICATION_ID", "0")))
tree = client.tree
clr = 0x2b2d31


async def Ignis_stats():
    stat_sv_ch_id = int(os.environ.get("STATS_SERVERS_CHANNEL_ID", "0"))
    stat_us_ch_id = int(os.environ.get("STATS_USERS_CHANNEL_ID", "0"))
    while True:
        await asyncio.sleep(600)
        try:
            servers = len(client.guilds)
            users = sum(g.member_count for g in client.guilds if g.member_count is not None)
            if stat_sv_ch_id:
                sv_ch = client.get_channel(stat_sv_ch_id)
                if sv_ch:
                    await sv_ch.edit(name="Servers : {}".format(servers))
            if stat_us_ch_id:
                users_ch = client.get_channel(stat_us_ch_id)
                if users_ch:
                    await users_ch.edit(name="Users : {}".format(users))
        except Exception as e:
            print(f"Stats update error: {e}")


@client.listen("on_guild_join")
async def dexterbalak(guild):
    try:
        with open('data/roles.json', 'r') as f:
            pp = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        pp = {}
    if guild and str(guild.id) not in pp:
        pp[str(guild.id)] = {"humanautoroles": [], "botautoroles": []}
        with open('data/roles.json', 'w') as f:
            json.dump(pp, f, indent=4)


@client.listen("on_member_join")
async def autorolessacks(member):
    if member.id == client.user.id:
        return
    gd = member.guild
    try:
        with open('data/roles.json') as f:
            idk = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return
    g_ = idk.get(str(member.guild.id))
    if not g_:
        return
    human_autoroles = g_.get('humanautoroles', [])
    bot_autoroles = g_.get('botautoroles', [])
    if not member.bot and human_autoroles:
        for role in human_autoroles:
            rl = gd.get_role(int(role))
            if rl:
                try:
                    await member.add_roles(rl, reason="Ignis Autoroles")
                except discord.Forbidden:
                    pass
    if member.bot and bot_autoroles:
        for rol in bot_autoroles:
            rml = gd.get_role(int(rol))
            if rml:
                try:
                    await member.add_roles(rml, reason="Ignis Autoroles")
                except discord.Forbidden:
                    pass


@client.event
async def on_ready():
    print(Fore.RED + "Loaded & Online!")
    print(Fore.BLUE + f"Logged in as: {client.user}")
    print(Fore.MAGENTA + f"Connected to: {len(client.guilds)} guilds")
    print(Fore.YELLOW + f"Connected to: {len(client.users)} users")
    asyncio.create_task(Ignis_stats())
    try:
        synced = await client.tree.sync()
        print(f"Synced {len(synced)} slash commands globally")
    except Exception as e:
        print(f"Failed to sync commands: {e}")


@client.command(name='makeinvite', aliases=['createinvite', 'makeinv'])
async def make_invite(ctx, guild_id: int = None):
    if not guild_id:
        guild_id = ctx.guild.id
    guild = client.get_guild(guild_id)
    if not guild:
        return await ctx.send("Invalid Guild ID. Please provide a valid Guild ID.")
    try:
        invite = await guild.system_channel.create_invite(max_age=0, max_uses=0, unique=True)
        await ctx.send(f"Invite Link For {guild.name}'s Server:\n{invite.url}")
    except discord.Forbidden:
        await ctx.send(f"I don't have 'Create Instant Invite' permission in {guild.name}")


@client.event
async def on_command_completion(context: Context) -> None:
    if not web:
        return
    full_command_name = context.command.qualified_name
    split = full_command_name.split("\n")
    executed_command = str(split[0])
    if not context.message.content.startswith("."):
        pcmd = f"`.{context.message.content}`"
    else:
        pcmd = f"`{context.message.content}`"
    if context.guild is not None:
        try:
            ray = discord.SyncWebhook.from_url(web)
            embed = discord.Embed(color=0x2b2d31)
            embed.set_author(
                name=f"Executed {executed_command} Command By : {context.author}",
                icon_url=str(context.author.display_avatar.url))
            embed.set_thumbnail(url=str(context.author.display_avatar.url))
            embed.add_field(name="Command Name :", value=f"{executed_command}", inline=False)
            embed.add_field(name="Command Content :", value="{}".format(pcmd), inline=False)
            embed.add_field(
                name="Command Executed By :",
                value=f"{context.author} | ID: [{context.author.id}](https://discord.com/users/{context.author.id})",
                inline=False)
            embed.add_field(
                name="Command Executed In :",
                value=f"{context.guild.name} | ID: [{context.guild.id}](https://discord.com/users/{context.author.id})",
                inline=False)
            embed.add_field(
                name="Command Executed In Channel :",
                value=f"{context.channel.name} | ID: [{context.channel.id}](https://discord.com/channel/{context.channel.id})",
                inline=False)
            embed.set_footer(text=f"Thank you for choosing {client.user.name}",
                             icon_url=client.user.display_avatar.url)
            ray.send(embed=embed)
        except Exception:
            pass
    else:
        try:
            ray = discord.SyncWebhook.from_url(web)
            embed1 = discord.Embed(color=0x2b2d31)
            embed1.set_author(
                name=f"Executed {executed_command} Command By : {context.author}",
                icon_url=str(context.author.display_avatar.url))
            embed1.set_thumbnail(url=str(context.author.display_avatar.url))
            embed1.add_field(name="Command Name :", value=f"{executed_command}", inline=False)
            embed1.add_field(
                name="Command Executed By :",
                value=f"{context.author} | ID: [{context.author.id}](https://discord.com/users/{context.author.id})",
                inline=False)
            embed1.set_footer(text=f"Thank you for choosing {client.user.name}",
                              icon_url=client.user.display_avatar.url)
            ray.send(embed=embed1)
        except Exception:
            pass


@client.command(aliases=['wh'])
@commands.has_permissions(administrator=True)
async def create_hook(ctx, name=None):
    if not name:
        await ctx.send("Please specify a name for the webhook.")
        return
    webhook = await ctx.channel.create_webhook(name=name)
    embed = discord.Embed(
        title=f"**<:cross:1348326385386651748> | Webhook __{webhook.name}__ created successfully **",
        color=0x2b2d31)
    try:
        await ctx.author.send(f"||{webhook.url}||")
        await ctx.author.send(embed=embed)
        await ctx.send(
            f"**<:cross:1348326385386651748>| Webhook :- __{webhook.name}__ created successfully.**\n** Check your DMs for the URL.\n {ctx.author.mention} **"
        )
    except discord.Forbidden:
        await ctx.send(
            f"**<:cross:1348326385386651748>|Webhook:- __{webhook.name}__ ||{webhook.url}|| (Unable to DM user) ** \n {ctx.author.mention}"
        )


@client.command()
@commands.has_permissions(administrator=True)
async def delete_hook(ctx, webhook_url: str):
    try:
        async with discord.AsyncWebhookAdapter(None):
            pass
        webhook = discord.SyncWebhook.from_url(webhook_url)
        webhook.delete()
        await ctx.send("Webhook deleted successfully.")
    except discord.NotFound:
        await ctx.send("Webhook not found.")
    except Exception as e:
        await ctx.send(f"Error deleting webhook: {e}")


@client.command(aliases=['all_hooks'])
async def list_hooks(ctx):
    webhooks = await ctx.channel.webhooks()
    if not webhooks:
        await ctx.send("No webhooks found in this channel.")
        return
    embed = discord.Embed(title="List of Webhooks", color=0x2b2d31)
    for webhook in webhooks:
        embed.add_field(name="__Name__", value=f"**<:cross:1348326385386651748> | {webhook.name} **")
        embed.add_field(name="__ID__", value=webhook.id)
        embed.add_field(name="\u200b", value="\u200b")
    await ctx.send(f"{ctx.author.mention}, Here are the webhooks in this channel", embed=embed)


@client.command(name='spotify', aliases=[])
async def spotify_cmd(ctx, user: discord.Member = None):
    if user is None:
        user = ctx.author
    if user.activities:
        for activity in user.activities:
            if isinstance(activity, Spotify):
                nemo = discord.Embed(
                    title=f"{user.name}'s Spotify",
                    description="Listening to {}".format(activity.title),
                    color=0x2b2d31)
                nemo.set_thumbnail(url=activity.album_cover_url)
                nemo.add_field(name="Artist", value=activity.artist)
                nemo.add_field(name="Album", value=activity.album)
                nemo.set_footer(text="Song started at {}".format(
                    activity.created_at.strftime("%H:%M")))
                await ctx.send(embed=nemo)
                return
        await ctx.send(f"{user.mention} is not listening to Spotify right now.")
    else:
        await ctx.send(f"{user.mention} has no active activities.")


@client.event
async def on_guild_join(guild):
    log_channel_id_str = os.environ.get("GUILD_JOIN_LOG_CHANNEL_ID", "")
    if log_channel_id_str:
        try:
            channel = client.get_channel(int(log_channel_id_str))
            if channel:
                await channel.send(f"Ignis has been added to the server: {guild.name}")
        except Exception:
            pass


@client.event
async def on_message(message):
    if message.author.bot:
        return
    await client.process_commands(message)


bot = client


@bot.command()
async def reaction(ctx):
    emoji = ["🍪", "🎉", "🧋", "🍒", "🍑", "💸", "🌙", "💕"]
    random_emoji = random.choice(emoji)
    random.shuffle(emoji)
    embed = discord.Embed(
        title="Reaction time",
        description="After 1-15 seconds I will reveal the emoji.",
        color=0x2b2d31)
    first = await ctx.send(embed=embed)
    for react in emoji:
        await first.add_reaction(react)
    await asyncio.sleep(2.5)
    embed.description = "Get ready!"
    await first.edit(embed=embed)
    await asyncio.sleep(random.randint(1, 15))
    embed.description = f"GET THE {random_emoji} EMOJI!"
    await first.edit(embed=embed)

    def check(reaction, user):
        return reaction.message.id == first.id and str(reaction.emoji) == random_emoji and user != bot.user

    try:
        start_time = time.time()
        reaction, user = await bot.wait_for("reaction_add", check=check, timeout=15)
        end_time = time.time()
        reaction_time = end_time - start_time
    except asyncio.TimeoutError:
        embed.description = "Timeout"
        await first.edit(embed=embed)
    else:
        total_second = f"**{reaction_time * 1000:.2f}ms**"
        if reaction_time > 1:
            total_second = f"**{reaction_time:.2f}s**"
        embed.description = f"{user.mention} got the {random_emoji} in {total_second}"
        await first.edit(embed=embed)


async def main():
    async with client:
        os.system("clear")
        init_db()
        await client.load_extension("cogs")
        await client.load_extension("jishaku")

        max_retries = 5
        for attempt in range(max_retries):
            try:
                await client.start(tkn)
                break
            except discord.HTTPException as e:
                if e.status == 429:
                    wait_time = min((2 ** attempt) + random.random(), 60)
                    print(f"Rate limited. Waiting {wait_time:.2f} seconds...")
                    await asyncio.sleep(wait_time)
                else:
                    raise
        else:
            raise Exception("Max retries exceeded")


if __name__ == "__main__":
    asyncio.run(main())
