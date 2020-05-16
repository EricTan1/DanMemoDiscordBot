import discord
from PIL import Image
import io
import asyncio
import time
from numpy.random import choice
from os.path import isfile
import datetime

from database.entities.User import User
from commands.utils import Status, get_emoji, mention_author, GachaRates, GachaRatesOnlyFourStars
from commands.cache import Cache
from database.DBcontroller import DBcontroller

async def run(dbConfig, client, ctx, *args):
    author = str(ctx.message.author)
    content = ctx.message.content

    print("\nReceived message from '"+author+"' with content '"+content+"'")

    user = User.get_user(dbConfig, author)

    currency_number = user.crepes
    if currency_number is None:
        currency_number = 0

    if currency_number == 0:
        await no_gacha(user, currency_number, ctx)
        return

    currency_number -= 1
    user.crepes = currency_number

    pulls = get_pulls(10, GachaRates)
    pulls.extend(get_pulls(1, GachaRatesOnlyFourStars))
    
    user.add_units(pulls)
    
    user.update_user(dbConfig,datetime.datetime.now(),content)

    await ten_pull_message(ctx, currency_number, pulls[:-1])
    await last_pull_message(ctx, pulls)


async def no_gacha(user, currency_number, ctx):
    emoji = get_emoji("crepe")
    emojiStr = emoji.toString(ctx)

    title = "Hold on! Who goes there?"

    description = "What do you think you are doing, " + mention_author(ctx) + "?"
    description += " Come back when you have something for me!"

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

    per_line = 5
    gif_path = "gacha.gif"
    ms_per_frame = 1000
    create_gif(gif_path,pulls,per_line,ms_per_frame)

    embed = discord.Embed()
    embed.color = Status.OK.value
    embed.title = title
    embed.description = description
    embed.set_footer(text=footer)
    embed.set_image(url="attachment://"+gif_path)

    await ctx.send(embed=embed, file=discord.File(gif_path))

async def last_pull_message(ctx, pulls):
    last_pull = pulls[-1]

    title = "Nom nom... Fuwa fuwa! ♡"
    last_pull_message = "The crepe was really good, " + mention_author(ctx) + "! Let me add this:"

    last_pull_file = "./lottery/"+last_pull.unit_label+" "+last_pull.character_name+"/hex.png"

    if not isfile(last_pull_file):
        print("Could not find file at:",last_pull_file)
        last_pull_file = "./lottery/gac_dummy/hex.png"

    last_pull_image = rarify("./lottery/"+last_pull.unit_label+" "+last_pull.character_name+"/",4)

    print(last_pull_file)

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

def create_gif(gif_path, pulls, per_line, ms_per_frame):
    suffix = "hex.png"

    hidden = "./lottery/gac_dummy/"
    hidden_image = Image.open(hidden+suffix)

    pulls_images = []

    for pull in pulls:
        path = "./lottery/"+pull.unit_label+" "+pull.character_name+"/"#+suffix
        if isfile(path+suffix):
            image = rarify(path,pull.stars)
        else:
            print("Could not find file at:",path+suffix)
            image = hidden_image

        pulls_images.append(image)

    gif_images = []

    for i in range(len(pulls_images)+1):
        images_current_iteration = pulls_images[:i] + [hidden_image] * (len(pulls_images)-i)

        full_imageBytes = concatenate_images(images_current_iteration, per_line)
        full_image = Image.open(full_imageBytes)

        gif_images.append(full_image)

    save_gif(gif_images, gif_path, ms_per_frame)

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

def concatenate_images_horizontally(images):
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

def create_rarity_hex(path, rarity):
    background_path = "./images/hex/"+str(rarity)+".png"
    foreground_path = path + "hex.png"
    border_path = "./images/hex/border.png"

    updated_path = path + "pull.png"

    background = Image.open(background_path).convert("RGBA")
    foreground = Image.open(foreground_path).convert("RGBA")
    border = Image.open(border_path).convert("RGBA")

    updated = Image.new("RGB", background.size, (255, 255, 255))
    updated.paste(background, (0,0), background)
    updated.paste(foreground, (0,0), foreground)
    updated.paste(border, (0,0), border)
    '''
    updated.paste(border,(0,0), mask = border.split()[3])
    updated.paste(background,(0,0), mask = background.split()[3])
    updated.paste(foreground,(0,0), mask = foreground.split()[3])
    '''
    updated.save(updated_path)

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