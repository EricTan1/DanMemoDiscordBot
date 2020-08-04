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
MEDAL_TOTAL_COLUMN=6
LIEUT_GEN_COLUMN = 3
ENEMY_MEDALS_LEFT = 5
ENEMY_ATTACKED_BY=6
async def run(client,ctx,target,medals:int):
    enemy_row = await calculateRowFWG(target)
    if(enemy_row != -1):
        # check if discord id inside the spreadsheet if not then add it with first time set up
        gc = gspread.service_account(filename="./gspread.json")
        sh = gc.open("Imanity FWG")
        ws = sh.worksheet("Basic Data")
        values_list = ws.col_values(DISCORD_ID_COLUMN, value_render_option='UNFORMATTED_VALUE')
        discord_id = str(ctx.message.author.id)
        msg = ctx.message
        print(values_list)
        print(discord_id)
        if(discord_id in values_list):
            row = values_list.index(discord_id)+1
        else:
            row = len(remove_values_from_list(values_list,""))
            ws.update_cell(row, DISCORD_ID_COLUMN, discord_id)
            ws.update_cell(row, DISCORD_MEMBER_NAME, ctx.message.author.name)
        # add one to medals (default whenever you run 1)
        # subtract run if equal to 0 then warn user
        # check if there are any runs left
        runs = ws.cell(row, RUNS_COLUMN, value_render_option='UNFORMATTED_VALUE').value
        is_medal = True
        # if its 0 give error msg
        if (str(runs) == "0"):
            await ctx.send("Unable to record runs because you have 0 left")
            await ctx.message.add_reaction(getDefaultEmoji("x"))
        else:
            ws = sh.worksheet("Enemy Data")
            # ask with reaction to see if its l or g or none (FIRST TIME ONLY)
            role = ws.cell(enemy_row, LIEUT_GEN_COLUMN, value_render_option='UNFORMATTED_VALUE').value
            role_column = ws.col_values(LIEUT_GEN_COLUMN, value_render_option='UNFORMATTED_VALUE')
            lieutenant_count = role_column.count("Lieutenant")
            general_count = role_column.count("General")
            print(general_count)
            print(lieutenant_count)
            if((role == "?" or role =="" ) and (general_count < 1 or lieutenant_count < 3)):
                print("in")
                x_emoji = getDefaultEmoji("regional_indicator_m")
                lieutenant_emoji = getDefaultEmoji("regional_indicator_l")
                general_emoji = getDefaultEmoji("regional_indicator_g")
                await msg.add_reaction(x_emoji)
                if(lieutenant_count < 3):
                    await msg.add_reaction(lieutenant_emoji)
                if(general_count < 1):
                    await msg.add_reaction(general_emoji)
                def check(reaction, user):
                    return (str(reaction.emoji) == x_emoji 
                            or str(reaction.emoji) == lieutenant_emoji 
                            or str(reaction.emoji) == general_emoji) and user !=client.user and reaction.message.id == msg.id
                
                def wait_for_reaction(event_name):
                    return client.wait_for(event_name,check=check)


                pending_tasks = [wait_for_reaction("reaction_add"), wait_for_reaction("reaction_remove")]
                done_tasks, pending_tasks = await asyncio.wait(pending_tasks, timeout=10.0, return_when=asyncio.FIRST_COMPLETED)

                timeout = len(done_tasks) == 0

                if not timeout:
                    task = done_tasks.pop()

                    reaction, user = await task
                if timeout:
                    is_medal=False
                    await msg.add_reaction(getDefaultEmoji("x"))

                for remaining in itertools.chain(done_tasks, pending_tasks):
                    remaining.cancel()                   

                if str(reaction.emoji) == x_emoji:
                    if(medals <= 3 and medals >=0):
                        ws.update_cell(enemy_row, LIEUT_GEN_COLUMN, "Member")
                        ws.update_cell(enemy_row, ENEMY_MEDALS_LEFT, 6-medals)
                    else:
                        is_medal=False
                if str(reaction.emoji) == lieutenant_emoji:
                    if(medals <=5 and medals >=0):
                        ws.update_cell(enemy_row, LIEUT_GEN_COLUMN, "Lieutenant")
                        ws.update_cell(enemy_row, ENEMY_MEDALS_LEFT, 45-medals)
                    else:
                        is_medal=False
                if str(reaction.emoji) == general_emoji:
                    if(medals <=6 and medals >=0):
                        ws.update_cell(enemy_row, LIEUT_GEN_COLUMN, "General")
                        ws.update_cell(enemy_row, ENEMY_MEDALS_LEFT, 66-medals)
                    else:
                        is_medal=False
            # 100% Member
            elif(role == "?" or role == ""):
                ws.update_cell(enemy_row, LIEUT_GEN_COLUMN, "Member")
                ws.update_cell(enemy_row, ENEMY_MEDALS_LEFT, 6-medals)
            else:
                # medals checking
                if(role == "General"):
                    if(not(medals <=6 and medals >=0)):
                        is_medal=False                
                elif(role == "Lieutenant"):
                    if(not(medals <=5 and medals >=0)):
                        is_medal=False
                #member
                else:
                    if(not(medals <=3 and medals >=0)):
                        is_medal=False         
                if(is_medal):
                    enemy_medals = ws.cell(enemy_row, ENEMY_MEDALS_LEFT, value_render_option='UNFORMATTED_VALUE').value
                    if(enemy_medals - medals < 0 ):
                        ws.update_cell(enemy_row, ENEMY_MEDALS_LEFT, 0)
                    else:
                        ws.update_cell(enemy_row, ENEMY_MEDALS_LEFT, enemy_medals-medals)
            if(is_medal):
                # add to attack by enemy data
                # check if win or lose (lose == 0)                
                ws = sh.worksheet("Enemy Data")
                attacked_by_info = ws.cell(enemy_row, ENEMY_ATTACKED_BY, value_render_option='UNFORMATTED_VALUE').value
                if(medals == 0):
                    ws.update_cell(enemy_row, ENEMY_ATTACKED_BY, "{}\nWin against {}".format(attacked_by_info,ctx.message.author.name))
                else:
                    ws.update_cell(enemy_row, ENEMY_ATTACKED_BY, "{}\nLose against {}".format(attacked_by_info,ctx.message.author.name))                
                # do the runs and other record now that everything is verified
                ws = sh.worksheet("Basic Data")
                # o/w if its empty then make it 3
                if(not str(runs).strip()):
                    runs = 2
                    ws.update_cell(row, RUNS_COLUMN, runs)
                # else if its not empty or 0 then subtract 1
                else:
                    runs = runs -1
                    ws.update_cell(row, RUNS_COLUMN, runs)
                # add to attack basic data
                attacked_info = ws.cell(row, ATTACKED_COLUMN, value_render_option='UNFORMATTED_VALUE').value
                if(medals == 0):
                    ws.update_cell(row, ATTACKED_COLUMN, "{}\nLose against {}".format(attacked_info,target))
                else:
                    ws.update_cell(row, ATTACKED_COLUMN, "{}\nWin {} Medals against {}".format(attacked_info,medals,target))
                # add to medals gained total
                curr_medals = ws.cell(row, MEDAL_TOTAL_COLUMN, value_render_option='UNFORMATTED_VALUE').value
                ws.update_cell(row, MEDAL_TOTAL_COLUMN, curr_medals + medals+1)
                await msg.add_reaction(getDefaultEmoji("white_check_mark"))
            else:
                await msg.add_reaction(getDefaultEmoji("x"))
    