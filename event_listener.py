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

    system_channel = guild.system_channel
    if system_channel is None:
        logger.debug(f"{guild.name} doesn't have a system channel.")

    else:
        await system_channel.send(
            f"""
Welcome! **{bot.user}** is here to help you and your organisation stay organised on projects and collaborate more efficiently.
- Your system's channel is set to **{system_channel.name}**.
- Type __/setup__ to complete setup process. This only works if user is an admin.
- Type __/help__ to see full documentation of commands and usage patterns.
- Type __/feedback__ followed by feedback content to make suggestions on improvements or changes to the Discord bot service.
        """
        )

    # TODO: Send welcome message
    # TODO: Create appropriate databases and bot setup checklist
    # TODO: List the permissions that the bot has and what commands can trigger help
    # TODO: Get list of guild channels and set system channel if none exists
    # TODO: Get list of roles and which roles have admin capabilities
    # TODO: Mention that feedback can be sent to users


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
async def guild_welcome(ctx):
    system_channel = ctx.guild.system_channel
    if system_channel is None:
        await ctx.send(
            f"""
{ctx.guild.name} doesn't have a system channel.
Admin should set a channel as system channel.
            """
        )
        logger.debug(f"{ctx.guild.name} doesn't have a system channel.")

    else:
        await system_channel.send(
            f"""
Welcome! **{bot.user}** is here to help you and your organisation stay organised on projects and collaborate more efficiently.
- Your system's channel is set to **{system_channel.name}**.
- Type __/setup__ to complete setup process. This only works if user is an admin.
- Type __/help__ to see full documentation of commands and usage patterns.
- Type __/feedback__ followed by feedback content to make suggestions on improvements or changes to the Discord bot service.
        """
        )


@bot.command()
async def set_system_channel(ctx, channel: discord.TextChannel):
    admin_role = discord.utils.get(ctx.guild.roles, name="admin")
    if admin_role in ctx.author.roles:
        await ctx.guild.edit(system_channel=channel)
        await ctx.send(f"System channel set to {channel.mention}")


bot.run(TOKEN)
