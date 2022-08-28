import discord
import operator
import math
import asyncio
import itertools

from database.entities.User import User
from commands.utils import Status, get_emoji, get_author

async def run(dbConfig, client, ctx, *args):
    author = str(ctx.message.author)
    authorUniqueId = str(ctx.message.author.id)
    content = ctx.message.content
    
    print("\nReceived message from '"+author+"("+authorUniqueId+")' with content '"+content+"'")

    user = User.get_user(dbConfig, author, authorUniqueId)

    if "summary" in args:
        await summary_message(user, client, ctx, *args)
    else:
        await detailed_message(user, client, ctx, *args)


async def summary_message(user, client, ctx, *args):
    crepes = user.crepes
    if crepes is None:
        crepes = 0

    currency_lines = []
    currency_line = str(crepes)+" x "+get_emoji("crepe").toString(ctx)+"\n"
    currency_lines.append(currency_line)

    units = []
    if user.units is not None:
        for key in user.units:
            units.append(user.units[key])
    print(units)

    units = sorted(units, key = operator.itemgetter("number"), reverse=True)
    units = sorted(units, key = operator.itemgetter("unit_type"))
    units = sorted(units, key = operator.itemgetter("stars"), reverse=True)

    sorted_categories = []
    previous_category = None
    previous_number = None
    for unit in units:
        category = "🌟"*unit["stars"]
        if unit["unit_type"] == "adventurer":
            category += " " + get_emoji("ad_filter").toString(ctx)
        elif unit["unit_type"] == "assist":
            category += " " + get_emoji("as_filter").toString(ctx)
        if unit["number"] > 1:
            number = min(unit["number"]-1,5)
            category += " " + get_emoji("limitbreak_"+str(number)).toString(ctx)

        if category == previous_category:
            previous_number += 1
            sorted_categories[-1] = (category,previous_number)
        else:
            previous_category = category
            previous_number = 1
            sorted_categories.append((category,previous_number))

    title = get_author(ctx)+"'s summary profile"

    units_lines = []
    for item in sorted_categories:
        units_line = item[0] + " x " + str(item[1]) + "\n"
        units_lines.append(units_line)
    
    description = ""
    for line in currency_lines:
        description += line
    for i in range(len(units_lines)):
        description += units_lines[i]

    footer = "Total distinct number: " + str(user.units_distinct_number) + "\n"
    footer += "Score: " + str(user.units_score)

    embed = discord.Embed()
    embed.color = Status.OK.value
    embed.set_thumbnail(url=ctx.message.author.avatar_url)
    embed.title = title
    embed.description = description
    embed.set_footer(text=footer)
    await ctx.send(embed=embed)


async def detailed_message(user, client, ctx, *args):
    crepes = user.crepes
    if crepes is None:
        crepes = 0

    currency_lines = []
    currency_line = str(crepes)+" x "+get_emoji("crepe").toString(ctx)+"\n"
    currency_lines.append(currency_line)

    units = []
    if user.units is not None:
        for key in user.units:
            units.append(user.units[key])
    print(units)

    units = sorted(units, key = operator.itemgetter("character_name"))
    units = sorted(units, key = operator.itemgetter("unit_label"))
    units = sorted(units, key = operator.itemgetter("unit_type"))
    units = sorted(units, key = operator.itemgetter("stars"), reverse=True)

    units_lines = []
    for unit in units:
        units_line = "🌟"*unit["stars"]
        if unit["unit_type"] == "adventurer":
            units_line += " " + get_emoji("ad_filter").toString(ctx)
        elif unit["unit_type"] == "assist":
            units_line += " " + get_emoji("as_filter").toString(ctx)
        units_line +=  " [" + unit["unit_label"] + "] " + unit["character_name"] + ": " + str(unit["number"])+"\n"
        units_lines.append(units_line)

    title = get_author(ctx)+"'s profile"

    current_page = 0
    per_page = 20
    number_pages = math.ceil(len(units_lines)/per_page)
    if number_pages == 0:
        number_pages = 1

    description = build_description(currency_lines,units_lines,current_page,per_page)

    footer_number = "Total distinct number: " + str(len(units_lines))
    footer_page = "Page {} of {}".format(current_page+1, number_pages)
    footer = footer_number + "\n" + footer_page

    embed = discord.Embed()
    embed.color = Status.OK.value
    embed.set_thumbnail(url=ctx.message.author.avatar_url)
    embed.title = title
    embed.description = description
    embed.set_footer(text=footer)
    msg = await ctx.send(embed=embed)

    if number_pages == 1:
        return

    # update description with reactions
    emoji_left_arrow = "\u2b05"
    emoji_right_arrow = "\u27a1"
    emojis = [emoji_left_arrow, emoji_right_arrow]
    for emoji in emojis:
        await msg.add_reaction(emoji)

    while True:
        pending_tasks = [wait_for_reaction(client, msg.id, emojis, "reaction_add"),
                        wait_for_reaction(client, msg.id, emojis, "reaction_remove")]
        done_tasks, pending_tasks = await asyncio.wait(pending_tasks, timeout=60.0, return_when=asyncio.FIRST_COMPLETED)

        timeout = len(done_tasks) == 0

        if not timeout:
            task = done_tasks.pop()

            reaction, user = await task

        for remaining in itertools.chain(done_tasks, pending_tasks):
            remaining.cancel()

        if timeout:
            embed.color = Status.KO.value
            await msg.edit(embed=embed)
            break

        emoji = str(reaction.emoji)

        if emoji == emoji_left_arrow:
            current_page = (current_page - 1) % number_pages
        elif emoji == emoji_right_arrow:
            current_page = (current_page + 1) % number_pages
        
        embed.description = build_description(currency_lines, units_lines, current_page, per_page)
        
        footer_page = "Page {} of {}".format(current_page+1, number_pages)
        footer = footer_number + "\n" + footer_page
        embed.set_footer(text=footer)
        
        await msg.edit(embed=embed)     


def build_description(currency_lines, units_lines, current_page, per_page):
    description = ""
    for line in currency_lines:
        description += line
    for i in range(len(units_lines)):
        if per_page*current_page <= i and i < per_page*(current_page+1):
            description += units_lines[i]
    return description


def wait_for_reaction(client, msg_id, emojis, event_name):
    def check(reaction, user):
        return str(reaction.emoji) in emojis and user != client.user and reaction.message.id == msg_id

    return client.wait_for(event_name,check=check)
