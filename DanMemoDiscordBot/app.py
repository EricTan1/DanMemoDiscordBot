import discord
import asyncio
import json
import sys
import os
import aiohttp
from discord.ext import commands
from DBcontroller import DBcontroller
from PIL import Image
import io
from urllib.parse import urlparse
import threading

sys.path.append('Entities/')
sys.path.append('webapp/')

from Adventurer import Adventurer,AdventurerSkill,AdventurerSkillEffects,AdventurerDevelopment, AdventurerStats
from BaseConstants import Element, Target, Type, Attribute,Modifier
from views import webapp

TOKEN = os.environ.get("DISCORD_TOKEN_DANMEMO")


result = urlparse(os.environ.get("CLEARDB_DATABASE_URL"))
USERNAME = result.username
PASSWORD = result.password
DATABASE = result.path[1:]
HOSTNAME = result.hostname
# "localhost","root","danmemo","3306","danmemo"
#USERNAME = "root"
#PASSWORD = "danmemo"
#DATABASE = "danmemo"
#HOSTNAME = "localhost"

_command_prefix = '!$'
client = commands.Bot(command_prefix=_command_prefix, help_command=None)

@client.event
async def on_ready():
    ''' () -> None
    This function initializes the bot.
    '''
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

@client.command(aliases=['cs'])
async def characterSearch(ctx, *search):
    is_embed = False
    is_files = False
    my_search = " "
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
        if("Ad" in (my_list[0])[3]):
            info = db.assembleAdventurer(((my_list[0])[3])[2:])
        else:
            info = db.assembleAssist(((my_list[0])[3])[2:])
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
                message= message + "[{}] {}\n".format(Adventurersid[1],Adventurersid[2])
            else:
                message= message + "[{}] {}\n".format(Adventurersid[1],Adventurersid[2])
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
        await ctx.send("Sorry unable to find results")
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
    if(len(skilleffects_id_list) <=100):
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
        file_list = []
        discord_file_list = []
        assist_dup = set()
        rotating_list.append(temp_list)
        total_results = len(my_set)
        for skillid in my_set:
            if("Ad" in skillid):
                adventurerid = db.getAdventurerIdFromSkill(skillid[2:])
                #db.assembleAdventurerCharacterData(adventurerid)
                skillinfo = db.assembleAdventurerSkill(skillid[2:])
                #skillinfo[0]+skillinfo[1]+"\n"
                names = db.assembleAdventurerCharacterName(adventurerid)
                temp_list.append(("[{}] {}".format(names[0],names[1]),skillinfo[0]+skillinfo[1]+"\n"))
                try:
                    file_name = "./lottery/"+"{} {}".format(names[0],names[1]).strip()+"/hex.png"
                    f = open(file_name,"r")
                    f.close()
                    file_list.append(file_name)                    
                except:
                    file_list.append("./lottery/gac_dummy/hex.png")
            elif("As" in skillid):
                assistid = db.getAssistIdFromSkill(skillid[2:])
                if (not(assistid in assist_dup)):
                    assist_dup.add(assistid)
                    #db.assembleAssistCharacterData(assistid)
                    skillinfo=db.assembleAssistSkill(skillid[2:])
                    #skillinfo[0] + skillinfo[1]+"\n"
                    names = db.assembleAssistCharacterName(assistid)
                    temp_list.append(("[{}] {}".format(names[0],names[1]),skillinfo[0] + skillinfo[1]+"\n"))
                    try:
                        file_name = "./lottery/"+"{} {}".format(names[0],names[1]).strip()+"/hex.png"
                        f = open(file_name,"r")
                        f.close()
                        file_list.append(file_name)
                    except:
                        file_list.append("./lottery/gac_dummy/hex.png")
                else:
                    count = count -1
                    total_results = total_results -1
            else:
                skillinfo=db.assembleAdventurerDevelopment(skillid[2:])
                #skillinfo[0] + skillinfo[1]+"\n"
                temp_list.append((skillinfo[2],skillinfo[0] + "\n"+ skillinfo[1]+"\n"))
                try:
                    file_name = "./lottery/"+skillinfo[2].strip()+"/hex.png"
                    f = open(file_name,"r")
                    f.close()
                    file_list.append(file_name)
                except:
                    file_list.append("./lottery/gac_dummy/hex.png")                    
            count = count +1
            if(count ==4):
                await imageHorizontalConcat(file_list,discord_file_list)
                temp_list = []
                file_list= []                
                rotating_list.append(temp_list)
                count=0
                
        # remove last empty list
        if(len(rotating_list[len(rotating_list)-1]) == 0):
            rotating_list.pop(len(rotating_list)-1)
        elif(len(rotating_list[len(rotating_list)-1]) < 4):
            await imageHorizontalConcat(file_list,discord_file_list)
        icons = await imageVerticalConcat(discord_file_list)
        await skillSearchRotatingPage(ctx, search,rotating_list,total_results,icons)
    else:
        temp_embed = discord.Embed()
        temp_embed.color = 16203840
        temp_embed.title = "ERROR"
        temp_embed.description = "Too many results please try to narrow it down further"
        await ctx.send(embed=temp_embed)        
    db.closeconnection()

async def imageHorizontalConcat(file_list,discord_file_list):
    images = [Image.open(x) for x in file_list]
    widths, heights = zip(*(i.size for i in images))
    
    total_width = sum(widths)
    max_height = max(heights)
    
    new_im = Image.new('RGBA', (total_width, max_height))
    
    x_offset = 0
    for im in images:
        new_im.paste(im, (x_offset,0))
        x_offset += im.size[0]
    # convert to bytes
    imgByteArr = io.BytesIO()
    new_im.save(imgByteArr, format='PNG')
    imgByteArr.seek(0)
    discord_file_list.append(imgByteArr)

async def imageVerticalConcat(file_list):
    images = [Image.open(x) for x in file_list]
    widths, heights = zip(*(i.size for i in images))
    
    total_width = max(widths)
    max_height = sum(heights)
    
    new_im = Image.new('RGBA', (total_width, max_height))
    
    y_offset = 0
    for im in images:
        new_im.paste(im, (0,y_offset))
        y_offset += im.size[1]
    # convert to bytes
    imgByteArr = io.BytesIO()
    new_im.save(imgByteArr, format='PNG')
    imgByteArr.seek(0)
    return imgByteArr

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
    


async def skillSearchRotatingPage(ctx, search, page_list, total_results,icons):
    temp_image_url = "attachment://"
    # set up
    current_page = 0
    temp_embed = discord.Embed()
    temp_embed.set_image(url=temp_image_url+"temp.png")        
    
    temp_embed.color = 3066993
    temp_embed.title = "{} results for {}".format(str(total_results),search)
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
    msg = await ctx.send(embed=temp_embed, file=discord.File(icons, filename="temp.png"))
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


@client.command(aliases=['sim food'])
async def food(ctx):
    temp_embed = discord.Embed()
    temp_embed.color = 3066993
    temp_embed.title = "Here is your bento box for today!"
    temp_embed.set_image(url="attachment://texture.png")
    await ctx.send(embed=temp_embed, file=discord.File("./lottery/A Loving Lunch Syr Flover" + "/texture.png"))
    
@client.command(aliases=['recordbuster','record buster', 'rbguide'])
async def rb(ctx, character):
    rb_list = ["ottar","revis","riveria"]
    if(character.lower() in rb_list):
        temp_embed = discord.Embed()
        temp_embed.color = 3066993
        temp_embed.set_author(name="Akuno#8965",url="https://discordapp.com",icon_url="https://cdn.discordapp.com/avatars/141222596610883584/0e51b4be33b83b17a4c98ceb381bda85.png?size=128")
        temp_embed.set_image(url="attachment://rb.png")
        await ctx.send(embed=temp_embed, file=discord.File("./rbguides/" + character+ ".png",filename="rb.png"))
    else:
        temp_embed = discord.Embed()
        temp_embed.color = 16203840
        temp_embed.title = "No character found"
        temp_embed.description= "There doesn't exist an RB for this character. Please search either: Ottar, Revis or Riveria"
        await ctx.send(embed=temp_embed)
        


@client.command(aliases=['dp','dispatchquest','dq'])
async def dispatch(ctx, *search):
    with open('./dispatchQuest/dispatch.json', 'r') as f:
        dispatch_dict = json.load(f)
    db = DBcontroller(HOSTNAME,USERNAME,PASSWORD,"3306",DATABASE)
    message = ""
    my_search = ""
    for words in search:
        my_search= my_search + words + " "
    ret_list = db.dispatchSearch(my_search)
    discord_file_list = []
    temp_embed = discord.Embed()    
    for ret in ret_list:
        char_list = [ret[4],ret[5],ret[6],ret[7]]
        file_list = []
        for char in char_list:
            print(dispatch_dict)
            print(char)
            try:
                file_list.append("./lottery/"+dispatch_dict.get(char)+"/hex.png")
            except:
                file_list.append("./lottery/gac_dummy/hex.png")
        if(ret[2]== None):
            temp_embed.add_field(name="{} - {}:".format(ret[1],ret[3]), value="{}, {}, {}, {}".format(ret[4],ret[5],ret[6],ret[7]), inline=False)
        else:
            #message = message + "{} - {} {}: {}, {}, {}, {}\n".format(ret[1],ret[2],ret[3],ret[4],ret[5],ret[6],ret[7])
            temp_embed.add_field(name="{} - {} {}:".format(ret[1],ret[2],ret[3]), value="{}, {}, {}, {}".format(ret[4],ret[5],ret[6],ret[7]), inline=False)
        await imageHorizontalConcat(file_list,discord_file_list)
    icons = await imageVerticalConcat(discord_file_list)
    temp_embed.color = 3066993
    temp_embed.title = "{} results for {}".format(len(ret_list),search)
    #temp_embed.description = message
    temp_embed.set_image(url="attachment://temp.png")
    try:
        msg = await ctx.send(embed=temp_embed, file=discord.File(icons, filename="temp.png"))
    except:
        temp_embed = discord.Embed()
        temp_embed.color = 16203840
        temp_embed.title = "Unable to find dispatch quest or too many dispatch quests"
        temp_embed.description= "Please narrow it down further"
        await ctx.send(embed=temp_embed)        
    
def run_webapp():
    webapp.run(debug=False)

def run_discord_bot():
    client.run(TOKEN)


if __name__ == "__main__":
    # Run the Discord bot
    discord_bot_thread = threading.Thread(target = run_discord_bot, daemon=True)
    discord_bot_thread.start()

    # Run the web application
    run_webapp()