import logging
import os

import nextcord
from dotenv import load_dotenv
from nextcord.ext import commands, tasks

load_dotenv("nextcord.env")

TOKEN = os.getenv("TOKEN")
TESTING_GUILD_ID = 1124338606140563629

intents = nextcord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(intents=intents)

logger = logging.getLogger("nextcord")
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename="nextcord.log", encoding="utf-8", mode="w")
handler.setFormatter(
    logging.Formatter("%(asctime)s:%(levelname)s:%(name)s: %(message)s")
)
logger.addHandler(handler)


# EVENTS
@bot.event
async def on_ready():
    logger.info(f"Logged in as {bot.user.name}#{bot.user.id}")


@bot.event
async def on_guild_join(guild):
    ...


@bot.event
async def on_member_join(member):
    ...


# COMMANDS
# Project
@bot.slash_command()
async def project_draft(ctx):
    ...


@bot.slash_command()
async def project(ctx):
    ...


@bot.slash_command()
async def project_info(ctx):
    ...


@bot.slash_command()
async def project_report(ctx):
    ...


# Members
@bot.slash_command()
async def member_register(ctx):
    ...


@bot.slash_command()
async def member_info(ctx):
    ...


# Extras
@bot.slash_command()
async def template(ctx):
    ...


@bot.slash_command()
async def help(ctx):
    ...


@bot.slash_command()
async def feedback(ctx):
    ...


# Reminders
@tasks.loop()
async def project_reminder():
    ...


@tasks.loop()
async def setup_reminder():
    ...


bot.run(TOKEN)
