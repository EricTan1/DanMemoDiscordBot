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
DISCORD_ID_COLUMN=1
DISCORD_MEMBER_NAME = 2
RUNS_COLUMN =3
ATTACKED_COLUMN=4
ATTACKED_BY_COLUMN=5
ATTACK_SUGGESTION_COLUMN = 7
MEDAL_TOTAL_COLUMN=6
LIEUT_GEN_COLUMN = 3
ENEMY_MEDALS_LEFT = 5
ENEMY_ATTACKED_BY=6
TEAM_PIC=8
async def run(ctx,optional):
    # check if discord id inside the spreadsheet if not then add it with first time set up
    gc = gspread.service_account(filename="./gspread.json")
    sh = gc.open("Imanity FWG")
    ws = sh.worksheet("Basic Data")
    values_list = ws.col_values(DISCORD_ID_COLUMN, value_render_option='UNFORMATTED_VALUE')
    print(optional)
    if(optional != None and optional != tuple()):
        discord_id = str(optional[0].id)
    else:
        discord_id = str(ctx.message.author.id)
    if(discord_id in values_list):
        row = values_list.index(discord_id)+1
    else:
        row = len(remove_values_from_list(values_list,""))
        ws.update_cell(row, DISCORD_ID_COLUMN, discord_id)
        ws.update_cell(row, DISCORD_MEMBER_NAME, ctx.message.author.name)
    temp_embed = discord.Embed()
    temp_embed.color = 3066993
    temp_embed.title = ws.cell(row, DISCORD_MEMBER_NAME, value_render_option='UNFORMATTED_VALUE').value

    medals_gained = ws.cell(row, MEDAL_TOTAL_COLUMN, value_render_option='UNFORMATTED_VALUE').value
    temp_embed.description = "Medals Gained Total: {}\n".format(medals_gained)

    attack_suggest = ws.cell(row, ATTACK_SUGGESTION_COLUMN, value_render_option='UNFORMATTED_VALUE').value
    if(attack_suggest != ""):
        temp_embed.add_field(name="Attack Suggestion (Made by Heart):",value=attack_suggest,inline=False)
    
    attacked = ws.cell(row, ATTACKED_COLUMN, value_render_option='UNFORMATTED_VALUE').value
    if(attacked != ""):
        temp_embed.add_field(name="Attacked:",value=attacked,inline=False)
    
    attacked_by = ws.cell(row, ATTACKED_BY_COLUMN, value_render_option='UNFORMATTED_VALUE').value
    if(attacked_by != ""):
        temp_embed.add_field(name="Attacked By:",value=attacked_by,inline=False)    
    
    regex = r'"([^"]*)"'
    image = ws.cell(row, TEAM_PIC, value_render_option='FORMULA').value
    image_str = re.findall(regex, image)
    if(len(image_str) != 0):
        temp_embed.set_image(url=image_str[0].replace('"',""))
    await ctx.send(embed=temp_embed)
    # Display your runs, who you were attacked by, attacked and attack suggestion from heart