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

from database.DBcontroller import DBcontroller
from database.entities.Adventurer import Adventurer, AdventurerSkill, AdventurerSkillEffects, AdventurerDevelopment, AdventurerStats
from database.entities.BaseConstants import Element, Target, Type, Attribute, Modifier
from commands.utils import imageHorizontalConcat, imageVerticalConcat, get_emoji, Status
from commands.cache import Cache


async def run(dbConfig, client, ctx, *search):
    """ Skill Search
    <CommandPrefix> <Search>
    
    Arguments:
        dbConfig {[DBcontroller.dbConfig]} -- Database config usually local/environmental variables
        client {[discord.Client]} -- the discord bot object
        ctx {[discord.context]} -- command message context
    """


    my_search = ""
    for words in search:
        my_search= my_search + words + " "
    db = DBcontroller(dbConfig)
    
    skilleffects_id_list = db.skillSearch(my_search,{})
    print(skilleffects_id_list)
    message =""
    # image concat breaks if 0 results
    if(len(skilleffects_id_list) == 0):
        temp_embed = discord.Embed()
        temp_embed.color = 16203840
        temp_embed.title = "ERROR"
        temp_embed.description = "No results!"
        await ctx.send(embed=temp_embed)
    else:
        rotating_list = []
        count = 0
        temp_list = []
        file_list = []
        discord_file_list = []
        dup_dict_ad = dict()
        dup_dict_as = dict()
        rotating_list.append(temp_list)
        # position  = len(rotating_list), len(temp_list)
        total_results = len(skilleffects_id_list)
        for skillid in skilleffects_id_list:
            if("Ad" in skillid):
                adventurerid = db.getAdventurerIdFromSkill(skillid[2:])
                if(adventurerid in dup_dict_ad):
                    count = count -1
                    total_results = total_results -1
                    skillinfo = db.assembleAdventurerSkill(skillid[2:])
                    (pos1,pos2) = dup_dict_ad.get(adventurerid)
                    # skill is on [1]
                    rotating_list[pos1][pos2][1] = rotating_list[pos1][pos2][1] +"***{}***\n".format(skillinfo[0].strip()) + "\n"+skillinfo[1]+"\n"
                else:
                    #db.assembleAdventurerCharacterData(adventurerid)
                    skillinfo = db.assembleAdventurerSkill(skillid[2:])
                    #skillinfo[0]+skillinfo[1]+"\n"
                    names = db.assembleAdventurerCharacterName(adventurerid)
                    # [TITLE + NAME, SKILL INFO, FILTERS]
                    temp_list.append(["__**[{}] {}**__".format(names[0],names[1]),"***{}***\n".format(skillinfo[0].strip()) + "\n"+skillinfo[1]+"\n",["adventurer"]])
                    try:
                        file_name = "./images/units/"+"{} [{}]".format(names[1],names[0]).strip()+"/hex.png"
                        f = open(file_name,"r")
                        f.close()
                        file_list.append(file_name)
                    except:
                        file_list.append("./images/units/gac_dummy/hex.png")
                    dup_dict_ad[adventurerid] = (len(rotating_list)-1, len(temp_list)-1)
            elif("As" in skillid):
                assistid = db.getAssistIdFromSkill(skillid[2:])
                if(assistid in dup_dict_as):
                    count = count -1
                    total_results = total_results -1
                    skillinfo = db.assembleAssistSkill(skillid[2:])
                    (pos1,pos2) = dup_dict_as.get(assistid)
                    # skill is on [1]
                    rotating_list[pos1][pos2][1] = rotating_list[pos1][pos2][1] + "***{}***\n".format(skillinfo[0].strip())+skillinfo[1]+"\n"
                else:
                    #db.assembleAssistCharacterData(assistid)
                    skillinfo=db.assembleAssistSkill(skillid[2:])
                    #skillinfo[0] + skillinfo[1]+"\n"
                    names = db.assembleAssistCharacterName(assistid)
                    temp_list.append(["__**[{}] {}**__".format(names[0],names[1]),"***{}***\n".format(skillinfo[0].strip()) + skillinfo[1]+"\n",["assist"]])
                    try:
                        file_name = "./images/units/"+"{} [{}]".format(names[1],names[0]).strip()+"/hex.png"
                        f = open(file_name,"r")
                        f.close()
                        file_list.append(file_name)
                    except:
                        file_list.append("./images/units/gac_dummy/hex.png")
                    dup_dict_as[assistid] = (len(rotating_list)-1, len(temp_list)-1)
            else:
                skillinfo=db.assembleAdventurerDevelopment(skillid[2:])
                adventurerid = skillinfo[4]
                if(adventurerid in dup_dict_ad):
                    count = count -1
                    total_results = total_results -1
                    (pos1,pos2) = dup_dict_ad.get(adventurerid)
                    # skill is on [1]
                    rotating_list[pos1][pos2][1] = rotating_list[pos1][pos2][1] + skillinfo[0].strip() + "\n"+skillinfo[1]+"\n"
                else:
                    temp_list.append(["[{}] {}".format(skillinfo[2],skillinfo[3]),skillinfo[0] + "\n"+ skillinfo[1]+"\n",["adventurer"],"{} {}".format(skillinfo[2],skillinfo[3]).strip()])
                    try:
                        file_name = "./images/units/{} [{}]".format(skillinfo[3],skillinfo[2]).strip()+"/hex.png"
                        f = open(file_name,"r")
                        f.close()
                        file_list.append(file_name)
                    except:
                        file_list.append("./images/units/gac_dummy/hex.png")
            count = count +1
            if(count ==4):
                await imageHorizontalConcat(client,file_list,discord_file_list)
                temp_list = []
                file_list= []                
                rotating_list.append(temp_list)
                count=0
                
        # remove last empty list
        if(len(rotating_list[len(rotating_list)-1]) == 0):
            rotating_list.pop(len(rotating_list)-1)
        elif(len(rotating_list[len(rotating_list)-1]) < 4):
            await imageHorizontalConcat(client,file_list,discord_file_list)
        icons = await imageVerticalConcat(client,discord_file_list)
        await skillSearchRotatingPage(client,ctx,search,rotating_list,total_results,icons)
    db.closeconnection()

async def skillSearchRotatingPage(client, ctx, search, page_list, total_results, icons):
    """This handles the message scrolling of the skill search and all the other
    page logic

    Arguments:
        client {discord.client} -- the discord bot object
        ctx {discord.context} -- command message context
        search {string} -- the search query
        page_list {list of list} -- list of pages, Pages are lists with skills. Skills are tuples with [TITLE + NAME, SKILL INFO, FILTERS]
        total_results {int} -- total number of results from the query
        icons {BytesIO} -- image for the characters being searched
    """
    filters = []
    current_page_list = page_list
    current_page = 0
    
    def filterAddRemove(name):
        if name in filters:
            filters.remove(name)
        else:
            filters.append(name)
        current_page_list = []
        print(filters)
        temp_page = []
        current_page_list.append(temp_page)
        for pages in page_list:
            for skills in pages:
                is_filtered = True
                for items in filters:
                    if(not(items in skills[2])):
                        is_filtered = False
                if is_filtered:
                    temp_page.append(skills)
                if len(temp_page) == 4:
                    temp_page =[]
                    current_page_list.append(temp_page)
        print(current_page_list)
        # remove last empty list
        if(len(current_page_list[len(current_page_list)-1]) == 0):
            current_page_list.pop(len(current_page_list)-1)
        return current_page_list
    temp_image_url = "attachment://"
    # set up
    temp_embed = discord.Embed()
    temp_embed.set_image(url=temp_image_url+"temp.png")
    
    temp_embed.color = 3066993
    temp_embed.title = "{} results for {}".format(str(total_results),search)
    if(len(current_page_list) == 0):
        current_page_list.append([["No relevant skills to display","End of List"]])
    temp_embed.set_footer(text="Page {} of {}".format(current_page+1,len(current_page_list)))

    def clearSetField(temp_embed:discord.Embed, field_list):
        temp_embed.description = "**Current Filters:** {}".format(str(filters))
        temp_embed.clear_fields()
        for skills in field_list:
            temp_embed.add_field(value=skills[1], name=skills[0],inline=False)
        return temp_embed
    
    temp_embed = clearSetField(temp_embed, field_list=current_page_list[current_page])
    msg = await ctx.send(embed=temp_embed, file=discord.File(icons, filename="temp.png"))
    emoji1 = '\u2b05'
    emoji2 = '\u27a1'
    ad_filter = get_emoji("ad_filter").toString(ctx)
    as_filter = get_emoji("as_filter").toString(ctx)
    await msg.add_reaction(emoji1)
    await msg.add_reaction(emoji2)
    await msg.add_reaction(ad_filter)
    await msg.add_reaction(as_filter)

    emojis = [emoji1, emoji2]
    def check(reaction, user):
                return (str(reaction.emoji) == emoji2 or 
                str(reaction.emoji) == emoji1 or 
                str(reaction.emoji)==ad_filter or 
                str(reaction.emoji)==as_filter) and user !=client.user and reaction.message.id == msg.id

    
    def wait_for_reaction(event_name):
        return client.wait_for(event_name,check=check)


    while True:
        pending_tasks = [wait_for_reaction("reaction_add"), wait_for_reaction("reaction_remove")]
        done_tasks, pending_tasks = await asyncio.wait(pending_tasks, timeout=60.0, return_when=asyncio.FIRST_COMPLETED)

        timeout = len(done_tasks) == 0

        if not timeout:
            task = done_tasks.pop()

            reaction, user = await task

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
                current_page = len(current_page_list)-1
        # right
        if str(reaction.emoji) == emoji2:
            if( current_page+1 < len(current_page_list)):
                current_page = current_page +1
            else:
                current_page = 0
        # FILTERS
        if str(reaction.emoji) == ad_filter:
            current_page_list = filterAddRemove("adventurer")
            current_page = 0
        if str(reaction.emoji) == as_filter:
            current_page_list = filterAddRemove("assist")
            current_page = 0
        if(len(current_page_list) == 0):
            current_page_list.append([["No relevant skills to display","End of List"]])
        temp_embed.set_footer(text="Page {} of {}".format(current_page+1,len(current_page_list)))
        temp_embed = clearSetField(temp_embed, field_list=current_page_list[current_page])
        await msg.edit(embed=temp_embed)     