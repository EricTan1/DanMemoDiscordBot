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

async def run(dbConfig, client, ctx, *search):
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
        dev_embed = discord.Embed()
        temp_embed.color = 3066993
        dev_embed.color = 3066993
        if "Ad" in (my_list[0])[3]:
            info = db.assembleAdventurer(((my_list[0])[3])[2:])
            for adventurerdev in info[3]:
                dev_embed.add_field(name=adventurerdev[0], value=adventurerdev[1], inline=False)
            is_adv = True
        else:
            info = db.assembleAssist(((my_list[0])[3])[2:])
            is_adv = False
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
            file_list.append(discord.File("./lottery/"+info[0]+"/hex.png"))
            #file_list.append(discord.File("./lottery/"+info[0], filename="texture.png"))        
            file_list.append(discord.File("./lottery/"+info[0] + "/texture.png"))
            temp_embed.set_thumbnail(url="attachment://hex.png")
            dev_embed.set_thumbnail(url="attachment://hex.png")
            temp_embed.set_image(url="attachment://texture.png")
            dev_embed.set_image(url="attachment://texture.png")
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
    #try:
    if(is_embed and is_files):
        if(is_adv):
            await pageHandler(client, ctx, temp_embed,file_list, dev_embed)
        else:
            await ctx.send(files=file_list,embed=temp_embed)
    elif(is_embed):
        await ctx.send(embed=temp_embed)
    elif(is_files):
        await ctx.send(files=file_list)
    else:         
        await ctx.send(message)
    #except:
        #await ctx.send("Sorry unable to find results")
    db.closeconnection()

async def pageHandler(client, ctx, temp_embed, file_list, dev_embed):
    current_page = 0
    page_list = [temp_embed, dev_embed]
    temp_embed.set_footer(text="Page {} of {}".format(current_page+1,len(page_list)))    
    msg = await ctx.send(files=file_list,embed=page_list[current_page])
    
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
            page_list[current_page].color=16203840
            await msg.edit(embed=page_list[current_page])
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
            page_list[current_page].set_footer(text="Page {} of {}".format(current_page+1,len(page_list)))            
            await msg.edit(embed=page_list[current_page])    
    