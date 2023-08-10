from asyncio import TimeoutError

from interactions import ActionRow, Client, ComponentContext, Embed, SlashContext

from commands.buttons import (
    next_page,
    previous_page,
    to_end,
    to_start,
    toggle_combat,
    toggle_counters,
    toggle_effects,
)
from commands.entities.adventurer import Adventurer
from commands.entities.assist import Assist
from commands.utils import TIMEOUT, Status, getDefaultEmoji

# emoji strings
arrow_left = "\u2b05"
arrow_right = "\u27a1"
rewind = "\u23ee"
forward = "\u23ed"
attacks_toggle = getDefaultEmoji("crossed_swords")
counters_toggle = getDefaultEmoji("shield")
info_toggle = getDefaultEmoji("information_source")

buttons = [
    to_start,
    previous_page,
    next_page,
    to_end,
    toggle_combat,
    toggle_counters,
    toggle_effects,
]

# button rows
row1 = ActionRow(*(buttons[:4]))
row2 = ActionRow(*(buttons[4:]))


async def pageRBHandler(
    client: Client,
    ctx: SlashContext,
    logs: list[dict],
    total_damage: int,
    total_score: float,
    unit_list: list[Adventurer],
    assist_list: list[Assist],
):
    """This handles the logic of the page handling for the single result adventurer"""

    page_list = []
    current_page = 0

    # first page
    first_page = Embed()
    page_list.append(first_page)
    first_page.color = Status.OK.value
    first_page.title = "Summary of Record Buster"
    # all the advs being used
    first_page.add_field(
        name="Adventurers",
        value=f"{unit_list[0].name}, {unit_list[1].name}, {unit_list[2].name}, {unit_list[3].name}, {unit_list[4].name}, {unit_list[5].name}",
    )
    # all the assists being used
    first_page.add_field(
        name="Assists",
        value=f"{assist_list[0].name}, {assist_list[1].name}, {assist_list[2].name}, {assist_list[3].name}, {assist_list[4].name}, {assist_list[5].name}",
    )
    # damage per adv
    # current_damage
    for adv in unit_list:
        first_page.add_field(
            name=f"{adv.name} total damage",
            value=f"{adv.current_damage:,}",
        )
    # total damage
    first_page.add_field(name="Total Damage", value=f"{total_damage:,}")
    # total score
    first_page.add_field(name="Total Score", value=f"{int(total_score):,}")

    toggle_log_list = {"attack": True, "counters": False, "info": False}

    # whenever toggles
    def updateStats(page_list):
        page_list = page_list[:1]
        logs_per_page = 1
        logs_per_page_counter = 1
        field_list_temp = []
        for turn, turn_logs in enumerate(logs):
            # attacks
            if toggle_log_list["attack"]:
                temp_value = ""
                # sa
                for sa in turn_logs["sa"]:
                    temp_value += f"{sa}\n"
                # combatskills
                for c_skill in turn_logs["combat_skills"]:
                    temp_value += f"{c_skill}\n"
                if temp_value != "":
                    field_list_temp.append(("**Skills**", temp_value))

            # counters
            if toggle_log_list["counters"]:
                temp_value = ""
                for counter_skill in turn_logs["counters"]:
                    temp_value += f"{counter_skill}\n"
                if temp_value != "":
                    field_list_temp.append(("**Counters**", temp_value))

            # boost check
            if toggle_log_list["info"]:
                temp_value = ""
                for effect in turn_logs["enemy"]:
                    temp_value += f"{effect}\n"
                if temp_value:
                    field_list_temp.append(("**RB Boss**", temp_value))

                # stats
                for active_adv_count in range(0, 4):
                    temp_value = ""
                    unit_key = f"unit{active_adv_count}"
                    # first field in unit log is used to save its name (already bold)
                    field_title = turn_logs[unit_key][0]
                    for effect in turn_logs[unit_key][1:]:
                        temp_value += f"{effect}\n"
                    if temp_value:
                        field_list_temp.append((field_title, temp_value))

            # instant actions
            temp_value = ""
            for instant_actions in turn_logs["instant_actions"]:
                temp_value += f"{instant_actions}\n"
            if temp_value != "":
                field_list_temp.append(("**Instant Actions**", temp_value))

            # sacs
            temp_value = ""
            for sacs in turn_logs["sacs"]:
                temp_value += f"{sacs}\n"
            if temp_value != "":
                field_list_temp.append(("**Sacs**", temp_value))

            if logs_per_page_counter == logs_per_page or turn == len(logs) - 1:
                temp_embed = Embed()
                temp_embed.color = Status.OK.value
                page_list.append(temp_embed)
                temp_embed.title = f"Damage for Turn {turn+1}"
                temp_embed.description = "Press buttons to switch pages"
                for fields in field_list_temp:
                    temp_embed.add_field(name=fields[0], value=fields[1])
                logs_per_page_counter = 1
                field_list_temp = []
            else:
                logs_per_page_counter += 1
        return page_list

    page_list = updateStats(page_list)
    # set footer for first page
    description = f"Press {arrow_left} or {arrow_right} to change pages\n{attacks_toggle} to toggle sa/combat skills\n{counters_toggle} to toggle counters\n{info_toggle}\
         to toggle buffs/debuffs"
    page_list[current_page].description = description
    page_list[current_page].set_footer(
        text=f"Page {current_page+1} of {len(page_list)}"
    )

    msg = await ctx.send(embeds=page_list[current_page], components=[row1, row2])

    while True:
        try:
            component_ctx: ComponentContext = (
                await client.wait_for_component(
                    components=buttons, messages=msg, timeout=TIMEOUT
                )
            ).ctx

            match component_ctx.custom_id:
                case "previous_page":
                    current_page = (current_page - 1) % len(page_list)
                case "next_page":
                    current_page = (current_page + 1) % len(page_list)
                case "to_start":
                    current_page = 0
                case "to_end":
                    current_page = len(page_list) - 1
                case "toggle_combat":
                    toggle_log_list["attack"] = not toggle_log_list.get("attack")
                    page_list = updateStats(page_list)
                case "toggle_counters":
                    toggle_log_list["counters"] = not toggle_log_list.get("counters")
                    page_list = updateStats(page_list)
                case "toggle_effects":
                    toggle_log_list["info"] = not toggle_log_list.get("info")
                    page_list = updateStats(page_list)

            page_list[current_page].set_footer(
                text=f"Page {current_page+1} of {len(page_list)}"
            )
            page_list[current_page].description = description
            page_list[current_page].set_footer(
                text=f"Page {current_page+1} of {len(page_list)}"
            )

            await component_ctx.edit_origin(embeds=page_list[current_page])

        except TimeoutError:
            page_list[current_page].color = Status.KO.value
            return await msg.edit(embeds=page_list[current_page], components=[])
