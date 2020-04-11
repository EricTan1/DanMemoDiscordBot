import discord
import datetime

from database.entities.User import User
from commands.utils import Status

class CustomEmoji:
    def __init__(self, id_inner, name, plural, id_discord):
        self.id_inner = id_inner
        self.name = name
        self.plural = plural
        self.id_discord = id_discord
    def toString(self,ctx):
        return str(ctx.bot.get_emoji(self.id_discord))

emojis = {  CustomEmoji("potato1","small potato","small potatoes",698248273387061439),
            CustomEmoji("potato2","medium potato","medium potatoes",698248273500307503),
            CustomEmoji("potato3","big potato","big potatoes",698248273613291590),
            CustomEmoji("crepe","crepe","crepes",698247637899411521)}

def get_emoji(id_inner):
    for emoji in emojis:
        if emoji.id_inner == id_inner:
            return emoji
    raise Exception("Unknown emoji id:",id_inner)

def mention_author(ctx):
    return ctx.message.author.mention

async def run(dbConfig, client, ctx):
    user = User.get_user(dbConfig, ctx.message.author)

    previous = user.get_last_bento_date()
    now = datetime.datetime.now()

    if previous != None and previous.date() >= now.date():
        await no_bento(user, client, ctx)
        return

    currency_number = user.get_crepes_number()
    if currency_number is None:
        currency_number = 0

    currency_number += 1
    user.set_crepes_number(currency_number)
    user.set_last_bento_date(now)
    user.updateUser(dbConfig)

    emoji = get_emoji("crepe")
    emojiStr = emoji.toString(ctx)

    title = "Wait! Are you going to the dungeon today? Please take this with you! >///<"

    description = mention_author(ctx) + " has received a " + emojiStr + "!"

    if currency_number > 1:
        footer = "There are " + str(currency_number) + " " + emoji.plural + " left in their bento box!"
    else:
        footer = "There is " + str(currency_number) + " " + emoji.name + " left in their bento box!"

    embed = discord.Embed()
    embed.color = Status.OK.value
    embed.title = title
    embed.description = description
    embed.set_footer(text=footer)
    embed.set_image(url="attachment://bento.png")
    await ctx.send(embed=embed, file=discord.File("./images/syr/bento.png"))


async def no_bento(user, client, ctx):
    currency_number = user.get_crepes_number()
    if currency_number is None:
        currency_number = 0

    emoji = get_emoji("crepe")
    emojiStr = emoji.toString(ctx)

    title = "You are back already?"

    description = "Sorry, I don't have anything ready for you, " + mention_author(ctx) + "..."
    description += " Please come back again tomorrow!"

    if currency_number > 1:
        footer = "There are " + str(currency_number) + " " + emoji.plural + " left in your bento box!"
    else:
        footer = "There is " + str(currency_number) + " " + emoji.name + " left in your bento box!"

    embed = discord.Embed()
    embed.color = Status.KO.value
    embed.title = title
    embed.description = description
    embed.set_footer(text=footer)
    embed.set_image(url="attachment://nope.png")
    await ctx.send(embed=embed, file=discord.File("./images/syr/nope.png"))
