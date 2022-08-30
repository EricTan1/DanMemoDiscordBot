import datetime

import interactions
from interactions.ext.files import CommandContext

from commands.utils import GachaModes, Status
from database.DBcontroller import DBConfig
from database.entities.User import User


async def run(dbConfig: DBConfig, ctx: CommandContext, mode: str):
    author = str(ctx.author)
    authorUniqueId = str(ctx.author.id)

    user = User.get_user(dbConfig, author, authorUniqueId)

    embed = interactions.Embed()
    if mode == "image":
        gacha_mode = GachaModes.IMG
    elif mode == "gif":
        gacha_mode = GachaModes.GIF
    else:
        embed.title = "Error changing gacha mode!"
        embed.color = Status.KO.value
        return await ctx.send(embeds=embed)

    user = User.get_user(dbConfig, author, authorUniqueId)
    user.gacha_mode = gacha_mode.value
    user.update_user(dbConfig, datetime.datetime.now(), "!$gachamode")

    embed.title = f"Changed gacha mode to {mode}"
    embed.color = Status.OK.value
    return await ctx.send(embeds=embed)
