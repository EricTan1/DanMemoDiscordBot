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
ATTACK_SUGGESTION_COLUMN = 7
MEDAL_TOTAL_COLUMN=6
LIEUT_GEN_COLUMN = 3
ENEMY_MEDALS_LEFT = 5
ENEMY_ATTACKED_BY=6
async def run(ctx,optional):
    # check if discord id inside the spreadsheet if not then add it with first time set up
    gc = gspread.service_account(filename="./gspread.json")
    sh = gc.open("Imanity FWG")
    ws = sh.worksheet("Basic Data")
    values_list = ws.col_values(DISCORD_ID_COLUMN, value_render_option='FORMULA')
    print(values_list)
    if(optional != None):
        discord_id = optional.id
    else:
        discord_id = ctx.message.author.id
    if(discord_id in values_list):
        row = values_list.index(discord_id)
    else:
        row = len(remove_values_from_list(values_list,""))-1
        ws.update_cell(row, DISCORD_ID_COLUMN, discord_id)
        ws.update_cell(row, DISCORD_MEMBER_NAME, ctx.message.author.nick)
    values_list = ws.row_values(row, value_render_option='FORMULA')
    temp_embed = discord.Embed()
    temp_embed.color = 3066993
    temp_embed.title = values_list[0]
    temp_embed.description = "Medals Gained Total{}\n".format(values_list[MEDAL_TOTAL_COLUMN-1])
    temp_embed.add_field(name="Attack Suggestion (Made by Heart):",value=values_list[ATTACK_SUGGESTION_COLUMN-1],inline=False)
    temp_embed.add_field(name="Attacked:",value=values_list[ATTACKED_COLUMN-1],inline=False)    
    temp_embed.add_field(name="Attacked By:",value=values_list[ATTACKED_BY_COLUMN-1],inline=False)    
    await ctx.send(embed=temp_embed)
    # Display your runs, who you were attacked by, attacked and attack suggestion from heart