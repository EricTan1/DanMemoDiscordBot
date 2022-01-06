import discord
import asyncio
import aiohttp
from PIL import Image, ImageDraw
from database.DBcontroller import DBcontroller
from math import ceil

# sizes in pixels
rowHeight = 141
hexLength = 100
hexScaledLength = 75
framePaddingX = 20
framePaddingY = 5
betweenPaddingX = -5
betweenPaddingY = -20
numRows = 12
lineWidth = 5


async def run(dbConfig, ctx):
    db = DBcontroller(dbConfig)
    killers = ["aqua killer", "dragon killer", "giant killer", "material killer", "ox slayer", "spirit killer", "beast killer", "fantasma killer", "insect killer", "ogre killer", "plant killer", "worm killer"]
    killer_images = []
    for enemy_type in killers:
        skills = db.skillSearch(enemy_type,{})
        file_list = []
        for skill in skills:
            skillinfo=db.assembleAdventurerDevelopment(skill[2:])
            adventurerid = skillinfo[4]
            names = db.assembleAdventurerCharacterName(adventurerid)
            try:
                file_name = "./images/units/"+"{} [{}]".format(names[1],names[0]).strip()+"/hex.png"
                f = open(file_name,"r")
                f.close()
                file_list.append(file_name)
            except:
                # Do something smarter for missing images?
                print("Image for '{} [{}]' missing".format(names[1],names[0]) )
                #file_list.append("./images/units/gac_dummy/hex.png")
        killer_images.append(file_list)
    
    mostKillers = get_most_killers(killer_images)

    base_im = Image.open("./infographic/killer_base.png", "r")
    width, height = base_im.size

    one_side_padding = (mostKillers+1) * (hexScaledLength + betweenPaddingX)//2 + 2* framePaddingX
    new_width = width + 2 * one_side_padding

    edited_im = Image.new(base_im.mode, (new_width, height), (35, 35, 35))
    edited_im.paste(base_im, ((new_width - width) // 2, 0))

    drawer = ImageDraw.Draw(edited_im)
    for i in range(1, numRows // 2):
        yPos = i*rowHeight - lineWidth//2
        drawer.line((0, yPos, new_width, yPos), fill = (10, 10, 10), width = lineWidth)

    rowNum = 0
    for row in killer_images:
        unitNum = 0
        for unit in row:
            with Image.open(unit, "r") as unit_im:
                unit_im = unit_im.convert("RGBA")
                unit_im = unit_im.resize((hexScaledLength, hexScaledLength))
                pos = get_hex_pos(rowNum, unitNum, new_width)
                edited_im.paste(unit_im, pos, unit_im)
            unitNum += 1
        rowNum += 1

    edited_im.save("./infographic/killer.png", quality = 95)

def get_most_killers(killer_lists):
    mostKillers = 0
    for killer_type in killer_lists:
        if len(killer_type) > mostKillers:
            mostKillers = len(killer_type)
    return mostKillers

def get_hex_pos(rowNum, unitNum, fullWidth):
    in_row_widths = (unitNum // 2) * hexScaledLength
    total_between_paddings = ((unitNum // 2) - 1 ) * betweenPaddingX
    in_row_x = in_row_widths + total_between_paddings + framePaddingX
    in_row_y = framePaddingY
    if unitNum % 2 == 1:
        in_row_x += hexScaledLength // 2 
        in_row_y += hexScaledLength + betweenPaddingY


    adjustedRowNum = (rowNum % (numRows // 2))
    row_top = adjustedRowNum * rowHeight

    y = row_top + in_row_y

    x = in_row_x if rowNum < numRows // 2 else fullWidth - in_row_x - hexScaledLength

    return (x,y)