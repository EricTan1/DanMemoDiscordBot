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
        values_list = ws.col_values(DISCORD_ID_COLUMN, value_render_option='FORMULA')
        print(values_list)
        discord_id = ctx.message.author.id
        if(discord_id in values_list):
            row = values_list.index(discord_id)
        else:
            row = len(remove_values_from_list(values_list,""))-1
            ws.update_cell(row, DISCORD_ID_COLUMN, discord_id)
            ws.update_cell(row, DISCORD_MEMBER_NAME, ctx.message.author.nick)
        # add one to medals (default whenever you run 1)
        # subtract run if equal to 0 then warn user
        # check if there are any runs left
        runs = ws.cell(row, RUNS_COLUMN, value_render_option='UNFORMATTED_VALUE').value
        print(runs)
        # if its 0 give error msg
        if (str(runs) == "0"):
            await ctx.send("Unable to record real run because you ran out of runs(treated as mock run). Runs left of today: {}".format(runs))
        else:
            # o/w if its empty then make it 3
            if(not str(runs).strip()):
                runs = 2
                ws.update_cell(row, RUNS_COLUMN, runs)
            # else if its not empty or 0 then subtract 1
            else:
                runs = runs -1
                ws.update_cell(row, RUNS_COLUMN, runs)
            # add to attack basic data
            if(medals == 0):
                ws.update_cell(row, ATTACKED_COLUMN, "Lose,Target:{},Medals:0\n".format(target))
            else:
                ws.update_cell(row, ATTACKED_COLUMN, "Win,Target:{},Medals:{}\n".format(target,medals))
            # add to medals gained total
            curr_medals = ws.cell(row, MEDAL_TOTAL_COLUMN, value_render_option='UNFORMATTED_VALUE').value
            ws.update_cell(row, MEDAL_TOTAL_COLUMN, curr_medals + medals+1)
            ws = sh.worksheet("Enemy Data")
            # ask with reaction to see if its l or g or none (FIRST TIME ONLY)
            role = ws.cell(row, RUNS_COLUMN, value_render_option='UNFORMATTED_VALUE').value
            if(role == "?"):
                x_emoji = getDefaultEmoji("x")
                lieutenant_emoji = getDefaultEmoji("regional_indicator_l")
                general_emoji = getDefaultEmoji("regional_indicator_g")
                msg = ctx.message
                await msg.add_reaction(x_emoji)
                await msg.add_reaction(lieutenant_emoji)
                await msg.add_reaction(general_emoji)
                def check(reaction, user):
                    return (str(reaction.emoji) == x_emoji 
                            or str(reaction.emoji) == lieutenant_emoji 
                            or str(reaction.emoji) == general_emoji) and user !=client.user and reaction.message.id == msg.id
                
                def wait_for_reaction(event_name):
                    return client.wait_for(event_name,check=check)


                pending_tasks = [wait_for_reaction("reaction_add"), wait_for_reaction("reaction_remove")]
                done_tasks, pending_tasks = await asyncio.wait(pending_tasks, timeout=60.0, return_when=asyncio.FIRST_COMPLETED)

                timeout = len(done_tasks) == 0

                if not timeout:
                    task = done_tasks.pop()

                    reaction, user = await task

                for remaining in itertools.chain(done_tasks, pending_tasks):
                    remaining.cancel()                   

                if str(reaction.emoji) == x_emoji:
                    ws.update_cell(row, LIEUT_GEN_COLUMN, "None")
                    ws.update_cell(row, ENEMY_MEDALS_LEFT, 6-medals)
                if str(reaction.emoji) == lieutenant_emoji:
                    ws.update_cell(row, LIEUT_GEN_COLUMN, "Lieutenant")
                    ws.update_cell(row, ENEMY_MEDALS_LEFT, 30-medals)
                if str(reaction.emoji) == general_emoji:
                    ws.update_cell(row, LIEUT_GEN_COLUMN, "General")
                    ws.update_cell(row, ENEMY_MEDALS_LEFT, 60-medals)
            else:
                enemy_medals = ws.cell(row, ENEMY_MEDALS_LEFT, value_render_option='UNFORMATTED_VALUE').value
                if(enemy_medals - medals < 0 ):
                    ws.update_cell(row, ENEMY_MEDALS_LEFT, 0)
                else:
                    ws.update_cell(row, ENEMY_MEDALS_LEFT, enemy_medals-medals)
            # add to attack by enemy data
            # check if win or lose (lose == 0)    
            if(medals == 0):
                ws.update_cell(row, ENEMY_ATTACKED_BY, "Win,Target:{}|{}\n".format(ctx.message.author.nick,discord_id))
            else:
                ws.update_cell(row, ENEMY_ATTACKED_BY, "Lose,Target:{}|{}\n".format(ctx.message.author.nick,discord_id))    
    