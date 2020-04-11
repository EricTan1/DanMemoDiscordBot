import discord
from PIL import Image
import io
import asyncio
import time
from numpy.random import choice

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

    user.updateUser(dbConfig)

    await first_message(ctx, currency_number)
    await second_message(ctx, pulls[:-1])
    await third_message(ctx, pulls)

    '''pull = get_emoji("hex").toString(ctx)
    description += "\n" + pull * 5
    description += "\n" + pull * 5'''


    # embed = discord.Embed()
    # embed.color = Status.OK.value
    # embed.title = title
    # embed.description = description
    # embed.set_footer(text=footer)
    # await ctx.send(embed=embed)#, file=discord.File(icons, filename="temp.png"))

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

async def first_message(ctx, currency_number):
    emoji = get_emoji("crepe")
    emojiStr = emoji.toString(ctx)

    title = "Hold on! Who goes there?"
    description = "I guess I could let you pull if you share your " + emoji.name + " with me. But please, don't get addicted."
    description += "\n" + mention_author(ctx) + " has shared one " + emojiStr + " with Ais!"

    if currency_number > 1:
        footer = "There are " + str(currency_number) + " " + emoji.plural + " left in your bento box!"
    else:
        footer = "There is " + str(currency_number) + " " + emoji.name + " left in your bento box!"

    embed = discord.Embed()
    embed.color = Status.OK.value
    embed.title = title
    embed.description = description
    embed.set_footer(text=footer)
    await ctx.send(embed=embed)

async def second_message(ctx, pulls):
    hidden = get_emoji("hexdummy").toString(ctx)
    emoji_list = [get_emoji("hex").toString(ctx)]*10

    perLine = 5

    interval = 0.5
    for i in range(len(emoji_list)+1):
        temp_list = emoji_list[:i] + [hidden] * (len(emoji_list)-i)

        content = ""
        for j in range(len(temp_list)):
            if j != 0 and j % perLine == 0:
                content += "\n"
            content += temp_list[j]

        if i == 0:
            msg = await ctx.send(content=content)
            previous_time = getTime()
        else:
            wait(previous_time,interval)
            await msg.edit(content=content)
            previous_time = getTime()
    #wait(previous_time,interval)

async def third_message(ctx, pulls):
    print(pulls)
    last_pull = pulls[-1]
    print(last_pull)

    title = "Nom nom... Fuwa fuwa! ♡"
    last_pull_message = "The crepe was really good, " + mention_author(ctx) + "! Let me add this:"
    last_pull_file = "./lottery/"+last_pull[3]+" "+last_pull[4]+"/hex.png"
    print(last_pull_file)
    #await ctx.send(content=last_pull_message,file=discord.File(last_pull_file))

    discord_file_list = []
    await imageHorizontalConcat([last_pull_file],discord_file_list)
    icons = await imageVerticalConcat(discord_file_list)

    footer = ""
    for pull in pulls:
        footer += "[" + pull[3] + "] " + pull[4] + " " + "🌟"*pull[1] + "\n"

    embed = discord.Embed()
    embed.color = Status.OK.value
    embed.title = title
    embed.description = last_pull_message
    #embed.add_field(name="x", value=last_pull_message, inline=False)
    embed.set_footer(text=footer)
    
    #msg = await ctx.send(embed=embed, file=discord.File(last_pull_file))
    embed.set_image(url="attachment://temp.png")        
    
    msg = await ctx.send(embed=embed, file=discord.File(icons, filename="temp.png"))



async def get_pulls_image(dbConfig, client, ctx):
    hidden = get_emoji("hexdummy").toString(ctx)
    emoji_list = [get_emoji("hex").toString(ctx)]*10

    perLine = 5

    interval = 0.5
    for i in range(len(emoji_list)+1):
        temp_list = emoji_list[:i] + [hidden] * (len(emoji_list)-i)

        content = ""
        for j in range(len(temp_list)):
            if j != 0 and j % perLine == 0:
                content += "\n"
            content += temp_list[j]

        if i == 0:
            msg = await ctx.send(content=content)
            previous_time = getTime()
        else:
            wait(previous_time,interval)
            await msg.edit(content=content)
            previous_time = getTime()

    wait(previous_time,interval)
    title = "Nom nom... Fuwa fuwa! ♡"
    last_pull_message = "The crepe was really good, " + mention_author(ctx) + "! Let me add this:"
    last_pull_file = "./lottery/Regiment Princess Ais Wallenstein/hex.png"
    #await ctx.send(content=last_pull_message,file=discord.File(last_pull_file))

    discord_file_list = []
    await imageHorizontalConcat(client,[last_pull_file],discord_file_list)
    icons = await imageVerticalConcat(client,discord_file_list)

    footer = "[Regiment Princess] Ais Wallenstein\n"*11

    embed = discord.Embed()
    embed.color = 3066993
    embed.title = title
    embed.description = last_pull_message
    #embed.add_field(name="x", value=last_pull_message, inline=False)
    embed.set_footer(text=footer)
    
    #msg = await ctx.send(embed=embed, file=discord.File(last_pull_file))
    embed.set_image(url="attachment://temp.png")        
    
    msg = await ctx.send(embed=embed, file=discord.File(icons, filename="temp.png"))



def getTime():
    return int(time.time())

#wait interval seconds
def wait(previous_time,interval):
    time_left = previous_time + interval - getTime()
    if time_left > 0:
        time.sleep(time_left)
    return 



'''
async def get_pulls_image(dbConfig, client, ctx, title, description, footer):
    hidden = "./lottery/gac_dummy/hex.png"
    file_list = ["./lottery/Regiment Princess Ais Wallenstein/hex.png"]*11

    perLine = 4

    msg = None
    for i in range(len(file_list)+1):
        temp_file_list = file_list[:i] + [hidden] * (len(file_list)-i)
        discord_file_list = []
        chunks = [temp_file_list[x:x+perLine] for x in range(0, len(temp_file_list), perLine)]
        for chunk in chunks:
            await imageHorizontalConcat(client,chunk,discord_file_list)
        icons = await imageVerticalConcat(client,discord_file_list)
        if msg is None:
            msg,embed = await skillSearchRotatingPage(client,ctx,title,description,footer,icons)
        else:
            await msg.edit(file=discord.File(icons, filename="temp.png"))
'''
async def imageHorizontalConcat(file_list, discord_file_list):
    images = [Image.open(x) for x in file_list]
    widths, heights = zip(*(i.size for i in images))
    
    total_width = sum(widths)
    max_height = max(heights)
    
    new_im = Image.new('RGBA', (total_width, max_height))
    
    x_offset = 0
    for im in images:
        new_im.paste(im, (x_offset,0))
        x_offset += im.size[0]
    # convert to bytes
    imgByteArr = io.BytesIO()
    new_im.save(imgByteArr, format='PNG')
    imgByteArr.seek(0)
    discord_file_list.append(imgByteArr)

async def imageVerticalConcat(file_list):
    images = [Image.open(x) for x in file_list]
    widths, heights = zip(*(i.size for i in images))
    
    total_width = max(widths)
    max_height = sum(heights)
    
    new_im = Image.new('RGBA', (total_width, max_height))
    
    y_offset = 0
    for im in images:
        new_im.paste(im, (0,y_offset))
        y_offset += im.size[1]
    # convert to bytes
    imgByteArr = io.BytesIO()
    new_im.save(imgByteArr, format='PNG')
    imgByteArr.seek(0)
    return imgByteArr
'''
async def skillSearchRotatingPage(client, ctx, title, description, footer, icons):
    temp_image_url = "attachment://"

    embed = discord.Embed()
    embed.set_image(url=temp_image_url+"temp.png")        
    
    embed.color = 3066993
    embed.title = title
    embed.description = description
    embed.set_footer(text=footer)
    
    msg = await ctx.send(embed=embed, file=discord.File(icons, filename="temp.png"))
    return msg,embed'''