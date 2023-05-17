# bot.py
import os
from dotenv import load_dotenv

# 1
import discord
import scrape
from discord import app_commands
from discord.ext import commands

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix="!", intents = discord.Intents.all())
bot.remove_command('help')

@bot.event
async def on_ready():
    print("Bot is ready!")
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} command(s)")
    except Exception as e:
        print(e)

@bot.tree.command(name="course")
@app_commands.describe(course_prefix = "EX: CS, ENGR, AEM, etc...", course_number = "What is the number of the course?")
async def say(interaction: discord.Interaction, course_prefix: str, course_number: str):
    course_info = scrape.scrape_course(course_prefix, course_number)
    if course_info is None:
        embed=discord.Embed(title=f"{course_prefix} {course_number}", url=f"https://ssb.ua.edu/pls/PROD/bwckctlg.p_disp_course_detail?cat_term_in=202340&subj_code_in={course_prefix}&crse_numb_in={course_number}", description="No course found.", color=0x9e1b32)
    else:
        embed=discord.Embed(title=f"{course_prefix} {course_number}", url=f"https://ssb.ua.edu/pls/PROD/bwckctlg.p_disp_course_detail?cat_term_in=202340&subj_code_in={course_prefix}&crse_numb_in={course_number}", description=course_info["Description"], color=0x9e1b32)
        embed.set_thumbnail(url="https://upload.wikimedia.org/wikipedia/commons/thumb/1/1b/Alabama_Crimson_Tide_logo.svg/2048px-Alabama_Crimson_Tide_logo.png")
        embed.add_field(name="Credit Hours", value=course_info["Credit Hours"])
        embed.add_field(name="Level", value=course_info["Levels"])
        embed.add_field(name="Type", value=course_info["Schedule Types"])
    await interaction.response.send_message(embed=embed)

bot.run(TOKEN)