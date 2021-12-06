
import discord
from commands.utils import get_emoji, Status
import asyncio
import itertools


async def pageRBHandler(client, ctx, logs, total_damage, total_score, unit_list, ast_list):
    """This handles the logic of the page handling for the single result adventurer

    Arguments:
        client {discord.client} -- the discord bot object
        ctx {discord.context} -- command message context
        pages {list of discord.embeds} -- adventurer stats/skills page
    """
    current_page = 0
    #temp_embed.set_footer(text="Page {} of {}".format(current_page+1,len(pages))) 

    page_list = []



    # first page
    first_page = discord.Embed()
    page_list.append(first_page)
    first_page.color = Status.OK.value
    first_page.title = "Summary of Record Buster"
    first_page.description="react to change pages"
    # all the advs being used
    first_page.add_field(name="Adventurers",value="{}, {}, {}, {}, {}, {}".format(unit_list[0].name,unit_list[1].name,unit_list[2].name,unit_list[3].name,unit_list[4].name,unit_list[5].name),inline=False)
    # all the assists being used
    first_page.add_field(name="Assists",value="{}, {}, {}, {}, {}, {}".format(ast_list[0].name,ast_list[1].name,ast_list[2].name,ast_list[3].name,ast_list[4].name,ast_list[5].name),inline=False)
    # damage per adv
    #current_damage
    for adv in unit_list:
        first_page.add_field(name="{} total damage".format(adv.name),value="{}".format(adv.current_damage),inline=False)
    # total damage
    first_page.add_field(name="Total Damage",value="{}".format(total_damage),inline=False)
    # total score
    first_page.add_field(name="Total Score",value="{}".format(total_score),inline=False)
    

    # enemy, unit{0-3}, turn
    # turn_logs = {"sa":[], "combat_skills":[], "counters":[], "sacs":[]}
    #### set up pages ####
    # title
    # description
    # color
    # footer
    # fields.append
    # page_list[current_page].color = Status.OK.value
    logs_per_page = 4
    logs_per_page_counter=1
    field_list_temp=[]
    for turn_logs in range(0,len(logs)):
        temp_value = ""

        # sa
        for sa in logs[turn_logs].get("sa"):
            temp_value +="{}\n".format(sa)
        # combatskills
        #for c_skill in logs[turn_logs].get("combat_skills"):
            #temp_value +="{}\n".format(c_skill)
        # counters
        for counter_skill in logs[turn_logs].get("counters"):
            temp_value +="{}\n".format(counter_skill)
        # sacs
        for sacs in logs[turn_logs].get("sacs"):
            temp_value +="{}\n".format(sacs)
        
        field_list_temp.append(("Turn {}".format(turn_logs+1),temp_value))
        
        if(logs_per_page_counter == logs_per_page or turn_logs ==len(logs)-1):
            temp_embed = discord.Embed()
            temp_embed.color = Status.OK.value
            page_list.append(temp_embed)
            temp_embed.title = "Damage for Turn {} - Turn {}".format(turn_logs+1-len(field_list_temp),turn_logs+1)
            temp_embed.description="react to change pages"
            for fields in field_list_temp:
                temp_embed.add_field(name=fields[0],value=fields[1],inline=False)
            logs_per_page_counter=1
            field_list_temp=[]
        else:
            logs_per_page_counter+=1


    # page_list[current_page].color = Status.OK.value
    logs_per_page = 1
    logs_per_page_counter=1
    field_list_temp=[]
    temp_value = ""
    for turn_logs in range(0,len(logs)):
        #temp_value+="Turn {}\n".format(turn_logs+1)
        temp_value+="{}\n{}\n".format("**RB Boss**", logs[turn_logs].get("enemy"))
        # stats
        for active_adv_count in range(0, 4):
            temp_value+="{}\n".format(logs[turn_logs].get("unit{}".format(active_adv_count)))
        
        field_list_temp.append(("Turn {}\n".format(turn_logs+1),temp_value))
        
        if(logs_per_page_counter == logs_per_page or turn_logs ==len(logs)-1):
            temp_embed = discord.Embed()
            temp_embed.color = Status.OK.value
            page_list.append(temp_embed)
            temp_embed.title = "Buffs/Debuffs Check for Turn {}".format(turn_logs+1)
            temp_embed.description="react to change pages\n"+temp_value
            logs_per_page_counter=1
            field_list_temp=[]
            temp_value=""
        else:
            logs_per_page_counter+=1

    
    # set footer for first page
    page_list[current_page].set_footer(text="Page {} of {}".format(current_page+1,len(page_list)))

    emoji1 = '\u2b05'
    emoji2 = '\u27a1'
    
    rewind = '\u23ea'
    forward = '\u23e9'
    async def updateStats():
        page_list[current_page].set_footer(text="Page {} of {}".format(current_page+1,len(page_list)))
    await updateStats()
    
    msg = await ctx.send(embed=page_list[current_page])
    await msg.add_reaction(rewind)
    await msg.add_reaction(emoji1)
    await msg.add_reaction(emoji2)
    await msg.add_reaction(forward)
    # set_field_at(index, *, name, value, inline=True)
    def check(reaction, user):
        return (str(reaction.emoji) == emoji2 
                or str(reaction.emoji) == emoji1 
                or str(reaction.emoji) == rewind
                or str(reaction.emoji) == forward)and user !=client.user and reaction.message.id == msg.id
    
    def wait_for_reaction(event_name):
        return client.wait_for(event_name,check=check)

    while True:
        pending_tasks = [wait_for_reaction("reaction_add"), wait_for_reaction("reaction_remove")]
        done_tasks, pending_tasks = await asyncio.wait(pending_tasks, timeout=60.0, return_when=asyncio.FIRST_COMPLETED)

        timeout = len(done_tasks) == 0

        if not timeout:
            task = done_tasks.pop()

            reaction, user = await task

        for remaining in itertools.chain(done_tasks, pending_tasks):
            remaining.cancel()

        if timeout:
            page_list[current_page].color = Status.KO.value
            await msg.edit(embed=page_list[current_page])
            break

        # left
        if str(reaction.emoji) == emoji1:
            if(current_page > 0):
                current_page = current_page -1
            else:
                current_page = len(page_list)-1
        # right
        if str(reaction.emoji) == emoji2:
            if( current_page+1 < len(page_list)):
                current_page = current_page +1
            else:
                current_page = 0
        if str(reaction.emoji) == rewind:
            current_page = 0
            #await updateStats()
        if str(reaction.emoji) == forward:
            current_page = len(page_list)-1
            #await updateStats()
        page_list[current_page].set_footer(text="Page {} of {}".format(current_page+1,len(page_list)))            
        await msg.edit(embed=page_list[current_page]) 