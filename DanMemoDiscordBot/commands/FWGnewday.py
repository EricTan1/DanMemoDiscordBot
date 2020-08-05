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

async def run(ctx):
    gc = gspread.service_account(filename="./gspread.json")
    sh = gc.open("Imanity FWG")
    #ENEMY DATA WIPE
    ws = sh.worksheet("Enemy Data")

    wipeRow(ws,"B2","B31","",30)
    wipeRow(ws,"C2","C31","",30)
    wipeRow(ws,"D2","D31","",30)
    wipeRow(ws,"E2","E31","",30)
    wipeRow(ws,"F2","F31","",30)
    wipeRow(ws,"G2","G31","",30)

    ws = sh.worksheet("Basic Data")
    wipeRow(ws,"C2","C31",3,30)
    wipeRow(ws,"D2","D31","",30)
    wipeRow(ws,"E2","E31","",30)
    wipeRow(ws,"G2","G31","",30)

    await ctx.message.add_reaction(getDefaultEmoji("white_check_mark"))


def wipeRow(ws,start,end,value,times):
    cell_list = ws.range('{}:{}'.format(start,end))
    cell_values = [value]*times
    for i, val in enumerate(cell_values):
        cell_list[i].value = val
    
    ws.update_cells(cell_list)