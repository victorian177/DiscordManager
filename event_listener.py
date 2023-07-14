import logging
import os
from asyncio import Event

import nextcord
from dotenv import load_dotenv
from nextcord.enums import ButtonStyle
from nextcord.ext import commands, tasks
from nextcord.interactions import Interaction
from tinydb import Query

from dropdown import Dropdown
from guild_databases import GuildDatabases
from messages import *
from textform import TextForm

load_dotenv("nextcord.env")

TOKEN = os.getenv("TOKEN")
TESTING_GUILD_ID = os.getenv("TESTING_GUILD_ID")
GUILD = os.getenv("GUILD")

intents = nextcord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(intents=intents)

guild_db = GuildDatabases(GUILD)

logger = logging.getLogger("nextcord")
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename="nextcord.log", encoding="utf-8", mode="w")
handler.setFormatter(
    logging.Formatter("%(asctime)s:%(levelname)s:%(name)s: %(message)s")
)
logger.addHandler(handler)


class FormButton(nextcord.ui.Button):
    def __init__(
        self,
        style: ButtonStyle = ButtonStyle.secondary,
        label: str | None = None,
    ):
        super().__init__(style=style, label=label)

    async def callback(self, interaction: Interaction):
        # Here the get_response function gets called

        return await super().callback(interaction)


class View(nextcord.ui.View):
    def __init__(self) -> None:
        super().__init__(timeout=5 * 60)
        self.add_item(FormButton(label="Confirm form completion"))


# EVENTS
@bot.event
async def on_ready():
    logger.info(f"Logged in as {bot.user.name}#{bot.user.id}")
    print("Running...")

    # TODO: When multiple guilds eventually get added.
    # for g in bot.guilds:
    #     _ = GuildDatabases(g.name)


@bot.event
async def on_guild_join(guild: nextcord.Guild):
    if guild.name == GUILD:
        pending_members = []
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

        member_info_link = os.getenv("MEMBER_INFO_LINK")

        role_names = ["Admin", "Member"]
        for role_name in role_names:
            role = nextcord.utils.get(guild.roles, name=role_name)
            if not role:
                await guild.create_role(name=role_name)

        for member in guild.members:
            if member.name != bot.user.name:
                if member.dm_channel is None:
                    channel = await member.create_dm()
                    dm_message = ON_MEMBER_JOINED_PRIVATE_MESSAGE.format(bot.user.name)
                    await channel.send(dm_message)

                data = Query().name == member.name
                if not guild_db.op_package(guild.name, "retrieve", data):
                    pending_members.append(member.name)
                    await member.dm_channel.send(member_info_link, view=View())

                linear_workspace_link = os.getenv("LINEAR_WORKSPACE_LINK")
                await member.dm_channel.send(
                    "Linear workspace", view=linear_workspace_link
                )


@bot.event
async def on_member_join(member: nextcord.Member):
    guild = member.guild
    system_channel = guild.system_channel
    if system_channel is not None:
        await system_channel.send(ON_MEMBER_JOINED_GENERAL_MESSAGE)

    channel = await member.create_dm()
    dm_message = ON_MEMBER_JOINED_PRIVATE_MESSAGE.format(bot.user.name)
    await channel.send(dm_message)

    member_info_link = os.getenv("MEMBER_INFO_LINK")
    await channel.send(member_info_link, view=View())

    linear_workspace_link = os.getenv("LINEAR_WORKSPACE_LINK")
    await channel.send(linear_workspace_link)


# COMMANDS
# @bot.slash_command()
# async def test(interaction: nextcord.Interaction):
#     dd = Dropdown("Hello, world!", options_list=["Python", "Java"], event=Event())
#     await interaction.send(view=dd)
#     await dd.event.wait()
#     print(dd.selected)


# Project
@bot.slash_command(
    description="Record your project idea. It would get reviewed and it could get implemented."
)
async def project_draft(interaction: nextcord.Interaction):
    event = Event()

    form_inputs = [
        {"label": "Project Title", "placeholder": None, "short": True},
        {"label": "Project Draft", "placeholder": None, "short": False},
        {"label": "Teams", "placeholder": "Enter project team names.", "short": False},
    ]
    draft = TextForm(
        name="Project Draft",
        form_inputs=form_inputs,
        response="Your project draft has been uploaded!",
    )
    await interaction.response.send_modal(draft)

    async def on_callback(interaction):
        await draft._callback(interaction)
        event.set()

    draft.callback = on_callback
    await event.wait()

    data = {}
    data["username"] = interaction.user.name
    data["title"] = draft.values["Project Title"]
    data["draft"] = draft.values["Project Draft"]
    data["teams"] = draft.values["Teams"]
    guild_db.op_package("project_drafts", "create", data)


@bot.slash_command(
    description="Creates a project. Can only be done a member with admin access."
)
async def project(interaction: nextcord.Interaction):
    # role = nextcord.utils.get(interaction.guild.roles, name="Role Name")

    data = {}
    data["query"] = None
    data["retrieve_info"] = ["title"]
    data["unique"] = False
    retrieve_data = guild_db.op_package("project_drafts", "retrieve", data)
    options = [v["title"] for v in retrieve_data]
    options.append("Create new project...")
    drafts_dropdown = Dropdown(
        placeholder="Select from drafts...",
        options_list=options,
    )
    await interaction.send(view=drafts_dropdown)
    await drafts_dropdown.event.wait()

    data = {}
    data["query"] = Query().title == drafts_dropdown.selected
    data["retrieve_info"] = []
    data["unique"] = True
    project_data = guild_db.op_package("project_drafts", "retrieve", data)[0]

    guild = interaction.user.guild
    category = await guild.create_category(project_data["title"])
    team_list = ["general"]
    team_list.extend(project_data["teams"].split())
    overwrites = {
        guild.default_role: nextcord.PermissionOverwrite(read_messages=False),
        guild.me: nextcord.PermissionOverwrite(read_messages=True),
    }
    for t in team_list:
        await guild.create_text_channel(
            t,
            overwrites=overwrites,
            category=category,
            reason=f"{t} for {project_data['title']}",
        )


# @bot.slash_command()
# async def create_proj_channels(interaction: nextcord.Interaction):
#     data = {"title": "test", "teams": "frontend, backend"}
#     guild = interaction.user.guild
#     category = await guild.create_category(data["title"])
#     team_list = ["general"]
#     team_list.extend(data["teams"].split())
#     overwrites = {
#         guild.default_role: nextcord.PermissionOverwrite(read_messages=False),
#         guild.me: nextcord.PermissionOverwrite(read_messages=True),
#     }
#     for t in team_list:
#         await guild.create_text_channel(
#             t,
#             overwrites=overwrites,
#             category=category,
#             reason=f"{t} for {data['title']}",
#         )


# @bot.slash_command()
# async def project_info(ctx):
#     ...


# Members
@bot.slash_command(description="Resends member registration link to user.")
async def member_register(ctx):
    member_info_link = os.getenv("MEMBER_INFO_LINK")
    await ctx.send(member_info_link, view=View())


# @bot.slash_command()
# async def member_info(ctx):
#     ...


# # Extras
# @bot.slash_command()
# async def template(ctx):
#     ...


# @bot.slash_command()
# async def help(ctx):
#     ...


@bot.slash_command(
    description="Record any improvements you wil like to be seen in upcoming versions."
)
async def feedback(interaction: nextcord.Interaction):
    event = Event()

    form_inputs = [{"label": "Feedback", "placeholder": None, "short": False}]
    fdbck = TextForm(
        name="Feedback",
        form_inputs=form_inputs,
        response="Your feedback has been taken!",
    )

    await interaction.response.send_modal(fdbck)

    async def on_callback(interaction):
        await fdbck._callback(interaction)
        event.set()

    fdbck.callback = on_callback
    await event.wait()

    data = {}
    data["username"] = interaction.user.name
    data["feedback"] = fdbck.values["Feedback"]
    guild_db.op_package("feedback", "create", data)


# # REMINDERS
# @tasks.loop()
# async def project_reminder():
#     ...


# @tasks.loop()
# async def member_setup_reminder():
#     ...


bot.run(TOKEN)
