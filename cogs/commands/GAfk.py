import discord
from discord.ext import commands
import json
import time

afk_path = "data/gafk.json"

class BasicView(discord.ui.View):
    def __init__(self, ctx: commands.Context, timeout: int = None):
        super().__init__(timeout=timeout)
        self.ctx = ctx
      
    async def interaction_check(self, interaction: discord.Interaction):
        if interaction.user.id != self.ctx.author.id:
            await interaction.response.send_message(embed=discord.Embed(description=f"Only **{self.user}** Can Use This Command. Use {self.ctx.prefix}**{self.ctx.command}** To Run This Command", color=self.ctx.author.color), ephemeral=True)
            return False
        return True

class OnOrOff(BasicView):
    def __init__(self, ctx: commands.Context):
        super().__init__(ctx, timeout=None)
        self.value = None

    @discord.ui.button(label="Yes", emoji="<:tick:1348326381611647046>", custom_id='Yes', style=discord.ButtonStyle.green)
    async def yes_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.value = 'Yes'
        self.stop()

    @discord.ui.button(label="No", emoji="<:cross:1348326385386651748>", custom_id='No', style=discord.ButtonStyle.danger)
    async def no_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.value = 'No'
        self.stop()

class gafk(commands.Cog):
    def __init__(self, client):
        self.client = client

    async def update_data(self, afk, user):
        if str(user.id) not in afk:
            afk[str(user.id)] = {'AFK': False, 'reason': None, 'time': None, 'mentions': 0, 'dm': False}

    async def time_formatter(self, seconds: float):
        minutes, seconds = divmod(int(seconds), 60)
        hours, minutes = divmod(minutes, 60)
        days, hours = divmod(hours, 24)
        return f"{days} days, {hours} hours, {minutes} minutes, {seconds} seconds"

    @commands.Cog.listener()
    async def on_message(self, message):
        try:
            with open(afk_path, 'r') as f:
                afk = json.load(f)

            if message.mentions:
                for user_mention in message.mentions:
                    if afk.get(str(user_mention.id)) and afk[str(user_mention.id)]['AFK']:
                        if message.author.bot: 
                            return
                        reason = afk[str(user_mention.id)]['reason']
                        time_afk = afk[str(user_mention.id)]['time']
                        embed = discord.Embed(description=f'**{str(user_mention)}** is AFK since <t:{time_afk}:R> : {reason}', color=0x2b2d31)
                        await message.channel.send(embed=embed)
                        afk[str(user_mention.id)]['mentions'] += 1
                        with open(afk_path, 'w') as f:
                            json.dump(afk, f)

            if afk.get(str(message.author.id)):
                if afk[str(message.author.id)]['time'] is not None:  # Check if 'time' is not None
                    meth = int(time.time()) - afk[str(message.author.id)]['time']
                    been_afk_for = await self.time_formatter(meth)
                    mentions = afk[str(message.author.id)]['mentions']
                    embed = discord.Embed(description=f'Welcome Back {str(message.author.mention)}, You got **{mentions}** Mentions while You were AFK, I removed your AFK. You were afk for **{been_afk_for}**', color=0x2b2d31)
                    await message.channel.send(embed=embed)
                    afk[str(message.author.id)]['AFK'] = False
                    afk[str(message.author.id)]['time'] = None
                    afk[str(message.author.id)]['reason'] = None
                    afk[str(message.author.id)]['mentions'] = 0
                    with open(afk_path, 'w') as f:
                        json.dump(afk, f)

        except KeyError:
            pass

    @commands.command(description="Set AFK status")
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def gafk(self, ctx, *, reason: str = "I am AFK"):
        with open(afk_path, 'r') as f:
            afk = json.load(f)

        afk[str(ctx.author.id)] = {'AFK': True, 'reason': reason, 'time': int(time.time()), 'mentions': 0, 'dm': False}

        view = OnOrOff(ctx)
        em = discord.Embed(description="Are you sure you want to set afk Globally?\nTo Use afk only for this server use `+afk`", color=0x2b2d31)
        try:
            em.set_author(name=str(ctx.author), icon_url=ctx.author.avatar.url)
        except:
            em.set_author(name=str(ctx.author))
        msg = await ctx.reply(embed=em, view=view)
        await view.wait()

        if view.value == 'No':
            await msg.edit(content="AFK setup cancelled.")
            return
        
        afk[str(ctx.author.id)]['dm'] = (view.value == 'Yes')

        with open(afk_path, 'w') as f:
            json.dump(afk, f)

        await msg.delete()
        embed1 = discord.Embed(description=f"{ctx.author.mention} Your AFK is now set to: {reason}",color=0x2b2d31)
        await ctx.send(embed=embed1)

def setup(client): 
    client.add_cog(gafk(client))
