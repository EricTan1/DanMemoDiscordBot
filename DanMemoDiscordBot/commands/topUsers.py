import interactions
from interactions.ext.files import CommandContext, ComponentContext
from interactions.ext.wait_for import WaitForClient
from typing import List
import math
import asyncio

from commands.utils import TIMEOUT, Status, TopCategories
from commands.buttons import previous_page, next_page, to_start, to_end
from database.DBcontroller import DBConfig, DBcontroller


async def run(
    dbConfig: DBConfig, client: WaitForClient, ctx: CommandContext, sub_command: str
):
    authorUniqueId = str(ctx.author.id)
    db = DBcontroller(dbConfig)

    if sub_command == "gourmets":
        category = TopCategories.GOURMETS
        thumbnail = "Ais Wallenstein [Santa Princess]"
    else:
        category = TopCategories.WHALES
        thumbnail = "Syr Flover [Countess]"

    users = db.get_top_users(category)

    rank = -1
    lines = []
    for i in range(len(users)):
        user = users[i]
        if authorUniqueId == user.discord_unique_id:
            rank = i + 1
        line = "**" + str(i + 1) + ".** " + user.discord_id + " **- "
        if category == TopCategories.GOURMETS:
            line += str(user.crepes)
        else:
            line += str(user.units_score)
        line += "**\n"
        lines.append(line)

    current_page = 0
    per_page = 10
    number_pages = math.ceil(len(lines) / per_page)
    if number_pages == 0:
        number_pages = 1

    description = build_description(lines, current_page)

    if rank == -1:
        footer_rank = "You are not ranked yet"
    else:
        footer_rank = "You are ranked #" + str(rank)

    footer_page = f"\n\nPage {current_page+1} of {number_pages}"
    footer = footer_rank + footer_page

    embed = interactions.Embed()
    embed.color = Status.OK.value
    embed.set_thumbnail(url="attachment://texture.png")
    embed.title = "Top " + category.name.lower().capitalize()
    embed.description = description
    embed.set_footer(text=footer)

    components = []
    if number_pages > 1:
        components = [to_start, previous_page, next_page, to_end]

    ifile = interactions.File("./images/units/" + thumbnail + "/texture.png")
    msg = await ctx.send(embeds=embed, components=components, files=ifile)

    if not components:
        return

    while True:
        ifile = interactions.File("./images/units/" + thumbnail + "/texture.png")
        try:
            component_ctx: ComponentContext = await client.wait_for_component(
                components=components,
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

            embed.description = build_description(lines, current_page)

            footer_page = f"\n\nPage {current_page+1} of {number_pages}"
            footer = footer_rank + footer_page
            embed.set_footer(text=footer)

            await component_ctx.edit(embeds=embed, components=components, files=ifile)

        except asyncio.TimeoutError:
            embed.color = Status.KO.value
            ifile = interactions.File("./images/units/" + thumbnail + "/texture.png")
            return await ctx.edit(embeds=embed, components=[], files=ifile)


def build_description(lines: List[str], current_page: int, per_page=10):
    description = ""
    for i in range(len(lines)):
        if per_page * current_page <= i and i < per_page * (current_page + 1):
            description += lines[i]
    return description
