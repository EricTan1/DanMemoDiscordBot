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

from commands.utils import get_emoji,HeroAscensionStatsP,HeroAscensionStatsB,HeroAscensionStatsM,Status, HeroAscensionStatsD, HeroAscensionStatsH, getDefaultEmoji, createGSpreadJSON,remove_values_from_list
from database.DBcontroller import DBcontroller
from database.entities.Adventurer import Adventurer, AdventurerSkill, AdventurerSkillEffects, AdventurerDevelopment, AdventurerStats
from database.entities.BaseConstants import Element, Target, Type, Attribute, Modifier


async def run(client, ctx:commands.context, *search):
    """ record your mock run

    Arguments:
        client {discord.client} -- discord bot object
        ctx {commands.context} -- context of the message
        
        search {string} -- contains arguments on the info of your run

            arguments for search:
            <day> : 1-7
            <diff>: 20,40,60,80,100,110
            <stage>: 1,2,3
            <damage>: >=0 (you can write 13m or 13kk instead of 13000000)

            Search template:
            diff<diff> day<day> stage<stage> damage<damage>
    """
    current_user = ctx.message.author
    print("in")
    if(current_user.guild.id == 708002106245775410):
        has_access = False
        print("correct server")
        print(current_user.roles)
        for temp_roles in current_user.roles:
            if(temp_roles.id ==708008774140690473 or temp_roles.id == 708005221586042881):
                has_access = True
        if(has_access):
            errors = ""
            score_list = []
            # number converting and understanding
            for arguments in search:
                if("diff" in arguments or "difficulty" in arguments):
                    difficulty_list = [20,40,60,80,100,110]
                    difficulty = int(arguments.replace("difficulty","").replace("diff","").strip())
                    if (not difficulty in difficulty_list):
                        errors = "invalid difficulty please have a difficulty that is: 20,40,60,80,100 or 110"
                elif("st" in arguments or "stage" in arguments):
                    try:
                        stage = int(arguments.replace("stage","").replace("st","").strip())
                    except:
                        errors = "no decimals in stage"
                    if(stage > 3 or stage < 1):
                        errors = "Incorrect stage value please have a day between 1-3"
                elif("dmg" in arguments or "damage" in arguments):
                    score = arguments.replace("damage","").replace("dmg","").replace(",","").strip()
                    temp_scores = score.split("$")
                    for items in temp_scores:
                        temp_item = items.lower()
                        if("m" in items):
                            temp_item = temp_item.replace("m","")
                            temp_item = float(temp_item)*1000000
                        elif("kk" in temp_item):
                            temp_item = temp_item.replace("kk","")
                            temp_item = float(temp_item)*1000000
                        elif("k" in temp_item):
                            temp_item = temp_item.replace("k","")
                            temp_item = float(temp_item)*1000
                        try:
                            temp_item = int(temp_item)
                            score_list.append(temp_item)
                        except:
                            errors = "please have a numerical damage or have 'm', 'kk' or 'k' in the damage"
                        if(temp_item <0):
                            errors = "Negative damage"
                elif("d" in arguments or "day" in arguments):
                    print(arguments)
                    try:
                        day = int(arguments.replace("day","").replace("d","").strip())
                    except:
                        errors = "no decimals in days"
                    if(day > 7 or day < 1):
                        errors = "Incorrect day value please have a day between 1-7"
            if(errors != ""):
                temp_embed = discord.Embed()
                temp_embed.color = 16203840
                temp_embed.title = "Argument Error"
                temp_embed.description= errors
                await ctx.send(embed=temp_embed)
            else:
                try:
                    for scores in score_list:
                        await recordMockRun(ctx, current_user, day, stage, difficulty, scores)
                    await ctx.message.add_reaction(getDefaultEmoji("white_check_mark"))
                except:
                    await ctx.message.add_reaction(getDefaultEmoji("x"))
                    temp_embed = discord.Embed()
                    temp_embed.color = 16203840
                    temp_embed.title = "Argument Error"
                    temp_embed.description= "missing an argument"
                    await ctx.send(embed=temp_embed)

async def recordMockRun(ctx, user, day, stage, difficulty, score:int):
    """ the logic and recording of the spreadsheet

    Arguments:
        ctx {discord.context} -- discord message context object
        user {discord.user} -- the user that has sent the message
        day {int} -- the day of the run: 1,2,3,4,5,6,7
        stage {int} -- the stage # :1,2,3
        difficulty {int} -- difficulty of the FR stage : 20,40,60,80,100,110
        score {int} -- the score of the run
    """
    gc = gspread.service_account(filename="./gspread.json")

    sh = gc.open("Imanity FR")
    # update the DB first
    ws = sh.worksheet("Database")

    # headers
    # find the discord id. if it doesnt exist create one on the very bottom
    discord_ids = ws.col_values(1, value_render_option='UNFORMATTED_VALUE')
    print(discord_ids)
    # check if user exists. if not then create a new row
    if(str(user.id) in discord_ids):
        row = discord_ids.index(str(user.id))+1
    else:
        row = len(remove_values_from_list(discord_ids,""))*3
        ws.update_cell(row, 1, str(user.id))
        ws.update_cell(row, 2, user.name)
    # record the actual run
    current_row = row+stage-1
    scores = remove_values_from_list(ws.row_values(current_row, value_render_option='UNFORMATTED_VALUE'),"")
    print(scores)
    column = len(scores)+1
    if(stage != 1):
        column = column + 2
    print("{} {}".format(current_row, column))
    ws.update_cell(current_row, column, score)
    # green, blue, pink, orange, purple, yellow
    difficulty_color = {
        "20":{
        "red": 0.0,
        "green": 0.5,
        "blue": 0.0},
        "40":{
        "red": 0.1,
        "green": 0.5,
        "blue": 0.9},
        "60":{
        "red": 0.3,
        "green": 0.1,
        "blue": 0.6},
        "80":{
        "red": 0.9,
        "green": 0.5,
        "blue": 0.1},
        "100":{
        "red": 0.592,
        "green": 0.333,
        "blue": 0.705},
        "110":{
        "red": 0.58,
        "green": 0.2,
        "blue": 0.2}
    }
    print(str(difficulty))
    print(difficulty_color.get(str(difficulty)))
    temp_dict = {
        "backgroundColor": {
                "red": 0.86274509803,
                "green": 0.86274509803,
                "blue": 0.86274509803
        }
    }
    my_dict = dict()
    temp_dict["textFormat"] = my_dict
    my_dict["foregroundColor"] = difficulty_color.get(str(difficulty))
    
    temp_add =ws.cell(current_row, column).address
    ws.format(str(temp_add),temp_dict)
    ws = sh.worksheet("Basic Data")

    # update basic data sheet
    discord_ids = ws.col_values(1)
    print(discord_ids)
    # find the discord id. if it doesnt exist create one on the very bottom
    # check if user exists. if not then create a new row
    if(str(user.id) in discord_ids):
        row = discord_ids.index(str(user.id))+1
    else:
        row = len(remove_values_from_list(discord_ids,""))+3
        ws.update_cell(row, 1, str(user.id))
        ws.update_cell(row, 2, user.name)
        #print(ws.cell(row, 1).address)
    #update most recent
    column = stage*3
    # recent score
    ws.update_cell(row, column+3, score)
    # attachments
    if (len(ctx.message.attachments) != 0):
        cell_info = ""
        for attachment in ctx.message.attachments:
            cell_info = cell_info + '=IMAGE("{}")'.format(attachment.url) + "\n"
            # end of stages column after 
            ws.update_cell(row, 9+3+stage, cell_info)
