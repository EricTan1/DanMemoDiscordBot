from typing import Optional, cast
from interactions.ext.files import CommandContext
from interactions.ext.wait_for import WaitForClient

import discord
from discord.ext import commands
import interactions
from interactions.ext.wait_for import setup
import os

from database.DBcontroller import DatabaseEnvironment, DBConfig
from commands.cache import Cache

import commands.bento as command_bento
import commands.unitsearch.commonSearch as command_commonSearch
import commands.dispatch as command_dispatch
import commands.gacha as command_gacha
import commands.gachaMode as command_gachaMode
import commands.help as command_help
import commands.invite as command_invite
import commands.profile as command_profile
import commands.rb as command_rb
import commands.support as command_support
import commands.topUsers as command_topUsers
import commands.popularity as command_popularity
import commands.addUpdateUnit as command_addUpdateUnit
import commands.saCalculator as command_saCalculator
import commands.killer as command_killer
import commands.elementAssists as command_elementAssists
import commands.getJson as command_getJson
import commands.init as command_init
import commands.recordbuster.recordBusterCalc as command_rbCalc
import traceback

from commands.utils import createGSpreadJSON


GUILD_ID = 698143969166622720 # ID of Sword Oratoria server
TOKEN = os.environ["DISCORD_TOKEN_DANMEMO"]
ENV = os.environ.get("ENV")

if ENV == "dev":
    dbConfig = DBConfig(DatabaseEnvironment.LOCAL)
    # Scopes bot commands to the Dev server for testing
    # since unscoped (global) commands may take a couple hours to update
    SCOPE: Optional[int] = GUILD_ID
else:
    dbConfig = DBConfig(DatabaseEnvironment.HEROKU)
    SCOPE = None

_command_prefix = os.environ.get("COMMAND_PREFIX")

client = commands.Bot(command_prefix=_command_prefix, help_command=None, case_insensitive=True, intents=None)
slash_client_pre = interactions.Client(token=TOKEN, default_scope=SCOPE)
slash_client_pre.load("interactions.ext.files")
slash_client: WaitForClient = setup(cast(WaitForClient, slash_client_pre)) # loads wait_for extension

cache = Cache(dbConfig)
@client.event
async def on_message(message):
    await client.process_commands(message)

@client.event
async def on_ready():
    ''' () -> None
    This function initializes the bot.
    '''
    print("test")
    client.add_cog(Infographic(client))
    createGSpreadJSON()
    print("Bot is ready!")


async def close(ctx):
    # embeded message to show that the bot is shut down
    temp_embed = discord.Embed()
    temp_embed.color = 3066993
    temp_embed.title = "Closed"
    temp_embed.description = "Bot has been successfully closed"
    await ctx.send(embeds=temp_embed)
    # shut down the bot
    await client.close()

@slash_client.command(
    name="sa-calculator",
    description="SA gauge Calculator",
    options=[
        interactions.Option(
            name="config",
            description="Config file for the calculator. If you do not provide one, the template will be offered for download",
            type=interactions.OptionType.ATTACHMENT,
            required=False
        )
    ]
)
async def sacalc(ctx: CommandContext, config: Optional[interactions.Attachment] = None):
    await command_saCalculator.run(slash_client, ctx, config)


@slash_client.command(
    name="recordbuster-calculator",
    description="Record Buster Score Calculator",
    options=[
        interactions.Option(
            name="config",
            description="Config file for the calculator. If you do not provide one, the template will be offered for download",
            type=interactions.OptionType.ATTACHMENT,
            required=False
        )
    ]
)
async def rbcalc(ctx: CommandContext, config: Optional[interactions.Attachment] = None):
    # imanity server only and ex-imanity role
    # if(await hasAccess(ctx.message.author,EDITORS) or ctx.message.author.guild.id == 685046495988154373):
    try:
        await command_rbCalc.run(slash_client,ctx,config)
    except:
        tb = traceback.format_exc()
        await ctx.send(f"ERROR:\n```{tb}```")


@slash_client.command(
    name="character-search",
    description="Search DanMemo units by name and title",
    options=[
        interactions.Option(
            name="keywords",
            description="Keywords to look for",
            type=interactions.OptionType.STRING,
            required=True,
        )
    ]
)
async def characterSearch(ctx: CommandContext, keywords: str):
    await command_commonSearch.run(dbConfig,slash_client,ctx,keywords,is_character_search=True)


@slash_client.command(
    name="skill-search",
    description="Search DanMemo units by skills",
    options=[
        interactions.Option(
            name="keywords",
            description="Keywords to look for",
            type=interactions.OptionType.STRING,
            required=True,
        )
    ]
)
async def skillSearch(ctx: CommandContext, keywords: str):
    await command_commonSearch.run(dbConfig,slash_client,ctx,keywords,is_character_search=False)


@slash_client.command(
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
        )
    ]
)
async def help(ctx: CommandContext, sub_command: str):
    await command_help.run(ctx, sub_command)


@slash_client.command(
    name="invite",
    description="Prints the server invite link for the bot",
)
async def invite(ctx: CommandContext):
    await command_invite.run(ctx)


@slash_client.command(
    name="support",
    description="Sends a link to our support server. Please contact Eric#5731 or Yon#7436",
)
async def support(ctx: CommandContext):
    await command_support.run(ctx)


@client.command()
async def popularity(ctx):
    await command_popularity.run(client,ctx)


@slash_client.command(
    name="bento",
    description="Syr's lunch box! Get crepes every two hours that can be traded for gacha rolls!",
)
async def bento(ctx: CommandContext):
    await command_bento.run(dbConfig,ctx)


@slash_client.command(
    name="gacha",
    description="Trade a crepe for an 11-draw gacha pull. In-game gacha rates. Limited and JP-only units are included",
)
async def gacha(ctx: CommandContext):
    await command_gacha.run(dbConfig,ctx)


@slash_client.command(
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
        )
    ]
)
async def gachamode(ctx: CommandContext, sub_command: str):
    await command_gachaMode.run(dbConfig,ctx,sub_command)


@client.command(aliases=["p","inventory"])
async def profile(ctx,*args):
    await command_profile.run(dbConfig,client,ctx,*args)


@client.command(aliases=["top"])
async def topUsers(ctx,*args):
    await command_topUsers.run(dbConfig,client,ctx,*args)


@client.command(aliases=["dp","dispatchquest","dq"])
async def dispatch(ctx, *search):
    print("work")
    await command_dispatch.run(dbConfig,client,ctx,*search)


unit_attachment = interactions.Option(
    name="unit_file",
    description="File containing the unit data in JSON format",
    type=interactions.OptionType.ATTACHMENT,
    required=True,
)

@slash_client.command(
    name="add-update-unit",
    description="Adds a unit or overwrites an existing one",
    scope=GUILD_ID, # so the command is only visible & available on the dev server
    default_scope=False,
    options=[
        interactions.Option(
            name="adventurer",
            description="Add an adventurer unit",
            type=interactions.OptionType.SUB_COMMAND,
            options=[unit_attachment]
        ),
        interactions.Option(
            name="assist",
            description="Add an assist unit",
            type=interactions.OptionType.SUB_COMMAND,
            options=[unit_attachment]
        )
    ]
)
async def addUpdateUnit(ctx: CommandContext, sub_command: str, unit_file: interactions.Attachment):
    await command_addUpdateUnit.run(dbConfig, slash_client, ctx, sub_command, unit_file)
    # refresh the cache
    cache = Cache(dbConfig)
    cache.refreshcache(dbConfig)


@slash_client.command(
    name="get-json",
    description="Get the unit database in JSON format",
    scope=GUILD_ID, # so the command is only visible & available on the dev server
    default_scope=False,
)
async def getJson(ctx: CommandContext):
    await command_getJson.run(ctx)


@client.command()
async def init(ctx):
    await command_init.run(ctx)

# commands that just bring up pictures
class Infographic(commands.Cog):
    #cp?

    @commands.command(aliases=["slayer","slayers","killers"])
    async def killer(self, ctx, *args):
        await command_killer.run(ctx, dbConfig, *args)


    @slash_client.command(
        name="elemental-assists",
        description="Posts an infographic of all elemental damage buffing/elemental resist debuffing assists in the game",
    )
    async def elementAssists(ctx: CommandContext):
        await command_elementAssists.run(ctx, dbConfig)


    @commands.command(aliases=["recordbuster","rbguide"])
    async def rb(self, ctx, character):
        await command_rb.run(ctx,character)




if __name__ == "__main__":
    #client.run(TOKEN)
    slash_client.start()
