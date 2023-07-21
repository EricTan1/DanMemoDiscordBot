import asyncio
import io
from typing import List, Optional, Tuple, Type, cast

import interactions
from interactions.ext.files import CommandContext, ComponentContext
from interactions.ext.wait_for import WaitForClient

from commands.buttons import (
    hero_ascend_add_button,
    hero_ascend_sub_button,
    limitbreak_add_button,
    limitbreak_sub_button,
    next_page,
    previous_page,
)
from commands.utils import (
    TIMEOUT,
    HeroAscensionStats,
    HeroAscensionStatsB,
    HeroAscensionStatsD,
    HeroAscensionStatsH,
    HeroAscensionStatsM,
    HeroAscensionStatsP,
    Status,
    get_emoji,
)
from database.DBcontroller import DBcontroller

limitbreak_sub_emoji = get_emoji("square_off").format
limitbreak_add_emoji = get_emoji("square_on").format
hero_ascend_sub_emoji = get_emoji("star_off").format
hero_ascend_add_emoji = get_emoji("star_on").format


# --- interface functions used by commonSearch ---
def get_unit_image_path(unit: tuple) -> str:
    return "./images/units/" + unit[2] + " [" + unit[1] + "]/"


def get_page_list(my_list: list) -> List[list]:
    page_list = []
    temp_page: List[list] = []
    page_list.append(temp_page)
    for Adventurersid in my_list:
        temp_page.append(Adventurersid)
        if len(temp_page) >= 10:
            temp_page = []
            page_list.append(temp_page)

    return page_list


def clearSetField(
    temp_embed: interactions.Embed, data: List[list]
) -> interactions.Embed:
    temp_embed.description = (
        "Select a unit via the dropdown menu or switch pages with the buttons"
    )
    temp_embed.clear_fields()
    value = ""
    for i, unit in enumerate(data):
        value += f"{i+1}. [{unit[1]}] {unit[2]}\n"
    temp_embed.add_field(name="Units", value=value)
    return temp_embed


# --- Single unit page ---
async def singleUnit(
    client: WaitForClient,
    ctx: CommandContext,
    db: DBcontroller,
    assistadventurerid: str,
):
    """This handles the logic of choosing of the character search and setting up
    for a single result search

    Arguments:
        client {interactions.ext.wait_for.WaitForClient} -- the discord bot object
        ctx {interactions.ext.files.CommandContext} -- command message context
        db {DBController.DBController} -- Database connector object
        assistadventurerid {str} -- the assist/adventurer id of the wanted search
    """

    temp_embed = interactions.Embed()
    dev_embed = interactions.Embed()
    temp_embed.color = Status.OK.value
    dev_embed.color = Status.OK.value
    if "Ad" in assistadventurerid:
        info = db.assembleAdventurer(assistadventurerid[2:])
        for adventurerdev in info[4]:
            dev_embed.add_field(
                name=adventurerdev[0], value=adventurerdev[1], inline=False
            )
        is_adv = True
    else:
        info = db.assembleAssist(assistadventurerid[2:])
        is_adv = False
    stats, abilities = assembleStats(info[3], 0, "", 0)
    temp_embed.add_field(name="Stats", value=stats, inline=True)
    temp_embed.add_field(name="Abilities", value=abilities, inline=True)
    temp_embed.title = info[1]
    dev_embed.title = info[1]
    for skills in info[2]:
        if skills[1] == "":
            temp_embed.add_field(name=skills[0], value="placeholder", inline=False)
        else:
            temp_embed.add_field(name=skills[0], value=skills[1], inline=False)

    file_list = []
    try:
        # images
        character_name = info[1].split("]")[1][1:].split("\n")[0]
        character_title = info[1].split("[")[1].split("]")[0]
        folder_name = character_name + " [" + character_title + "]"
        print("./images/units/" + folder_name + "/hex.png")
        file_list.append(
            interactions.File("./images/units/" + folder_name + "/hex.png")
        )
        file_list.append(
            interactions.File("./images/units/" + folder_name + "/all_rectangle.png")
        )
        temp_embed.set_thumbnail(url="attachment://hex.png")
        dev_embed.set_thumbnail(url="attachment://hex.png")
        temp_embed.set_image(url="attachment://all_rectangle.png")
        dev_embed.set_image(url="attachment://all_rectangle.png")
    except:
        pass

    if is_adv:
        await pageHandler(
            client, ctx, file_list, info[3], temp_embed, dev_embed, info[6], info[5]
        )
    else:
        await pageHandler(client, ctx, file_list, info[3], temp_embed)


async def pageHandler(
    client: WaitForClient,
    ctx: CommandContext,
    file_list: list,
    stats_dict: dict,
    temp_embed: interactions.Embed,
    dev_embed: Optional[interactions.Embed] = None,
    unit_type: str = "",
    ascended: Optional[bool] = None,
):
    """This handles the logic of the page handling for the single result unit

    Arguments:
        client {interactions.ext.wait_for.WaitForClient} -- the discord bot object
        ctx {interactions.ext.files.CommandContext} -- command message context
        file_list {list of pictures} -- images to be displayed for pages
        stats_dict {dict} -- the stats of the current unit
        temp_embed {interactions.embed} -- adventurer stats/skills page
        dev_embed {interactions.embed} -- the adventurer development page
        unit_type {string} -- balance,physical,magical for stats calculation
        ascended {bool} -- adventurer has hero ascension or not
    """

    def updateStats():
        temp_embed.description = (
            limitbreak_add_emoji * current_limitbreak
            + limitbreak_sub_emoji * (MAXLB - current_limitbreak)
        )
        if ascended:
            temp_embed.description = (
                temp_embed.description
                + "    "
                + hero_ascend_add_emoji.format * current_ha
                + hero_ascend_sub_emoji.format * (MAXHA - current_ha)
            )

        stats, abilities = assembleStats(
            stats_dict, current_limitbreak, unit_type, current_ha
        )

        temp_embed.set_field_at(0, name="Stats", value=stats, inline=True)
        temp_embed.set_field_at(1, name="Abilities", value=abilities, inline=True)

    MAXLB = 5
    MAXHA = 6
    current_page = 0
    current_limitbreak = 5
    current_ha = 0
    page_list = [temp_embed]
    if dev_embed:
        page_list.append(dev_embed)
    temp_embed.set_footer(text=f"Page {current_page+1} of {len(page_list)}")

    updateStats()
    stats_buttons = [limitbreak_sub_button, limitbreak_add_button]
    if ascended:
        stats_buttons += [hero_ascend_sub_button, hero_ascend_add_button]
    stats_button_row = interactions.ActionRow(components=stats_buttons)
    components = [stats_button_row]
    if len(page_list) > 1:
        arrow_row = interactions.ActionRow(components=[previous_page, next_page])
        components = [arrow_row] + components
    msg = await ctx.send(
        files=file_list, embeds=page_list[current_page], components=components
    )

    buttons = [previous_page, next_page, limitbreak_sub_button, limitbreak_add_button]

    while True:
        # files seem to be automatically closed, have to reopen them on every loop execution
        refresh_files(file_list)
        try:
            component_ctx: ComponentContext = await client.wait_for_component(
                components=buttons,  # type: ignore [arg-type]
                messages=msg,
                timeout=TIMEOUT,
            )

            if component_ctx.custom_id == "previous_page":
                current_page = (current_page - 1) % len(page_list)
            elif component_ctx.custom_id == "next_page":
                current_page = (current_page + 1) % len(page_list)
            elif component_ctx.custom_id == "limitbreak_sub":
                current_limitbreak = (current_limitbreak - 1) % (MAXLB + 1)
                updateStats()
            elif component_ctx.custom_id == "limitbreak_add":
                current_limitbreak = (current_limitbreak + 1) % (MAXLB + 1)
                updateStats()
            elif component_ctx.custom_id == "hero_ascend_sub":
                current_ha = (current_ha - 1) % (MAXHA + 1)
                updateStats()
            elif component_ctx.custom_id == "hero_ascend_add":
                current_ha = (current_ha + 1) % (MAXHA + 1)
                updateStats()

            page_list[current_page].set_footer(
                text=f"Page {current_page+1} of {len(page_list)}"
            )
            # it shouldn't be necessary to pass the files again on edit
            # but for some reason it doesn't work otherwise
            await component_ctx.edit(files=file_list, embeds=page_list[current_page])

        except asyncio.TimeoutError:
            page_list[current_page].color = Status.KO.value
            return await msg.edit(
                files=file_list, embeds=page_list[current_page], components=None
            )


def refresh_files(file_list: List[interactions.File]):
    for file in file_list:
        file._fp = open(cast(io.BufferedReader, file._fp).name, "rb")


def assembleStats(
    stats_dict: dict, limitbreak: int, unit_type: str, heroascend: int
) -> Tuple[str, str]:
    """Calculates Abilities based on limit break and hero ascension (if avaliable)

    Arguments:
        stats_dict {dict} -- the stats dictionary
        limitbreak {int} -- the limit break of a unit, 0 = no LB, 5 = MLB
        unit_type {str} -- balance, physical, magical
        heroascend {int} -- the hero ascension #, 0 = no HA and 6 = MHA

    Returns:
        str -- the stats string
    """

    if unit_type.lower() == "physical_type":
        ascension_stats: Type[HeroAscensionStats] = HeroAscensionStatsP
    elif unit_type.lower() == "magic_type":
        ascension_stats = HeroAscensionStatsM
    elif unit_type.lower() == "healer_type":
        ascension_stats = HeroAscensionStatsH
    elif unit_type.lower() == "defense_type":
        ascension_stats = HeroAscensionStatsD
    else:
        ascension_stats = HeroAscensionStatsB

    temp_hp = int(stats_dict["hp"][limitbreak]) + ascension_stats.HP[heroascend]
    temp_mp = int(stats_dict["mp"][limitbreak]) + ascension_stats.MP[heroascend]
    temp_pat = (
        int(stats_dict["physical_attack"][limitbreak]) + ascension_stats.PAT[heroascend]
    )
    temp_mat = (
        int(stats_dict["magic_attack"][limitbreak]) + ascension_stats.MAT[heroascend]
    )
    temp_def = int(stats_dict["defense"][limitbreak]) + ascension_stats.DEF[heroascend]

    res1 = f"HP : {temp_hp}\n"
    res1 += f"MP : {temp_mp}\n"
    res1 += f"P.AT : {temp_pat}\n"
    res1 += f"M.AT : {temp_mat}\n"
    res1 += f"DEF : {temp_def}\n"

    temp_str = int(stats_dict["strength"][limitbreak]) + ascension_stats.STR[heroascend]
    temp_end = (
        int(stats_dict["endurance"][limitbreak]) + ascension_stats.END[heroascend]
    )
    temp_dex = (
        int(stats_dict["dexterity"][limitbreak]) + ascension_stats.DEX[heroascend]
    )
    temp_agi = int(stats_dict["agility"][limitbreak]) + ascension_stats.AGI[heroascend]
    temp_mag = int(stats_dict["magic"][limitbreak]) + ascension_stats.MAG[heroascend]

    res2 = f"Str. : {temp_str}\n"
    res2 += f"End. : {temp_end}\n"
    res2 += f"Dex. : {temp_dex}\n"
    res2 += f"Agi. : {temp_agi}\n"
    res2 += f"Mag. : {temp_mag}\n"

    return (res1, res2)
