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


async def run(ctx,target, note):
    curr_note = ""
    for words in note:
        curr_note = curr_note + words + " " 
    # get the row based on target
    row = await calculateRowFWG(target)
    # update note on the enemy
    if(row != -1):
        gc = gspread.service_account(filename="./gspread.json")
        sh = gc.open("Imanity FWG")
        ws = sh.worksheet("Enemy Data")
        cell_info = ws.cell(row, NOTE_COLUMN, value_render_option='UNFORMATTED_VALUE').value
        ws.update_cell(row,NOTE_COLUMN,cell_info + "\n•" + curr_note)
    if(row != -1):
        await ctx.message.add_reaction(getDefaultEmoji("white_check_mark"))
    else:
        await ctx.message.add_reaction(getDefaultEmoji("x"))