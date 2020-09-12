import discord
import asyncio
import datetime

from database.entities.User import User
from commands.utils import GachaModes, getDefaultEmoji
from database.DBcontroller import DBcontroller

async def run(dbConfig, client, ctx, *args):
    author = str(ctx.message.author)
    authorUniqueId = str(ctx.message.author.id)
    content = ctx.message.content
    
    print("\nReceived message from '"+author+"("+authorUniqueId+")' with content '"+content+"'")

    user = User.get_user(dbConfig, author, authorUniqueId)

    if "img" in args:
        gacha_mode = GachaModes.IMG
    elif "gif" in args:
        gacha_mode = GachaModes.GIF
    else:
        await ctx.message.add_reaction(getDefaultEmoji("x"))

    user = User.get_user(dbConfig, author, authorUniqueId)
    user.gacha_mode = gacha_mode.value
    user.update_user(dbConfig,datetime.datetime.now(),content)

    await ctx.message.add_reaction(getDefaultEmoji("white_check_mark"))