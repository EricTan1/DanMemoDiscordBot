import discord
import asyncio
import json
import sys
import os
import aiohttp
from discord.ext import commands
from PIL import Image
import io
from urllib.parse import urlparse
import itertools

from commands.utils import get_emoji,HeroAscensionStatsP,HeroAscensionStatsB,HeroAscensionStatsM,Status, HeroAscensionStatsD, HeroAscensionStatsH, getDefaultEmoji
from database.DBcontroller import DBcontroller
from database.entities.Adventurer import Adventurer, AdventurerSkill, AdventurerSkillEffects, AdventurerDevelopment, AdventurerStats
from database.entities.BaseConstants import Element, Target, Type, Attribute, Modifier

async def run(dbConfig, client, ctx, *search):
    """ Character Search
    <CommandPrefix> <Search>
    
    Arguments:
        dbConfig {[DBcontroller.dbConfig]} -- Database config usually local/environmental variables
        client {[discord.Client]} -- the discord bot object
        ctx {[discord.context]} -- command message context
    """
    my_search = " "
    for words in search:
        my_search = my_search + words + " "

    db = DBcontroller(dbConfig)
    my_list = db.characterSearch(my_search.replace("[","").replace("]",""),{})
    print(my_list)
    # exactly 1 result then display
    if len(my_list) == 0:
        message = "Sorry there are no results"
    elif len(my_list) == 1:
        await singleAdventurer(client, ctx, db,my_list[0])
    else:
        page_list=[]
        temp_page = []
        page_list.append(temp_page)
        total_results = 0
        for Adventurersid in my_list:
            total_results = total_results+1
            temp_page.append(Adventurersid)
            if(len(temp_page)>=10):
                temp_page = []
                page_list.append(temp_page)

        if(len(page_list) != 0 and len(page_list[len(page_list)-1])==0):
            page_list.pop(len(page_list)-1)
        
        await pageUnitsHandler(client,ctx,page_list,db,total_results,search)
    db.closeconnection()

async def pageUnitsHandler(client, ctx, page_list,db,total_results,search):
    """This handles the message scrolling of the character search and all the other
    page logic for multiple results

    Arguments:
        client {discord.client} -- the discord bot object
        ctx {discord.context} -- command message context
        page_list {list of list} -- list of pages, Pages are lists with adventurers. Adventurers are tuples with (id,title,adventurername) 
        db {DBController.DBController} -- Database connector object
        total_results {int} -- total number of results from the query
        search {string} -- the search query
    """
    # set up
    current_page = 0
    temp_embed = discord.Embed()
    temp_embed.description = "React on the numbers to display the corresponding units!"
    temp_embed.color = Status.OK.value
    temp_embed.title = "{} results for {}".format(str(total_results),search)
    if(len(page_list) == 0):
        page_list.append([["","No relevant characters to display","End of List"]])
    temp_embed.set_footer(text="Page {} of {}".format(current_page+1,len(page_list)))
    emoji1 = '\u2b05'
    emoji2 = '\u27a1'
    emoji_list = ["zero","one","two","three","four","five","six","seven","eight","nine"]
    emoji_react = getDefaultEmoji(emoji_list)
    def clearSetField(temp_embed:discord.Embed, field_list):
        temp_embed.clear_fields()
        count = 0
        for skills in field_list:
            temp_embed.add_field(value="[{}] {}".format(skills[1],skills[2]), name=emoji_react[count],inline=False)
            count = count +1
        return temp_embed
    
    temp_embed = clearSetField(temp_embed, field_list=page_list[current_page])
    temp_embed.set_image(url="attachment://temp.png")
    icons = get_units_image(page_list)
    msg = await ctx.send(embed=temp_embed, file=discord.File(icons, filename="temp.png"))
    
    await msg.add_reaction(emoji1)
    await msg.add_reaction(emoji2)
    for emoji in emoji_react:
        await msg.add_reaction(emoji)
    def check(payload):
        return ((str(payload.emoji) in emoji_react) or (str(payload.emoji) == emoji1) or (str(payload.emoji) == emoji2)) and payload.user_id !=client.user.id and payload.message_id == msg.id
    def wait_for_reaction(event_name):
        return client.wait_for(event_name,check=check)
    while True:
        pending_tasks = [wait_for_reaction("raw_reaction_add"), wait_for_reaction("raw_reaction_remove")]
        done_tasks, pending_tasks = await asyncio.wait(pending_tasks, timeout=60.0, return_when=asyncio.FIRST_COMPLETED)

        timeout = len(done_tasks) == 0

        if not timeout:
            task = done_tasks.pop()

            reaction = await task

        for remaining in itertools.chain(done_tasks, pending_tasks):
            remaining.cancel()

        if timeout:
            temp_embed.color = Status.KO.value
            await msg.edit(embed=temp_embed)
            break

        # left
        if str(reaction.emoji) == emoji1:
            if(current_page > 0):
                current_page = current_page -1
            else:
                current_page = len(page_list)-1
            temp_embed.set_footer(text="Page {} of {}".format(current_page+1,len(page_list)))
            temp_embed = clearSetField(temp_embed, field_list=page_list[current_page])
            await msg.edit(embed=temp_embed)
        # right
        if str(reaction.emoji) == emoji2:
            if( current_page+1 < len(page_list)):
                current_page = current_page +1
            else:
                current_page = 0
            temp_embed.set_footer(text="Page {} of {}".format(current_page+1,len(page_list)))
            temp_embed = clearSetField(temp_embed, field_list=page_list[current_page])
            await msg.edit(embed=temp_embed)
        if((str(reaction.emoji) in emoji_react)):
            if(len(page_list[current_page]) > emoji_react.index(reaction.emoji)):
                await msg.delete()
                await singleAdventurer(client, ctx, db,page_list[current_page][emoji_react.index(reaction.emoji)])
       

async def singleAdventurer(client, ctx, db,assistadventurerid):
    """This handles the logic of choosing of the character search and setting up
    for a single result search

    Arguments:
        client {discord.client} -- the discord bot object
        ctx {discord.context} -- command message context
        db {DBController.DBController} -- Database connector object
        assistadventurerid {int} -- the assist/adventurer id of the wanted search
    """
    is_embed = False
    is_files = False
    temp_embed = discord.Embed()
    dev_embed = discord.Embed()
    temp_embed.color = Status.OK.value
    dev_embed.color = Status.OK.value
    if "Ad" in (assistadventurerid)[3]:
        info = db.assembleAdventurer(((assistadventurerid)[3])[2:])
        #print(info)
        for adventurerdev in info[4]:
            dev_embed.add_field(name=adventurerdev[0], value=adventurerdev[1], inline=False)
        is_adv = True
    else:
        info = db.assembleAssist(((assistadventurerid)[3])[2:])
        #print(info)
        is_adv = False
    print(info)
    temp_embed.add_field(name="Stats", value=await assembleStats(info[3],0,"",0), inline=True)
    temp_embed.add_field(name="Abilities", value=await assembleAbilities(info[3],0,"",0), inline=True)
    temp_embed.title = info[1]
    dev_embed.title = info[1]
    for skills in info[2]:
        if skills[1] == "":
            temp_embed.add_field(name=skills[0], value="placeholder", inline=False)                
        else:
            temp_embed.add_field(name=skills[0], value=skills[1], inline=False)
            
    try:
        # images
        file_list = []
        # file_list.append(discord.File("./lottery/"+info[0], filename="hex.png"))
        character_name = info[1].split("]")[1][1:].split("\n")[0]
        character_title = info[1].split("[")[1].split("]")[0]
        folder_name = character_name + " [" + character_title + "]"
        print(folder_name)
        print("./images/units/"+ folder_name + "/hex.png")
        file_list.append(discord.File("./images/units/"+ folder_name + "/hex.png"))
        #file_list.append(discord.File("./lottery/"+info[0], filename="texture.png"))        
        file_list.append(discord.File("./images/units/"+ folder_name + "/all_rectangle.png"))
        temp_embed.set_thumbnail(url="attachment://hex.png")
        dev_embed.set_thumbnail(url="attachment://hex.png")
        temp_embed.set_image(url="attachment://all_rectangle.png")
        dev_embed.set_image(url="attachment://all_rectangle.png")
        is_files = True
    except:
        pass
    
    is_embed = True
    #try:
    if(is_embed and is_files):
        if(is_adv):
            await pageAdHandler(client, ctx, temp_embed,file_list, dev_embed,info[3], info[6], info[5])
        else:
            await pageASHandler(client, ctx,temp_embed,file_list,info[3])
    elif(is_embed):
        if(is_adv):
            await pageAdHandler(client, ctx, temp_embed,None, dev_embed,info[3], info[6], info[5])
        else:
            await pageASHandler(client, ctx,temp_embed,None,info[3])    

async def pageAdHandler(client, ctx, temp_embed:discord.Embed, file_list, dev_embed, stats_dict, unit_type,ascended):
    """This handles the logic of the page handling for the single result adventurer

    Arguments:
        client {discord.client} -- the discord bot object
        ctx {discord.context} -- command message context
        temp_embed {discord.embed} -- adventurer stats/skills page
        file_list {list of pictures} -- images to be displayed for pages
        dev_embed {discord.embed} -- the adventurer development page
        stats_dict {dict} -- the stats of the current unit
        unit_type {string} -- balance,physical,magical for stats calculation
        ascended {bool} -- adventurer has hero ascension or not
    """
    MAXLB = 5
    MAXHA = 6
    current_page = 0
    current_limitbreak = 0
    current_ha = 0
    page_list = [temp_embed, dev_embed]
    temp_embed.set_footer(text="Page {} of {}".format(current_page+1,len(page_list))) 

    emoji1 = '\u2b05'
    emoji2 = '\u27a1'
    limit_break_add = get_emoji("square_on").toString(ctx)
    limit_break_sub = get_emoji("square_off").toString(ctx)
    hero_ascend_add = get_emoji("star_on").toString(ctx)
    hero_ascend_sub = get_emoji("star_off").toString(ctx)
    async def updateStats():
        temp_embed.description = limit_break_add * current_limitbreak + limit_break_sub*(MAXLB-current_limitbreak)
        if(ascended):
            temp_embed.description = temp_embed.description + "    " + hero_ascend_add * current_ha + hero_ascend_sub*(MAXHA-current_ha)
        # Stats 
        temp_embed.set_field_at(0,name="Stats", value=await assembleStats(stats_dict,current_limitbreak,unit_type,current_ha), inline=True)
        # Abilities
        temp_embed.set_field_at(1,name="Abilities", value=await assembleAbilities(stats_dict,current_limitbreak,unit_type,current_ha), inline=True)
    await updateStats()
    if(file_list != None):
        msg = await ctx.send(files=file_list,embed=page_list[current_page])
    else:
        msg = await ctx.send(embed=page_list[current_page])
    await msg.add_reaction(emoji1)
    await msg.add_reaction(emoji2)
    await msg.add_reaction(limit_break_sub)
    await msg.add_reaction(limit_break_add)
    if(ascended):
        await msg.add_reaction(hero_ascend_sub)
        await msg.add_reaction(hero_ascend_add)

    # set_field_at(index, *, name, value, inline=True)
    def check(payload):
        
        return (str(payload.emoji) == emoji2 
                or str(payload.emoji) == emoji1 
                or str(payload.emoji) == hero_ascend_add
                or str(payload.emoji) == hero_ascend_sub
                or str(payload.emoji) == limit_break_add
                or str(payload.emoji) == limit_break_sub) and payload.user_id !=client.user.id and payload.message_id == msg.id
    
    def wait_for_reaction(event_name):
        return client.wait_for(event_name,check=check)


    while True:
        pending_tasks = [wait_for_reaction("raw_reaction_add"), wait_for_reaction("raw_reaction_remove")]
        done_tasks, pending_tasks = await asyncio.wait(pending_tasks, timeout=60.0, return_when=asyncio.FIRST_COMPLETED)

        timeout = len(done_tasks) == 0

        if not timeout:
            task = done_tasks.pop()

            reaction = await task

        for remaining in itertools.chain(done_tasks, pending_tasks):
            remaining.cancel()

        if timeout:
            page_list[current_page].color = Status.KO.value
            await msg.edit(embed=page_list[current_page])
            break

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
        if str(reaction.emoji) == limit_break_sub:
            if(current_limitbreak > 0):
                current_limitbreak = current_limitbreak -1
            else:
                current_limitbreak = MAXLB
            await updateStats()
        if str(reaction.emoji) == limit_break_add:
            if(current_limitbreak < MAXLB):
                current_limitbreak = current_limitbreak +1
            else:
                current_limitbreak = 0
            await updateStats()
        if str(reaction.emoji) == hero_ascend_sub and ascended:
            if(current_ha > 0):
                current_ha = current_ha -1
            else:
                current_ha = MAXHA
            await updateStats()
        if str(reaction.emoji) == hero_ascend_add and ascended:
            if(current_ha < MAXHA):
                current_ha = current_ha +1
            else:
                current_ha = 0
            await updateStats()
        page_list[current_page].set_footer(text="Page {} of {}".format(current_page+1,len(page_list)))            
        await msg.edit(embed=page_list[current_page])    


async def pageASHandler(client, ctx, temp_embed:discord.Embed, file_list, stats_dict):
    """This handles the logic of the page handling for the single result assist

    Arguments:
        client {discord.client} -- the discord bot object
        ctx {discord.context} -- command message context
        temp_embed {discord.embed} -- assist stats/skills page
        file_list {list of pictures} -- images to be displayed for pages
        stats_dict {dict} -- the stats of the current unit
    """
    MAXLB = 5
    current_page = 0
    current_limitbreak = 0
    current_ha = 0
    page_list = [temp_embed]
    temp_embed.set_footer(text="Page {} of {}".format(current_page+1,len(page_list))) 

    limit_break_add = get_emoji("square_on").toString(ctx)
    limit_break_sub = get_emoji("square_off").toString(ctx)
    async def updateStats():
        temp_embed.description = limit_break_add * current_limitbreak + limit_break_sub*(MAXLB-current_limitbreak)
        # Stats 
        temp_embed.set_field_at(0,name="Stats", value=await assembleStats(stats_dict,current_limitbreak,"",current_ha), inline=True)
        # Abilities
        temp_embed.set_field_at(1,name="Abilities", value=await assembleAbilities(stats_dict,current_limitbreak,"",current_ha), inline=True)
    await updateStats()
    msg = await ctx.send(files=file_list,embed=page_list[current_page])
    await msg.add_reaction(limit_break_sub)
    await msg.add_reaction(limit_break_add)
    # set_field_at(index, *, name, value, inline=True)
    def check(payload):
        return (str(payload.emoji) == limit_break_add
                or str(payload.emoji) == limit_break_sub) and payload.user_id !=client.user.id and payload.message_id == msg.id
    def wait_for_reaction(event_name):
        return client.wait_for(event_name,check=check)
    while True:
        pending_tasks = [wait_for_reaction("raw_reaction_add"), wait_for_reaction("raw_reaction_remove")]
        done_tasks, pending_tasks = await asyncio.wait(pending_tasks, timeout=60.0, return_when=asyncio.FIRST_COMPLETED)

        timeout = len(done_tasks) == 0

        if not timeout:
            task = done_tasks.pop()

            reaction = await task

        for remaining in itertools.chain(done_tasks, pending_tasks):
            remaining.cancel()

        if timeout:
            page_list[current_page].color = Status.KO.value
            await msg.edit(embed=page_list[current_page])
            break

        if str(reaction.emoji) == limit_break_sub:
            if(current_limitbreak > 0):
                current_limitbreak = current_limitbreak -1
            else:
                current_limitbreak = MAXLB
            await updateStats()
        if str(reaction.emoji) == limit_break_add:
            if(current_limitbreak < MAXLB):
                current_limitbreak = current_limitbreak +1
            else:
                current_limitbreak = 0
            await updateStats()
        page_list[current_page].set_footer(text="Page {} of {}".format(current_page+1,len(page_list)))
        await msg.edit(embed=page_list[current_page])    



async def assembleStats(stats_dict : dict, limitbreak:int,unit_type:str,heroascend:int):
    """ Calculates stats based on limit break and hero ascension (if avaliable)

    Arguments:
        stats_dict {dict} -- the stats dictionary
        limitbreak {int} -- the limit break of a unit, 0 = no LB, 5 = MLB
        unit_type {str} -- balance, physical, magical
        heroascend {int} -- the hero ascension #, 0 = no HA and 6 = MHA

    Returns:
        dict -- the stats dictionary
    """
    if (unit_type.lower() == "physical_type"):
        temp_hp = str(int(stats_dict.get("hp")[limitbreak]) + HeroAscensionStatsP.HP.value[heroascend])
        temp_mp = str(int(stats_dict.get("mp")[limitbreak]) + HeroAscensionStatsP.MP.value[heroascend])
        temp_pat = str(int(stats_dict.get("physical_attack")[limitbreak]) + HeroAscensionStatsP.PAT.value[heroascend])
        temp_mat = str(int(stats_dict.get("magic_attack")[limitbreak]) + HeroAscensionStatsP.MAT.value[heroascend])
        temp_def = str(int(stats_dict.get("defense")[limitbreak]) + HeroAscensionStatsP.DEF.value[heroascend])
    elif (unit_type.lower() == "magic_type"):
        temp_hp = str(int(stats_dict.get("hp")[limitbreak]) + HeroAscensionStatsM.HP.value[heroascend])
        temp_mp = str(int(stats_dict.get("mp")[limitbreak]) + HeroAscensionStatsM.MP.value[heroascend])
        temp_pat = str(int(stats_dict.get("physical_attack")[limitbreak]) + HeroAscensionStatsM.PAT.value[heroascend])
        temp_mat = str(int(stats_dict.get("magic_attack")[limitbreak]) + HeroAscensionStatsM.MAT.value[heroascend])
        temp_def = str(int(stats_dict.get("defense")[limitbreak]) + HeroAscensionStatsM.DEF.value[heroascend])
    # healer
    elif(unit_type.lower() == "healer_type"):
        temp_hp = str(int(stats_dict.get("hp")[limitbreak]) + HeroAscensionStatsH.HP.value[heroascend])
        temp_mp = str(int(stats_dict.get("mp")[limitbreak]) + HeroAscensionStatsH.MP.value[heroascend])
        temp_pat = str(int(stats_dict.get("physical_attack")[limitbreak]) + HeroAscensionStatsH.PAT.value[heroascend])
        temp_mat = str(int(stats_dict.get("magic_attack")[limitbreak]) + HeroAscensionStatsH.MAT.value[heroascend])
        temp_def = str(int(stats_dict.get("defense")[limitbreak]) + HeroAscensionStatsH.DEF.value[heroascend])
    # defense
    elif(unit_type.lower() == "defense_type"):
        temp_hp = str(int(stats_dict.get("hp")[limitbreak]) + HeroAscensionStatsD.HP.value[heroascend])
        temp_mp = str(int(stats_dict.get("mp")[limitbreak]) + HeroAscensionStatsD.MP.value[heroascend])
        temp_pat = str(int(stats_dict.get("physical_attack")[limitbreak]) + HeroAscensionStatsD.PAT.value[heroascend])
        temp_mat = str(int(stats_dict.get("magic_attack")[limitbreak]) + HeroAscensionStatsD.MAT.value[heroascend])
        temp_def = str(int(stats_dict.get("defense")[limitbreak]) + HeroAscensionStatsD.DEF.value[heroascend])
    # balance
    else:
        temp_hp = str(int(stats_dict.get("hp")[limitbreak]) + HeroAscensionStatsB.HP.value[heroascend])
        temp_mp = str(int(stats_dict.get("mp")[limitbreak]) + HeroAscensionStatsB.MP.value[heroascend])
        temp_pat = str(int(stats_dict.get("physical_attack")[limitbreak]) + HeroAscensionStatsB.PAT.value[heroascend])
        temp_mat = str(int(stats_dict.get("magic_attack")[limitbreak]) + HeroAscensionStatsB.MAT.value[heroascend])
        temp_def = str(int(stats_dict.get("defense")[limitbreak]) + HeroAscensionStatsB.DEF.value[heroascend])

    ret = ""
    ret = ret + "{} : {}\n".format("HP",temp_hp)
    ret = ret + "{} : {}\n".format("MP",temp_mp)
    ret = ret + "{} : {}\n".format("P.AT",temp_pat)
    ret = ret + "{} : {}\n".format("M.AT",temp_mat)
    ret = ret + "{} : {}\n".format("DEF",temp_def)
    return ret
async def assembleAbilities(stats_dict : dict,limitbreak:int,unit_type:str,heroascend:int):
    """ Calculates Abilities based on limit break and hero ascension (if avaliable)

    Arguments:
        stats_dict {dict} -- the stats dictionary
        limitbreak {int} -- the limit break of a unit, 0 = no LB, 5 = MLB
        unit_type {str} -- balance, physical, magical
        heroascend {int} -- the hero ascension #, 0 = no HA and 6 = MHA

    Returns:
        dict -- the stats dictionary
    """
    if (unit_type.lower() == "physical_type"):
        temp_str = str(int(stats_dict.get("strength")[limitbreak]) + HeroAscensionStatsP.STR.value[heroascend])
        temp_end = str(int(stats_dict.get("endurance")[limitbreak]) + HeroAscensionStatsP.END.value[heroascend])
        temp_dex = str(int(stats_dict.get("dexterity")[limitbreak]) + HeroAscensionStatsP.DEX.value[heroascend])
        temp_agi = str(int(stats_dict.get("agility")[limitbreak]) + HeroAscensionStatsP.AGI.value[heroascend])
        temp_mag = str(int(stats_dict.get("magic")[limitbreak]) + HeroAscensionStatsP.MAG.value[heroascend])
    elif (unit_type.lower() == "magic_type"):
        temp_str = str(int(stats_dict.get("strength")[limitbreak]) + HeroAscensionStatsM.STR.value[heroascend])
        temp_end = str(int(stats_dict.get("endurance")[limitbreak]) + HeroAscensionStatsM.END.value[heroascend])
        temp_dex = str(int(stats_dict.get("dexterity")[limitbreak]) + HeroAscensionStatsM.DEX.value[heroascend])
        temp_agi = str(int(stats_dict.get("agility")[limitbreak]) + HeroAscensionStatsM.AGI.value[heroascend])
        temp_mag = str(int(stats_dict.get("magic")[limitbreak]) + HeroAscensionStatsM.MAG.value[heroascend])
    elif (unit_type.lower() == "healer_type"):
        temp_str = str(int(stats_dict.get("strength")[limitbreak]) + HeroAscensionStatsH.STR.value[heroascend])
        temp_end = str(int(stats_dict.get("endurance")[limitbreak]) + HeroAscensionStatsH.END.value[heroascend])
        temp_dex = str(int(stats_dict.get("dexterity")[limitbreak]) + HeroAscensionStatsH.DEX.value[heroascend])
        temp_agi = str(int(stats_dict.get("agility")[limitbreak]) + HeroAscensionStatsH.AGI.value[heroascend])
        temp_mag = str(int(stats_dict.get("magic")[limitbreak]) + HeroAscensionStatsH.MAG.value[heroascend])
    elif (unit_type.lower() == "defense_type"):
        temp_str = str(int(stats_dict.get("strength")[limitbreak]) + HeroAscensionStatsD.STR.value[heroascend])
        temp_end = str(int(stats_dict.get("endurance")[limitbreak]) + HeroAscensionStatsD.END.value[heroascend])
        temp_dex = str(int(stats_dict.get("dexterity")[limitbreak]) + HeroAscensionStatsD.DEX.value[heroascend])
        temp_agi = str(int(stats_dict.get("agility")[limitbreak]) + HeroAscensionStatsD.AGI.value[heroascend])
        temp_mag = str(int(stats_dict.get("magic")[limitbreak]) + HeroAscensionStatsD.MAG.value[heroascend])
    else:
        temp_str = str(int(stats_dict.get("strength")[limitbreak]) + HeroAscensionStatsB.STR.value[heroascend])
        temp_end = str(int(stats_dict.get("endurance")[limitbreak]) + HeroAscensionStatsB.END.value[heroascend])
        temp_dex = str(int(stats_dict.get("dexterity")[limitbreak]) + HeroAscensionStatsB.DEX.value[heroascend])
        temp_agi = str(int(stats_dict.get("agility")[limitbreak]) + HeroAscensionStatsB.AGI.value[heroascend])
        temp_mag = str(int(stats_dict.get("magic")[limitbreak]) + HeroAscensionStatsB.MAG.value[heroascend])

    ret = ""
    ret = ret + "{} : {}\n".format("Str.",temp_str)
    ret = ret + "{} : {}\n".format("End.",temp_end)
    ret = ret + "{} : {}\n".format("Dex.",temp_dex)
    ret = ret + "{} : {}\n".format("Agi.",temp_agi)
    ret = ret + "{} : {}\n".format("Mag.",temp_mag)
    return ret


def get_units_image(page_list):
    images = []
    for page in page_list:
        for unit in page:
            path = "./images/units/"+unit[2]+" ["+unit[1]+"]/"
            if not os.path.isdir(path):
                print("Could not find folder:",path)
                path = "./images/units/gac_dummy/"
            path += "hex.png"

            image = Image.open(path)
            images.append(image)

    full_image = concatenate_images(images, per_line=5, white_background=False)
    return full_image

def concatenate_images(images, per_line=4, white_background=False):
    chunks = [images[x:x+per_line] for x in range(0, len(images), per_line)]

    images_lines = []
    for chunk in chunks:
        images_line = concatenate_images_horizontally(chunk,True,white_background)
        images_lines.append(images_line)

    full_image = concatenate_images_vertically(images_lines,True)
    return full_image

def concatenate_images_horizontally(images,to_bytes=False,white_background=False):
    widths, heights = zip(*(i.size for i in images))
    
    total_width = sum(widths)
    max_height = max(heights)
    
    new_im = Image.new("RGBA", (total_width, max_height))
    x_offset = 0
    for im in images:
        new_im.paste(im, (x_offset,0))
        x_offset += im.size[0]

    if white_background:
        new_im.load() # required for png.split()
        image = Image.new("RGB", new_im.size, (255, 255, 255))
        image.paste(new_im, mask=new_im.split()[3]) # 3 is the alpha channel
    else:
        image = new_im

    if to_bytes:
        return convert_to_bytes(image)
    else:
        return image

def concatenate_images_vertically(image_paths,to_bytes=False):
    images = [Image.open(x) for x in image_paths]
    widths, heights = zip(*(i.size for i in images))
    
    total_width = max(widths)
    max_height = sum(heights)
    
    new_im = Image.new('RGBA', (total_width, max_height))
    
    y_offset = 0
    for im in images:
        new_im.paste(im, (0,y_offset))
        y_offset += im.size[1]

    if to_bytes:
        return convert_to_bytes(new_im)
    else:
        return new_im

def convert_to_bytes(img):
    imgByteArr = io.BytesIO()
    img.save(imgByteArr, format='PNG')
    imgByteArr.seek(0)
    return imgByteArr