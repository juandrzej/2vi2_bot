import os
import discord
import openpyxl
from discord.ext import commands
from dropdown import ReportView
from datetime import date

from dotenv import load_dotenv
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents)
today = date.today()
game_number = 1
game_reports = []


def excel_writer(reports):
    xname = "reports.xlsx"
    xwb = openpyxl.load_workbook(xname)
    xws = xwb.active
    last_row = xws.max_row
    xws.cell(row=last_row+2, column=1, value=reports[0])
    xws.cell(row=last_row+2, column=2, value=reports[1])
    xws.cell(row=last_row+2, column=3, value=reports[2])
    xwb.save(xname)


@bot.command()
async def report(ctx, member1: discord.Member, member2: discord.Member,
                 member3: discord.Member, member4: discord.Member):

    report_info = [[ctx.author], [member1, member2, member3, member4]]
    view = ReportView(ctx, report_info)

    await ctx.send('Please select an option:', view=view)


@bot.event
async def on_reaction_add(reaction, user):
    message = reaction.message
    if message.channel.id == 1079879823725432852:
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

            if reaction.emoji == '✅':
                if user.id == 1079843505049980930:
                    global game_number
                    game_reports[0] = game_number
                    game_number += 1
                    game_reports[1] = today
                    game_reports[2] = message.content
                    excel_writer(game_reports)

                    lines = message.content.splitlines()
                    if "Team 1" in message:
                        selected_lines = [lines[0], lines[2], lines[4], lines[7], lines[5], lines[6]]
                    else:
                        selected_lines = [lines[0], lines[2], lines[5], lines[6], lines[4], lines[7]]

                    selected_lines[2] = f'1. {selected_lines[2]}'
                    selected_lines[3] = f'1. {selected_lines[3]}'
                    selected_lines[4] = f'2. {selected_lines[4]}'
                    selected_lines[5] = f'2. {selected_lines[5]}'

                    mod_channel = bot.get_channel(413532530268962816)
                    mod_report = '\n'.join(selected_lines)
                    await mod_channel.send(mod_report)


@bot.command()
async def game_reports(ctx):
    user = ctx.author
    file = discord.File("reports.xlsx")
    await user.send(file=file)


bot.run(TOKEN)
