import discord
import scrape
import helpers
from discord import app_commands
from discord.ext import commands

TOKEN = (helpers.get_secret()).get("DISCORD_TOKEN")

bot = commands.Bot(command_prefix="!", intents = discord.Intents.default())
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
@app_commands.describe(course_prefix = "EX: CS, ENGR, AEM, etc...", course_number = "What is the number of the course?", term = "What is the term of the course?")
async def say(interaction: discord.Interaction, course_prefix: str, course_number: str, term: str = ""):
    term = helpers.get_term(term)
    course_prefix = course_prefix.upper()
    embed_color = helpers.find_embed_color(course_prefix)
    course_info = scrape.scrape_course(course_prefix, course_number)
    if course_info is None:
        embed=discord.Embed(title=f"{course_prefix} {course_number}", url=f"https://ssb.ua.edu/pls/PROD/bwckctlg.p_disp_course_detail?cat_term_in={term}&subj_code_in={course_prefix}&crse_numb_in={course_number}", description="No course found.", color=embed_color)
    else:
        embed=discord.Embed(title=f"{course_prefix} {course_number}", url=f"https://ssb.ua.edu/pls/PROD/bwckctlg.p_disp_course_detail?cat_term_in={term}&subj_code_in={course_prefix}&crse_numb_in={course_number}", description=course_info["Description"], color=embed_color)
        embed.set_thumbnail(url="https://upload.wikimedia.org/wikipedia/commons/thumb/1/1b/Alabama_Crimson_Tide_logo.svg/2048px-Alabama_Crimson_Tide_logo.png")
        embed.add_field(name="Credit Hours", value=course_info["Credit Hours"])
        embed.add_field(name="Level", value=course_info["Levels"])
        embed.add_field(name="Type", value=course_info["Schedule Types"])
        if course_info["Prerequisites"] != None:
            embed.add_field(name="Prerequisites", value=course_info["Prerequisites"], inline=False)
    await interaction.response.send_message(embed=embed)

bot.run(TOKEN)