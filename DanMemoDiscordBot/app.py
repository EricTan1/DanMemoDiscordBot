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
import commands.killerUpdate as command_killerUpdate
import commands.elementAssists as command_elementAssists
import commands.elementAssistsUpdate as command_elementAssistsUpdate
import commands.getJson as command_getJson
import commands.init as command_init
import commands.recordbuster.recordBusterCalc as command_rbCalc
import traceback


from commands.utils import createGSpreadJSON, checkperms,hasAccess


_command_prefix = os.environ.get("COMMAND_PREFIX")
# INTENTS
#intents = discord.Intents.default()
#intents.members = True

client = commands.Bot(command_prefix=_command_prefix, help_command=None, case_insensitive=True)
dbConfig = DBConfig(DatabaseEnvironment.HEROKU)
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
    #temp = [(e.id, e.name) for e in client.emojis]
    #print(temp)
    client.add_cog(Infographic(client))
    await createGSpreadJSON()
    print("Bot is ready!")


async def close(ctx):
    # embeded message to show that the bot is shut down
    temp_embed = discord.Embed()
    temp_embed.color = 3066993
    temp_embed.title = "Closed"
    temp_embed.description = "Bot has been successfully closed"
    await ctx.send(embed=temp_embed)
    # shut down the bot
    await client.close()

@client.command(aliases=["sa","sacalculator"])
async def sacalc(ctx):
    await command_saCalculator.run(ctx)
    #await command_saCalculator.calculate()

@client.command(aliases=["rbc"])
async def rbcalc(ctx):
    # imanity server only and ex-imanity role
    if(await hasAccess(ctx.message.author,[708002106245775410,698143969166622720],[708008774140690473,825721805489700876,699277609816555580,708302206780309544,913489903671738440,685466436923162634,685472735996018699,619478476713361409,933110903484858409]) or ctx.message.author.guild.id == 685046495988154373):
        try:
            await command_rbCalc.run(client,ctx)
        except:
            tb = traceback.format_exc()
            await ctx.send("ERROR:\n```{}```".format(tb))

@client.command(aliases=["cs"])
async def characterSearch(ctx, *search):
    await command_characterSearch.run(dbConfig,client,ctx,*search)

@client.command(aliases=["ss"])
async def skillSearch(ctx, *search):
    await command_skillSearch.run(dbConfig,client,ctx,*search)

@client.command(aliases=["h","command","commands"])
async def help(ctx,*args):
    await command_help.run(ctx,*args)

@client.command()
async def invite(ctx):
    await command_invite.run(ctx)

@client.command(aliases=["imanity","bestFamilia"])
async def support(ctx):
    await command_support.run(ctx)

@client.command()
async def popularity(ctx):
    await command_popularity.run(client,ctx)

@client.command(aliases=["daily","b"])
async def bento(ctx):
    await command_bento.run(dbConfig,ctx)

@client.command(aliases=["pull","g"])
async def gacha(ctx,*args):
    await command_gacha.run(dbConfig,client,ctx,*args)

@client.command(aliases=["gm"])
async def gachamode(ctx,*args):
    await command_gachaMode.run(dbConfig,client,ctx,*args)

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
    #killers
    @commands.command(aliases=["slayer","slayers","killers"])
    async def killer(self, ctx):
        await command_killer.run(ctx)

    @commands.command(aliases=["ku"])
    async def killerUpdate(self, ctx):
        await command_killerUpdate.run(dbConfig)

    @commands.command(aliases=["ea"])
    async def elementAssists(self, ctx):
        await command_elementAssists.run(ctx)

    @commands.command(aliases=["eau"])
    async def elementAssistsUpdate(self, ctx):
        await command_elementAssistsUpdate.run(dbConfig)

    @commands.command(aliases=["recordbuster","rbguide"])
    async def rb(self, ctx, character):
        await command_rb.run(ctx,character)




if __name__ == "__main__":
    TOKEN = os.environ.get("DISCORD_TOKEN_DANMEMO")
    client.run(TOKEN)