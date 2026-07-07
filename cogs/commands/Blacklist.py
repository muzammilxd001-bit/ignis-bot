import discord
from discord.ext import commands
import json
import os

# Load or initialize data/blacklist.json
def read_blacklist():
    if os.path.exists('data/blacklist.json'):
        with open('data/blacklist.json', 'r') as f:
            try:
                data = json.load(f)
                return data.get('ids', [])
            except json.JSONDecodeError:
                return []
    return []

def write_blacklist(blacklist):
    with open('data/blacklist.json', 'w') as f:
        json.dump({'ids': blacklist}, f, indent=4)

class Blacklist(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.blacklist = read_blacklist()

    @commands.command(name='addblacklist')
    @commands.has_permissions(administrator=True)
    async def add_blacklist(self, ctx, member: discord.Member):
        if member.id in self.blacklist:
            await ctx.send(f'{member.mention} is already in the blacklist.')
            return

        self.blacklist.append(str(member.id))  # Ensure ID is a string
        write_blacklist(self.blacklist)
        await ctx.send(f'{member.mention} has been added to the blacklist.')

    @commands.command(name='removeblacklist')
    @commands.has_permissions(administrator=True)
    async def remove_blacklist(self, ctx, member: discord.Member):
        if str(member.id) not in self.blacklist:
            await ctx.send(f'{member.mention} is not in the blacklist.')
            return

        self.blacklist.remove(str(member.id))  # Ensure ID is a string
        write_blacklist(self.blacklist)
        await ctx.send(f'{member.mention} has been removed from the blacklist.')

    @commands.command(name='checkblacklist')
    @commands.has_permissions(administrator=True)
    async def check_blacklist(self, ctx):
        if not self.blacklist:
            await ctx.send('The blacklist is empty.')
            return

        embed = discord.Embed(title="Blacklist", description="List of blacklisted members", color=0xFF0000)
        for idx, user_id in enumerate(self.blacklist, start=1):
            user = self.bot.get_user(int(user_id))
            if user:
                embed.add_field(name=f"#{idx} {user.name}", value=f"ID: {user_id}", inline=False)
            else:
                embed.add_field(name=f"#{idx} Unknown User", value=f"ID: {user_id}", inline=False)

        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Blacklist(bot))
