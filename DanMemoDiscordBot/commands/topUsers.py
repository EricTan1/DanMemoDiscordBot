import discord
import operator
import math
import asyncio
import itertools

from database.entities.User import User
from commands.utils import Status, get_emoji, get_author, mention_author, dict_to_sns, sns_to_dict, TopCategories
from commands.cache import Cache
from database.DBcontroller import DBcontroller

async def run(dbConfig, client, ctx, *args):
    author = str(ctx.message.author)
    authorUniqueId = str(ctx.message.author.id)
    content = ctx.message.content
    
    print("\nReceived message from '"+author+"("+authorUniqueId+")' with content '"+content+"'")

    db = DBcontroller(dbConfig)
    
    if "crepes" in args:
        category = TopCategories.GOURMETS
        thumbnail = "Ais Wallenstein [Santa Princess]"
    else:
        category = TopCategories.WHALES
        thumbnail = "Syr Flover [Countess]"

    users = db.get_top_users(category)
    
    title = "Top "+category.name.lower().capitalize()
        
    rank = None
    lines = []
    for i in range(len(users)):
        user = users[i]
        if authorUniqueId == user.discord_unique_id:
            rank = i+1
        line = "**"+str(i+1)+".** " + user.discord_id + " **- "
        if category == TopCategories.GOURMETS:
            line += str(user.crepes)
        else:
            line += str(user.units_score)
        line += "**\n"
        lines.append(line)
    
    current_page = 0
    per_page = 10
    number_pages = math.ceil(len(lines)/per_page)
    if number_pages == 0:
        number_pages = 1

    description = build_description(lines,current_page,per_page)

    if rank is None:
        footer_rank = "You are not ranked yet"
    else:
        footer_rank = "You are ranked #" + str(rank)

    footer_page = "Page {} of {}".format(current_page+1, number_pages)
    footer = footer_rank + "\n" + footer_page

    embed = discord.Embed()
    embed.color = Status.OK.value
    #embed.set_thumbnail(url=ctx.message.author.avatar_url)
    embed.set_thumbnail(url="attachment://texture.png")
    embed.title = title
    embed.description = description
    embed.set_footer(text=footer)
    msg = await ctx.send(embed=embed, file=discord.File("./images/units/"+thumbnail+"/texture.png"))

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
        
        embed.description = build_description(lines, current_page, per_page)
        
        footer_page = "Page {} of {}".format(current_page+1, number_pages)
        footer = footer_rank + "\n" + footer_page
        embed.set_footer(text=footer)
        
        await msg.edit(embed=embed)

def build_description(lines, current_page, per_page):
    description = ""
    for i in range(len(lines)):
        if per_page*current_page <= i and i < per_page*(current_page+1):
            description += lines[i]
    return description

def wait_for_reaction(client, msg_id, emojis, event_name):
    def check(reaction, user):
        return str(reaction.emoji) in emojis and user != client.user and reaction.message.id == msg_id

    return client.wait_for(event_name,check=check)
