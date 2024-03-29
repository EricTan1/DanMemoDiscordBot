import datetime

from interactions import Embed, File, SlashContext

from commands.emojis import crepe_emoji
from commands.utils import Status
from database.DBcontroller import DBConfig
from database.entities.User import User


async def run(db_config: DBConfig, ctx: SlashContext):
    author = str(ctx.author)
    authorUniqueId = str(ctx.author.id)

    user = User.get_user(db_config, author, authorUniqueId)

    now = datetime.datetime.now(datetime.timezone.utc)

    previous_bento: datetime.datetime = user.last_bento_date
    if previous_bento is not None:
        next_bracket = previous_bento.replace(microsecond=0, second=0, minute=0)
        if previous_bento.hour % 2 == 0:
            next_bracket += datetime.timedelta(hours=1)
        else:
            next_bracket += datetime.timedelta(hours=2)

        next_bracket = next_bracket.replace(tzinfo=datetime.timezone.utc)

        difference = (next_bracket - now).total_seconds()
        if difference > 0:
            await no_bento(user, ctx, difference)
            return

    if user.crepes is None:
        user.crepes = 0
    user.crepes += 1

    user.last_bento_date = now

    user.update_user(db_config, now, "!$bento")

    title = "Wait! Are you going to the dungeon today? Please take this with you! >///<"

    description = ctx.author.mention + " has received a " + crepe_emoji + "!"

    if user.crepes == 1:
        footer = "There is " + str(user.crepes) + " crepe left in their bento box!"
    else:
        footer = "There are " + str(user.crepes) + " crepes left in their bento box!"

    await make_message(ctx, title, description, footer, True)


async def no_bento(user: User, ctx: SlashContext, difference: float):
    currency_number = user.crepes
    if currency_number is None:
        currency_number = 0

    title = "You are back already?"

    minutes_left = int(difference / 60)

    description = (
        "Sorry, I don't have anything ready for you, " + ctx.author.mention + "..."
    )
    description += " Please come back again in **" + str(minutes_left) + "** min!"

    if currency_number > 1:
        footer = "There are " + str(currency_number) + " crepes left in your bento box!"
    else:
        footer = "There is " + str(currency_number) + " crepe left in your bento box!"

    await make_message(ctx, title, description, footer, False)


async def make_message(
    ctx: SlashContext, title: str, description: str, footer: str, yes: bool
):
    embed = Embed()
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
    await ctx.send(embeds=embed, files=File(f"./images/bento/{filename}.png"))
