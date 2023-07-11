import os

import nextcord
from dotenv import load_dotenv
from nextcord.ext import commands

load_dotenv("discord.env")

TOKEN = os.getenv("TOKEN")
TESTING_GUILD_ID = 1124338606140563629

intents = nextcord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user.name}.")


class DropdownView(nextcord.ui.View):
    def __init__(self) -> None:
        super().__init__()
        self.add_item(
            nextcord.ui.Select(
                placeholder="Testing...",
                options=[
                    nextcord.SelectOption(label="Python", description="ML, Backend"),
                    nextcord.SelectOption(
                        label="Javascript", description="Frontend, Backend"
                    ),
                ],
            )
        )


@bot.command()
async def lang(ctx):
    view = DropdownView()
    await ctx.send("Choose your lang...", view=view)


bot.run(TOKEN)
