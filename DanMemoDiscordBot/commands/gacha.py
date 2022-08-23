from typing import List
import interactions
from interactions.ext.files import CommandContext
from PIL import Image
import io
from numpy.random import choice
from os.path import abspath, isdir
import datetime
from threading import Lock
from collections import Counter

from database.entities.User import User
from commands.utils import Status, mention_author, GachaRates, GachaRatesEleventh, GachaRatesOnlyFourStars, getDefaultEmoji, GachaModes
from commands.cache import Cache
from database.DBcontroller import DBConfig

MS_PER_FRAME = 500

star_emoji = '\u2b50'

lock = Lock()

async def run(dbConfig: DBConfig, ctx: CommandContext):
    acquired = lock.acquire(blocking=False)
    if not acquired:
        return await try_again_later(ctx)
    try:
        await engine(dbConfig,ctx)
    finally:
        if acquired:
            lock.release()

async def try_again_later(ctx: CommandContext):
    embed = interactions.Embed()
    embed.title = "Sorry, please try again later"
    embed.color = Status.KO.value
    await ctx.send(embeds=embed)

async def engine(dbConfig: DBConfig, ctx: CommandContext):
    author = str(ctx.author)
    authorUniqueId = str(ctx.author.id)

    user = User.get_user(dbConfig, author, authorUniqueId)

    if user.crepes is None:
        user.crepes = 0

    if user.crepes == 0:
        await no_gacha(ctx)
        return

    user.crepes -= 1

    pulls = get_pulls(10, GachaRates)
    pulls.extend(get_pulls(1, GachaRatesEleventh))
    
    user.add_units(pulls)
    user.update_stats()
    
    user.update_user(dbConfig,datetime.datetime.now(),"!$gacha")

    await pull_messages(ctx, user.crepes, pulls, user.gacha_mode)

async def no_gacha(ctx: CommandContext):
    title = "Hold on! Who goes there?"

    description = "What do you think you are doing, " + mention_author(ctx) + "?"
    description += " Come back when you have something for me!"

    footer = "There are 0 crepes left in your bento box!"

    embed = interactions.Embed()
    embed.color = Status.KO.value
    embed.title = title
    embed.description = description
    embed.set_footer(text=footer)
    embed.set_image(url="attachment://nope.png")
    await ctx.send(embeds=embed, files=interactions.File("./images/gacha/nope.png"))

def get_pulls(number: int, gacha_rates) -> list:
    pulls_category = random_pulls(number,gacha_rates)
    pulls = []
    for category in pulls_category:
        pulls.append(get_random_unit(category))
    return pulls

def random_pulls(number: int, gacha_rates) -> list:
    possibilities = [e.name for e in gacha_rates]
    probabilities = [e.value for e in gacha_rates]
    pulls = []
    for _ in range(number):
        pulls.append(choice(possibilities,p=probabilities))
    return pulls

def get_random_unit(gacha_category: GachaRates):
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

async def pull_messages(ctx: CommandContext, currency_number: int, pulls: list, gacha_mode: int):
    title = "Nom nom... Fuwa fuwa! ♡"

    description = "The crepe was really good, " + mention_author(ctx) + "! Please take this:" + "\n"
    for pull in pulls:
        description += star_emoji*pull.stars + " [" + pull.unit_label + "] " + pull.character_name + "\n"
    if currency_number == 1:
        footer = "There is " + str(currency_number) + " crepe left in your bento box!"
    else:
        footer = "There are " + str(currency_number) + " crepes left in your bento box!"

    if gacha_mode == GachaModes.IMG.value:
        img_path = "./images/gacha.png"
        create_image(img_path,pulls)
        await ctx.send(files=interactions.File(img_path))
    else:
        gif_path = "./images/gacha.gif"
        create_gif(gif_path,pulls)
        await ctx.send(files=interactions.File(gif_path))

    embed = interactions.Embed()
    embed.color = Status.OK.value
    embed.title = title
    embed.description = description
    embed.set_footer(text=footer)
    embed.set_image(url="attachment://yes.png")
    await ctx.send(embeds=embed, files=interactions.File("./images/gacha/yes.png"))


def create_image(img_path: str, pulls: list):
    pulls_images = []
    for pull in pulls:
        path = get_folder(pull)
        image = rarify(path, pull.stars)
        pulls_images.append(image)

    full_imageBytes = concatenate_images_eleven_pulls(pulls_images)
    full_image = Image.open(full_imageBytes)

    full_image.save(img_path, "PNG")


def create_gif(gif_path: str, pulls: list):
    pulls_images = []
    for pull in pulls:
        path = get_folder(pull)
        image = rarify(path, pull.stars)
        pulls_images.append(image)

    gif_images = []
    hidden_image = Image.open("./images/units/gac_dummy/hex.png")
    for i in range(len(pulls_images)+1):
        images_current_iteration = pulls_images[:i] + [hidden_image] * (len(pulls_images)-i)

        full_imageBytes = concatenate_images_eleven_pulls(images_current_iteration)
        full_image = Image.open(full_imageBytes)

        gif_images.append(full_image)

    save_gif(gif_images, gif_path)

def save_gif(images: List[Image.Image], path: str):
    print("Absolute path:",abspath(path))
    images[0].save(path, save_all=True, append_images=images[1:], optimize=False, duration=MS_PER_FRAME)#, transparency=0) #loop=1

def concatenate_images_eleven_pulls(images: List[Image.Image]) -> io.BytesIO:
    first_line = concatenate_images_horizontally(images[:6])
    second_line = concatenate_images_horizontally(images[6:])

    w1, h1 = first_line.size
    w2, h2 = second_line.size

    resized_second_line = Image.new(second_line.mode, (w1, h2), (255, 255, 255))
    resized_second_line.paste(second_line, ((w1-w2)//2, 0))

    images_lines = [convert_to_bytes(first_line),convert_to_bytes(resized_second_line)]

    full_image = concatenate_images_vertically(images_lines)
    return full_image

def concatenate_images(images, per_line=5):
    chunks = [images[x:x+per_line] for x in range(0, len(images), per_line)]

    images_lines = []
    for chunk in chunks:
        images_line = concatenate_images_horizontally(chunk,True)
        images_lines.append(images_line)

    full_image = concatenate_images_vertically(images_lines)
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

    return convert_to_bytes(new_im)

def convert_to_bytes(img):
    imgByteArr = io.BytesIO()
    img.save(imgByteArr, format='PNG')
    imgByteArr.seek(0)
    return imgByteArr

def rarify(path: str, rarity) -> Image.Image:
    background_path = "./images/hex/"+str(rarity)+".png"
    foreground_path = path + "hex.png"
    border_path = "./images/hex/border.png"

    background = Image.open(background_path).convert("RGBA")
    foreground = Image.open(foreground_path).convert("RGBA")
    border = Image.open(border_path).convert("RGBA")

    updated = Image.new("RGB", background.size, (255, 255, 255))
    updated.paste(background,(0,0), background)
    updated.paste(foreground,(0,0), foreground)
    updated.paste(border, (0,0), border)
    
    return updated

def get_folder(unit) -> str:
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
