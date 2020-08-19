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
import re

from commands.utils import calculateRowFWG,get_emoji,HeroAscensionStatsP,HeroAscensionStatsB,HeroAscensionStatsM,Status, HeroAscensionStatsD, HeroAscensionStatsH, getDefaultEmoji, createGSpreadJSON,remove_values_from_list
from database.DBcontroller import DBcontroller
from database.entities.Adventurer import Adventurer, AdventurerSkill, AdventurerSkillEffects, AdventurerDevelopment, AdventurerStats
from database.entities.BaseConstants import Element, Target, Type, Attribute, Modifier
LIEUT_GEN_COLUMN = 3
NOTES_COLUMN = 4
ENEMY_MEDALS_LEFT = 5
ENEMY_ATTACKED_BY=6
ENEMY_ATTACKED = 7
POSITION = 1
TEAM_PIC = 2

async def run(ctx,target):
    row = await calculateRowFWG(target)
    if(row != -1):
        gc = gspread.service_account(filename="./gspread.json")
        sh = gc.open("Imanity FWG")
        ws = sh.worksheet("Enemy Data")
        
        temp_embed = discord.Embed()
        temp_embed.color = 3066993
        temp_embed.title = ws.cell(row, POSITION, value_render_option='UNFORMATTED_VALUE').value
        
        role = ws.cell(row, LIEUT_GEN_COLUMN, value_render_option='UNFORMATTED_VALUE').value
        temp_embed.description = "Role: {}\n".format(role)
        note = role = ws.cell(row, NOTES_COLUMN, value_render_option='UNFORMATTED_VALUE').value
        if(note != ""):
            temp_embed.add_field(name="Notes:",value=note,inline=False)
        medals_left = role = ws.cell(row, ENEMY_MEDALS_LEFT, value_render_option='UNFORMATTED_VALUE').value
        if(medals_left != ""):
            temp_embed.add_field(name="Medals Left:",value=medals_left,inline=False)
        attack_by = role = ws.cell(row, ENEMY_ATTACKED_BY, value_render_option='UNFORMATTED_VALUE').value
        if(attack_by != ""):
            temp_embed.add_field(name="Attacked By:",value=attack_by,inline=False)
        attacked = role = ws.cell(row, ENEMY_ATTACKED, value_render_option='UNFORMATTED_VALUE').value
        if(attacked != ""):
            temp_embed.add_field(name="Attacked:",value=attacked,inline=False)
        regex = r'"([^"]*)"'
        
        image = ws.cell(row, TEAM_PIC, value_render_option='FORMULA').value
        image_str = re.findall(regex, image)
        if(len(image_str) != 0):
            temp_embed.set_image(url=image_str[0].replace('"',""))
        await ctx.send(embed=temp_embed)
    # title = position
    # display medals left, notes
    # Display his team pic
    # display attacked by and attacked
    