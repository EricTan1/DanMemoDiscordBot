
from typing import List
import asyncio
import interactions
from interactions.ext.wait_for import WaitForClient
from commands.utils import TIMEOUT, getDefaultEmoji, Status
from commands.entities.adventurer import Adventurer
from commands.entities.assist import Assist

# emoji strings
arrow_left = '\u2b05'
arrow_right = '\u27a1'
rewind = '\u23ee'
forward = '\u23ed'
attacks_toggle = getDefaultEmoji("crossed_swords")
counters_toggle = getDefaultEmoji("shield")
info_toggle = getDefaultEmoji("information_source")

# buttons
previous_page = interactions.Button(
    style=interactions.ButtonStyle.PRIMARY,
    label=arrow_left,
    custom_id="previous_page"
)
next_page = interactions.Button(
    style=interactions.ButtonStyle.PRIMARY,
    label=arrow_right,
    custom_id="next_page"
)
to_start = interactions.Button(
    style=interactions.ButtonStyle.PRIMARY,
    label=rewind,
    custom_id="to_start"
)
to_end = interactions.Button(
    style=interactions.ButtonStyle.PRIMARY,
    label=forward,
    custom_id="to_end"
)
toggle_combat = interactions.Button(
    style=interactions.ButtonStyle.PRIMARY,
    label=attacks_toggle,
    custom_id="toggle_combat"
)
toggle_counters = interactions.Button(
    style=interactions.ButtonStyle.PRIMARY,
    label=counters_toggle,
    custom_id="toggle_counters"
)
toggle_effects = interactions.Button(
    style=interactions.ButtonStyle.PRIMARY,
    label=info_toggle,
    custom_id="toggle_effects"
)

buttons = [to_start, previous_page, next_page, to_end, toggle_combat, toggle_counters, toggle_effects]

# button rows
row1 = interactions.ActionRow(components=buttons[:4])
row2 = interactions.ActionRow(components=buttons[4:])


async def pageRBHandler(client: WaitForClient, ctx: interactions.CommandContext, logs: List[dict], total_damage: int, total_score: float, unit_list: List[Adventurer], assist_list: List[Assist]):
    """This handles the logic of the page handling for the single result adventurer

    Arguments:
        client {interactions.client} -- the discord interactions bot object
        ctx {interactions.CommandContext} -- command message context
        pages {list of interactions.embeds} -- adventurer stats/skills pages
    """

    page_list = []
    current_page = 0

    # first page
    first_page = interactions.Embed()
    page_list.append(first_page)
    first_page.color = Status.OK.value
    first_page.title = "Summary of Record Buster"
    # all the advs being used
    first_page.add_field(name="Adventurers",value="{}, {}, {}, {}, {}, {}".format(unit_list[0].name,unit_list[1].name,unit_list[2].name,unit_list[3].name,unit_list[4].name,unit_list[5].name),inline=False)
    # all the assists being used
    first_page.add_field(name="Assists",value="{}, {}, {}, {}, {}, {}".format(assist_list[0].name,assist_list[1].name,assist_list[2].name,assist_list[3].name,assist_list[4].name,assist_list[5].name),inline=False)
    # damage per adv
    #current_damage
    for adv in unit_list:
        first_page.add_field(name="{} total damage".format(adv.name),value="{:,}".format(int(adv.current_damage)),inline=False)
    # total damage
    first_page.add_field(name="Total Damage",value="{:,}".format(int(total_damage)),inline=False)
    # total score
    first_page.add_field(name="Total Score",value="{:,}".format(int(total_score)),inline=False)
    
    toggle_log_list={"attack":True, "counters":False,"info":False}


    """  # page_list[current_page].color = Status.OK.value
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
            temp_embed = interactions.Embed()
            temp_embed.color = Status.OK.value
            page_list.append(temp_embed)
            temp_embed.title = "Buffs/Debuffs Check for Turn {}".format(turn_logs+1)
            temp_embed.description="react to change pages\n"+temp_value
            logs_per_page_counter=1
            field_list_temp=[]
            temp_value=""
        else:
            logs_per_page_counter+=1 """


    # whenever toggles
    async def updateStats(page_list):
        page_list = page_list[:1]
        logs_per_page = 1
        logs_per_page_counter=1
        field_list_temp=[]
        for turn_logs in range(0,len(logs)):

            # attacks
            if(toggle_log_list.get("attack")==True):
                temp_value = ""
                # sa
                for sa in logs[turn_logs].get("sa"):
                    temp_value +="{}\n".format(sa)
                # combatskills
                for c_skill in logs[turn_logs].get("combat_skills"):
                    temp_value +="{}\n".format(c_skill)
                if(temp_value != ""):
                    field_list_temp.append(("**Skills**",temp_value))

            # counters
            if (toggle_log_list.get("counters")==True):
                temp_value = ""
                for counter_skill in logs[turn_logs].get("counters"):
                    temp_value +="{}\n".format(counter_skill)
                if(temp_value != ""):
                    field_list_temp.append(("**Counters**",temp_value))

            # boost check
            if(toggle_log_list.get("info")== True):
                #temp_value+="Turn {}\n".format(turn_logs+1)
                temp_value = ""
                if(len(logs[turn_logs].get("enemy")) != 0):
                    field_list_temp.append(("**RB Boss**",logs[turn_logs].get("enemy")))

                # stats
                for active_adv_count in range(0, 4):
                    #temp_value+="{}\n".format(logs[turn_logs].get("unit{}".format(active_adv_count)))
                    if(len(logs[turn_logs].get("unit{}".format(active_adv_count))) != 0):
                        field_list_temp.append(("\U0000200e", logs[turn_logs].get("unit{}".format(active_adv_count))))
                    
                    #field_list_temp.append(("**Info**",temp_value))

            # sacs
            temp_value = ""
            for sacs in logs[turn_logs].get("sacs"):
                temp_value +="{}\n".format(sacs)
            
            if(temp_value != ""):
                field_list_temp.append(("**Sacs**",temp_value))
            
            if(logs_per_page_counter == logs_per_page or turn_logs ==len(logs)-1):
                temp_embed = interactions.Embed()
                temp_embed.color = Status.OK.value
                page_list.append(temp_embed)
                temp_embed.title = "Damage for Turn {}".format(turn_logs+1)
                temp_embed.description="react to change pages"
                for fields in field_list_temp:
                    temp_embed.add_field(name=fields[0],value=fields[1],inline=False)
                logs_per_page_counter=1
                field_list_temp=[]
            else:
                logs_per_page_counter+=1
        return page_list


    page_list = await updateStats(page_list)
    # set footer for first page
    page_list[current_page].description="react {} or {} to change pages\n{} to toggle sa/combat skills\n{} to toggle counters\n{}\
         to toggle buffs/debuffs".format(arrow_left,arrow_right,attacks_toggle,counters_toggle,info_toggle)
    page_list[current_page].set_footer(text="Page {} of {}".format(current_page+1,len(page_list)))

    msg = await ctx.send(embeds=page_list[current_page], components=[row1, row2])

    while True:
        try:
            component_ctx: interactions.ComponentContext = await client.wait_for_component(
                components=buttons, messages=msg, timeout=TIMEOUT
            )

            if(component_ctx.custom_id == "previous_page"):
                if(current_page > 0):
                    current_page = current_page -1
                else:
                    current_page = len(page_list)-1
            elif(component_ctx.custom_id == "next_page"):
                if(current_page+1 < len(page_list)):
                    current_page = current_page +1
                else:
                    current_page = 0
            elif(component_ctx.custom_id == "to_start"):
                current_page = 0
            elif(component_ctx.custom_id == "to_end"):
                current_page = len(page_list)-1
            elif(component_ctx.custom_id == "toggle_combat"):
                toggle_log_list["attack"] = not toggle_log_list.get("attack")
                page_list = await updateStats(page_list)
            elif(component_ctx.custom_id == "toggle_counters"):
                toggle_log_list["counters"] = not toggle_log_list.get("counters")
                page_list = await updateStats(page_list)
            elif(component_ctx.custom_id == "toggle_effects"):
                toggle_log_list["info"] = not toggle_log_list.get("info")
                page_list = await updateStats(page_list)

            page_list[current_page].set_footer(text="Page {} of {}".format(current_page+1,len(page_list)))
            page_list[current_page].description="react {} or {} to change pages\n{} to toggle sa/combat skills\n{} to toggle counters\n{}\
                to toggle buffs/debuffs".format(arrow_left,arrow_right,attacks_toggle,counters_toggle,info_toggle)
            page_list[current_page].set_footer(text="Page {} of {}".format(current_page+1,len(page_list)))
    
            await component_ctx.edit(embeds=page_list[current_page])

        except asyncio.TimeoutError:
            page_list[current_page].color = Status.KO.value
            return await ctx.edit(embeds=page_list[current_page], components=[])
