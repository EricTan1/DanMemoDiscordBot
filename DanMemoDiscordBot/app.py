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
        temp_embed.color = 3066993
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
    if(len(skilleffects_id_list) <=60):
        for skilleffectsid in skilleffects_id_list:
            print(skilleffectsid)
            if("Ad" in skilleffectsid):
                skillid = db.getAdSkillIdFromEffect(skilleffectsid[2:])
                my_set.add("Ad"+str(skillid))            
            elif("As" in skilleffectsid):
                skillid = db.getAsSkillIdFromEffect(skilleffectsid[2:])
                my_set.add("As"+str(skillid))
            else:
                my_set.add(str(skilleffectsid))                
        rotating_list = []
        count = 0
        temp_list = []
        rotating_list.append(temp_list)
        for skillid in my_set:
            if("Ad" in skillid):
                adventurerid = db.getAdventurerIdFromSkill(skillid[2:])
                #db.assembleAdventurerCharacterData(adventurerid)
                skillinfo = db.assembleAdventurerSkill(skillid[2:])
                #skillinfo[0]+skillinfo[1]+"\n"
                temp_list.append((db.assembleAdventurerCharacterData(adventurerid),skillinfo[0]+skillinfo[1]+"\n"))
            elif("As" in skillid):
                assistid = db.getAssistIdFromSkill(skillid[2:])
                #db.assembleAssistCharacterData(assistid)
                skillinfo=db.assembleAssistSkill(skillid[2:])
                #skillinfo[0] + skillinfo[1]+"\n"
                temp_list.append((db.assembleAssistCharacterData(assistid),skillinfo[0] + skillinfo[1]+"\n"))
            else:
                skillinfo=db.assembleAdventurerDevelopment(skillid[2:])
                #skillinfo[0] + skillinfo[1]+"\n"
                temp_list.append((skillinfo[2],skillinfo[0] + "\n"+ skillinfo[1]+"\n"))
            count = count +1
            if(count ==4):
                temp_list = []
                rotating_list.append(temp_list)
                count=0
        # remove last empty list
        if(len(rotating_list[len(rotating_list)-1]) == 0):
            rotating_list.pop(len(rotating_list)-1)
        await skillSearchRotatingPage(ctx, search,rotating_list,my_set)
    else:
        temp_embed = discord.Embed()
        temp_embed.color = 16203840
        temp_embed.title = "ERROR"
        temp_embed.description = "Too many results please try to narrow it down further"
        await ctx.send(embed=temp_embed)        
    db.closeconnection()

@client.command(aliases=['h','command','commands'])
async def help(ctx):
    temp_embed = discord.Embed()
    temp_embed.color = 3066993
    temp_embed.title = "Command List"
    with open('./help.txt') as fp:
        line = fp.readline()
        print(line.strip())
        
        while(line):
            print(line.strip())
            if(line.strip() =="F"):
                line = fp.readline()
                name = line
                value = ""
                line = fp.readline()
                while line.strip() !="F" and line.strip() !="E":
                    value = value + line
                    line = fp.readline()
                temp_embed.add_field(name=name, value=value, inline=False)
            elif(line.strip()=="E"):
                break;
        temp_embed.set_thumbnail(url="https://static.myfigurecollection.net/pics/figure/large/571996.jpg")
    await ctx.author.send(embed=temp_embed)
    await ctx.send("Sent info to your DM!")
    


async def skillSearchRotatingPage(ctx, search, page_list, my_set):
    print(page_list)
    # set up
    current_page = 0
    temp_embed = discord.Embed()
    temp_embed.color = 3066993
    temp_embed.title = "{} results for {}".format(str(len(my_set)),search)
    if(len(page_list) == 0):
        page_list.append([["No relevant skills to display","End of List"]])    
    temp_embed.set_footer(text="Page {} of {}".format(current_page+1,len(page_list)))
    def clearSetField(temp_embed:discord.Embed, field_list):
        temp_embed.clear_fields()
        print(field_list)
        for skills in field_list:
            print(skills)
            temp_embed.add_field(value=skills[1], name=skills[0],inline=False)
        return temp_embed
    
    temp_embed = clearSetField(temp_embed, field_list=page_list[current_page])
    msg = await ctx.send(embed=temp_embed)
    emoji1 = '\u2b05'
    emoji2 = '\u27a1'
    await msg.add_reaction(emoji1)
    await msg.add_reaction(emoji2)
    emojis = [emoji1, emoji2]
    def check(reaction, user):
        return (str(reaction.emoji) == emoji2 or str(reaction.emoji) == emoji1) and user !=client.user
    while True:
        try:
            reaction, user = await client.wait_for('reaction_add', timeout=60.0, check=check)
        except asyncio.TimeoutError:
            temp_embed.color=16203840
            await msg.edit(embed=temp_embed)
            break
        else:
            # left
            if str(reaction.emoji) == emoji1:
                if(current_page > 0):
                    current_page = current_page -1
                else:
                    current_page = len(page_list)-1
            # right
            if str(reaction.emoji) == emoji2:
                if( current_page+1 < len(page_list)):
                    current_page = current_page +1
                else:
                    current_page = 0
            temp_embed.set_footer(text="Page {} of {}".format(current_page+1,len(page_list)))            
            temp_embed = clearSetField(temp_embed, field_list=page_list[current_page])
            await msg.edit(embed=temp_embed)


if __name__ == "__main__":
    # Run the bot
    client.run(TOKEN)
