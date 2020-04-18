import discord
from PIL import Image
import io
import asyncio
import time
from numpy.random import choice
from os.path import isfile

from database.entities.User import User
from commands.utils import Status, get_emoji, mention_author, GachaRates, GachaRatesOnlyFourStars #, imageHorizontalConcat, imageVerticalConcat, skillSearchRotatingPage
from database.DBcontroller import DBcontroller

async def run(dbConfig, client, ctx, *args):
    user = User.get_user(dbConfig, ctx.message.author)

    currency_number = user.get_crepes_number()
    if currency_number is None:
        currency_number = 0

    if currency_number == 0:
        await no_gacha(user, currency_number, ctx)
        return

    currency_number -= 1
    user.set_crepes_number(currency_number)

    pulls = get_pulls(dbConfig, 10, GachaRates)
    pulls.extend(get_pulls(dbConfig, 1, GachaRatesOnlyFourStars))
    #pulls = [("adventurer", 4, 1, "Regiment Princess", "Ais Wallenstein")]*11
    '''pulls = []
    pulls.append(("adventurer",3,603,"Cyclop's New Year","Tsubaki Collbrande"))
    pulls.append(("adventurer",3,556,"Little Detective","Lunor Faust"))
    pulls.append(("adventurer",3,583,"Fist Fighter","Shakti Varma"))
    pulls.append(("assist",3,325,"Goddess of Purity","Hestia"))
    pulls.append(("adventurer",3,576,"Gale in Yukata","Ryu Lion"))
    pulls.append(("adventurer",3,513,"Evanescent","Hitachi Chigusa"))
    pulls.append(("assist",3,277,"Advisor","Eina Tulle"))
    pulls.append(("adventurer",3,539,"Artel Tart","Liliruca Arde"))
    pulls.append(("adventurer",3,607,"Ignis","Welf Crozzo"))
    pulls.append(("adventurer",3,501,"Maenads","Filvis Challia"))
    pulls.append(("assist",4,387,"In The End","Orna"))'''
    
    user.updateUser(dbConfig)

    await ten_pull_message(ctx, currency_number, pulls[:-1])
    await last_pull_message(ctx, pulls)


async def no_gacha(user, currency_number, ctx):
    emoji = get_emoji("crepe")
    emojiStr = emoji.toString(ctx)

    title = "Hold on! Who goes there?"

    description = "What do you think you are doing, " + mention_author(ctx) + "?"
    description += " Come back when you have some " + emoji.name + " for me!"

    footer = "There is " + str(currency_number) + " " + emoji.name + " left in your bento box!"

    embed = discord.Embed()
    embed.color = Status.KO.value
    embed.title = title
    embed.description = description
    embed.set_footer(text=footer)
    embed.set_image(url="attachment://nope.png")
    await ctx.send(embed=embed, file=discord.File("./images/gacha/nope.png"))

def random_pulls(number,gacha_rates):
    possibilities = [e.name for e in gacha_rates]
    probabilities = [e.value for e in gacha_rates]
    pulls = []
    for i in range(number):
        pulls.append(choice(possibilities,p=probabilities))
    return pulls

def get_pulls(dbConfig, number, gacha_rates):
    db = DBcontroller(dbConfig)

    pulls_category = random_pulls(number,gacha_rates)
    pulls = []
    for category in pulls_category:
        unit_type, stars, unit_id, title, name = db.getRandomUnit(category)
        pulls.append((unit_type, stars, unit_id, title, name))

    db.closeconnection()
    return pulls

async def ten_pull_message(ctx, currency_number, pulls):
    emoji = get_emoji("crepe")
    emojiStr = emoji.toString(ctx)

    title = "Hold on! Who goes there?"
    description = "I guess I could let you pull if you share your " + emoji.name + " with me. But please, don't get addicted."
    description += "\n" + mention_author(ctx) + " has shared one " + emojiStr + " with Ais!"

    if currency_number > 1:
        footer = "There are " + str(currency_number) + " " + emoji.plural + " left in your bento box!"
    else:
        footer = "There is " + str(currency_number) + " " + emoji.name + " left in your bento box!"

    hidden = "./lottery/gac_dummy/hex.png"
    pulls_images = []

    for pull in pulls:
        path = "./lottery/"+pull[3]+" "+pull[4]+"/hex.png"
        if not isfile(path):
            path = hidden
        pulls_images.append(path)

    per_line = 5
    gif_images = []

    for i in range(len(pulls_images)+1):
        images_current_iteration = pulls_images[:i] + [hidden] * (len(pulls_images)-i)

        full_imageBytes = concatenate_images(images_current_iteration, per_line)
        full_image = Image.open(full_imageBytes)

        gif_images.append(full_image)

    gif_path = "gacha.gif"
    save_gif(gif_images, gif_path, 1000)

    embed = discord.Embed()
    embed.color = Status.OK.value
    embed.title = title
    embed.description = description
    embed.set_footer(text=footer)
    embed.set_image(url="attachment://"+gif_path)
    #await ctx.send(embed=embed)

    await ctx.send(embed=embed, file=discord.File(gif_path))

async def last_pull_message(ctx, pulls):
    last_pull = pulls[-1]

    title = "Nom nom... Fuwa fuwa! ♡"
    last_pull_message = "The crepe was really good, " + mention_author(ctx) + "! Let me add this:"
    last_pull_file = "./lottery/"+last_pull[3]+" "+last_pull[4]+"/hex.png"
    print(last_pull_file)

    image_path = "pull11.png"

    footer = ""
    for pull in pulls:
        footer += "[" + pull[3] + "] " + pull[4] + " " + "🌟"*pull[1] + "\n"

    embed = discord.Embed()
    embed.color = Status.OK.value
    embed.title = title
    embed.description = last_pull_message
    #embed.add_field(name="x", value=last_pull_message, inline=False)
    embed.set_footer(text=footer)
    
    #await ctx.send(embed=embed, file=discord.File(last_pull_file))
    embed.set_image(url="attachment://"+image_path)
    
    await ctx.send(embed=embed, file=discord.File(last_pull_file, filename=image_path))

def save_gif(images, path, ms_per_frame):
    images[0].save(path, save_all=True, append_images=images[1:], optimize=False, duration=ms_per_frame)#, transparency=0) #loop=1

def concatenate_images(images, per_line=5):
    chunks = [images[x:x+per_line] for x in range(0, len(images), per_line)]

    images_lines = []
    for chunk in chunks:
        images_line = concatenate_images_horizontally(chunk)
        images_lines.append(images_line)

    full_image = concatenate_images_vertically(images_lines)
    return full_image

def concatenate_images_horizontally(image_paths):
    images = [Image.open(x) for x in image_paths]
    widths, heights = zip(*(i.size for i in images))
    
    total_width = sum(widths)
    max_height = max(heights)
    
    new_im = Image.new("RGBA", (total_width, max_height))
    x_offset = 0
    for im in images:
        new_im.paste(im, (x_offset,0))
        x_offset += im.size[0]

    new_im.load() # required for png.split()
    white_bg = Image.new("RGB", new_im.size, (255, 255, 255))
    white_bg.paste(new_im, mask=new_im.split()[3]) # 3 is the alpha channel

    # convert to bytes
    imgByteArr = io.BytesIO()
    white_bg.save(imgByteArr, format='PNG')
    imgByteArr.seek(0)

    return imgByteArr

def concatenate_images_vertically(image_paths):
    images = [Image.open(x) for x in image_paths]
    widths, heights = zip(*(i.size for i in images))
    
    total_width = max(widths)
    max_height = sum(heights)
    
    new_im = Image.new('RGBA', (total_width, max_height), "WHITE")
    
    y_offset = 0
    for im in images:
        new_im.paste(im, (0,y_offset))
        y_offset += im.size[1]

    # convert to bytes
    imgByteArr = io.BytesIO()
    new_im.save(imgByteArr, format='PNG')
    imgByteArr.seek(0)

    return imgByteArr