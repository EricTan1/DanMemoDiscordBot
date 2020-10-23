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

from commands.utils import get_emoji,HeroAscensionStatsP,HeroAscensionStatsB,HeroAscensionStatsM,Status, HeroAscensionStatsD, HeroAscensionStatsH, getDefaultEmoji, createGSpreadJSON
from database.DBcontroller import DBcontroller
from database.entities.Adventurer import Adventurer, AdventurerSkill, AdventurerSkillEffects, AdventurerDevelopment, AdventurerStats
from database.entities.BaseConstants import Element, Target, Type, Attribute, Modifier


async def run(client, ctx:commands.context, *search):
    """ ping everyone who hasn't done all their runs

    Arguments:
        client {discord.client} -- discord bot object
        ctx {commands.context} -- context of the message
    """
    overkill=False
    # stage 1, stage 2, stage 3
    stage_roles = [712986243712942141,712986411040768060,712986433123516488]
    temp_search = 0
    if len(search) >= 1:
        if search[0] == "1" or search[0] == "2" or search[0] == "3" or search[0].lower() == "stage1" or search[0].lower() == "stage2" or search[0].lower() == "stage3":
            temp_search = int(search[0].replace("stage",""))
            msg = "Stage {} is up! Please try to leave 1 run for overkill if you can\n".format(temp_search)
        # OK etc
        if(len(search) == 2):
            if(search[1].lower()=="overkill" or search[1].lower()=="ok"):
                msg = "Please prepare for Stage {} Overkill\n".format(temp_search)
                overkill=True
    else:
        msg = "Please finish your runs before reset!\n"
    current_user = ctx.message.author
    print("in")
    if(current_user.guild.id == 708002106245775410):
        has_access = False
        for temp_roles in current_user.roles:
            if(temp_roles.id == 708008774140690473):
                has_access = True
        if(has_access):
            gc = gspread.service_account(filename="./gspread.json")

            sh = gc.open("Imanity FR")
            ws = sh.worksheet("Basic Data")

            discordids = ws.col_values(1, value_render_option='UNFORMATTED_VALUE')
            runs = ws.col_values(3, value_render_option='UNFORMATTED_VALUE')
            print(discordids)
            print(runs)
            for index in range(0,len(runs)):
                if(isinstance(runs[index], int)):
                    if(runs[index] != 0 and runs[index] <= 4 and index < len(discordids) and (discordids[index].strip() != "" or discordids[index]!= None)):
                        member = ctx.message.guild.get_member(int(discordids[index]))
                        if(member != None):
                            if(temp_search!=0):
                                for temp_roles in member.roles:
                                    if(temp_roles.id == stage_roles[temp_search-1]):
                                        #OK = 1 run or more, not OK = 2 runs at least
                                        if overkill == False and runs[index] >1:
                                            msg = msg + "<@!{}>\n".format(discordids[index])
                                        elif overkill == True:
                                            msg = msg + "<@!{}>\n".format(discordids[index])
                            else:
                                msg = msg + "<@!{}>\n".format(discordids[index])
            #temp_embed = discord.Embed()
            #temp_embed.color = 16203840
            #temp_embed.title = "Familia Rush Notice"
            #temp_embed.description= msg
            # everyone did their 4 runs
            #if(msg == "Please finish your runs before reset!\n"):
                #msg ="That was the last out of the 120 finest runs we had to offer! Was it enough to solidify our position as the greatest familia on the EU server? Yes? **Great! All according to plan!** Was it barely not good enough? Don't worry, operation #beatdivinemyth is still in progress. Strive to do even a little bit better than today, and we're sure to beat them eventually! がんばって!"
            await ctx.send(msg)
            #else:
                #await ctx.send(msg,files=[discord.File("./ngnl.jpg")])