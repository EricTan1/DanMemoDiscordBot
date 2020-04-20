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

from database.DBcontroller import DBcontroller
from database.entities.Adventurer import Adventurer, AdventurerSkill, AdventurerSkillEffects, AdventurerDevelopment, AdventurerStats
from database.entities.BaseConstants import Element, Target, Type, Attribute, Modifier
from commands.utils import imageHorizontalConcat, imageVerticalConcat, skillSearchRotatingPage

async def run(dbConfig, client, ctx, *search):
    print(search)
    my_search = ""
    for words in search:
        my_search= my_search + words + " "
    db = DBcontroller(dbConfig)
    
    skilleffects_id_list = db.skillSearch(my_search,{})
    print(skilleffects_id_list)
    
    
    my_set = set()
    message =""
    # image concat breaks if 0 results
    if(len(skilleffects_id_list) == 0):
        temp_embed = discord.Embed()
        temp_embed.color = 16203840
        temp_embed.title = "ERROR"
        temp_embed.description = "No results!"
        await ctx.send(embed=temp_embed)
    elif(len(skilleffects_id_list) <=100):
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
        dup_dict_ad = dict()
        dup_dict_as = dict()
        rotating_list.append(temp_list)
        # position  = len(rotating_list), len(temp_list)
        total_results = len(my_set)
        for skillid in my_set:
            if("Ad" in skillid):
                adventurerid = db.getAdventurerIdFromSkill(skillid[2:])
                if(adventurerid in dup_dict_ad):
                    count = count -1
                    total_results = total_results -1
                    skillinfo = db.assembleAdventurerSkill(skillid[2:])
                    (pos1,pos2) = dup_dict_ad.get(adventurerid)
                    # skill is on [1]
                    rotating_list[pos1][pos2][1] = rotating_list[pos1][pos2][1] + skillinfo[0]+skillinfo[1]+"\n"
                else:
                    #db.assembleAdventurerCharacterData(adventurerid)
                    skillinfo = db.assembleAdventurerSkill(skillid[2:])
                    #skillinfo[0]+skillinfo[1]+"\n"
                    names = db.assembleAdventurerCharacterName(adventurerid)
                    temp_list.append(["[{}] {}".format(names[0],names[1]),skillinfo[0]+skillinfo[1]+"\n"])
                    try:
                        file_name = "./lottery/"+"{} {}".format(names[0],names[1]).strip()+"/hex.png"
                        f = open(file_name,"r")
                        f.close()
                        file_list.append(file_name)
                    except:
                        file_list.append("./lottery/gac_dummy/hex.png")
                    dup_dict_ad[adventurerid] = (len(rotating_list)-1, len(temp_list)-1)
            elif("As" in skillid):
                assistid = db.getAssistIdFromSkill(skillid[2:])
                if(assistid in dup_dict_as):
                    count = count -1
                    total_results = total_results -1
                    skillinfo = db.assembleAssistSkill(skillid[2:])
                    (pos1,pos2) = dup_dict_as.get(assistid)
                    # skill is on [1]
                    rotating_list[pos1][pos2][1] = rotating_list[pos1][pos2][1] + skillinfo[0]+skillinfo[1]+"\n"
                else:
                    #db.assembleAssistCharacterData(assistid)
                    skillinfo=db.assembleAssistSkill(skillid[2:])
                    #skillinfo[0] + skillinfo[1]+"\n"
                    names = db.assembleAssistCharacterName(assistid)
                    temp_list.append(["[{}] {}".format(names[0],names[1]),skillinfo[0] + skillinfo[1]+"\n"])
                    try:
                        file_name = "./lottery/"+"{} {}".format(names[0],names[1]).strip()+"/hex.png"
                        f = open(file_name,"r")
                        f.close()
                        file_list.append(file_name)
                    except:
                        file_list.append("./lottery/gac_dummy/hex.png")
                    dup_dict_as[assistid] = (len(rotating_list)-1, len(temp_list)-1)
            else:
                skillinfo=db.assembleAdventurerDevelopment(skillid[2:])
                #skillinfo[0] + skillinfo[1]+"\n"
                temp_list.append([skillinfo[2],skillinfo[0] + "\n"+ skillinfo[1]+"\n"])
                try:
                    file_name = "./lottery/"+skillinfo[2].strip()+"/hex.png"
                    f = open(file_name,"r")
                    f.close()
                    file_list.append(file_name)
                except:
                    file_list.append("./lottery/gac_dummy/hex.png")                    
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
    else:
        temp_embed = discord.Embed()
        temp_embed.color = 16203840
        temp_embed.title = "ERROR"
        temp_embed.description = "Too many results please try to narrow it down further"
        await ctx.send(embed=temp_embed)        
    db.closeconnection()

