import discord
from PIL import Image
import io
import asyncio
from enum import Enum

class Status(Enum):
    OK = 3066993
    KO = 16203840

class GachaRates(Enum):
    ADVENTURER_3_STARS = 0.64
    ASSIST_3_STARS = 0.33
    ADVENTURER_4_STARS = 0.02
    ASSIST_4_STARS = 0.01

class GachaRatesOnlyFourStars(Enum):
    ADVENTURER_4_STARS = 0.67
    ASSIST_4_STARS = 0.33

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
            CustomEmoji("crepe","crepe","crepes",698247637899411521),
            CustomEmoji("hexdummy","hexdummy","hexdummy",698471235927146526),
            CustomEmoji("hex","hex","hex",698357886492999753)}

def get_emoji(id_inner):
    for emoji in emojis:
        if emoji.id_inner == id_inner:
            return emoji
    raise Exception("Unknown emoji id:",id_inner)

def mention_author(ctx):
    return ctx.message.author.mention

def get_author(ctx):
    return str(ctx.message.author)

async def imageHorizontalConcat(client, file_list, discord_file_list):
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

async def imageVerticalConcat(client, file_list):
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

async def skillSearchRotatingPage(client, ctx, search, page_list, total_results, icons):
    temp_image_url = "attachment://"
    # set up
    current_page = 0
    temp_embed = discord.Embed()
    temp_embed.set_image(url=temp_image_url+"temp.png")        
    
    temp_embed.color = 3066993
    temp_embed.title = "{} results for {}".format(str(total_results),search)
    if(len(page_list) == 0):
        page_list.append([["No relevant skills to display","End of List"]])    
    temp_embed.set_footer(text="Page {} of {}".format(current_page+1,len(page_list)))
    def clearSetField(temp_embed:discord.Embed, field_list):
        temp_embed.clear_fields()
        print(field_list)
        for skills in field_list:
            print(skills)
            temp_embed.add_field(value=skills[1], name=skills[0],inline=False)
        return temp_embed
    
    temp_embed = clearSetField(temp_embed, field_list=page_list[current_page])
    msg = await ctx.send(embed=temp_embed, file=discord.File(icons, filename="temp.png"))
    emoji1 = '\u2b05'
    emoji2 = '\u27a1'
    await msg.add_reaction(emoji1)
    await msg.add_reaction(emoji2)
    emojis = [emoji1, emoji2]
    def check(reaction, user):
        return (str(reaction.emoji) == emoji2 or str(reaction.emoji) == emoji1) and user !=client.user
    while True:
        try:
            reaction, user = await client.wait_for('reaction_add', timeout=60.0, check=check)
        except asyncio.TimeoutError:
            temp_embed.color=16203840
            await msg.edit(embed=temp_embed)
            break
        else:
            # left
            if str(reaction.emoji) == emoji1:
                if(current_page > 0):
                    current_page = current_page -1
                else:
                    current_page = len(page_list)-1
            # right
            if str(reaction.emoji) == emoji2:
                if( current_page+1 < len(page_list)):
                    current_page = current_page +1
                else:
                    current_page = 0
            temp_embed.set_footer(text="Page {} of {}".format(current_page+1,len(page_list)))            
            temp_embed = clearSetField(temp_embed, field_list=page_list[current_page])
            await msg.edit(embed=temp_embed)