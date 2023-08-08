import os
from asyncio import TimeoutError
from typing import Type

from interactions import (
    ActionRow,
    Client,
    ComponentContext,
    Embed,
    EmbedField,
    File,
    SlashContext,
)

from commands.buttons import (
    hero_ascend_add_button,
    hero_ascend_sub_button,
    limitbreak_add_button,
    limitbreak_sub_button,
    next_page,
    previous_page,
)
from commands.emojis import (
    hero_ascend_add_emoji,
    hero_ascend_sub_emoji,
    limitbreak_add_emoji,
    limitbreak_sub_emoji,
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
)
from database.DBcontroller import DBcontroller


# --- interface functions used by commonSearch ---
def get_unit_image_path(unit: tuple) -> str:
    return "./images/units/" + unit[2] + " [" + unit[1] + "]/"


def get_page_list(my_list: list) -> list[list]:
    page_list = []
    temp_page: list[list] = []
    page_list.append(temp_page)
    for Adventurersid in my_list:
        temp_page.append(Adventurersid)
        if len(temp_page) >= 10:
            temp_page = []
            page_list.append(temp_page)

    return page_list


def clearSetField(temp_embed: Embed, data: list[list]) -> Embed:
    temp_embed.description = (
        "Select a unit via the dropdown menu or switch pages with the buttons"
    )
    temp_embed.fields = []
    value = ""
    for i, unit in enumerate(data):
        value += f"{i+1}. [{unit[1]}] {unit[2]}\n"
    temp_embed.add_field(name="Units", value=value)
    return temp_embed


# --- Single unit page ---
async def singleUnit(
    client: Client,
    ctx: SlashContext,
    db: DBcontroller,
    assistadventurerid: str,
):
    """This handles the logic of choosing of the character search and setting up
    for a single result search

    Arguments:
        client -- the discord bot object
        ctx -- command message context
        db -- Database connector object
        assistadventurerid -- the assist/adventurer id of the wanted search
    """

    temp_embed = Embed()
    dev_embed = Embed()
    temp_embed.color = Status.OK.value
    dev_embed.color = Status.OK.value
    if "Ad" in assistadventurerid:
        info = db.assembleAdventurer(assistadventurerid[2:])
        for adventurerdev in info[4]:
            dev_embed.add_field(name=adventurerdev[0], value=adventurerdev[1])
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
            temp_embed.add_field(name=skills[0], value="placeholder")
        else:
            temp_embed.add_field(name=skills[0], value=skills[1])

    file_list = []
    # images
    character_name = info[1].split("]")[1][1:].split("\n")[0]
    character_title = info[1].split("[")[1].split("]")[0]
    folder_name = character_name + " [" + character_title + "]"
    path = "./images/units/" + folder_name
    if os.path.isdir(path):
        file_list.append(File(path + "/hex.png"))
        file_list.append(File(path + "/all_rectangle.png"))
        temp_embed.set_thumbnail(url="attachment://hex.png")
        dev_embed.set_thumbnail(url="attachment://hex.png")
        temp_embed.set_image(url="attachment://all_rectangle.png")
        dev_embed.set_image(url="attachment://all_rectangle.png")

    if is_adv:
        await pageHandler(
            client, ctx, file_list, info[3], temp_embed, dev_embed, info[6], info[5]
        )
    else:
        await pageHandler(client, ctx, file_list, info[3], temp_embed)


async def pageHandler(
    client: Client,
    ctx: SlashContext,
    file_list: list,
    stats_dict: dict,
    temp_embed: Embed,
    dev_embed: Embed | None = None,
    unit_type: str = "",
    ascended: bool | None = None,
):
    """This handles the logic of the page handling for the single result unit

    Arguments:
        client -- the discord bot object
        ctx -- command message context
        file_list -- images to be displayed for pages
        stats_dict -- the stats of the current unit
        temp_embed -- adventurer stats/skills page
        dev_embed -- the adventurer development page
        unit_type -- balance,physical,magical for stats calculation
        ascended -- adventurer has hero ascension or not
    """

    def updateStats():
        temp_embed.description = str(limitbreak_add_emoji) * current_limitbreak + str(
            limitbreak_sub_emoji
        ) * (MAXLB - current_limitbreak)
        if ascended:
            temp_embed.description = (
                temp_embed.description
                + "    "
                + str(hero_ascend_add_emoji) * current_ha
                + str(hero_ascend_sub_emoji) * (MAXHA - current_ha)
            )

        stats, abilities = assembleStats(
            stats_dict, current_limitbreak, unit_type, current_ha
        )

        temp_embed.fields[0] = EmbedField(name="Stats", value=stats, inline=True)
        temp_embed.fields[1] = EmbedField(
            name="Abilities", value=abilities, inline=True
        )

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
    components = [ActionRow(*stats_buttons)]
    if len(page_list) > 1:
        components = [ActionRow(previous_page, next_page)] + components
    msg = await ctx.send(
        files=file_list, embeds=page_list[current_page], components=components
    )

    buttons = [previous_page, next_page, limitbreak_sub_button, limitbreak_add_button]

    while True:
        try:
            component_ctx: ComponentContext = (
                await client.wait_for_component(
                    components=buttons,
                    messages=msg,
                    timeout=TIMEOUT,
                )
            ).ctx

            match component_ctx.custom_id:
                case "previous_page":
                    current_page = (current_page - 1) % len(page_list)
                case "next_page":
                    current_page = (current_page + 1) % len(page_list)
                case "limitbreak_sub":
                    current_limitbreak = (current_limitbreak - 1) % (MAXLB + 1)
                    updateStats()
                case "limitbreak_add":
                    current_limitbreak = (current_limitbreak + 1) % (MAXLB + 1)
                    updateStats()
                case "hero_ascend_sub":
                    current_ha = (current_ha - 1) % (MAXHA + 1)
                    updateStats()
                case "hero_ascend_add":
                    current_ha = (current_ha + 1) % (MAXHA + 1)
                    updateStats()

            page_list[current_page].set_footer(
                text=f"Page {current_page+1} of {len(page_list)}"
            )
            await component_ctx.edit_origin(embeds=page_list[current_page])

        except TimeoutError:
            page_list[current_page].color = Status.KO.value
            return await msg.edit(
                files=file_list, embeds=page_list[current_page], components=None
            )


def assembleStats(
    stats_dict: dict, limitbreak: int, unit_type: str, heroascend: int
) -> tuple[str, str]:
    """Calculates Abilities based on limit break and hero ascension (if avaliable)

    Arguments:
        stats_dict -- the stats dictionary
        limitbreak -- the limit break of a unit, 0 = no LB, 5 = MLB
        unit_type -- balance, physical, magical
        heroascend -- the hero ascension #, 0 = no HA and 6 = MHA

    Returns:
        the stats string
    """

    match unit_type.lower():
        case "physical_type":
            ascension_stats: Type[HeroAscensionStats] = HeroAscensionStatsP
        case "magic_type":
            ascension_stats = HeroAscensionStatsM
        case "healer_type":
            ascension_stats = HeroAscensionStatsH
        case "defense_type":
            ascension_stats = HeroAscensionStatsD
        case _:
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
