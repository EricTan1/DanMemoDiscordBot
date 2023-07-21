import datetime

import interactions
from interactions.ext.files import CommandContext

from commands.utils import Status, get_emoji
from database.DBcontroller import DBConfig
from database.entities.User import User

crepe_emoji = get_emoji("crepe").format


async def run(db_config: DBConfig, ctx: CommandContext):
    author = str(ctx.author)
    authorUniqueId = str(ctx.author.id)  # type: ignore [union-attr]

    user = User.get_user(db_config, author, authorUniqueId)

    now = datetime.datetime.now(datetime.timezone.utc)

    previous_bento: datetime.datetime = user.last_bento_date
    if previous_bento is not None:
        next_bracket = previous_bento.replace(microsecond=0, second=0, minute=0)
        if previous_bento.hour % 2 == 0:
            next_bracket += datetime.timedelta(hours=1)
        else:
            next_bracket += datetime.timedelta(hours=2)

        print("previous_bento:", previous_bento)
        print("next_bracket:", next_bracket)
        next_bracket = next_bracket.replace(tzinfo=datetime.timezone.utc)
        print("next_bracket aware:", next_bracket)

        difference = (next_bracket - now).total_seconds()
        print("now:", now)
        print("difference:", difference)
        if difference > 0:
            await no_bento(user, ctx, difference)
            return

    if user.crepes is None:
        user.crepes = 0
    user.crepes += 1

    user.last_bento_date = now

    user.update_user(db_config, now, "!$bento")

    title = "Wait! Are you going to the dungeon today? Please take this with you! >///<"

    description = ctx.author.mention + " has received a " + crepe_emoji + "!"  # type: ignore [union-attr]

    if user.crepes == 1:
        footer = "There is " + str(user.crepes) + " crepe left in their bento box!"
    else:
        footer = "There are " + str(user.crepes) + " crepes left in their bento box!"

    await make_message(ctx, title, description, footer, True)


async def no_bento(user: User, ctx: CommandContext, difference: float):
    currency_number = user.crepes
    if currency_number is None:
        currency_number = 0

    title = "You are back already?"

    minutes_left = int(difference / 60)

    description = (
        "Sorry, I don't have anything ready for you, " + ctx.author.mention + "..."  # type: ignore [union-attr]
    )
    description += " Please come back again in **" + str(minutes_left) + "** min!"

    if currency_number > 1:
        footer = "There are " + str(currency_number) + " crepes left in your bento box!"
    else:
        footer = "There is " + str(currency_number) + " crepe left in your bento box!"

    await make_message(ctx, title, description, footer, False)


async def make_message(
    ctx: CommandContext, title: str, description: str, footer: str, yes: bool
):
    embed = interactions.Embed()
    embed.title = title
    embed.description = description
    embed.set_footer(text=footer)
    if yes:
        embed.color = Status.OK.value
        filename = "yes"
    else:
        embed.color = Status.KO.value
        filename = "nope"
    embed.set_image(url=f"attachment://{filename}.png")
    await ctx.send(
        embeds=embed, files=interactions.File(f"./images/bento/{filename}.png")
    )
