import asyncio
import io
import os
from types import ModuleType
from typing import Callable, List

import interactions
from interactions.ext.files import CommandContext, ComponentContext
from interactions.ext.wait_for import WaitForClient
from PIL import Image

from commands.buttons import (
    filter_adventurer,
    filter_assist,
    next_page,
    previous_page,
    to_end,
    to_start,
)
from commands.unitsearch import characterSearch, skillSearch
from commands.utils import (
    TIMEOUT,
    Status,
    imageHorizontalConcat,
    imageToBytes,
    imageVerticalConcat,
)
from database.DBcontroller import DBConfig, DBcontroller


async def run(
    dbConfig: DBConfig,
    client: WaitForClient,
    ctx: CommandContext,
    search_words: str,
    is_character_search: bool,
):
    """Common base for skill and character Search
    <CommandPrefix> <Search>

    Arguments:
        dbConfig {[DBcontroller.dbConfig]} -- Database config usually local/environmental variables
        client {[interactions.ext.wait_for.WaitForClient]} -- the discord bot object
        ctx {[interactions.ext.files.CommandContext]} -- command message context
        search_words {str} -- the search query
        is_character_search {bool} -- True for character search, false for skill search
    """
    search = search_words.split()
    my_search = ""
    for words in search:
        my_search += words + " "

    db = DBcontroller(dbConfig)

    if is_character_search:
        my_list = db.characterSearch(my_search.replace("[", "").replace("]", ""))
    else:
        my_list = db.skillSearch(my_search)
    print(my_list)

    if len(my_list) == 0:
        temp_embed = interactions.Embed()
        temp_embed.title = "There are no results"
        temp_embed.color = Status.KO.value
        await ctx.send(embeds=temp_embed)
    elif is_character_search and len(my_list) == 1:
        await characterSearch.singleUnit(client, ctx, db, my_list[0][3])
    else:
        if is_character_search:
            page_list = characterSearch.get_page_list(my_list)
            total_results = len(my_list)
        else:
            page_list, total_results = skillSearch.get_page_list(my_list, db)

        if len(page_list) != 0 and len(page_list[len(page_list) - 1]) == 0:
            page_list.pop(len(page_list) - 1)

        await pageUnitsHandler(
            client, ctx, page_list, db, total_results, search, is_character_search
        )
    db.closeconnection()


async def pageUnitsHandler(
    client: WaitForClient,
    ctx: CommandContext,
    page_list: List[list],
    db: DBcontroller,
    total_results: int,
    search: List[str],
    is_character_search: bool,
):
    """This handles the message scrolling of the character search and all the other
    page logic for multiple results

    Arguments:
        client {interactions.ext.wait_for.WaitForClient} -- the discord bot object
        ctx {interactions.ext.files.CommandContext} -- command message context
        page_list {list of list} -- list of pages, Pages are lists with units. Units are tuples with (some number,title,adventurername,id)
        db {DBController.DBController} -- Database connector object
        total_results {int} -- total number of results from the query
        search {list[str]} -- list of words in the search query
        is_character_search {bool} -- True for character search, false for skill search
    """

    if is_character_search:
        search_module: ModuleType = characterSearch
    else:
        search_module = skillSearch

    # set up
    current_page = 0
    filter = ""
    current_page_list = page_list

    temp_embed = interactions.Embed()
    temp_embed.color = Status.OK.value
    temp_embed.title = f"{total_results} results for {search}"
    temp_embed.description = "Select a unit via the dropdown menu, switch pages with the buttons or filter by unit type"
    if not is_character_search:
        temp_embed.description += " or filter by unit type"
    temp_embed.set_footer(text=f"Page {current_page+1} of {len(current_page_list)}")
    temp_embed.set_image(url="attachment://temp.png")

    temp_embed = search_module.clearSetField(
        temp_embed, current_page_list[current_page]
    )
    iconsIm = get_units_image(page_list, search_module.get_unit_image_path)
    ifile = make_ifile(iconsIm)

    components = build_components(page_list, current_page, is_character_search)

    msg = await ctx.send(embeds=temp_embed, files=ifile, components=components)

    current_results = total_results

    while True:
        try:
            component_ctx: ComponentContext = await client.wait_for_component(
                components=components, # type: ignore [arg-type] # should not pass components but list of buttons
                messages=msg,
                timeout=TIMEOUT,
            )

            if component_ctx.custom_id == "previous_page":
                current_page = (current_page - 1) % len(current_page_list)
            elif component_ctx.custom_id == "next_page":
                current_page = (current_page + 1) % len(current_page_list)
            elif component_ctx.custom_id == "to_start":
                current_page = 0
            elif component_ctx.custom_id == "to_end":
                current_page = len(current_page_list) - 1
            elif component_ctx.custom_id == "filter_adventurer":
                (
                    current_page_list,
                    filter,
                    current_results,
                ) = skillSearch.filterAddRemove(
                    page_list, filter, "adventurer", total_results
                )
                current_page = 0
                temp_embed.title = f"{current_results} results for {search}"
                temp_embed.description = "Select a unit via the dropdown menu, switch pages with the buttons or filter by unit type\n"
                temp_embed.description += f"**Current filter:** {filter}"
                iconsIm = get_units_image(
                    current_page_list, search_module.get_unit_image_path
                )
            elif component_ctx.custom_id == "filter_assist":
                (
                    current_page_list,
                    filter,
                    current_results,
                ) = skillSearch.filterAddRemove(
                    page_list, filter, "assist", total_results
                )
                current_page = 0
                temp_embed.title = f"{current_results} results for {search}"
                temp_embed.description = "Select a unit via the dropdown menu, switch pages with the buttons or filter by unit type\n"
                temp_embed.description += f"**Current filter:** {filter}"
                iconsIm = get_units_image(
                    current_page_list, search_module.get_unit_image_path
                )
            elif component_ctx.custom_id == "unit_select":
                await msg.delete()
                return await characterSearch.singleUnit(
                    client, ctx, db, component_ctx.data.values[0] # type: ignore [index]
                )

            components = build_components(
                current_page_list, current_page, is_character_search
            )

            # If filter led to empty list
            if len(current_page_list) == 0:
                # temp_embed = interactions.Embed()
                temp_embed.clear_fields()
                temp_embed.footer = None
                temp_embed.title = "No relevant skills to display"
                temp_embed.description = f"**Current filter:** {filter}"
                temp_embed.color = Status.KO.value
                await component_ctx.edit(embeds=temp_embed, components=components)
            else:
                temp_embed = search_module.clearSetField(
                    temp_embed, current_page_list[current_page]
                )
                temp_embed.color = Status.OK.value
                temp_embed.set_footer(
                    text=f"Page {current_page+1} of {len(current_page_list)}"
                )

                # for some reason open files (BytesIO objects) get closed after every loop execution
                # thus we keep the Image.Image object in memory instead, recreating the object on every iteration
                ifile = make_ifile(iconsIm)
                # it shouldn't be necessary to pass the files again on edit
                # but for some reason it doesn't work otherwise
                await component_ctx.edit(
                    files=ifile, embeds=temp_embed, components=components
                )

        except asyncio.TimeoutError:
            ifile = make_ifile(iconsIm)
            temp_embed.color = Status.KO.value
            return await ctx.edit(files=ifile, embeds=temp_embed, components=[])


def build_components(
    page_list: List[list], current_page: int, is_character_search: bool
) -> List[interactions.ActionRow]:
    components = []

    if is_character_search:
        select_menu = interactions.SelectMenu(
            placeholder="Choose a unit",
            custom_id="unit_select",
            options=[
                interactions.SelectOption(
                    label=f"[{unit[1]}] - {unit[2]}",
                    value=unit[3],
                )
                for unit in page_list[current_page]
            ],
        )
        select_row = interactions.ActionRow(components=[select_menu])
        components.append(select_row)

    if len(page_list) > 1:
        arrow_row = interactions.ActionRow(
            components=[to_start, previous_page, next_page, to_end]
        )
        components.append(arrow_row)

    if not is_character_search:
        filter_row = interactions.ActionRow(
            components=[filter_adventurer, filter_assist]
        )
        components.append(filter_row)

    return components


def make_ifile(image: Image.Image) -> interactions.File:
    byteImage = imageToBytes(image)
    ifile = interactions.File(fp=byteImage, filename="temp.png")
    return ifile


def get_units_image(
    page_list: List[list], path_getter: Callable[[tuple], str]
) -> Image.Image:
    if len(page_list) == 0:
        return

    paths = []
    for page in page_list:
        for unit in page:
            path = path_getter(unit)
            if not os.path.isdir(path):
                print("Could not find folder:", path)
                path = "./images/units/gac_dummy/"
            path += "hex.png"

            paths.append(path)

    full_image = concatenate_images(paths)
    return Image.open(full_image)


def concatenate_images(images: List[str]) -> io.BytesIO:
    per_line = 5
    chunks = [images[x : x + per_line] for x in range(0, len(images), per_line)]

    images_lines = []
    for chunk in chunks:
        images_line = imageHorizontalConcat(chunk)
        images_lines.append(images_line)

    return imageVerticalConcat(images_lines)
