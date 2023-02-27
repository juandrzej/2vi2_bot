# bot.py
import os
import discord
from discord.ext import commands
from dropdown import ReportView
# from bot_excel import excel_writer
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents)


@bot.command()
async def report(ctx, member1: discord.Member, member2: discord.Member,
                 member3: discord.Member, member4: discord.Member):

    report_info = [[ctx.author], [member1, member2, member3, member4]]
    view = ReportView(report_info)

    await ctx.send('Please select an option:', view=view)


@bot.event
async def on_reaction_add(reaction, user):
    message = reaction.message
    if message.author.id == 1079843505049980930:
        players = message.mentions
        if reaction.emoji == '👍':
            if user.id in [player.id for player in players]:
                players = [player for player in players if player.id != user.id]
                if any(players):
                    await message.edit(
                        content=f"Players pending confirmation: "
                                f"{','.join([player.mention for player in players])}"
                    )
                else:
                    await message.edit(content=f"All players reacted; report has been produced.")
                    channel = message.channel
                    async for mes in channel.history(limit=1, before=message):
                        await mes.add_reaction('✅')


bot.run(TOKEN)
