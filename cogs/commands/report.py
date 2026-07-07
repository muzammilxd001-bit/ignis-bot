import discord
from discord.ext import commands
from discord.ui import View, Button
from discord import Embed, ButtonStyle

class report1(View):
    def __init__(self, bot, user_id: int, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.bot = bot
        self.user_id = user_id

    @discord.ui.button(label='Accept', style=ButtonStyle.success)
    async def accept_report(self, button: Button, interaction: discord.Interaction):
        # Logic to handle accepted report
        user = await self.bot.fetch_user(self.user_id)
        await user.send('Your report has been accepted.')

    @discord.ui.button(label='Decline', style=ButtonStyle.danger)
    async def decline_report(self, button: Button, interaction: discord.Interaction):
        # Logic to handle declined report
        user = await self.bot.fetch_user(self.user_id)
        await user.send('Your report has been declined.')

class report(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(name="report", aliases=["bug"], usage='Report <bug>', 
        description='Report a bug or issue with the bot.', help='Report a bug or issue with the bot.', 
        with_app_command=True)
    @commands.cooldown(1, 60, commands.BucketType.channel)
    async def report_command(self, ctx, *, bug: str):
        button1 = Button(label="Invite", url = "https://discord.com/api/oauth2/authorize?client_id=1355539303475712032&permissions=4398046511103&scope=applications.commands+bot")
        button2 = Button(label="Support", url = "https://discord.gg/nakhre")
        report_view = report1(self.bot, user_id=ctx.author.id)  # Pass the bot instance here

        embed = Embed(
            title='Bug Reported',
            description=bug,
            color=0x2b2d31
        )
        embed.add_field(name='Reported By', value=f'{ctx.author}', inline=True)
        embed.add_field(name="Reported ID", value=ctx.author.id, inline=True)
        embed.add_field(name="Server", value=ctx.guild.name, inline=True)
        embed.add_field(name="Channel", value=ctx.channel.name, inline=True)

        report_channel = self.bot.get_channel(1356216441363234976)
        await report_channel.send(embed=embed, view=report_view)

        confirm_embed = Embed(
            description="Thank you for reporting the bug. We will look into it shortly.",
            color=0x2b2d31
        )
        view = View()
        view.add_item(button1)
        #view.add_item(button)
        view.add_item(button2)
        await ctx.send(embed=confirm_embed, view=view)

def setup(bot):
    bot.add_cog(report(bot))