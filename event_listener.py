import logging
import os

import nextcord
from dotenv import load_dotenv
from nextcord.ext import commands, tasks

from messages import *

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
    system_channel = guild.system_channel

    if system_channel is not None:
        logger.info(
            f"{bot.user.name} has joined {guild.name} and has a system channel."
        )
        await system_channel.send(ON_GUILD_JOINED)
    else:
        if guild.text_channels:
            logger.info(
                f"{bot.user.name} has joined {guild.name} and does not a system channel."
            )
            await guild.text_channels[0].send(NO_SYSTEM_CHANNEL)
            await guild.text_channels[0].send(ON_GUILD_JOINED)


@bot.event
async def on_member_join(member):
    ...


# COMMANDS
@bot.slash_command()
async def test(ctx):
    await ctx.send("Testing...")


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


# REMINDERS
@tasks.loop()
async def project_reminder():
    ...


@tasks.loop()
async def member_setup_reminder():
    ...


bot.run(TOKEN)
