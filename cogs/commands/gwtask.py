import discord
import asyncio
from discord.ext import commands, tasks
import datetime
import time 
import json
import random
import os 
from discord.ui import View, Button

class gwtask(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.color = 0x2b2d31
        self.giveaway_task.start()

    def cog_unload(self):
        self.giveaway_task.cancel()

    @tasks.loop(seconds=5)
    async def giveaway_task(self):
        await self.bot.wait_until_ready()
        with open("data/giveaways.json", "r") as f:
            giveaways = json.load(f)

        if len(giveaways) == 0:
            return

        current_time = int(time.time())
        
        for giveaway_id, data in giveaways.items():
            if current_time > data["end_time"] and not data["ended"]:
                
                # Channel check
                channel = self.bot.get_channel(data["channel_id"])
                if channel is None:
                    print(f"Giveaway channel not found for ID: {giveaway_id}")
                    giveaways[giveaway_id]["ended"] = True
                    with open("data/giveaways.json", "w") as f:
                        json.dump(giveaways, f, indent=4)
                    continue 
                
                # Message check
                try:
                    giveaway_message = await channel.fetch_message(int(giveaway_id))
                except discord.NotFound:
                    print(f"Giveaway message not found for ID: {giveaway_id}")
                    giveaways[giveaway_id]["ended"] = True
                    with open("data/giveaways.json", "w") as f:
                        json.dump(giveaways, f, indent=4)
                    continue

                # Get participants
                reaction = discord.utils.get(giveaway_message.reactions, emoji="🎉")
                participants = [user.id async for user in reaction.users() if not user.bot]
                giveaways[giveaway_id]["participants"] = participants
                giveaways[giveaway_id]["entries"] = len(participants)

                # No participants case
                if len(participants) == 0:
                    no_winner_embed = discord.Embed(
                        title=f"<a:Gift:1514218947786838066> {data['prize']} <a:Gift:1514218947786838066>",
                        color=0x00b0f4,
                        description=(
                            f"<a:blackdot:1514219180600328293> Hosted by: <@{data['host']}>\n"
                            f"<a:blackdot:1514219180600328293> Total participant(s) : 0\n\n"
                            f"<a:blackdot:1514219180600328293> **Winner :**\n"
                            f"No one participated!"
                        )
                    )
                    no_winner_embed.set_footer(text="Ended")
                    no_winner_embed.timestamp = discord.utils.utcnow()
                    await giveaway_message.edit(
                        content="<a:Gift:1514218947786838066> **Giveaway Ended** <a:Gift:1514218947786838066>",
                        embed=no_winner_embed,
                        view=None
                    )
                    giveaways[giveaway_id]["ended"] = True
                    with open("data/giveaways.json", "w") as f:
                        json.dump(giveaways, f, indent=4)
                    continue

                # Validate winner count
                winner_count = min(data["winners"], len(participants))
                if winner_count <= 0:
                    winner_count = 1

                # Select winners
                winners = random.sample(participants, winner_count)
                winner_mentions = '\n'.join([f'<@{winner}>' for winner in winners])

                # Build ended embed matching Falcon style
                ended_embed = discord.Embed(
                    title=f"<a:Gift:1514218947786838066> {data['prize']} <a:Gift:1514218947786838066>",
                    color=0x00b0f4,
                    description=(
                        f"<a:blackdot:1514219180600328293> Hosted by: <@{data['host']}>\n"
                        f"<a:blackdot:1514219180600328293> Total participant(s) : {len(participants)}\n\n"
                        f"<a:blackdot:1514219180600328293> **Winner :**\n"
                        f"{winner_mentions}"
                    )
                )
                ended_embed.set_footer(text="Ended")
                ended_embed.timestamp = discord.utils.utcnow()

                await giveaway_message.edit(
                    content="<a:Gift:1514218947786838066> **Giveaway Ended** <a:Gift:1514218947786838066>",
                    embed=ended_embed,
                    view=None
                )

                # Send congratulations message
                await channel.send(
                    f"🎉 Congratulations {winner_mentions}!\n"
                    f"You won **{data['prize']}**, hosted by <@{data['host']}>!"
                )

                giveaways[giveaway_id]["ended"] = True

                with open("data/giveaways.json", "w") as f:
                    json.dump(giveaways, f, indent=4)