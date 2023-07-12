import logging
import os

import nextcord
from dotenv import load_dotenv
from nextcord.ext import commands, tasks

from dropdown import Dropdown
from messages import *
from textform import TextForm

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
async def on_guild_join(guild: nextcord.Guild):
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

    for member in guild.members:
        print(f"Member: {member.name}")
        if member.dm_channel is None and member.name != bot.user.name:
            channel = await member.create_dm()
            dm_message = ON_MEMBER_JOINED_PRIVATE_MESSAGE.format(bot.user.name)
            await channel.send(dm_message)

    # TODO: Create Guild entity for managing guild specific databases


@bot.event
async def on_member_join(member: nextcord.Member):
    guild = member.guild
    system_channel = guild.system_channel
    if system_channel is not None:
        await system_channel.send(ON_MEMBER_JOINED_GENERAL_MESSAGE)

    channel = await member.create_dm()
    dm_message = ON_MEMBER_JOINED_PRIVATE_MESSAGE.format(bot.user.name)
    await channel.send(dm_message)

    # TODO: Unhighlight the code below when member registration form is complete
    # member_info_link = os.getenv("MEMBER_INFO_LINK")
    # await channel.send(member_info_link)


# COMMANDS
@bot.slash_command()
async def test(ctx):
    ...


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
