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
DISCORD_ID_COLUMN=1
DISCORD_MEMBER_NAME = 2
RUNS_COLUMN =3
ATTACKED_COLUMN=4
ATTACKED_BY_COLUMN=5
MEDAL_TOTAL_COLUMN=6
LIEUT_GEN_COLUMN = 3
ENEMY_MEDALS_LEFT = 5
ENEMY_ATTACKED_BY=6
ATTACK_SUGGESTION_COLUMN = 7

async def run(ctx,ally:discord.Member,enemy):
    # check if valid enemy
    enemy_row = await calculateRowFWG(enemy)
    if(enemy_row != -1):
        # check if discord id inside the spreadsheet if not then add it with first time set up
        gc = gspread.service_account(filename="./gspread.json")
        sh = gc.open("Imanity FWG")
        ws = sh.worksheet("Basic Data")
        values_list = ws.col_values(DISCORD_ID_COLUMN, value_render_option='FORMULA')
        print(values_list)
        discord_id = ally.id
        if(discord_id in values_list):
            row = values_list.index(discord_id)
        else:
            row = len(remove_values_from_list(values_list,""))-1
            ws.update_cell(row, DISCORD_ID_COLUMN, discord_id)
            ws.update_cell(row, DISCORD_MEMBER_NAME, ally.nick)
        # get all current suggestions and add on to it
        curr_suggestions = ws.cell(row, ATTACK_SUGGESTION_COLUMN, value_render_option='UNFORMATTED_VALUE').value
        ws.update_cell(row, ATTACK_SUGGESTION_COLUMN, "{}\n{}".format(curr_suggestions,enemy))
