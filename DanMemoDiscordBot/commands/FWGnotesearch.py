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
import gspread

from commands.utils import calculateRowFWG,get_emoji,HeroAscensionStatsP,HeroAscensionStatsB,HeroAscensionStatsM,Status, HeroAscensionStatsD, HeroAscensionStatsH, getDefaultEmoji, createGSpreadJSON,remove_values_from_list
from database.DBcontroller import DBcontroller
from database.entities.Adventurer import Adventurer, AdventurerSkill, AdventurerSkillEffects, AdventurerDevelopment, AdventurerStats
from database.entities.BaseConstants import Element, Target, Type, Attribute, Modifier

NOTE_COLUMN = 4
POSITION_COLUMN = 1

async def run(ctx, search):
    curr_note = ""
    for words in search:
        curr_note = curr_note + words + " " 
    curr_note = curr_note.strip()
    print(curr_note)
    # get the row based on target
    #row = await calculateRowFWG(target)
    # update note on the enemy
    row = 0
    gc = gspread.service_account(filename="./gspread.json")
    sh = gc.open("Imanity FWG")
    ws = sh.worksheet("Enemy Data")
    note_list = ws.col_values(NOTE_COLUMN, value_render_option='UNFORMATTED_VALUE')
    position_list = ws.col_values(POSITION_COLUMN, value_render_option='UNFORMATTED_VALUE')
    print(note_list)    
    ret_list = []
    # search here
    for notes in range(1, len(position_list)):
        if(curr_note in note_list[notes]):
            # append (position, note for that position)
            ret_list.append((position_list[notes],note_list[notes].replace(curr_note,"**{}**".format(curr_note))))
    print(ret_list)

    temp_embed = discord.Embed()
    temp_embed.color = 3066993
    temp_embed.title = ""
    if(len(ret_list) > 0):
        for ret in ret_list:
            temp_embed.add_field(name="Role: {}".format(ret[0]),value="Note:\n{}".format(ret[1]),inline=False)
    else:
        temp_embed.description = "Can not find related notes for your search"

    await ctx.send(embed=temp_embed)