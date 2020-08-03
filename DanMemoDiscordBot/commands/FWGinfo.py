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

async def run(ctx,target):
    row = await calculateRowFWG(target)
    if(row != -1):
        gc = gspread.service_account(filename="./gspread.json")
        sh = gc.open("Imanity FWG")
        ws = sh.worksheet("Enemy Data")
        values_list = ws.row_values(row, value_render_option='FORMULA')

        temp_embed = discord.Embed()
        temp_embed.color = 3066993
        temp_embed.title = values_list[0]
        temp_embed.description = "Role: {}\n".format(values_list[2])
        temp_embed.add_field(name="Notes:",value=values_list[3],inline=False)
        temp_embed.add_field(name="Medals Left:",value=values_list[4],inline=False)
        temp_embed.add_field(name="Attacked By:",value=values_list[5],inline=False)
        temp_embed.add_field(name="Attacked:",value=values_list[6],inline=False)
        print(values_list)
        regex = r'"([^"]*)"'
        image_str = re.findall(regex, values_list[1])
        temp_embed.set_image(url=image_str[0].replace('"',""))
        await ctx.send(embed=temp_embed)
        print(values_list)
    # title = position
    # display medals left, notes
    # Display his team pic
    # display attacked by and attacked
    