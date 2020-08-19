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

async def run(message):
    # header
    errors = ""
    current_message = message.content.lower()
    row = await calculateRowFWG(current_message)
    if(row != -1):
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
    if(errors == "" and row != -1):
        await message.add_reaction(getDefaultEmoji("white_check_mark"))
    else:
        await message.add_reaction(getDefaultEmoji("x"))