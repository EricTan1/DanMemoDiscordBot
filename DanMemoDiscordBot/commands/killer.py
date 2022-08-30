import interactions
from interactions.ext.files import CommandContext
from PIL import Image, ImageDraw
from typing import Dict, List, Tuple


from database.DBcontroller import DBConfig, DBcontroller
from commands.utils import Status

# Spacings and sizes in pixels
rowHeight = 141
hexLength = 100
hexScaledLength = 75
framePaddingX = 20
framePaddingY = 5
betweenPaddingX = -5
betweenPaddingY = -20
numRows = 12
numRowsPerColumn = numRows // 2
lineWidth = 5

# List of killers
killers = [
    "aqua killer", "dragon killer", "giant killer", "material killer",
    "ox slayer", "spirit killer", "beast killer", "fantasma killer",
    "insect killer", "ogre killer", "plant killer", "worm killer"
]

async def run(ctx: CommandContext, dbConfig: DBConfig, sub_command: str):
    await ctx.defer() # generating the image takes longer than the default 3s Discord timeout
    generateInfographic(dbConfig)

    if sub_command != "all":
        killerName = sub_command.lower()
        fullKillerName = ""
        if killerName == "ox":
            fullKillerName = f"{killerName} slayer"
        else:
            fullKillerName = f"{killerName} killer"
        if fullKillerName in killers:
            graphic = Image.open("./infographic/killer.png", "r")
            width, height = graphic.size
            killerNumber = killers.index(fullKillerName)
            columnNumber = killerNumber // numRowsPerColumn
            rowNumber = killerNumber % numRowsPerColumn

            leftBorder = width // 2 * columnNumber
            rightBorder = leftBorder + width // 2
            topBorder = height // numRowsPerColumn * rowNumber
            bottomBorder = topBorder + height // numRowsPerColumn

            croppedGraphic = graphic.crop((leftBorder, topBorder, rightBorder, bottomBorder))
            croppedGraphic.save("./infographic/killer.png", quality = 95)

    embed = interactions.Embed()
    embed.set_image(url="attachment://killer.png")
    embed.color = Status.OK.value
    await ctx.send(embeds=embed, files=interactions.File("./infographic/killer.png"))

def generateInfographic(dbConfig: DBConfig):
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
def getKillerDict(db: DBcontroller) -> Dict[str, List[str]]:
    killerImages = dict()
    for enemyType in killers:
        skills = db.skillSearch(enemyType)
        fileList = []
        for skill in skills:
            skillinfo=db.assembleAdventurerDevelopment(skill[2:])
            adventurerid = skillinfo[4]
            names = db.assembleAdventurerCharacterName(adventurerid)
            try:
                fileName = f"./images/units/{names[1]} [{names[0]}]/hex.png"
                file = open(fileName,"r")
                file.close()
                fileList.append(fileName)
            except:
                # Do something smarter for missing images?
                print(f"Image for '{names[1]} [{names[0]}]' missing")

        killerImages[enemyType] = fileList

    return killerImages

# Returns the number of units that have the killer type that has the most units
def getMostKillers(killerDict: Dict[str, List[str]]) -> int:
    mostKillers = 0
    for key in killerDict:
        if len(killerDict[key]) > mostKillers:
            mostKillers = len(killerDict[key])
    return mostKillers

# Computes the position for insertion of an adventurer image
def getHexPos(rowNum: int, unitNum: int, fullWidth: int) -> Tuple[int, int]:
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
