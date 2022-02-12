import discord
from PIL import Image, ImageDraw
from database.DBcontroller import DBcontroller

# Spacings and sizes in pixels
rowHeight = 141
hexLength = 100
hexScaledLength = 75
framePaddingX = 20
framePaddingY = 5
betweenPaddingX = -5
betweenPaddingY = -20
numRows = 12
lineWidth = 5

# List of killers
killers = [ "aqua killer", "dragon killer", "giant killer", "material killer",
            "ox slayer", "spirit killer", "beast killer", "fantasma killer",
            "insect killer", "ogre killer", "plant killer", "worm killer"]

async def run(ctx, dbConfig):
    generateInfographic(dbConfig)

    temp_embed = discord.Embed()
    temp_embed.color = 3066993
    temp_embed.set_image(url="attachment://slayer.png")
    await ctx.send(embed=temp_embed, file=discord.File("./infographic/killer.png",filename="slayer.png"))


def generateInfographic(dbConfig):
    db = DBcontroller(dbConfig)
    killerDict = getKillerDict(db)

    mostKillers = getMostKillers(killerDict)

    baseIm = Image.open("./infographic/killer_base.png", "r")
    width, height = baseIm.size

    oneSidePadding = (mostKillers+1) * (hexScaledLength + betweenPaddingX)//2 + 2* framePaddingX
    newWidth = width + 2 * oneSidePadding

    editedIm = Image.new(baseIm.mode, (newWidth, height), (35, 35, 35))
    editedIm.paste(baseIm, ((newWidth - width) // 2, 0))

    drawer = ImageDraw.Draw(editedIm)
    for i in range(1, numRows // 2):
        yPos = i*rowHeight - lineWidth//2
        drawer.line((0, yPos, newWidth, yPos), fill = (10, 10, 10), width = lineWidth)

    rowNum = 0
    for key in killerDict:
        unitNum = 0
        for unit in killerDict[key]:
            with Image.open(unit, "r") as unitIm:
                unitIm = unitIm.convert("RGBA")
                unitIm = unitIm.resize((hexScaledLength, hexScaledLength))
                pos = getHexPos(rowNum, unitNum, newWidth)
                editedIm.paste(unitIm, pos, unitIm)
            unitNum += 1
        rowNum += 1

    editedIm.save("./infographic/killer.png", quality = 95)

# Returns a dict of the form { Killertype: [image filepaths] }
def getKillerDict(db):
    killerImages = dict()
    for enemyType in killers:
        skills = db.skillSearch(enemyType,{})
        fileList = []
        for skill in skills:
            skillinfo=db.assembleAdventurerDevelopment(skill[2:])
            adventurerid = skillinfo[4]
            names = db.assembleAdventurerCharacterName(adventurerid)
            try:
                fileName = "./images/units/"+"{} [{}]".format(names[1],names[0]).strip()+"/hex.png"
                file = open(fileName,"r")
                file.close()
                fileList.append(fileName)
            except:
                # Do something smarter for missing images?
                print("Image for '{} [{}]' missing".format(names[1],names[0]) )

        killerImages[enemyType] = fileList

    return killerImages

# Returns the number of units that have the killer type that has the most units
def getMostKillers(killerDict):
    mostKillers = 0
    for key in killerDict:
        if len(killerDict[key]) > mostKillers:
            mostKillers = len(killerDict[key])
    return mostKillers

# Computes the position for insertion of an adventurer image
def getHexPos(rowNum, unitNum, fullWidth):
    inRowWidths = (unitNum // 2) * hexScaledLength
    totalBetweenPaddings = ((unitNum // 2) - 1 ) * betweenPaddingX
    inRowX = inRowWidths + totalBetweenPaddings + framePaddingX
    inRowY = framePaddingY
    if unitNum % 2 == 1:
        inRowX += hexScaledLength // 2
        inRowY += hexScaledLength + betweenPaddingY

    adjustedRowNum = (rowNum % (numRows // 2))
    rowTop = adjustedRowNum * rowHeight

    y = rowTop + inRowY

    x = inRowX if rowNum < numRows // 2 else fullWidth - inRowX - hexScaledLength

    return (x,y)
