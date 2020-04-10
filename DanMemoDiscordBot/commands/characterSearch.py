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

async def run(dbConfig, ctx, *search):
    is_embed = False
    is_files = False

    my_search = " "
    for words in search:
        my_search = my_search + words + " "

    db = DBcontroller(dbConfig)
    my_list = db.characterSearch(my_search,{})
    print(my_list)

    message = ""

    # exactly 1 result then display
    if len(my_list) == 0:
        message = "Sorry there are no results"
    elif len(my_list) == 1:
        temp_embed = discord.Embed()
        temp_embed.color = 3066993
        if "Ad" in (my_list[0])[3]:
            info = db.assembleAdventurer(((my_list[0])[3])[2:])
        else:
            info = db.assembleAssist(((my_list[0])[3])[2:])
        temp_embed.title = info[1]
        for skills in info[2]:
            if skills[1] == "":
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
