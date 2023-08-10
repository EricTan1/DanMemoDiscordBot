import math
from asyncio import TimeoutError

from interactions import Client, ComponentContext, Embed, File, SlashContext

from commands.buttons import next_page, previous_page, to_end, to_start
from commands.utils import TIMEOUT, Status, TopCategories
from database.DBcontroller import DBConfig, DBcontroller


async def run(dbConfig: DBConfig, client: Client, ctx: SlashContext, sub_command: str):
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

    embed = Embed()
    embed.color = Status.OK.value
    embed.set_thumbnail(url="attachment://texture.png")
    embed.title = "Top " + category.name.lower().capitalize()
    embed.description = description
    embed.set_footer(text=footer)

    components = []
    if number_pages > 1:
        components = [to_start, previous_page, next_page, to_end]

    ifile = File("./images/units/" + thumbnail + "/texture.png")
    msg = await ctx.send(embeds=embed, components=components, files=ifile)

    if not components:
        return

    while True:
        ifile = File("./images/units/" + thumbnail + "/texture.png")
        try:
            component_ctx: ComponentContext = (
                await client.wait_for_component(
                    components=components,
                    messages=msg,
                    timeout=TIMEOUT,
                )
            ).ctx

            match component_ctx.custom_id:
                case "previous_page":
                    current_page = (current_page - 1) % number_pages
                case "next_page":
                    current_page = (current_page + 1) % number_pages
                case "to_start":
                    current_page = 0
                case "to_end":
                    current_page = number_pages - 1

            embed.description = build_description(lines, current_page)

            footer_page = f"\n\nPage {current_page+1} of {number_pages}"
            footer = footer_rank + footer_page
            embed.set_footer(text=footer)

            await component_ctx.edit_origin(embeds=embed, components=components)

        except TimeoutError:
            embed.color = Status.KO.value
            ifile = File("./images/units/" + thumbnail + "/texture.png")
            return await msg.edit(embeds=embed, components=[])


def build_description(lines: list[str], current_page: int, per_page=10):
    description = ""
    for i in range(len(lines)):
        if per_page * current_page <= i and i < per_page * (current_page + 1):
            description += lines[i]
    return description
