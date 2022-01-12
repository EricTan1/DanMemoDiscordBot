from PIL import Image, ImageDraw, ImageFont
from database.DBcontroller import DBcontroller

elements = ["Light", "Dark", "Fire", "Water", "Thunder", "Earth", "Wind"]
elementColors = [(255,255,255), (208,148,208), (255,144,144), (128,192,255), (232,232,128), (204,160,120), (128,192,128)]
numElements = len(elements)
effectTypes = [("Foes", "Resist"), ("Allies", "Attack")]

colorDimming = (80,80,80)

elementFiles = {"Light": "element_06.png", "Dark": "element_07.png", "Fire": "element_01.png", "Water": "element_04.png",
                "Thunder": "element_05.png", "Earth": "element_02.png", "Wind": "element_03.png"}

backgroundColor = (40,40,40)
textColor = (255,255,255)
strokeColor = (0,0,0)
strokeWidth = 4

fontType = "NotoSans-Regular.ttf"
fontSize = 25

framePaddingX = 130
outerFramePaddingX = 10
textPaddingX = 50
betweenPaddingX = 0
betweenPaddingY = -20
innerFramePaddingY = 5
betweenRowPadding = 10
hexScaledLength = 100
elemScaledLength = 84
innerRowHeight = innerFramePaddingY * 2 + hexScaledLength
lineWidth = 5
textLineHeightFactor = 0.21/2   # /2 because the modifier text has 2 lines 

async def run(dbConfig):
    db = DBcontroller(dbConfig)
    assistDict = getElementAssistDict(db)

    #for el in elements:
    #    print(el)
    #    for ef in effectTypes:
    #        print("\t"+ ef[1])
    #        for mod in assistDict[el][ef[1]]:
    #            print("\t\t" + str(mod) +": " + str(assistDict[el][ef[1]][mod]))

    wf = getWidthFactor(assistDict)
    heightFactors = getRowHeights(assistDict)

    imWidth = 2 * ((hexScaledLength + betweenPaddingX) * wf + framePaddingX + outerFramePaddingX)
    imHeight = (numElements) * betweenRowPadding + innerRowHeight * sum(heightFactors)
    im = Image.new("RGB", (imWidth, imHeight), backgroundColor)
    drawer = ImageDraw.Draw(im)

    rowOffset = 0
    for elNum in range(numElements):
        rowHeight = innerRowHeight * heightFactors[elNum] + betweenRowPadding
        #print("Row of height " + str(rowHeight) + " at offset " + str(rowOffset))
        dimmedColor = tuple([c1 - c2 for c1, c2 in  zip(elementColors[elNum], colorDimming)])
        rowIm = Image.new("RGB", (imWidth, rowHeight), dimmedColor)
        im.paste(rowIm, (0, rowOffset))
        rowOffset += rowHeight

    rowOffset = 0
    centerX = imWidth//2
    for rowNum in range(numElements):
        el = elements[rowNum]
        pasteElement(im, rowNum, rowOffset, centerX)
        # 2 for sides left and right
        for side in [0, 1]:
            efType = effectTypes[side][1]
            modifiers = list(assistDict[el][efType].keys())
            print(el + efType + " has keys: " + str(modifiers))
            modifiers = sorted(modifiers, key = abs)
            for innerRowNum in range(len(modifiers)):
                mod = modifiers[innerRowNum]
                drawModifier(drawer, mod, side, centerX, rowOffset, innerRowNum)
                unitNum = 0
                for unit in assistDict[el][efType][mod]:
                    with Image.open(unit, "r") as unitIm:
                        unitIm = unitIm.convert("RGBA")
                        unitIm = unitIm.resize((hexScaledLength, hexScaledLength))
                        pos = getHexPos(rowOffset, side, centerX, innerRowNum, unitNum)
                        im.paste(unitIm, pos, unitIm)
                    unitNum += 1

        rowHeight = betweenRowPadding + innerRowHeight * heightFactors[rowNum]
        rowOffset += rowHeight
        drawer.line((0, rowOffset, imWidth, rowOffset), fill = (10, 10, 10), width = lineWidth)


    im.save("./infographic/elementAssists.png", quality = 95)

def pasteElement(image, rowNum, rowOffset, centerX):
    elementPath = "./images/elements/" + elementFiles[elements[rowNum]]
    with Image.open(elementPath, "r") as elIm:
        elIm = elIm.convert("RGBA")
        elIm = elIm.resize((elemScaledLength, elemScaledLength))
        elLength, _ = elIm.size
        xPos = centerX - elLength//2
        yPos = rowOffset + betweenRowPadding + hexScaledLength//2 - elemScaledLength//2
        image.paste(elIm, (xPos, yPos), elIm)

def drawModifier(drawer, modifier, side, centerX, rowOffset, innerRowNum):
    text = str(modifier) + "%"
    if side == 1:
        text = "+" + text + "\n Dmg."
    else:
        text = "-" + text + "\n Res."

    font = ImageFont.truetype(fontType, fontSize)
    tw, th = drawer.textsize(text, font=font, stroke_width=strokeWidth)

    xPos = centerX
    if side == 0:
        xPos -= (tw + textPaddingX)
    else:
        xPos += textPaddingX
    inRowY = hexScaledLength//2 - th//2 - int(th * textLineHeightFactor)
    yPos = rowOffset + betweenRowPadding + innerRowNum * innerRowHeight + inRowY
    drawer.text((xPos, yPos), text, fill=textColor, font=font, stroke_fill=strokeColor, stroke_width=strokeWidth)

def getHexPos(rowOffset, side, centerX, innerRowNum, unitNum):
    inRowWidths = unitNum * hexScaledLength
    totalBetweenPaddings = (unitNum - 1) * betweenPaddingX
    inRowX = inRowWidths + totalBetweenPaddings + framePaddingX
    inRowY = innerRowHeight * innerRowNum + betweenRowPadding

    y = rowOffset + inRowY
    x = centerX - inRowX - hexScaledLength if side == 0 else centerX + inRowX
    return (x,y)

# returns the number of assists in the largest subdict
def getWidthFactor(assistDict):
    max = -1
    for el in elements:
        for ef in effectTypes:
            for mod in assistDict[el][ef[1]]:
                if len(assistDict[el][ef[1]][mod]) > max:
                    max = len(assistDict[el][ef[1]][mod])
    return max

# Sums up the amount of different modifiers per element
def getRowHeights(assistDict):
    heightFactors = []
    for el in elements:
        inRowHeights = []
        for ef in effectTypes:
            # number of modifiers 
            mods = len(assistDict[el][ef[1]].keys())
            inRowHeights.append(mods)
        # for each element, only the effect type with the most modifiers counts
        heightFactors.append(max(inRowHeights))
    return heightFactors

# Returns a dict of the form { Element: { EffectType: { Modifier: [image filepaths] }}}
#   So each element subdict has two subdicts "Attack" and "Resist",
#   with each one a key for each modifier,
#   under which lies a list of assists with that effect type for that element and that modifier
def getElementAssistDict(db):
    assistImages = dict()
    for elem in elements:

        assistImages[elem] = dict()
        assistImages[elem][effectTypes[0][1]] = dict()
        assistImages[elem][effectTypes[1][1]] = dict()
        for efType in effectTypes:
            query = elem + " " + efType[0] + " " + efType[1]
            results = db.skillSearch(query,{})

            fileList = dict()
            for skill in results:
                if "As" in skill:
                    skillinfo = db.assembleAssistSkill(skill[2:])

                    # filters so base skills don't lead to duplicates, and ignores assist instant effects
                    if "++" in skillinfo[0] and not "instant effect" in skillinfo[0]:
                        assistid = db.getAssistIdFromSkill(skill[2:])
                        names = db.assembleAssistCharacterName(assistid)
                        mod = abs(getModifier(elem, efType[0], efType[1], skillinfo[1]))

                        try:
                            fileName = "./images/units/"+"{} [{}]".format(names[1],names[0]).strip()+"/hex.png"
                            file = open(fileName,"r")
                            file.close()
                            if mod not in assistImages[elem][efType[1]]:
                                assistImages[elem][effectTypes[0][1]][mod] = []
                                assistImages[elem][effectTypes[1][1]][mod] = []
                            assistImages[elem][efType[1]][mod].append(fileName)
                        except:
                            # Do something smarter for missing images?
                            print("Image for '{} [{}]' missing".format(names[1],names[0]) )
                            #file_list.append("./images/units/gac_dummy/hex.png")

    return assistImages

def getModifier(elem, target, type, effect):
    rightDelimiter = elem + " " + type
    positions = findAll(rightDelimiter, effect)
    #print("Positions: " + str(positions))
    foundPos = -1
    for pos in positions:
        foundTarget = getEffectTarget(effect, pos)
        #print("For pos " + str(pos) + " got target " + foundTarget)
        if foundTarget == target:
            foundPos = pos

    rightPos = effect.rfind('%', 0, foundPos)
    leftPos = effect.rfind(']', 0, foundPos)

    #print("Effect found: " + effect[leftPos:foundPos].strip())
    try:
        return int(effect[leftPos+1:rightPos].strip())
    except:
        return 0

def getEffectTarget(effect, startPos):
    leftPos = effect.rfind('[', 0, startPos)
    rightPos = effect.rfind(']', leftPos, startPos)
    return effect[leftPos+1:rightPos]

def findAll(query, effect):
    indexes = []
    max = -1
    while True:
        match = effect.find(query, max+1)
        if match >= 0:
            indexes.append(match)
            max = match
        else:
            break
    return indexes



