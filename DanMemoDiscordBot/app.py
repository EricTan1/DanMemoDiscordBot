import os
import traceback
from datetime import datetime

from interactions import (
    Attachment,
    AutoDefer,
    Client,
    IntervalTrigger,
    Message,
    OptionType,
    SlashCommandChoice,
    SlashContext,
    Task,
    listen,
    slash_command,
    slash_option,
)
from interactions.api.events import Startup

import commands.addUpdateUnit as command_addUpdateUnit
import commands.bento as command_bento
import commands.dispatch as command_dispatch
import commands.elementAssists as command_elementAssists
import commands.gacha as command_gacha
import commands.gachaMode as command_gachaMode
import commands.getJson as command_getJson
import commands.help as command_help
import commands.init as command_init
import commands.invite as command_invite
import commands.killer as command_killer
import commands.popularity as command_popularity
import commands.profile as command_profile
import commands.rb as command_rb
import commands.recordbuster.recordBusterCalc as command_rbCalc
import commands.saCalculator as command_saCalculator
import commands.support as command_support
import commands.topUsers as command_topUsers
import commands.unitsearch.commonSearch as command_commonSearch
from commands.cache import Cache
from commands.utils import createGSpreadJSON
from database.DBcontroller import DatabaseEnvironment, DBConfig

GUILD_ID = 698143969166622720  # ID of Sword Oratoria server
STATUS_CHANNEL_ID = 1131919933660475433  # ID of Sword Oratoria's bot-status channel
TOKEN = os.environ["DISCORD_TOKEN_DANMEMO"]
ENV = os.environ.get("ENV")
HEARTRATE = 300  # Heartbeat interval in seconds

if ENV == "dev":
    dbConfig = DBConfig(DatabaseEnvironment.LOCAL)
else:
    dbConfig = DBConfig(DatabaseEnvironment.HEROKU)

# Discord times out a command after 3s if it wasn't answered.
# Auto defer should prevent this, but may lead to breakages for times > 0.0
client = Client(token=TOKEN, auto_defer=AutoDefer(enabled=True, time_until_defer=0.0))

cache = Cache(dbConfig)

status_message: Message | None = None


# Updates heartbeat file and bot status message on Discord
@Task.create(IntervalTrigger(seconds=HEARTRATE))
async def status_update():
    boot_text = status_message.content.split("\n")[0]
    timestamp = int(datetime.now().timestamp())
    await status_message.edit(
        content=boot_text + f"\nLast heartbeat: <t:{timestamp}:R>"
    )
    with open("heartbeat-file.txt", "w") as f:
        f.write(str(timestamp))


@listen(Startup)
async def on_start(_: Startup):
    """() -> None
    This function initializes the bot.
    """
    print("test")
    createGSpreadJSON()
    print("Bot is ready!")

    # Create initial status message in bot-status channel
    channel = client.get_channel(STATUS_CHANNEL_ID)
    global status_message
    timestamp = int(datetime.now().timestamp())
    status_message = await channel.send(
        f"Bot going online at <t:{timestamp}:F>\nLast heartbeat: <t:{timestamp}:R>"
    )
    # Starts the scheduler for the status_update task
    status_update.start()


@slash_command(
    name="sa-calculator",
    description="SA gauge Calculator",
)
@slash_option(
    name="config",
    description="Config file for the calculator. If you do not provide one, the template will be offered for download",
    opt_type=OptionType.ATTACHMENT,
    required=False,
)
async def sacalc(ctx: SlashContext, config: Attachment | None = None):
    await command_saCalculator.run(ctx, config)


@slash_command(
    name="recordbuster-calculator",
    description="Record Buster Score Calculator",
)
@slash_option(
    name="config",
    description="Config file for the calculator. If you do not provide one, the template will be offered for download",
    opt_type=OptionType.ATTACHMENT,
    required=False,
)
async def rbcalc(ctx: SlashContext, config: Attachment | None = None):
    try:
        await command_rbCalc.run(client, ctx, config)
    except:
        tb = traceback.format_exc()
        await ctx.send(f"ERROR:\n```{tb}```")


@slash_command(
    name="character-search",
    description="Search DanMemo units by name and title",
)
@slash_option(
    name="keywords",
    description="Keywords to look for",
    opt_type=OptionType.STRING,
    required=True,
)
async def characterSearch(ctx: SlashContext, keywords: str):
    await command_commonSearch.run(
        dbConfig, client, ctx, keywords, is_character_search=True
    )


@slash_command(
    name="skill-search",
    description="Search DanMemo units by skills",
)
@slash_option(
    name="keywords",
    description="Keywords to look for",
    opt_type=OptionType.STRING,
    required=True,
)
async def skillSearch(ctx: SlashContext, keywords: str):
    await command_commonSearch.run(
        dbConfig, client, ctx, keywords, is_character_search=False
    )


@slash_command(
    name="help",
    description="Instructions on using the bot",
)
async def help(ctx: SlashContext):
    await command_help.run(ctx)


@slash_command(
    name="invite",
    description="Prints the server invite link for the bot",
)
async def invite(ctx: SlashContext):
    await command_invite.run(ctx)


@slash_command(
    name="support",
    description="Sends a link to our support server. Please contact Eric#5731 or Yon#7436",
)
async def support(ctx: SlashContext):
    await command_support.run(ctx)


@slash_command(
    name="popularity",
    description="Displays current Ais bot popularity",
)
async def popularity(ctx: SlashContext):
    await command_popularity.run(client, ctx)


@slash_command(
    name="bento",
    description="Syr's lunch box! Get crepes every two hours that can be traded for gacha rolls!",
)
async def bento(ctx: SlashContext):
    await command_bento.run(dbConfig, ctx)


@slash_command(
    name="gacha",
    description="Trade a crepe for an 11-draw gacha pull. In-game gacha rates. Limited and JP-only units are included",
)
async def gacha(ctx: SlashContext):
    await command_gacha.run(dbConfig, ctx)


@slash_command(
    name="gacha-mode",
    description="Changes the way your gacha pulls are shown",
)
@slash_option(
    name="sub_command",
    description="Setting whether to send your pull results as image or gif",
    opt_type=OptionType.STRING,
    required=True,
    choices=[
        SlashCommandChoice("image", "image"),
        SlashCommandChoice("gif", "gif"),
    ],
)
async def gachamode(ctx: SlashContext, sub_command: str):
    await command_gachaMode.run(dbConfig, ctx, sub_command)


@slash_command(
    name="profile",
    description="Your personal stats and inventory",
)
@slash_option(
    name="sub_command",
    description="Whether you want a detailed list or short summary of your inventory",
    opt_type=OptionType.STRING,
    required=True,
    choices=[
        SlashCommandChoice("detailed", "detailed"),
        SlashCommandChoice("summary", "summary"),
    ],
)
async def profile(ctx: SlashContext, sub_command: str):
    await command_profile.run(dbConfig, client, ctx, sub_command)


@slash_command(
    name="top-whales",
    description="Shows top players by total score of owned gacha units, all servers combined",
)
async def topWhales(ctx: SlashContext):
    await command_topUsers.run(dbConfig, client, ctx, "whales")


@slash_command(
    name="top-gourmets",
    description="Shows top players by crepes owned, all servers combined",
)
async def topGourmets(ctx: SlashContext):
    await command_topUsers.run(dbConfig, client, ctx, "gourmets")


@slash_command(
    name="dispatch",
    description="Displays all the special board dispatch quests related to the search",
)
@slash_option(
    name="keywords",
    description="Keywords to look for",
    opt_type=OptionType.STRING,
    required=True,
)
async def dispatch(ctx: SlashContext, keywords: str):
    await command_dispatch.run(dbConfig, ctx, keywords)


@slash_command(
    name="add-update-unit",
    description="Adds a unit or overwrites an existing one",
    scopes=[GUILD_ID],  # so the command is only visible & available on the dev server
)
@slash_option(
    name="unit_file",
    description="File containing the unit data in JSON format",
    opt_type=OptionType.ATTACHMENT,
    required=True,
)
async def addUpdateUnit(ctx: SlashContext, unit_file: Attachment):
    await command_addUpdateUnit.run(dbConfig, ctx, unit_file)
    # refresh the cache
    cache = Cache(dbConfig)
    cache.refreshcache(dbConfig)


@slash_command(
    name="get-json",
    description="Get the unit database in JSON format",
    scopes=[GUILD_ID],  # so the command is only visible & available on the dev server
)
async def getJson(ctx: SlashContext):
    await command_getJson.run(ctx)


@slash_command(
    name="init",
    description="No idea what this does tbh",
    scopes=[GUILD_ID],  # so the command is only visible & available on the dev server
)
async def init(ctx: SlashContext):
    await command_init.run(ctx)


# commands that just bring up pictures
killer_subcommands = [
    SlashCommandChoice(killer_type, killer_type)
    for killer_type in [
        "all",
        "aqua",
        "dragon",
        "giant",
        "material",
        "ox",
        "spirit",
        "beast",
        "fantasma",
        "insect",
        "ogre",
        "plant",
        "worm",
    ]
]


@slash_command(
    name="killers",
    description="Posts infographic of all killer units in the game.",
)
@slash_option(
    name="sub_command",
    description="The monster type to filter for.",
    opt_type=OptionType.STRING,
    required=True,
    choices=killer_subcommands,
)
async def killer(ctx, sub_command: str):
    await command_killer.run(ctx, dbConfig, sub_command)


@slash_command(
    name="elemental-assists",
    description="Posts an infographic of all elemental damage buffing/elemental resist debuffing assists in the game",
)
async def elementAssists(ctx: SlashContext):
    await command_elementAssists.run(ctx, dbConfig)


@slash_command(
    name="recordbuster",
    description="Posts a guide for the given RB character",
)
@slash_option(
    name="sub_command",
    description="The RB boss to show a guide for",
    opt_type=OptionType.STRING,
    required=True,
    choices=[
        SlashCommandChoice("finn", "finn"),
        SlashCommandChoice("ottarl", "ottarl"),
        SlashCommandChoice("revis", "revis"),
        SlashCommandChoice("riveria", "riveria"),
    ],
)
async def rb(ctx: SlashContext, sub_command: str):
    await command_rb.run(client, ctx, sub_command)


if __name__ == "__main__":
    client.start()
