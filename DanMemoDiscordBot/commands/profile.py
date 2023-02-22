import asyncio
import math
import operator
from typing import Any, Dict, List, Tuple

import interactions
from interactions.ext.files import CommandContext, ComponentContext
from interactions.ext.wait_for import WaitForClient

from commands.buttons import next_page, previous_page, to_end, to_start
from commands.utils import TIMEOUT, Status, get_emoji
from database.DBcontroller import DBConfig
from database.entities.User import User

arrow_left = "\u2b05"
arrow_right = "\u27a1"
star_emoji = "\u2b50"
crepe_emoji = get_emoji("crepe")
adventurer_emoji = get_emoji("ad_filter")
assist_emoji = get_emoji("as_filter")
limitbreak_emojis = [get_emoji(f"limitbreak_{number}") for number in range(1, 6)]


async def run(
    dbConfig: DBConfig, client: WaitForClient, ctx: CommandContext, sub_command: str
):
    author = str(ctx.author)
    authorUniqueId = str(ctx.author.id)  # type: ignore [union-attr]
    user = User.get_user(dbConfig, author, authorUniqueId)

    if sub_command == "summary":
        is_summary = True
    else:
        is_summary = False

    crepes = user.crepes
    if crepes is None:
        crepes = 0

    currency_line = f"{crepes} x {crepe_emoji.format}\n"

    units = []
    if user.units is not None:
        for key in user.units:
            units.append(user.units[key])
    print(units)

    units = sorted(units, key=operator.itemgetter("character_name"))
    units = sorted(units, key=operator.itemgetter("unit_label"))
    units = sorted(units, key=operator.itemgetter("number"), reverse=True)
    units = sorted(units, key=operator.itemgetter("unit_type"))
    units = sorted(units, key=operator.itemgetter("stars"), reverse=True)

    if is_summary:
        units_lines = get_summarized_unit_lines(units)
    else:
        units_lines = get_detailed_unit_lines(units)

    current_page = 0
    per_page = 20
    number_pages = math.ceil(len(units_lines) / per_page)
    if number_pages == 0:
        number_pages = 1

    if is_summary:
        description = currency_line
        for i in range(len(units_lines)):
            description += units_lines[i]
    else:
        description = build_detailed_description(
            currency_line, units_lines, current_page
        )

    upper_footer = f"Total distinct number: {user.units_distinct_number}"
    upper_footer += f"\nScore: {user.units_score}"
    if not is_summary:
        footer = upper_footer + f"\n\nPage {current_page+1} of {number_pages}"
    else:
        footer = upper_footer

    embed = interactions.Embed()
    embed.color = Status.OK.value
    embed.set_thumbnail(url=ctx.author.user.avatar_url)  # type: ignore [union-attr]
    embed.title = f"{ctx.author.nick}'s summary profile"
    embed.description = description
    embed.set_footer(text=footer)

    components = []
    if number_pages > 1 and not is_summary:
        components = [to_start, previous_page, next_page, to_end]
    msg = await ctx.send(embeds=embed, components=components)

    if not components:
        return

    while True:
        try:
            component_ctx: ComponentContext = await client.wait_for_component(
                components=components,  # type: ignore [arg-type]
                messages=msg,
                timeout=TIMEOUT,
            )

            if component_ctx.custom_id == "previous_page":
                current_page = (current_page - 1) % number_pages
            elif component_ctx.custom_id == "next_page":
                current_page = (current_page + 1) % number_pages
            elif component_ctx.custom_id == "to_start":
                current_page = 0
            elif component_ctx.custom_id == "to_end":
                current_page = number_pages - 1

            embed.description = build_detailed_description(
                currency_line, units_lines, current_page
            )
            footer = upper_footer + f"\n\nPage {current_page+1} of {number_pages}"
            embed.set_footer(text=footer)

            await component_ctx.edit(embeds=embed)

        except asyncio.TimeoutError:
            embed.color = Status.KO.value
            return await ctx.edit(embeds=embed, components=[])


def get_summarized_unit_lines(units: List[Dict[str, Any]]) -> List[str]:
    sorted_categories: List[Tuple[str, int]] = []
    previous_category = ""
    previous_number = 0
    for unit in units:
        category = star_emoji * unit["stars"] + " "
        if unit["unit_type"] == "adventurer":
            category += adventurer_emoji.format
        elif unit["unit_type"] == "assist":
            category += assist_emoji.format

        if unit["number"] > 1:
            number = min(unit["number"] - 2, 4)
            category += " " + limitbreak_emojis[number].format

        if category == previous_category:
            previous_number += 1
            sorted_categories[-1] = (category, previous_number)
        else:
            previous_category = category
            previous_number = 1
            sorted_categories.append((category, previous_number))

    units_lines = []
    for item in sorted_categories:
        units_line = f"{item[0]} x {item[1]}\n"
        units_lines.append(units_line)

    return units_lines


def get_detailed_unit_lines(units: List[Dict[str, Any]]) -> List[str]:
    units_lines = []
    for unit in units:
        units_line = star_emoji * unit["stars"] + " "
        if unit["unit_type"] == "adventurer":
            units_line += adventurer_emoji.format
        elif unit["unit_type"] == "assist":
            units_line += assist_emoji.format
        units_line += (
            f" [{unit['unit_label']}] {unit['character_name']}: {unit['number']}\n"
        )
        units_lines.append(units_line)

    return units_lines


def build_detailed_description(
    currency_line: str, units_lines: List[str], current_page: int, per_page=20
):
    description = currency_line
    for i in range(len(units_lines)):
        if per_page * current_page <= i and i < per_page * (current_page + 1):
            description += units_lines[i]
    return description
