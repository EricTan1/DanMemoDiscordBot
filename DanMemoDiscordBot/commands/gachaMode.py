import discord
import asyncio
import datetime

from database.entities.User import User
from commands.utils import GachaModes, getDefaultEmoji
from database.DBcontroller import DBcontroller

async def run(dbConfig, client, ctx, *args):
    author = str(ctx.message.author)
    content = ctx.message.content

    print("\nReceived message from '"+author+"' with content '"+content+"'")

    if "img" in args:
        gacha_mode = GachaModes.IMG
    elif "gif" in args:
        gacha_mode = GachaModes.GIF
    else:
        await ctx.message.add_reaction(getDefaultEmoji("x"))

    user = User.get_user(dbConfig, author)
    user.gacha_mode = gacha_mode.value
    user.update_user(dbConfig,datetime.datetime.now(),content)

    await ctx.message.add_reaction(getDefaultEmoji("white_check_mark"))