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
TEAM_PIC_COLUMN = 2

DISCORD_ID_COLUMN=1
DISCORD_MEMBER_NAME = 2
RUNS_COLUMN =3
ATTACKED_COLUMN=4
ATTACKED_BY_COLUMN=5
MEDAL_TOTAL_COLUMN=6
LIEUT_GEN_COLUMN = 3
ENEMY_MEDALS_LEFT = 5
ENEMY_ATTACKED_BY=6
TEAM_PIC_ALLY = 8
async def run(message, isally):
    # header
    errors = ""
    current_message = message.content.lower()
    row = await calculateRowFWG(current_message)
    # enemy team update
    if(row != -1 and isally == False):
        if(len(message.attachments) != 0):
            gc = gspread.service_account(filename="./gspread.json")
            sh = gc.open("Imanity FWG")
            ws = sh.worksheet("Enemy Data")
            cell_info = ""
            for attachment in message.attachments:
                cell_info = cell_info + '=IMAGE("{}",4,192,384)'.format(attachment.url) + "\n"
                # end of stages column after 
                ws.update_cell(row,TEAM_PIC_COLUMN,cell_info)
        else:
            errors = "no attachment found"
    # ally pic update
    elif(isally == True):
        gc = gspread.service_account(filename="./gspread.json")
        sh = gc.open("Imanity FWG")
        ws = sh.worksheet("Basic Data")
        values_list = ws.col_values(DISCORD_ID_COLUMN, value_render_option='UNFORMATTED_VALUE')
        discord_id = str(message.author.id)
        print(values_list)
        print(discord_id)
        if(discord_id in values_list):
            row = values_list.index(discord_id)+1
        else:
            row = len(remove_values_from_list(values_list,""))
            ws.update_cell(row, DISCORD_ID_COLUMN, discord_id)
            ws.update_cell(row, DISCORD_MEMBER_NAME, message.author.name)
        cell_info = ""
        # update ally pic
        for attachment in message.attachments:
                cell_info = cell_info + '=IMAGE("{}",4,192,384)'.format(attachment.url) + "\n"
                # end of stages column after 
                ws.update_cell(row,TEAM_PIC_ALLY,cell_info)
        

    if(errors == "" and row != -1):
        await message.add_reaction(getDefaultEmoji("white_check_mark"))
    else:
        await message.add_reaction(getDefaultEmoji("x"))