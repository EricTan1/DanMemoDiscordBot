import discord
from PIL import Image
import io
import asyncio
import time
from numpy.random import choice
from os.path import isfile, abspath, isdir
import datetime
from threading import Lock
from collections import Counter

from database.entities.User import User
from commands.utils import Status, get_emoji, mention_author, GachaRates, GachaRatesEleventh, GachaRatesOnlyFourStars, getDefaultEmoji, GachaModes
from commands.cache import Cache
from database.DBcontroller import DBcontroller

lock = Lock()

async def run(dbConfig, client, ctx, *args):
    #acquired = lock.acquire(blocking=True, timeout=60)
    acquired = lock.acquire(blocking=False)
    if acquired:
        await ctx.message.add_reaction(getDefaultEmoji("white_check_mark"))
    else:
        await ctx.message.add_reaction(getDefaultEmoji("x"))
        return
    try:
        await engine(dbConfig,client,ctx,*args)
    finally:
        if acquired:
            lock.release()

async def engine(dbConfig, client, ctx, *args):
    author = str(ctx.message.author)
    authorUniqueId = str(ctx.message.author.id)
    content = ctx.message.content
    
    print("\nReceived message from '"+author+"("+authorUniqueId+")' with content '"+content+"'")

    user = User.get_user(dbConfig, author, authorUniqueId)

    currency_number = user.crepes
    if currency_number is None:
        currency_number = 0

    if currency_number == 0:
        await no_gacha(user, currency_number, ctx)
        return

    currency_number -= 1
    user.crepes = currency_number

    pulls = get_pulls(10, GachaRates)
    pulls.extend(get_pulls(1, GachaRatesEleventh))
    
    user.add_units(pulls)
    user.update_stats()
    
    user.update_user(dbConfig,datetime.datetime.now(),content)

    await pull_messages(ctx, currency_number, pulls, user.gacha_mode)

async def no_gacha(user, currency_number, ctx):
    emoji = get_emoji("crepe")
    emojiStr = emoji.toString(ctx)

    title = "Hold on! Who goes there?"

    description = "What do you think you are doing, " + mention_author(ctx) + "?"
    description += " Come back when you have something for me!"

    if currency_number == 1:
        footer = "There is " + str(currency_number) + " " + emoji.name + " left in your bento box!"
    else:
        footer = "There are " + str(currency_number) + " " + emoji.plural + " left in your bento box!"

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

def get_random_unit(gacha_category):
    cache = Cache()
    if gacha_category == GachaRates.ADVENTURER_2_STARS.name:
        stars = 2
        units = cache.get_all_adventurers()
    elif gacha_category == GachaRates.ADVENTURER_3_STARS.name:
        stars = 3
        units = cache.get_all_adventurers()
    elif gacha_category == GachaRates.ADVENTURER_4_STARS.name:
        stars = 4
        units = cache.get_all_adventurers()
    elif gacha_category == GachaRates.ASSIST_2_STARS.name:
        stars = 2
        units = cache.get_all_assists()
    elif gacha_category == GachaRates.ASSIST_3_STARS.name:
        stars = 3
        units = cache.get_all_assists()
    elif gacha_category == GachaRates.ASSIST_4_STARS.name:
        stars = 4
        units = cache.get_all_assists()
    else:
        raise Exception("Unknown gacha category:",gacha_category)

    units = [unit for unit in units if unit.stars == stars]
    unit = choice(units)
    return unit

def get_pulls(number, gacha_rates):
    pulls_category = random_pulls(number,gacha_rates)
    pulls = []
    for category in pulls_category:
        pulls.append(get_random_unit(category))
    return pulls

async def pull_messages(ctx, currency_number, pulls, gacha_mode):
    emoji = get_emoji("crepe")
    emojiStr = emoji.toString(ctx)

    #title = "Hold on! Who goes there?"
    #description = "I guess I could let you pull if you share your " + emoji.name + " with me. But please, don't get addicted."
    #description += "\n" + mention_author(ctx) + " has shared one " + emojiStr + " with Ais!"

    title = "Nom nom... Fuwa fuwa! ♡"

    description = "The crepe was really good, " + mention_author(ctx) + "! Please take this:" + "\n"
    for pull in pulls:
        description += "🌟"*pull.stars + " [" + pull.unit_label + "] " + pull.character_name + "\n"

    if currency_number == 1:
        footer = "There is " + str(currency_number) + " " + emoji.name + " left in your bento box!"
    else:
        footer = "There are " + str(currency_number) + " " + emoji.plural + " left in your bento box!"

    if gacha_mode == GachaModes.IMG.value:
        img_path = "./images/gacha.png"
        create_image(img_path,pulls)
        await ctx.send(file=discord.File(img_path))
    else:
        #per_line = 5
        gif_path = "./images/gacha.gif"
        ms_per_frame = 500
        create_gif(gif_path,pulls,ms_per_frame)
        await ctx.send(file=discord.File(gif_path))

    embed = discord.Embed()
    embed.color = Status.OK.value
    embed.title = title
    embed.description = description
    embed.set_footer(text=footer)
    embed.set_image(url="attachment://yes.png")
    await ctx.send(embed=embed, file=discord.File("./images/gacha/yes.png"))


'''async def last_pull_message(ctx, pulls):
    last_pull = pulls[-1]

    title = "Nom nom... Fuwa fuwa! ♡"
    last_pull_message = "The crepe was really good, " + mention_author(ctx) + "! Let me add this:"

    last_pull_path = get_folder(last_pull)
    last_pull_image = rarify(last_pull_path,4)

    image_path = "pull11.png"
    imgByteArr = io.BytesIO()
    last_pull_image.save(imgByteArr, format='PNG')
    imgByteArr.seek(0)

    footer = ""
    for pull in pulls:
        footer += "[" + pull.unit_label + "] " + pull.character_name + " " + "🌟"*pull.stars + "\n"

    embed = discord.Embed()
    embed.color = Status.OK.value
    embed.title = title
    embed.description = last_pull_message
    #embed.add_field(name="x", value=last_pull_message, inline=False)
    embed.set_footer(text=footer)
    #await ctx.send(embed=embed, file=discord.File(last_pull_file))
    embed.set_image(url="attachment://"+image_path)
    await ctx.send(embed=embed, file=discord.File(imgByteArr, filename=image_path))
'''

def create_image(img_path, pulls):
    pulls_images = []
    for pull in pulls:
        path = get_folder(pull)
        image = rarify(path,pull.stars)
        pulls_images.append(image)

    full_imageBytes = concatenate_images_eleven_pulls(pulls_images)
    full_image = Image.open(full_imageBytes)

    full_image.save(img_path, "PNG")


def create_gif(gif_path, pulls, ms_per_frame):
    pulls_images = []
    for pull in pulls:
        path = get_folder(pull)
        image = rarify(path,pull.stars)
        pulls_images.append(image)

    gif_images = []
    hidden_image = Image.open("./images/units/gac_dummy/hex.png")
    for i in range(len(pulls_images)+1):
        images_current_iteration = pulls_images[:i] + [hidden_image] * (len(pulls_images)-i)

        full_imageBytes = concatenate_images_eleven_pulls(images_current_iteration)
        full_image = Image.open(full_imageBytes)

        gif_images.append(full_image)

    save_gif(gif_images, gif_path, ms_per_frame)

def save_gif(images, path, ms_per_frame):
    print("Absolute path:",abspath(path))
    images[0].save(path, save_all=True, append_images=images[1:], optimize=False, duration=ms_per_frame)#, transparency=0) #loop=1

def concatenate_images_eleven_pulls(images):
    first_line = concatenate_images_horizontally(images[:6])
    second_line = concatenate_images_horizontally(images[6:])

    w1, h1 = first_line.size
    w2, h2 = second_line.size

    resized_second_line = Image.new(second_line.mode, (w1, h2), (255, 255, 255))
    resized_second_line.paste(second_line, ((w1-w2)//2, 0))

    images_lines = [convert_to_bytes(first_line),convert_to_bytes(resized_second_line)]

    full_image = concatenate_images_vertically(images_lines,True)
    return full_image

def concatenate_images(images, per_line=5):
    chunks = [images[x:x+per_line] for x in range(0, len(images), per_line)]

    images_lines = []
    for chunk in chunks:
        images_line = concatenate_images_horizontally(chunk,True)
        images_lines.append(images_line)

    full_image = concatenate_images_vertically(images_lines,True)
    return full_image

def concatenate_images_horizontally(images,to_bytes=False):
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

    if to_bytes:
        return convert_to_bytes(white_bg)
    else:
        return white_bg

def concatenate_images_vertically(image_paths,to_bytes=False):
    images = [Image.open(x) for x in image_paths]
    widths, heights = zip(*(i.size for i in images))
    
    total_width = max(widths)
    max_height = sum(heights)
    
    new_im = Image.new('RGBA', (total_width, max_height), "WHITE")
    
    y_offset = 0
    for im in images:
        new_im.paste(im, (0,y_offset))
        y_offset += im.size[1]

    if to_bytes:
        return convert_to_bytes(new_im)
    else:
        return new_im

def convert_to_bytes(img):
    imgByteArr = io.BytesIO()
    img.save(imgByteArr, format='PNG')
    imgByteArr.seek(0)
    return imgByteArr

def rarify(path, rarity):
    background_path = "./images/hex/"+str(rarity)+".png"
    foreground_path = path + "hex.png"
    border_path = "./images/hex/border.png"

    updated_path = path + "pull.png"

    background = Image.open(background_path).convert("RGBA")
    foreground = Image.open(foreground_path).convert("RGBA")
    border = Image.open(border_path).convert("RGBA")

    updated = Image.new("RGB", background.size, (255, 255, 255))
    updated.paste(background,(0,0), background)
    updated.paste(foreground,(0,0), foreground)
    updated.paste(border, (0,0), border)
    
    return updated

def get_folder(unit):
    path = "./images/units/"+unit.character_name+" ["+unit.unit_label+"]/"

    if not isdir(path):
        print("Could not find folder:",path)
        path = "./images/units/gac_dummy/"

    return path

def test_gacha_rates():
    number = 100_000
    print("Simulating "+str(number)+" pulls")
    pulls = random_pulls(number,GachaRatesEleventh)
    print("Aggregating results")
    counter = Counter(pulls)
    print(counter)

'''
Result:
Counter({
'ADVENTURER_2_STARS': 54125, 
'ASSIST_2_STARS': 28052, 
'ADVENTURER_3_STARS': 9909, 
'ASSIST_3_STARS': 4936, 
'ADVENTURER_4_STARS': 1961, 
'ASSIST_4_STARS': 1017})

Expected:
ADVENTURER_2_STARS = 0.54
ASSIST_2_STARS = 0.28
ADVENTURER_3_STARS = 0.10
ASSIST_3_STARS = 0.05
ADVENTURER_4_STARS = 0.02
ASSIST_4_STARS = 0.01
'''