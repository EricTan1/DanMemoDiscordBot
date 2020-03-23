import discord
import asyncio
import json
import sys
import os
import aiohttp
from discord.ext import commands
from DBcontroller import DBcontroller

import os
import sys
from urllib.parse import urlparse
sys.path.append('Entities/')

from Adventurer import Adventurer,AdventurerSkill,AdventurerSkillEffects,AdventurerDevelopment, AdventurerStats
from BaseConstants import Element, Target, Type, Attribute,Modifier

TOKEN = os.environ.get("DISCORD_TOKEN_DANMEMO")


result = urlparse(os.environ.get("CLEARDB_DATABASE_URL"))
USERNAME = result.username
PASSWORD = result.password
DATABASE = result.path[1:]
HOSTNAME = result.hostname

_command_prefix = '!$'
client = commands.Bot(command_prefix=_command_prefix, help_command=None)

@client.event
async def on_ready():
    ''' () -> None
    This function initializes the bot.
    '''
    print("Bot is ready!")

@client.command()
async def close(ctx):
    # embeded message to show that the bot is shut down
    temp_embed = discord.Embed()
    temp_embed.color = 3066993
    temp_embed.title = "Closed"
    temp_embed.description = "Bot has been successfully closed"
    await ctx.send(embed=temp_embed)
    # shut down the bot
    await client.close()

@client.command(aliases=['cs'])
async def characterSearch(ctx, *search):
    is_embed = False
    is_files = False
    my_search = ""
    for words in search:
        my_search= my_search + words + " "
    db = DBcontroller(HOSTNAME,USERNAME,PASSWORD,"3306",DATABASE)
    my_list = db.characterSearch(my_search,{})
    print(my_list)
    message = ""

    # exactly 1 result then display
    if(len(my_list)==0):
        message = "Sorry there are no results"
    elif(len(my_list) == 1):
        temp_embed = discord.Embed()
        temp_embed.color = 4975455
        if("Ad" in my_list[0]):
            info = db.assembleAdventurer((my_list[0])[2:])
        else:
            info = db.assembleAssist((my_list[0])[2:])
        temp_embed.title = info[1]
        for skills in info[2]:
            if(skills[1] == ""):
                temp_embed.add_field(name=skills[0], value="placeholder", inline=False)
            else:
                temp_embed.add_field(name=skills[0], value=skills[1], inline=False)
                
        try:
            # images
            file_list = []
            # file_list.append(discord.File("./lottery/"+info[0], filename="hex.png"))
            file_list.append(discord.File("./lottery/"+info[0]+"/hex.png"))
            #file_list.append(discord.File("./lottery/"+info[0], filename="texture.png"))        
            file_list.append(discord.File("./lottery/"+info[0] + "/texture.png"))
            temp_embed.set_thumbnail(url="attachment://hex.png")
            temp_embed.set_image(url="attachment://texture.png")
            is_files = True            
        except:
            pass
        
        is_embed = True
    else:
        for Adventurersid in my_list:
            if("Ad" in Adventurersid):
                message= message + db.getAdventurerName(Adventurersid[2:]) + "\n"
            else:
                message= message + db.getAssistName(Adventurersid[2:]) + "\n"
    try:
        if(is_embed and is_files):
            await ctx.send(files=file_list,embed=temp_embed)
        elif(is_embed):
            await ctx.send(embed=temp_embed)
        elif(is_files):
            await ctx.send(files=file_list)        
        else:         
            await ctx.send(message)
    except:
        await ctx.send("too many results please try to narrow it down further")
    db.closeconnection()


@client.command(aliases=['ss'])
async def skillSearch(ctx, *search):
    print(search)
    my_search = ""
    for words in search:
        my_search= my_search + words + " "
    db = DBcontroller(HOSTNAME,USERNAME,PASSWORD,"3306",DATABASE)
    
    skilleffects_id_list = db.skillSearch(my_search,{})
    print(skilleffects_id_list)
    my_set = set()
    message =""
    for skilleffectsid in skilleffects_id_list:
        print(skilleffectsid)
        if("Ad" in skilleffectsid):
            skillid = db.getAdSkillIdFromEffect(skilleffectsid[2:])
            my_set.add("Ad"+str(skillid))            
        else:
            skillid = db.getAsSkillIdFromEffect(skilleffectsid[2:])
            my_set.add("As"+str(skillid))
        
    for skillid in my_set:
        if("Ad" in skillid):
            adventurerid = db.getAdventurerIdFromSkill(skillid[2:])
            message =message +  db.assembleAdventurerCharacterData(adventurerid)
            message = message + db.assembleAdventurerSkill(skillid[2:])
        else:
            assistid = db.getAssistIdFromSkill(skillid[2:])
            message =message +  db.assembleAssistCharacterData(assistid)
            message = message + db.assembleAssistSkill(skillid[2:])
        

    try:
        await ctx.send(message)
    except:
        await ctx.send("too many results please try to narrow it down further")
    db.closeconnection()


if __name__ == "__main__":
    # Run the bot
    client.run(TOKEN)
