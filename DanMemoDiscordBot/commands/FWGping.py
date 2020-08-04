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
    ws = sh.worksheet("Basic Data")

    discordids = ws.col_values(1, value_render_option='UNFORMATTED_VALUE')
    runs = ws.col_values(3, value_render_option='UNFORMATTED_VALUE')
    print(discordids)
    print(runs)
    msg = "Please finish your runs before reset!\n"
    for index in range(0,len(runs)):
        if(isinstance(runs[index], int)):
            if(runs[index] != 0  and index < len(discordids) and discordids[index].strip() != "" and discordids[index]!= None):
                print(ctx.message)
                print(discordids[index].strip())
                print(ctx.message.guild)
                msg = msg + "<@!{}>\n".format(discordids[index])
                
    #temp_embed = discord.Embed()
    #temp_embed.color = 16203840
    #temp_embed.title = "Familia Rush Notice"
    #temp_embed.description= msg
    # everyone did their 4 runs
    if(msg == "Please finish your runs before reset!\n"):
        msg ="That was the last out of the 90 finest runs we had to offer! Was it enough to solidify our position as the greatest familia on the EU server? Yes? **Great! All according to plan!** Was it barely not good enough? Don't worry, operation #beatdivinemyth is still in progress. Strive to do even a little bit better than today, and we're sure to beat them eventually! がんばって!"
        await ctx.send(msg,files=[discord.File("./ngnl.jpg")])    # ping everyone who doesnt have runs ==0
    else:
        await ctx.send(msg)