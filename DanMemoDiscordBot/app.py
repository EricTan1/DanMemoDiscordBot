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
import commands.profile as command_profile
import commands.rb as command_rb
import commands.skillSearch as command_skillSearch
import commands.FRrun as command_FRrun
import commands.FRmock as command_FRmock
import commands.FRping as command_FRping
import commands.FRnewday as command_FRnewday
import commands.addUpdateUnit as command_addUpdateUnit
import commands.FWGupdateteam as command_FWGUpdateTeam
import commands.FWGinfo as command_FWGInfo
import commands.FWGupdatenote as command_FWGUpdateNote
import commands.FWGtargets as command_FWGTargets
import commands.FWGattack as command_FWGAttack
import commands.FWGsettarget as command_FWGSetTarget
import commands.FWGping as command_FWGPing
import commands.FWGleft as command_FWGLeft
import commands.FWGtargets as command_FWGTargets
import commands.FWGenemyattack as command_FWGEnemyAttack

from commands.utils import createGSpreadJSON

if "IS_HEROKU" in os.environ:
    _command_prefix = "!$"
else:
    _command_prefix = "$$"

client = commands.Bot(command_prefix=_command_prefix, help_command=None, case_insensitive=True)
dbConfig = DBConfig(DatabaseEnvironment.HEROKU)
cache = Cache(dbConfig)
@client.event
async def on_message(message):
    # #screenshots
    # if(message.channel.id==738834866002722967):
    #     await command_FWGUpdateTeam.run(message)
    # #enemy attacks
    # elif(message.channel.id==739875599463743570):
    #     await command_FWGEnemyAttack.run(message)
    await client.process_commands(message)

@client.event
async def on_ready():
    ''' () -> None
    This function initializes the bot.
    '''
    #temp = [(e.id, e.name) for e in client.emojis]
    #print(temp)
    #client.add_cog(FamiliaRush())
    #client.add_cog(FamiliaWarGame(client))
    #await createGSpreadJSON()
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
    
@client.command(aliases=["pull","g"])
async def gacha(ctx,*args):
    await command_gacha.run(dbConfig,client,ctx,*args)

@client.command(aliases=["gm"])
async def gachamode(ctx,*args):
    await command_gachaMode.run(dbConfig,client,ctx,*args)

@client.command(aliases=["p","inventory"])
async def profile(ctx,*args):
    await command_profile.run(dbConfig,client,ctx,*args)

@client.command(aliases=["recordbuster","record buster", "rbguide"])
async def rb(ctx, character):
    await command_rb.run(ctx,character)

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

class FamiliaRush(commands.Cog):
    @client.command(aliases=["frr","familiarushrun"])
    async def frrun(self, ctx, *search):
        await command_FRrun.run(client,ctx,*search)

    @client.command(aliases=["frm","familiarushmock"])
    async def frmock(self, ctx, *search):
        await command_FRmock.run(client,ctx,*search)

    @client.command(aliases=["frp","familiarushping"])
    async def frping(self,ctx, *search):
        await command_FRping.run(client,ctx,*search)

    @client.command(aliases=["frnd","familiarushnewday"])
    async def frnewday(self, ctx, *search):
        await command_FRnewday.run(client,ctx,*search)

class FamiliaWarGame(commands.Cog):
    # not too sure whether to implement since manually prob faster/better
    @commands.command(aliases=["fwgnd"])
    async def fwgNewDay(self, ctx):
        pass
    #@commands.command(aliases=["fwgut"])
    async def fwgUpdateTeam(self, ctx, target:str):
        await command_FWGUpdateTeam.run(ctx.message)
    @commands.command(aliases=["fwga"])
    async def fwgAttack(self, ctx, target,medals:int):
        await command_FWGAttack.run(client,ctx,target, medals)
    #@commands.command(aliases=["fwgea"])
    async def fwgEnemyAttack(self, ctx, target,medals:int):
        await command_FWGAttack.run(client,ctx,target, medals)
    @commands.command(aliases=["fwgp"])
    async def fwgPing(self, ctx):
        await command_FWGPing.run(ctx)
    @commands.command(aliases=["fwgst"])
    async def fwgSetTarget(self, ctx,ally:discord.Member,enemy):
        await command_FWGSetTarget.run(ctx,ally,enemy)
    @commands.command(aliases=["fwgt","fwgTarget"])
    async def fwgTargets(self, ctx,*optional:discord.Member):
        await command_FWGTargets.run(ctx, optional)
    @commands.command(aliases=["fwgl"])
    async def fwgLeft(self, ctx):
        await command_FWGLeft.run(ctx)
    @commands.command(aliases=["fwun"])
    async def fwgupdatenote(self, ctx, target, *note):
        await command_FWGUpdateNote.run(ctx,target,note)
    @commands.command(aliases=["fwgi"])
    async def fwgInfo(self,ctx, target):
        await command_FWGInfo.run(ctx,target)

if __name__ == "__main__":
    TOKEN = os.environ.get("DISCORD_TOKEN_DANMEMO")
    client.run(TOKEN)