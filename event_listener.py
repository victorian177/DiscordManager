import logging
import logging.handlers
import os

import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv("discord.env")

TOKEN = os.getenv("TOKEN")


intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix="/", intents=intents)

logger = logging.getLogger("discord")
logger.setLevel(logging.DEBUG)
logging.getLogger("discord.http").setLevel(logging.INFO)

handler = logging.handlers.RotatingFileHandler(
    filename="discord.log",
    encoding="utf-8",
    maxBytes=32 * 1024 * 1024,  # 32 MiB
    backupCount=5,  # Rotate through 5 files
)
dt_fmt = "%Y-%m-%d %H:%M:%S"
formatter = logging.Formatter(
    "[{asctime}] [{levelname:<8}] {name}: {message}", dt_fmt, style="{"
)
handler.setFormatter(formatter)
logger.addHandler(handler)


# Events
@bot.event
async def on_ready():
    logger.info(f"Logged in as {bot.user} (ID: {bot.user.id}).")


@bot.event
async def on_guild_join(guild):
    logger.info(f"{guild.name}-{guild.id} has just been added.")
    # Ask for system default channel, 


@bot.event
async def on_member_join(member):
    welcome_message = f"Welcome to the {member.guild}"


# Commands
@bot.command()
async def leave(ctx):
    await ctx.send("Leaving server...")
    await ctx.guild.leave()
    logger.info("Bot has left the server.")


@bot.command()
async def set_system_channel(ctx, channel: discord.TextChannel):
    admin_role = discord.utils.get(ctx.guild.roles, name="admin")
    if admin_role in ctx.author.roles:
        await ctx.guild.edit(system_channel=channel)
        await ctx.send(f"System channel set to {channel.mention}")


bot.run(TOKEN)
