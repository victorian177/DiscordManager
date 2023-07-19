import logging
import os
from asyncio import Event

import nextcord
from dotenv import load_dotenv
from nextcord.enums import ButtonStyle
from nextcord.ext import commands, tasks
from nextcord.interactions import Interaction

from dropdown import Dropdown
from guild_database import GuildDatabase
from messages import *
from textform import TextForm

load_dotenv("nextcord.env")

TOKEN = os.getenv("TOKEN")
TESTING_GUILD_ID = os.getenv("TESTING_GUILD_ID")

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


class FormButton(nextcord.ui.Button):
    def __init__(
        self,
        style: ButtonStyle = ButtonStyle.secondary,
        label: str | None = None,
    ):
        super().__init__(style=style, label=label)

    async def callback(self, interaction: Interaction):
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

    for g in bot.guilds:
        guild_db = GuildDatabase(g.name)
        guild_db.close()


@bot.event
async def on_guild_join(guild: nextcord.Guild):
    system_channel = guild.system_channel
    guild_db = GuildDatabase(guild.name)

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

            data = {"columns": "username", "where": f"username='{member.name}'"}
            if not guild_db.op_package("Members", "select", data):
                await member.dm_channel.send(member_info_link, view=View())

            linear_workspace_link = os.getenv("LINEAR_WORKSPACE_LINK")
            await member.dm_channel.send("Linear workspace", view=linear_workspace_link)

    guild_db.close()


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


@bot.event
async def on_voice_state_update(member, before, after):
    if before.channel is None and after.channel is not None:
        # The member joined a channel
        print(f"{member.name} joined {after.channel.name}!")

    elif before.channel is not None and after.channel is None:
        # The member left a channel
        print(f"{member.name} left {before.channel.name}!")


# COMMANDS
@bot.slash_command()
async def test(interaction: nextcord.Interaction):
    guild = interaction.guild
    categories = [c for c in guild.channels if isinstance(c, nextcord.CategoryChannel)]
    print(categories)


# Project
@bot.slash_command(
    description="Creates a project. Can only be done a member with admin access."
)
async def project_create(interaction: nextcord.Interaction):
    # role = nextcord.utils.get(interaction.guild.roles, name="Role Name")

    event = Event()

    form_inputs = [
        {"label": "Project Title", "placeholder": None, "short": True},
        {"label": "Project Summary", "placeholder": None, "short": False},
        {
            "label": "Project Teams",
            "placeholder": "Enter team names separated by a comma.",
            "short": False,
        },
    ]
    project_data = TextForm(
        name="Project",
        form_inputs=form_inputs,
        response="Project channels are being created!",
    )
    await interaction.response.send_modal(project_data)

    async def on_callback(interaction):
        await project_data._callback(interaction)
        event.set()

    project_data.callback = on_callback
    await event.wait()

    guild = interaction.user.guild

    guild_db = GuildDatabase(guild.name)
    guild_db.op_package(
        "OngoingProjects",
        "insert",
        {
            "values": (
                project_data.values["Project Title"],
                project_data.values["Project Summary"],
                project_data.values["Project Teams"],
                "",
            )
        },
    )
    guild_db.close()

    category = await guild.create_category(project_data.values["Project Title"])
    team_list = ["general"]
    team_list.extend(project_data.values["Project Teams"].split(", "))
    overwrites = {
        guild.default_role: nextcord.PermissionOverwrite(read_messages=False),
        guild.me: nextcord.PermissionOverwrite(read_messages=True),
    }
    for t in team_list:
        await guild.create_text_channel(
            t,
            overwrites=overwrites,
            category=category,
        )


@bot.slash_command()
async def project_info(interaction: nextcord.Interaction):
    guild = interaction.guild

    guild_db = GuildDatabase(guild.name)
    data = {"columns": "title", "where": None}
    project_titles = guild_db.op_package("OngoingProjects", "select", data)
    options_list = [t[0] for t in project_titles]
    print(options_list)

    dd_data = {"Select a project...": options_list}
    dd = Dropdown(dd_data)
    await interaction.send(view=dd)
    await dd.event.wait()

    project_title = dd.selected[0]
    data = {"columns": None, "where": f"title='{project_title}'"}
    project_titles = guild_db.op_package("OngoingProjects", "select", data)
    disp = guild_db.op_package("OngoingProjects", "select", data)
    guild_db.close()

    await interaction.channel.send(disp)


@bot.slash_command()
async def project_close(interaction: nextcord.Interaction):
    guild = interaction.guild

    guild_db = GuildDatabase(guild.name)
    data = {"columns": "title", "where": None}
    data = {"columns": "title", "where": None}
    project_titles = guild_db.op_package("OngoingProjects", "select", data)
    options_list = [t[0] for t in project_titles]

    dd_data = {
        "Select a project...": options_list,
        "Reason for deletion": ["Cancelled", "Completed"],
    }
    dd = Dropdown(dd_data)
    await interaction.send(view=dd)
    await dd.event.wait()

    project_title, reason = dd.selected

    if reason == "Completed":
        project_data = guild_db.op_package(
            "OngoingProjects",
            "select",
            {"columns": None, "where": f"title='{project_title}'"},
        )[0]

        guild_db.op_package("CompletedProjects", "insert", {"values": project_data})

    guild_db.op_package(
        "OngoingProjects", "delete", {"where": f"title='{project_title}'"}
    )
    guild_db.close()

    for cat in guild.categories:
        category_to_del = None
        if (cat.name).lower() == (project_title).lower():
            category_to_del = cat

        if category_to_del is not None:
            for channel in category_to_del.channels:
                await channel.delete()

            await category_to_del.delete()


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

    guild = interaction.guild
    guild_db = GuildDatabase(guild.name)
    guild_db.op_package("Feedback", "insert", {"values": (fdbck.values["Feedback"])})
    guild_db.close()


# # REMINDERS
# @tasks.loop()
# async def project_reminder():
#     ...


# @tasks.loop()
# async def member_setup_reminder():
#     ...


@tasks.loop(hours=3)
async def check_guilds():
    for guild in bot.guilds:
        guild_db = GuildDatabase(guild.name)
        # Get all the categories in the guild

        categories = guild.categories
        for category in categories:
            title = category.name
            teams = []
            members = []

            print("Category:", title)
            # Get all the channels in the category
            channels = category.channels
            for channel in channels:
                # Check if the channel is a voice channel
                if isinstance(channel, nextcord.TextChannel):
                    print("Channel:", channel.name)
                    if channel.name != "general":
                        teams.append(channel.name)

                    teams.append([])
                    # Get all the members in the channel
                    members = channel.members
                    for member in members:
                        print("Member:", member.name)
                        teams[-1].append(member.name)

            teams_text = ", ".join(teams)
            per_team_members_text = [", ".join(tm) for tm in members]
            members_text = ["; ".join(team) for team in per_team_members_text]

            guild_db.op_package(
                "OngoingProjects",
                "update",
                {
                    "values": {"teams": teams_text, "members": members_text},
                    "where": f"title={title}",
                },
            )


bot.run(TOKEN)
