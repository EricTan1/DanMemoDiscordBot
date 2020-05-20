import asyncio
import discord
from discord.ext import commands
import os

from database.DBcontroller import DatabaseEnvironment, DBConfig
from commands.cache import Cache

import commands.bento as command_bento
import commands.characterSearch as command_characterSearch
import commands.dispatch as command_dispatch
import commands.gacha as command_gacha
import commands.help as command_help
import commands.profile as command_profile
import commands.rb as command_rb
import commands.skillSearch as command_skillSearch
import commands.FRrun as command_FRrun
import commands.FRmock as command_FRmock

from commands.utils import createGSpreadJSON

if "IS_HEROKU" in os.environ:
    _command_prefix = "!$"
else:
    _command_prefix = "$$"

client = commands.Bot(command_prefix=_command_prefix, help_command=None)
dbConfig = DBConfig(DatabaseEnvironment.HEROKU)
cache = Cache(dbConfig)

@client.event
async def on_ready():
    ''' () -> None
    This function initializes the bot.
    '''
    #temp = [(e.id, e.name) for e in client.emojis]
    #print(temp)
    print("Bot is ready!")
    await createGSpreadJSON()

async def close(ctx):
    # embeded message to show that the bot is shut down
    temp_embed = discord.Embed()
    temp_embed.color = 3066993
    temp_embed.title = "Closed"
    temp_embed.description = "Bot has been successfully closed"
    await ctx.send(embed=temp_embed)
    # shut down the bot
    await client.close()

@client.command(aliases=["cs"])
async def characterSearch(ctx, *search):
    await command_characterSearch.run(dbConfig,client,ctx,*search)

@client.command(aliases=["ss"])
async def skillSearch(ctx, *search):
    await command_skillSearch.run(dbConfig,client,ctx,*search)

@client.command(aliases=["h","command","commands"])
async def help(ctx):
    await command_help.run(ctx)

@client.command(aliases=["daily","b"])
async def bento(ctx):
    await command_bento.run(dbConfig,ctx)
    
@client.command(aliases=["pull"])
async def gacha(ctx,*args):
    await command_gacha.run(dbConfig,client,ctx,*args)

@client.command(aliases=["p"])
async def profile(ctx,*args):
    await command_profile.run(dbConfig,client,ctx,*args)

@client.command(aliases=["recordbuster","record buster", "rbguide"])
async def rb(ctx, character):
    await command_rb.run(ctx,character)

@client.command(aliases=["dp","dispatchquest","dq"])
async def dispatch(ctx, *search):
    await command_dispatch.run(dbConfig,client,ctx,*search)

@client.command(aliases=["frr","familiarushrun"])
async def frrun(ctx, *search):
    print("in")
    await command_FRrun.run(client,ctx,*search)

@client.command(aliases=["frm","familiarushmock"])
async def frmock(ctx, *search):
    print("in")
    await command_FRmock.run(client,ctx,*search)

if __name__ == "__main__":
    TOKEN = os.environ.get("DISCORD_TOKEN_DANMEMO")
    client.run(TOKEN)