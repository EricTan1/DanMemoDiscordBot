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

MEDALS_LEFT_COLUMN = 5
POSITION_COLUMN = 1

async def run(ctx):
    gc = gspread.service_account(filename="./gspread.json")

    sh = gc.open("Imanity FWG")
    ws = sh.worksheet("Enemy Data")

    discordids = ws.col_values(POSITION_COLUMN, value_render_option='UNFORMATTED_VALUE')
    runs = ws.col_values(MEDALS_LEFT_COLUMN, value_render_option='UNFORMATTED_VALUE')
    print(discordids)
    print(runs)
    msg = "Enemies left:\n"
    for index in range(0,len(runs)):
        if(runs[index] != 0 and index < len(discordids) and (discordids[index].strip() != "" or discordids[index]!= None)):
            msg = msg + "**Position:** {} **Medals** Left: {}\n".format(discordids[index],runs[index])
    if(msg == "Enemies left:\n"):
        msg ="There are no more enemies left"
        await ctx.send(msg)
    else:
        await ctx.send(msg)
                
    