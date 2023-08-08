import datetime

from interactions import Embed, SlashContext

from commands.utils import GachaModes, Status
from database.DBcontroller import DBConfig
from database.entities.User import User


async def run(dbConfig: DBConfig, ctx: SlashContext, mode: str):
    author = str(ctx.author)
    authorUniqueId = str(ctx.author.id)  # type: ignore [union-attr]

    user = User.get_user(dbConfig, author, authorUniqueId)

    embed = Embed()
    if mode == "image":
        gacha_mode = GachaModes.IMG
    elif mode == "gif":
        gacha_mode = GachaModes.GIF

    user = User.get_user(dbConfig, author, authorUniqueId)
    user.gacha_mode = gacha_mode.value
    user.update_user(dbConfig, datetime.datetime.now(), "!$gachamode")

    embed.title = f"Changed gacha mode to {mode}"
    embed.color = Status.OK.value
    return await ctx.send(embeds=embed)
