import asyncio
import os
import interactions
from interactions.ext.wait_for import WaitForClient
from interactions.ext.files import CommandContext, ComponentContext
from PIL import Image
import io

from typing import Optional, Tuple, List

from commands.utils import TIMEOUT, get_emoji,HeroAscensionStatsP,HeroAscensionStatsB,HeroAscensionStatsM,Status, HeroAscensionStatsD, HeroAscensionStatsH
from database.DBcontroller import DBcontroller


# emojis
arrow_left = '\u2b05'
arrow_right = '\u27a1'
rewind = '\u23ee'
forward = '\u23ed'
limitbreak_sub_emoji = get_emoji("square_off")
limitbreak_add_emoji = get_emoji("square_on")
hero_ascend_sub_emoji = get_emoji("star_off")
hero_ascend_add_emoji = get_emoji("star_on")

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
limitbreak_sub_button = interactions.Button(
    style=interactions.ButtonStyle.PRIMARY,
    emoji=limitbreak_sub_emoji,
    custom_id="limitbreak_sub"
)
limitbreak_add_button = interactions.Button(
    style=interactions.ButtonStyle.PRIMARY,
    emoji=limitbreak_add_emoji,
    custom_id="limitbreak_add"
)
hero_ascend_sub_button = interactions.Button(
    style=interactions.ButtonStyle.PRIMARY,
    emoji=hero_ascend_sub_emoji,
    custom_id="hero_ascend_sub"
)
hero_ascend_add_button = interactions.Button(
    style=interactions.ButtonStyle.PRIMARY,
    emoji=hero_ascend_add_emoji,
    custom_id="hero_ascend_add"
)


async def run(dbConfig, client: WaitForClient, ctx: CommandContext, search_words: str):
    """ Character Search
    <CommandPrefix> <Search>
    
    Arguments:
        dbConfig {[DBcontroller.dbConfig]} -- Database config usually local/environmental variables
        client {[interactions.ext.wait_for.WaitForClient]} -- the discord bot object
        ctx {[interactions.ext.files.CommandContext]} -- command message context
    """

    search = search_words.split()
    my_search = " "
    for words in search:
        my_search = my_search + words + " "

    db = DBcontroller(dbConfig)
    my_list = db.characterSearch(my_search.replace("[","").replace("]",""))
    print(my_list)
    if len(my_list) == 0:
        temp_embed = interactions.Embed()
        temp_embed.title = "There are no results"
        temp_embed.color = Status.KO.value
        await ctx.send(embeds=temp_embed)
    elif len(my_list) == 1:
        await singleAdventurer(client, ctx, db,my_list[0][3])
    else:
        page_list=[]
        temp_page: List[list] = []
        page_list.append(temp_page)
        total_results = 0
        for Adventurersid in my_list:
            total_results = total_results+1
            temp_page.append(Adventurersid)
            if(len(temp_page)>=10):
                temp_page = []
                page_list.append(temp_page)

        if(len(page_list) != 0 and len(page_list[len(page_list)-1])==0):
            page_list.pop(len(page_list)-1)
        
        await pageUnitsHandler(client,ctx,page_list,db,total_results,search)
    db.closeconnection()

async def pageUnitsHandler(client: WaitForClient, ctx: CommandContext, page_list: List[List[list]], db: DBcontroller, total_results: int, search: List[str]):
    """This handles the message scrolling of the character search and all the other
    page logic for multiple results

    Arguments:
        client {interactions.ext.wait_for.WaitForClient} -- the discord bot object
        ctx {interactions.ext.files.CommandContext} -- command message context
        page_list {list of list} -- list of pages, Pages are lists with adventurers. Adventurers are tuples with (some number,title,adventurername,id)
        db {DBController.DBController} -- Database connector object
        total_results {int} -- total number of results from the query
        search {list[str]} -- list of words in the search query
    """

    # set up
    current_page = 0
    temp_embed = interactions.Embed()
    temp_embed.description = "Selet a unit via the dropdown menu, or switch pages with the buttons"
    temp_embed.color = Status.OK.value
    temp_embed.title = "{} results for {}".format(str(total_results),search)
    temp_embed.set_footer(text="Page {} of {}".format(current_page+1,len(page_list)))
    
    temp_embed = clearSetField(temp_embed, page_list[current_page])
    temp_embed.set_image(url="attachment://temp.png")
    iconsIm = get_units_image(page_list)
    ifile = make_ifile(iconsIm)

    components = build_components(page_list, current_page)
    msg = await ctx.send(embeds=temp_embed, files=ifile, components=components)

    while True:
        # for some reason open files (BytesIO objects) get closed after every loop execution
        # thus we keep the Image.Image object in memory instead, recreating the 
        ifile = make_ifile(iconsIm)
        try:
            component_ctx: ComponentContext = await client.wait_for_component(
                components=components, messages=msg, timeout=TIMEOUT,
            )

            if(component_ctx.custom_id == "previous_page"):
                if(current_page > 0):
                    current_page = current_page -1
                else:
                    current_page = len(page_list)-1
                temp_embed = clearSetField(temp_embed, page_list[current_page])
            elif(component_ctx.custom_id == "next_page"):
                if( current_page+1 < len(page_list)):
                    current_page = current_page +1
                else:
                    current_page = 0
                temp_embed = clearSetField(temp_embed, page_list[current_page])
            elif(component_ctx.custom_id == "unit_select"):
                await msg.delete()
                await singleAdventurer(client, ctx, db, component_ctx.data.values[0])
                break

            temp_embed.set_footer(text="Page {} of {}".format(current_page+1,len(page_list)))
            components = build_components(page_list, current_page)
            # it shouldn't be necessary to pass the files again on edit
            # but for some reason it doesn't work otherwise
            await component_ctx.edit(files=ifile, embeds=temp_embed, components=components)

        except asyncio.TimeoutError:
            temp_embed.color = Status.KO.value
            return await ctx.edit(files=ifile, embeds=temp_embed, components=[])


def build_components(page_list: List[list], current_page: int) -> List[interactions.ActionRow]:
    select_menu = interactions.SelectMenu(
        placeholder="Choose a unit",
        custom_id="unit_select",
        options=[
            interactions.SelectOption(
                label=f"{unit[1]} - {unit[2]}",
                value=unit[3],
            )
            for unit in page_list[current_page]
        ]
    )
    select_row = interactions.ActionRow(components=[select_menu])
    interactions.ActionRow(components=[to_start, previous_page, next_page, to_end])
    components = [select_row]
    if len(page_list) > 1:
        arrow_row = interactions.ActionRow(components=[to_start, previous_page, next_page, to_end])
        components.append(arrow_row)

    return components

def make_ifile(file: Image.Image) -> interactions.File:
    imgByteArr = io.BytesIO()
    file.save(imgByteArr, format='PNG')
    imgByteArr.seek(0)
    ifile = interactions.File(fp=imgByteArr, filename="temp.png")
    return ifile

def clearSetField(temp_embed: interactions.Embed, units: List[list]) -> interactions.Embed:
    temp_embed.clear_fields()
    value = ""
    for i, unit in enumerate(units):
        value += f"{i+1}. [{unit[1]}] {unit[2]}\n"
    temp_embed.add_field(name="Units", value=value)
    return temp_embed


async def singleAdventurer(client: WaitForClient, ctx: CommandContext, db: DBcontroller, assistadventurerid):
    """This handles the logic of choosing of the character search and setting up
    for a single result search

    Arguments:
        client {interactions.ext.wait_for.WaitForClient} -- the discord bot object
        ctx {interactions.ext.files.CommandContext} -- command message context
        db {DBController.DBController} -- Database connector object
        assistadventurerid {int} -- the assist/adventurer id of the wanted search
    """

    temp_embed = interactions.Embed()
    dev_embed = interactions.Embed()
    temp_embed.color = Status.OK.value
    dev_embed.color = Status.OK.value
    if "Ad" in assistadventurerid:
        info = db.assembleAdventurer(assistadventurerid[2:])
        for adventurerdev in info[4]:
            dev_embed.add_field(name=adventurerdev[0], value=adventurerdev[1], inline=False)
        is_adv = True
    else:
        info = db.assembleAssist(assistadventurerid[2:])
        is_adv = False
    stats, abilities = assembleStats(info[3],0,"",0)
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
        print(folder_name)
        print("./images/units/"+ folder_name + "/hex.png")
        file_list.append(interactions.File("./images/units/"+ folder_name + "/hex.png"))
        file_list.append(interactions.File("./images/units/"+ folder_name + "/all_rectangle.png"))
        temp_embed.set_thumbnail(url="attachment://hex.png")
        dev_embed.set_thumbnail(url="attachment://hex.png")
        temp_embed.set_image(url="attachment://all_rectangle.png")
        dev_embed.set_image(url="attachment://all_rectangle.png")
    except:
        pass
    
    if(is_adv):
        await pageHandler(client, ctx, file_list, info[3], temp_embed, dev_embed, info[6], info[5])
    else:
        await pageHandler(client, ctx, file_list, info[3], temp_embed)

async def pageHandler(
    client: WaitForClient,
    ctx: CommandContext,
    file_list: list,
    stats_dict: dict,
    temp_embed: interactions.Embed,
    dev_embed: Optional[interactions.Embed] = None,
    unit_type: Optional[str] = "",
    ascended: Optional[bool] = None
):
    """This handles the logic of the page handling for the single result unit

    Arguments:
        client {interactions.ext.wait_for.WaitForClient} -- the discord bot object
        ctx {interactions.ext.files.CommandContext} -- command message context
        temp_embed {interactions.embed} -- adventurer stats/skills page
        file_list {list of pictures} -- images to be displayed for pages
        dev_embed {interactions.embed} -- the adventurer development page
        stats_dict {dict} -- the stats of the current unit
        unit_type {string} -- balance,physical,magical for stats calculation
        ascended {bool} -- adventurer has hero ascension or not
    """

    def updateStats():
        temp_embed.description = str(limitbreak_add_emoji) * current_limitbreak + str(limitbreak_sub_emoji) * (MAXLB-current_limitbreak)
        if(ascended):
            temp_embed.description = temp_embed.description + "    " + hero_ascend_add_emoji * current_ha + hero_ascend_sub_emoji*(MAXHA-current_ha)

        stats, abilities = assembleStats(stats_dict,current_limitbreak,unit_type,current_ha)

        # have to remove and insert again, since set_field_at doesn't work
        # a fix is waiting for release: https://github.com/interactions-py/library/pull/1033
        temp_embed.remove_field(0)
        temp_embed.insert_field_at(0,name="Stats", value=stats, inline=True)
        temp_embed.remove_field(1)
        temp_embed.insert_field_at(1,name="Abilities", value=abilities, inline=True)


    MAXLB = 5
    MAXHA = 6
    current_page = 0
    current_limitbreak = 5
    current_ha = 0
    page_list = [temp_embed]
    if dev_embed:
        page_list.append(dev_embed)
    temp_embed.set_footer(text="Page {} of {}".format(current_page+1,len(page_list))) 

    updateStats()
    stats_buttons = [limitbreak_sub_button, limitbreak_add_button]
    if(ascended):
        stats_buttons += [hero_ascend_sub_button, hero_ascend_add_button]
    stats_button_row = interactions.ActionRow(components=stats_buttons)
    components = [stats_button_row]
    if(len(page_list) > 1):
        arrow_row = interactions.ActionRow(components=[previous_page, next_page])
        components = [arrow_row] + components
    msg = await ctx.send(files=file_list,embeds=page_list[current_page], components=components)

    buttons = [previous_page, next_page, limitbreak_sub_button, limitbreak_add_button]

    while True:
        # files seem to be automatically closed, have to reopen them on every loop execution
        refresh_files(file_list)
        try:
            component_ctx: ComponentContext = await client.wait_for_component(
                components=buttons,
                messages=msg,
                timeout=TIMEOUT,
            )

            if(component_ctx.custom_id == "previous_page"):
                if(current_page > 0):
                    current_page = current_page -1
                else:
                    current_page = len(page_list)-1
            elif(component_ctx.custom_id == "next_page"):
                if( current_page+1 < len(page_list)):
                    current_page = current_page +1
                else:
                    current_page = 0
            elif(component_ctx.custom_id == "limitbreak_sub"):
                if(current_limitbreak > 0):
                    current_limitbreak = current_limitbreak -1
                else:
                    current_limitbreak = MAXLB
                updateStats()
            elif(component_ctx.custom_id == "limitbreak_add"):
                if(current_limitbreak < MAXLB):
                    current_limitbreak = current_limitbreak +1
                else:
                    current_limitbreak = 0
                updateStats()
            elif(component_ctx.custom_id == "hero_ascend_sub"):
                if(current_ha > 0):
                    current_ha = current_ha -1
                else:
                    current_ha = MAXHA
                updateStats()
            elif(component_ctx.custom_id == "hero_ascend_add"):
                if(current_ha < MAXHA):
                    current_ha = current_ha +1
                else:
                    current_ha = 0
                updateStats()

            page_list[current_page].set_footer(text="Page {} of {}".format(current_page+1,len(page_list)))
            # it shouldn't be necessary to pass the files again on edit
            # but for some reason it doesn't work otherwise
            await component_ctx.edit(files=file_list,embeds=page_list[current_page])

        except asyncio.TimeoutError:
            page_list[current_page].color = Status.KO.value
            return await msg.edit(files=file_list, embeds=page_list[current_page], components=[])

def refresh_files(file_list: List[interactions.File]):
    for file in file_list:
        file._fp = open(file._fp.name, "rb")

def assembleStats(stats_dict: dict, limitbreak: int, unit_type: str, heroascend: int) -> Tuple[str, str]:
    """ Calculates Abilities based on limit break and hero ascension (if avaliable)

    Arguments:
        stats_dict {dict} -- the stats dictionary
        limitbreak {int} -- the limit break of a unit, 0 = no LB, 5 = MLB
        unit_type {str} -- balance, physical, magical
        heroascend {int} -- the hero ascension #, 0 = no HA and 6 = MHA

    Returns:
        str -- the stats string
    """

    if (unit_type.lower() == "physical_type"):
        ascension_stats = HeroAscensionStatsP
    elif (unit_type.lower() == "magic_type"):
        ascension_stats = HeroAscensionStatsM
    elif (unit_type.lower() == "healer_type"):
        ascension_stats = HeroAscensionStatsH
    elif (unit_type.lower() == "defense_type"):
        ascension_stats = HeroAscensionStatsD
    else:
        ascension_stats = HeroAscensionStatsB

    temp_hp = int(stats_dict["hp"][limitbreak]) + ascension_stats.HP.value[heroascend]
    temp_mp = int(stats_dict["mp"][limitbreak]) + ascension_stats.MP.value[heroascend]
    temp_pat = int(stats_dict["physical_attack"][limitbreak]) + ascension_stats.PAT.value[heroascend]
    temp_mat = int(stats_dict["magic_attack"][limitbreak]) + ascension_stats.MAT.value[heroascend]
    temp_def = int(stats_dict["defense"][limitbreak]) + ascension_stats.DEF.value[heroascend]

    res1 = f"HP : {temp_hp}\n"
    res1 += f"MP : {temp_mp}\n"
    res1 += f"P.AT : {temp_pat}\n"
    res1 += f"M.AT : {temp_mat}\n"
    res1 += f"DEF : {temp_def}\n"

    temp_str = int(stats_dict["strength"][limitbreak]) + ascension_stats.STR.value[heroascend]
    temp_end = int(stats_dict["endurance"][limitbreak]) + ascension_stats.END.value[heroascend]
    temp_dex = int(stats_dict["dexterity"][limitbreak]) + ascension_stats.DEX.value[heroascend]
    temp_agi = int(stats_dict["agility"][limitbreak]) + ascension_stats.AGI.value[heroascend]
    temp_mag = int(stats_dict["magic"][limitbreak]) + ascension_stats.MAG.value[heroascend]

    res2 = f"Str. : {temp_str}\n"
    res2 += f"End. : {temp_end}\n"
    res2 += f"Dex. : {temp_dex}\n"
    res2 += f"Agi. : {temp_agi}\n"
    res2 += f"Mag. : {temp_mag}\n"

    return (res1, res2)


def get_units_image(page_list) -> Image.Image:
    images = []
    for page in page_list:
        for unit in page:
            path = "./images/units/"+unit[2]+" ["+unit[1]+"]/"
            if not os.path.isdir(path):
                print("Could not find folder:",path)
                path = "./images/units/gac_dummy/"
            path += "hex.png"

            image = Image.open(path)
            images.append(image)

    full_image = concatenate_images(images, per_line=5, white_background=False)
    return full_image

def concatenate_images(images, per_line=4, white_background=False) -> Image.Image:
    chunks = [images[x:x+per_line] for x in range(0, len(images), per_line)]

    images_lines = []
    for chunk in chunks:
        images_line = concatenate_images_horizontally(chunk,white_background)
        images_lines.append(images_line)

    full_image = concatenate_images_vertically(images_lines)
    return full_image

def concatenate_images_horizontally(images,white_background=False) -> io.BytesIO:
    widths, heights = zip(*(i.size for i in images))
    
    total_width = sum(widths)
    max_height = max(heights)
    
    new_im = Image.new("RGBA", (total_width, max_height))
    x_offset = 0
    for im in images:
        new_im.paste(im, (x_offset,0))
        x_offset += im.size[0]

    if white_background:
        new_im.load() # required for png.split()
        image = Image.new("RGB", new_im.size, (255, 255, 255))
        image.paste(new_im, mask=new_im.split()[3]) # 3 is the alpha channel
    else:
        image = new_im

    return convert_to_bytes(image)

def concatenate_images_vertically(image_paths) -> Image.Image:
    images = [Image.open(x) for x in image_paths]
    widths, heights = zip(*(i.size for i in images))
    
    total_width = max(widths)
    max_height = sum(heights)
    
    new_im = Image.new('RGBA', (total_width, max_height))
    
    y_offset = 0
    for im in images:
        new_im.paste(im, (0,y_offset))
        y_offset += im.size[1]

    return new_im

def convert_to_bytes(img: Image.Image) -> io.BytesIO:
    imgByteArr = io.BytesIO()
    img.save(imgByteArr, format='PNG')
    imgByteArr.seek(0)
    return imgByteArr