from typing import Optional
from interactions.ext.files import CommandContext

import discord
from discord.ext import commands
import interactions
from interactions.ext.wait_for import setup
import os

from database.DBcontroller import DatabaseEnvironment, DBConfig
from commands.cache import Cache

import commands.bento as command_bento
import commands.characterSearch as command_characterSearch
import commands.dispatch as command_dispatch
import commands.gacha as command_gacha
import commands.gachaMode as command_gachaMode
import commands.help as command_help
import commands.invite as command_invite
import commands.profile as command_profile
import commands.rb as command_rb
import commands.skillSearch as command_skillSearch
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
TOKEN = os.environ.get("DISCORD_TOKEN_DANMEMO")
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
slash_client = interactions.Client(token=TOKEN, default_scope=SCOPE)
slash_client.load("interactions.ext.files")
setup(slash_client) # loads wait_for extension

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
    await createGSpreadJSON()
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

@client.command(aliases=["sa","sacalculator"])
async def sacalc(ctx):
    await command_saCalculator.run(ctx)
    #await command_saCalculator.calculate()


@client.command(aliases=["rbc"])
async def rbcalc(ctx):
    # imanity server only and ex-imanity role
    # if(await hasAccess(ctx.message.author,[708002106245775410,698143969166622720],[708008774140690473,825721805489700876,699277609816555580,708302206780309544,913489903671738440,685466436923162634,685472735996018699,619478476713361409,933110903484858409]) or ctx.message.author.guild.id == 685046495988154373):
    try:
        await command_rbCalc.run(client,ctx,ctx.message.attachments)
    except:
        tb = traceback.format_exc()
        await ctx.send("ERROR:\n```{}```".format(tb))

@slash_client.command(
    name="rbcalc",
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
    try:
        await command_rbCalc.run(slash_client,ctx,config)
    except:
        tb = traceback.format_exc()
        await ctx.send("ERROR:\n```{}```".format(tb))


@client.command(aliases=["cs"])
async def characterSearch(ctx, *search):
    await command_characterSearch.run(dbConfig,client,ctx,*search)

@slash_client.command(
    name="character-search",
    description="Search DanMemo units by name and title",
    options=[
        interactions.Option(
            name="keywords",
            description="Keywords to look for",
            type=interactions.OptionType.STRING,
        )
    ]
)
async def characterSearch(ctx: CommandContext, keywords: str):
    await command_characterSearch.run(dbConfig,slash_client,ctx,keywords)


@client.command(aliases=["ss"])
async def skillSearch(ctx, *search):
    await command_skillSearch.run(dbConfig,client,ctx,*search)


@client.command(aliases=["h","command","commands"])
async def help(ctx,*args):
    await command_help.run(ctx,*args)

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


@client.command()
async def invite(ctx):
    await command_invite.run(ctx)

@slash_client.command(
    name="invite",
    description="Prints the server invite link for the bot",
)
async def invite(ctx: CommandContext):
    await command_invite.run(ctx)


@client.command(aliases=["imanity","bestFamilia"])
async def support(ctx):
    await command_support.run(ctx)

@slash_client.command(
    name="support",
    description="Sends a link to our support server. Please contact Eric#5731 or Yon#7436",
)
async def support(ctx: CommandContext):
    await command_support.run(ctx)


@client.command()
async def popularity(ctx):
    await command_popularity.run(client,ctx)

@client.command(aliases=["daily","b"])
async def bento(ctx):
    await command_bento.run(dbConfig,ctx)

@slash_client.command(
    name="bento",
    description="Syr's lunch box! Get crepes every two hours that can be traded for gacha rolls!",
)
async def bento(ctx: CommandContext):
    await command_bento.run(dbConfig,ctx)


@client.command(aliases=["pull","g"])
async def gacha(ctx):
    await command_gacha.run(dbConfig,ctx)

@slash_client.command(
    name="gacha",
    description="Trade a crepe for an 11-draw gacha pull. In-game gacha rates. Limited and JP-only units are included",
)
async def gacha(ctx: CommandContext):
    await command_gacha.run(dbConfig,ctx)


@client.command(aliases=["gm"])
async def gachamode(ctx,*args):
    await command_gachaMode.run(dbConfig,client,ctx,*args)

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


@client.command(aliases=["auu"])
async def addUpdateUnit(ctx, *search):
    await command_addUpdateUnit.run(dbConfig,client,ctx,*search)
    # refresh the cache
    cache = Cache(dbConfig)
    cache.refreshcache(dbConfig)


@client.command(aliases=["gj"])
async def getJson(ctx):
    await command_getJson.run(client,ctx)


@client.command()
async def init(ctx):
    await command_init.run(ctx)

# commands that just bring up pictures
class Infographic(commands.Cog):
    #cp?

    @commands.command(aliases=["slayer","slayers","killers"])
    async def killer(self, ctx, *args):
        await command_killer.run(ctx, dbConfig, *args)


    @commands.command(aliases=["ea"])
    async def elementAssists(self, ctx):
        await command_elementAssists.run(ctx, dbConfig)

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
