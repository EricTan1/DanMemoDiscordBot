import os
import traceback
from typing import Optional, cast
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from datetime import datetime

import interactions
from interactions.ext.files import CommandContext
from interactions.ext.wait_for import WaitForClient, setup

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
    # Scopes bot commands to the Dev server for testing
    # since unscoped (global) commands may take a couple hours to update
    SCOPE: Optional[int] = GUILD_ID
else:
    dbConfig = DBConfig(DatabaseEnvironment.HEROKU)
    SCOPE = None

client_pre = interactions.Client(token=TOKEN, default_scope=SCOPE)
client_pre.load("interactions.ext.files")
client: WaitForClient = setup(
    cast(WaitForClient, client_pre)
)  # loads wait_for extension

cache = Cache(dbConfig)

status_message = interactions.Message()


# Updates heartbeat file and bot status message on Discord
async def status_update():
    boot_text = status_message.content.split("\n")[0]
    timestamp = int(datetime.now().timestamp())
    await status_message.edit(boot_text + f"\nLast heartbeat: <t:{timestamp}:R>")
    with open("heartbeat-file.txt", "w") as f:
        f.write(str(timestamp))


@client.event
async def on_start():
    """() -> None
    This function initializes the bot.
    """
    print("test")
    createGSpreadJSON()
    print("Bot is ready!")

    # Create initial status message in bot-status channel
    channel_dict = await client._http.get_channel(STATUS_CHANNEL_ID)
    channel = interactions.Channel(**channel_dict, _client=client._http)
    global status_message
    timestamp = int(datetime.now().timestamp())
    status_message = await channel.send(
        f"Bot going online at <t:{timestamp}:F>\nLast heartbeat: <t:{timestamp}:R>"
    )
    # Setup & start heartbeat scheduler
    scheduler = AsyncIOScheduler()
    scheduler.add_job(status_update, "interval", seconds=HEARTRATE)
    scheduler.start()


@client.command(
    name="sa-calculator",
    description="SA gauge Calculator",
    options=[
        interactions.Option(
            name="config",
            description="Config file for the calculator. If you do not provide one, the template will be offered for download",
            type=interactions.OptionType.ATTACHMENT,
            required=False,
        )
    ],
)
async def sacalc(ctx: CommandContext, config: Optional[interactions.Attachment] = None):
    # to tell Discord this command may take longer than the default 3s timeout
    # Used because autodefer() doesn't work: https://github.com/interactions-py/interactions.py/issues/1021
    await ctx.defer()
    await command_saCalculator.run(client, ctx, config)


@client.command(
    name="recordbuster-calculator",
    description="Record Buster Score Calculator",
    options=[
        interactions.Option(
            name="config",
            description="Config file for the calculator. If you do not provide one, the template will be offered for download",
            type=interactions.OptionType.ATTACHMENT,
            required=False,
        )
    ],
)
async def rbcalc(ctx: CommandContext, config: Optional[interactions.Attachment] = None):
    try:
        # to tell Discord this command may take longer than the default 3s timeout
        await ctx.defer()
        await command_rbCalc.run(client, ctx, config)
    except:
        tb = traceback.format_exc()
        await ctx.send(f"ERROR:\n```{tb}```")


@client.command(
    name="character-search",
    description="Search DanMemo units by name and title",
    options=[
        interactions.Option(
            name="keywords",
            description="Keywords to look for",
            type=interactions.OptionType.STRING,
            required=True,
        )
    ],
)
async def characterSearch(ctx: CommandContext, keywords: str):
    # to tell Discord this command may take longer than the default 3s timeout
    await ctx.defer()
    await command_commonSearch.run(
        dbConfig, client, ctx, keywords, is_character_search=True
    )


@client.command(
    name="skill-search",
    description="Search DanMemo units by skills",
    options=[
        interactions.Option(
            name="keywords",
            description="Keywords to look for",
            type=interactions.OptionType.STRING,
            required=True,
        )
    ],
)
async def skillSearch(ctx: CommandContext, keywords: str):
    # to tell Discord this command may take longer than the default 3s timeout
    await ctx.defer()
    await command_commonSearch.run(
        dbConfig, client, ctx, keywords, is_character_search=False
    )


@client.command(
    name="help",
    description="Instructions on using the bot",
    options=[
        interactions.Option(
            name="user",
            description="Send help via DM to the requesting user",
            type=interactions.OptionType.SUB_COMMAND,
            required=False,
        ),
        interactions.Option(
            name="server",
            description="Send help to the server instead of sending a DM to the user",
            type=interactions.OptionType.SUB_COMMAND,
            required=False,
        ),
    ],
)
async def help(ctx: CommandContext, sub_command: str):
    # to tell Discord this command may take longer than the default 3s timeout
    await ctx.defer()
    await command_help.run(ctx, sub_command)


@client.command(
    name="invite",
    description="Prints the server invite link for the bot",
)
async def invite(ctx: CommandContext):
    # to tell Discord this command may take longer than the default 3s timeout
    await ctx.defer()
    await command_invite.run(ctx)


@client.command(
    name="support",
    description="Sends a link to our support server. Please contact Eric#5731 or Yon#7436",
)
async def support(ctx: CommandContext):
    # to tell Discord this command may take longer than the default 3s timeout
    await ctx.defer()
    await command_support.run(ctx)


@client.command(
    name="popularity",
    description="Displays current Ais bot popularity",
)
async def popularity(ctx: CommandContext):
    # to tell Discord this command may take longer than the default 3s timeout
    await ctx.defer()
    await command_popularity.run(client, ctx)


@client.command(
    name="bento",
    description="Syr's lunch box! Get crepes every two hours that can be traded for gacha rolls!",
)
async def bento(ctx: CommandContext):
    # to tell Discord this command may take longer than the default 3s timeout
    await ctx.defer()
    await command_bento.run(dbConfig, ctx)


@client.command(
    name="gacha",
    description="Trade a crepe for an 11-draw gacha pull. In-game gacha rates. Limited and JP-only units are included",
)
async def gacha(ctx: CommandContext):
    # to tell Discord this command may take longer than the default 3s timeout
    await ctx.defer()
    await command_gacha.run(dbConfig, ctx)


@client.command(
    name="gacha-mode",
    description="Changes the way your gacha pulls are shown",
    options=[
        interactions.Option(
            name="image",
            description="Send pull results as image",
            type=interactions.OptionType.SUB_COMMAND,
            required=False,
        ),
        interactions.Option(
            name="gif",
            description="Send pull results as GIF",
            type=interactions.OptionType.SUB_COMMAND,
            required=False,
        ),
    ],
)
async def gachamode(ctx: CommandContext, sub_command: str):
    # to tell Discord this command may take longer than the default 3s timeout
    await ctx.defer()
    await command_gachaMode.run(dbConfig, ctx, sub_command)


@client.command(
    name="profile",
    description="Your personal stats and inventory",
    options=[
        interactions.Option(
            name="detailed",
            description="Detailed inventory listing",
            type=interactions.OptionType.SUB_COMMAND,
            required=False,
        ),
        interactions.Option(
            name="summary",
            description="Short summary of your inventory",
            type=interactions.OptionType.SUB_COMMAND,
            required=False,
        ),
    ],
)
async def profile(ctx: CommandContext, sub_command: str):
    # to tell Discord this command may take longer than the default 3s timeout
    await ctx.defer()
    await command_profile.run(dbConfig, client, ctx, sub_command)


@client.command(
    name="top-users",
    description="Shows the biggest whales/gourmets, all servers combined",
    options=[
        interactions.Option(
            name="whales",
            description="Top players by total score of owned gacha units",
            type=interactions.OptionType.SUB_COMMAND,
            required=False,
        ),
        interactions.Option(
            name="gourmets",
            description="Top players by crepes owned",
            type=interactions.OptionType.SUB_COMMAND,
            required=False,
        ),
    ],
)
async def topUsers(ctx: CommandContext, sub_command: str):
    # to tell Discord this command may take longer than the default 3s timeout
    await ctx.defer()
    await command_topUsers.run(dbConfig, client, ctx, sub_command)


@client.command(
    name="dispatch",
    description="Displays all the special board dispatch quests related to the search",
    options=[
        interactions.Option(
            name="keywords",
            description="Keywords to look for",
            type=interactions.OptionType.STRING,
            required=True,
        )
    ],
)
async def dispatch(ctx: CommandContext, keywords: str):
    # to tell Discord this command may take longer than the default 3s timeout
    await ctx.defer()
    await command_dispatch.run(dbConfig, ctx, keywords)


@client.command(
    name="add-update-unit",
    description="Adds a unit or overwrites an existing one",
    scope=GUILD_ID,  # so the command is only visible & available on the dev server
    default_scope=False,
    options=[
        interactions.Option(
            name="unit_file",
            description="File containing the unit data in JSON format",
            type=interactions.OptionType.ATTACHMENT,
            required=True,
        )
    ],
)
async def addUpdateUnit(ctx: CommandContext, unit_file: interactions.Attachment):
    # to tell Discord this command may take longer than the default 3s timeout
    await ctx.defer()
    await command_addUpdateUnit.run(dbConfig, client, ctx, unit_file)
    # refresh the cache
    cache = Cache(dbConfig)
    cache.refreshcache(dbConfig)


@client.command(
    name="get-json",
    description="Get the unit database in JSON format",
    scope=GUILD_ID,  # so the command is only visible & available on the dev server
    default_scope=False,
)
async def getJson(ctx: CommandContext):
    # to tell Discord this command may take longer than the default 3s timeout
    await ctx.defer()
    await command_getJson.run(ctx)


@client.command(
    name="init",
    description="No idea what this does tbh",
    scope=GUILD_ID,  # so the command is only visible & available on the dev server
    default_scope=False,
)
async def init(ctx: CommandContext):
    # to tell Discord this command may take longer than the default 3s timeout
    await ctx.defer()
    await command_init.run(ctx)


# commands that just bring up pictures
killer_subcommands = [
    interactions.Option(
        name=killer_type,
        description=f"Shows {killer_type} killer units",
        type=interactions.OptionType.SUB_COMMAND,
    )
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


@client.command(
    name="killers",
    description="Posts infographic of all killer units in the game. Can also filter to one monster type.",
    options=killer_subcommands,
)
async def killer(ctx, sub_command: str):
    # to tell Discord this command may take longer than the default 3s timeout
    await ctx.defer()
    await command_killer.run(ctx, dbConfig, sub_command)


@client.command(
    name="elemental-assists",
    description="Posts an infographic of all elemental damage buffing/elemental resist debuffing assists in the game",
)
async def elementAssists(ctx: CommandContext):
    # to tell Discord this command may take longer than the default 3s timeout
    await ctx.defer()
    await command_elementAssists.run(ctx, dbConfig)


@client.command(
    name="recordbuster",
    description="Posts a guide for the given RB character",
    options=[
        interactions.Option(
            name="finn",
            description="RB guide for Finn",
            type=interactions.OptionType.SUB_COMMAND,
        ),
        interactions.Option(
            name="ottarl",
            description="RB guide for Ottarl",
            type=interactions.OptionType.SUB_COMMAND,
        ),
        interactions.Option(
            name="revis",
            description="RB guide for Revis",
            type=interactions.OptionType.SUB_COMMAND,
        ),
        interactions.Option(
            name="riveria",
            description="RB guide for Riveria",
            type=interactions.OptionType.SUB_COMMAND,
        ),
    ],
)
async def rb(ctx: CommandContext, sub_command: str):
    # to tell Discord this command may take longer than the default 3s timeout
    await ctx.defer()
    await command_rb.run(client, ctx, sub_command)


if __name__ == "__main__":
    client.start()
