import os
from asyncio import TimeoutError
from io import BytesIO
from types import ModuleType
from typing import Callable

from interactions import (
    ActionRow,
    Client,
    ComponentContext,
    Embed,
    File,
    SlashContext,
    StringSelectMenu,
    StringSelectOption,
)
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
    client: Client,
    ctx: SlashContext,
    search_words: str,
    is_character_search: bool,
):
    """Common base for skill and character Search
    <CommandPrefix> <Search>

    Arguments:
        dbConfig -- Database config usually local/environmental variables
        client -- the discord bot object
        ctx -- command message context
        search_words -- the search query
        is_character_search -- True for character search, false for skill search
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
        temp_embed = Embed()
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
    client: Client,
    ctx: SlashContext,
    page_list: list[list],
    db: DBcontroller,
    total_results: int,
    search: list[str],
    is_character_search: bool,
):
    """This handles the message scrolling of the character search and all the other
    page logic for multiple results

    Arguments:
        client -- the discord bot object
        ctx -- command message context
        page_list -- list of pages, Pages are lists with units. Units are tuples with (some number,title,adventurername,id)
        db -- Database connector object
        total_results -- total number of results from the query
        search -- list of words in the search query
        is_character_search -- True for character search, false for skill search
    """

    if is_character_search:
        search_module: ModuleType = characterSearch
    else:
        search_module = skillSearch

    # set up
    current_page = 0
    filter = ""
    current_page_list = page_list

    temp_embed = Embed()
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

    unnested_components = []
    for row in components:
        unnested_components += row.components

    while True:
        image_changed = False
        try:
            component_ctx: ComponentContext = (
                await client.wait_for_component(
                    components=unnested_components,
                    messages=msg,
                    timeout=TIMEOUT,
                )
            ).ctx

            match component_ctx.custom_id:
                case "previous_page":
                    current_page = (current_page - 1) % len(current_page_list)
                case "next_page":
                    current_page = (current_page + 1) % len(current_page_list)
                case "to_start":
                    current_page = 0
                case "to_end":
                    current_page = len(current_page_list) - 1
                case "filter_adventurer":
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
                    image_changed = True
                case "filter_assist":
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
                    image_changed = True
                case "unit_select":
                    await msg.delete()
                    return await characterSearch.singleUnit(
                        client, ctx, db, component_ctx.values[0]
                    )

            components = build_components(
                current_page_list, current_page, is_character_search
            )

            # If filter led to empty list
            if len(current_page_list) == 0:
                temp_embed.fields = []
                temp_embed.footer = None
                temp_embed.title = "No relevant skills to display"
                temp_embed.description = f"**Current filter:** {filter}"
                temp_embed.color = Status.KO.value
                await component_ctx.edit_origin(
                    embeds=temp_embed, components=components
                )
            else:
                temp_embed = search_module.clearSetField(
                    temp_embed, current_page_list[current_page]
                )
                temp_embed.color = Status.OK.value
                temp_embed.set_footer(
                    text=f"Page {current_page+1} of {len(current_page_list)}"
                )

                # We don't change the files unless necessary, for performance reasons
                if image_changed:
                    ifile = make_ifile(iconsIm)
                    await component_ctx.edit_origin(
                        files=ifile, embeds=temp_embed, components=components
                    )
                else:
                    await component_ctx.edit_origin(
                        embeds=temp_embed, components=components
                    )

        except TimeoutError:
            temp_embed.color = Status.KO.value
            return await msg.edit(embeds=temp_embed, components=[])


def build_components(
    page_list: list[list], current_page: int, is_character_search: bool
) -> list[ActionRow]:
    components = []

    if is_character_search:
        select_menu = StringSelectMenu(
            [
                StringSelectOption(
                    label=f"[{unit[1]}] - {unit[2]}",
                    value=unit[3],
                )
                for unit in page_list[current_page]
            ],
            placeholder="Choose a unit",
            custom_id="unit_select",
        )
        select_row = ActionRow(select_menu)
        components.append(select_row)

    if len(page_list) > 1:
        arrow_row = ActionRow(to_start, previous_page, next_page, to_end)
        components.append(arrow_row)

    if not is_character_search:
        filter_row = ActionRow(filter_adventurer, filter_assist)
        components.append(filter_row)

    return components


def make_ifile(image: Image.Image) -> File:
    byteImage = imageToBytes(image)
    ifile = File(byteImage, file_name="temp.png")
    return ifile


def get_units_image(
    page_list: list[list], path_getter: Callable[[tuple], str]
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


def concatenate_images(images: list[str]) -> BytesIO:
    per_line = 5
    chunks = [images[x : x + per_line] for x in range(0, len(images), per_line)]

    images_lines = []
    for chunk in chunks:
        images_line = imageHorizontalConcat(chunk)
        images_lines.append(images_line)

    return imageVerticalConcat(images_lines)
