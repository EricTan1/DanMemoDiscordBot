import discord
# WANT TO CONNECT THIS TO DB SO CAN BE ANY SA_GUAGE
from commands.cache import Cache

async def run(ctx):
    # check if there is attachment if not send them a template attachment
    message = ctx.message
    errors = ""
    if(len(message.attachments) == 1):
        # if template attached start to verify it
        contents = await message.attachments[0].read()
        contents_decode = contents.decode("utf-8").split("\n")
        #print(contents_decode)
        for line in contents_decode:
            print(line)
            #buff wipe verify
            stripped_line = line.strip()
            if(stripped_line.startswith("BUFF_WIPE=")):
                stripped_line= stripped_line.replace("BUFF_WIPE=","")
                if(stripped_line.lower()=="true"):
                    is_revis = True
                elif(stripped_line.lower()=="false"):
                    is_revis = False
                else:
                    errors += "buff wipe is not True or False\n"
            #adventurer title format list
            elif(stripped_line.startswith("ADVENTURER=")):
                stripped_line= stripped_line.replace("ADVENTURER=","")
                try:
                    adventurer_order = stripped_line.split(",")
                except :
                    errors += "unable to read adventurer make sure there are 5 commas\n"
            #assist title format list
            elif(stripped_line.startswith("ASSIST=")):
                stripped_line= stripped_line.replace("ASSIST=","")
                try:
                    assists_order = stripped_line.split(",")
                except :
                    errors += "unable to read assist make sure there are 5 commas\n"
            # turn orders len 15
            elif(stripped_line.startswith("P3=")):
                stripped_line= stripped_line.replace("P3=","").replace("||",",")
                try:
                    p3 = verifyAndCast(stripped_line.split(","))
                except:
                    errors += "make turn orders are numeric and it is either separated by commas or ||\n"
            elif(stripped_line.startswith("P4=")):
                stripped_line= stripped_line.replace("P4=","").replace("||",",")
                try:
                    p4 = verifyAndCast(stripped_line.split(","))
                except:
                    errors += "make turn orders are numeric and it is either separated by commas or ||\n"
            elif(stripped_line.startswith("P5=")):
                stripped_line= stripped_line.replace("P5=","").replace("||",",")
                try:
                    p5 = verifyAndCast(stripped_line.split(","))
                except:
                    errors += "make turn orders are numeric and it is either separated by commas or ||\n"
            elif(stripped_line.startswith("P6=")):
                stripped_line= stripped_line.replace("P6=","").replace("||",",")
                try:
                    p6 = verifyAndCast(stripped_line.split(","))
                except:
                    errors += "make turn orders are numeric and it is either separated by commas or ||\n"
            elif(stripped_line.startswith("TURNS=")):
                stripped_line= stripped_line.replace("TURNS=","")
                try:
                    turns = int(stripped_line)
                except:
                    errors += "make turns numeric"
        # errors handling
        if (errors == ""):
            # try:
            await calculate(ctx,is_revis,adventurer_order,assists_order,p3,p4,p5,p6,turns)
            # except:
            #     temp_embed = discord.Embed()
            #     temp_embed.color = 16203840
            #     temp_embed.title = "ERROR"
            #     temp_embed.description = "Error trying to calculate SA"
            #     await ctx.send(embed=temp_embed)
        else:
            temp_embed = discord.Embed()
            temp_embed.color = 16203840
            temp_embed.title = "ERROR"
            temp_embed.description = errors
            await ctx.send(embed=temp_embed)
    else:
        await ctx.send("For this to work, you need to download the file, edit it, and reupload it into the channel with ais bot in it with the description !$sa", file=discord.File("sacalc.txt"))

def verifyAndCast(my_list):
    ret = []
    print(my_list)
    for items in my_list:
        ret.append(int(items))
    return ret

# Speed Tier needs to be added and calcs need to happen at buff phase
async def calculate(ctx,is_revis, adventurer_order, assists_order,p3,p4,p5,p6,turns):
    curr_message = ""
    cache = Cache()
    # 1,2 = sacs in order aka index 0 and 1
    #is_revis = True
    current_turn = 0
    # sac choices
    # welf, galmus,kotori, alise, idol ais, haru
    #adventurer_order = ["twilight supporter","","","","",""]
    #assists_order = ["","","","","","key strategist"]
    mlb_assist = [False,False,False,False,False,False]
    
    for x in range(len(assists_order)):
        temp_order = assists_order[x].lower()
        if ("mlb" in temp_order):
            mlb_assist[x] =True
            temp_order = temp_order.replace("mlb","").strip()

        skill = [skilleffect for skilleffect in cache.get_assist_sa_gauge() 
                        if temp_order == skilleffect.title.lower().strip()]
        if(len(skill) > 0):
            assists_order[x] = skill
        else:
            assists_order[x] = ""
    #print(assists_order)

    for x in range(len(adventurer_order)):
        skill = [skilleffect for skilleffect in cache.get_adventurer_sa_gauge() 
                        if adventurer_order[x].lower().strip() == skilleffect.title.lower().strip()]
        if(len(skill) > 0):
            adventurer_order[x] = skill
        else:
            adventurer_order[x] = ""
    #print(adventurer_order)
    #ad_skill_effects_ret = [skilleffect for skilleffect in ad_skill_effects 
                            #if new_words == skilleffect.element.lower()]
    # party members turn order
    add_on = [0]*turns
    print(add_on)
    p1 = [1]+add_on
    p2 = [2]+add_on

    print("p1 = : " + str(p1))
    # p3 = [1,1,1,1,1,
    #         1,1,2,1,1,
    #         1,1,3,3,4]
    # # last one that comes in
    # p4 = [1,1,1,1,1,
    #         1,1,2,1,1,
    #         1,1,3,3,4]
    # p5 = [1,1,1,1,1,
    #         1,1,2,1,4,
    #         1,1,3,3,4]
    # p6 = [0,0,3,4,1,
    #         1,1,2,1,4,
    #         1,1,3,3,3]
    turn_order_list = [p1,p2,p3,p4,p5,p6]
    # base sa guage current buffs
    sa_guage_adv = [0,0,0,0,0,0]
    sa_guage_as = [0,0,0,0,0,0]
    # every 14 = 1 full charge
    current_sa_guage = 0
    while current_turn < turns:
        curr_message = curr_message + "start of turn {}:\n".format(current_turn+1)
        #print("start of turn {}:".format(current_turn+1))
        # WIPE BUFFS FOR FINN,OTTARL,RIVERIA TURN 4/8
        if ((current_turn == 3 or current_turn == 7) and is_revis == False):
            print("buffs wiped")
            sa_guage_adv = [0,0,0,0,0,0]
        # first sac
        if(current_turn == 0):
            # APPLY ASSIST BUFFS t1 (first 4 assists) 0 = not mlb 1 = mlb
            for index in [0,2,3,4]:
                if(assists_order[index] != ""):
                    if(mlb_assist[index]):
                        assist_skill = assists_order[index][1]
                    else:
                        assist_skill = assists_order[index][0]
                    # check mlb?
                    curr_mod = int(assist_skill.modifier)/100
                    if(assist_skill.target.lower() == "self"):
                        if(sa_guage_as[x] < curr_mod):
                            sa_guage_as[index] = curr_mod
                    elif(assist_skill.target.lower() == "allies"):
                        for x in [0,2,3,4]:
                            if(sa_guage_as[x] < curr_mod):
                                sa_guage_as[x] = curr_mod
        # second sac
        elif(current_turn == 1):
            if(assists_order[1] != ""):
                if(mlb_assist[1]):
                    assist_skill = assists_order[1][1]
                else:
                    assist_skill = assists_order[1][0]
                # check mlb?
                curr_mod = int(assist_skill.modifier)/100
                if(assist_skill.target.lower() == "self"):
                    if(sa_guage_as[1] < curr_mod):
                        sa_guage_as[1] =curr_mod
                elif(assist_skill.target.lower() == "allies"):
                    for x in range(1,5):
                        if(sa_guage_as[x] < curr_mod):
                            sa_guage_as[x] = curr_mod
        # last person comes in
        elif(current_turn == 2):
            if(assists_order[5] != ""):
                if(mlb_assist[5]):
                    assist_skill = assists_order[5][1]
                else:
                    assist_skill = assists_order[5][0]
                # check mlb?
                curr_mod = int(assist_skill.modifier)/100
                if(assist_skill.target.lower() == "self"):
                    if(sa_guage_as[5] < curr_mod):
                        sa_guage_as[5] = curr_mod
                elif(assist_skill.target.lower() == "allies"):
                    for x in range(2,6):
                        if(sa_guage_as[x] < curr_mod):
                            sa_guage_as[x] = curr_mod
        # calculate adventurers SA guage
        for index in range(len(adventurer_order)):
            if(adventurer_order[index] != ""):
                adv_skill = adventurer_order[index][0]
                adv_mod = int(adv_skill.modifier)/100
                if(adv_skill.target.lower() == "self"):
                    if(not(turn_order_list[index][current_turn] != 4 and adv_skill.skilltype.lower() == "special")):
                        if(sa_guage_adv[index] < adv_mod):
                            sa_guage_adv[index] = adv_mod
                elif(adv_skill.target.lower() == "allies"):
                    if(current_turn == 0 and index == 0):
                        for x in [0,2,3,4]:
                            if(sa_guage_adv[x] < adv_mod):
                                sa_guage_adv[x] = adv_mod
                        if(sa_guage_adv[0] < adv_mod):
                            sa_guage_adv[0] = adv_mod
                    elif(current_turn == 1 and index == 1):
                        for x in range(1,5):
                            if(sa_guage_adv[x] < adv_mod):
                                sa_guage_adv[x] = adv_mod
                        if(sa_guage_adv[1] < adv_mod):
                            sa_guage_adv[1] = adv_mod
                    # ignore first and second adv now since not their turn
                    elif(index != 0 and index != 1):
                        for x in range(2,6):
                            if(sa_guage_adv[x] < adv_mod):
                                sa_guage_adv[x] = adv_mod
        if(current_turn==0):
            current_sa_guage = current_sa_guage + sa_guage_adv[0] + sa_guage_as[0] +1
            current_sa_guage = round(current_sa_guage,1)
        if(current_turn==1):
            current_sa_guage = current_sa_guage + sa_guage_adv[1] + sa_guage_as[1] +1
            current_sa_guage = round(current_sa_guage,1)

        for x in range(2,5):
            if(turn_order_list[x][current_turn] != 4):
                current_sa_guage = current_sa_guage + sa_guage_adv[x] + sa_guage_as[x] +1
                current_sa_guage = round(current_sa_guage,1)
            else:
                #print("MEMBER {} SA THIS TURN".format(x+1))
                curr_message = curr_message + "MEMBER {} SA THIS TURN\n".format(x+1)
                current_sa_guage = current_sa_guage - 14
        # last person who comes in after 2 sacs
        if(p6[current_turn] != 4 and current_turn > 1):
            current_sa_guage = current_sa_guage + sa_guage_adv[5] + sa_guage_as[5] +1
            current_sa_guage = round(current_sa_guage,1)
        elif (p6[current_turn] == 4 and current_turn > 1):
            print("MEMBER {} SA THIS TURN".format(6))
            curr_message = curr_message + "MEMBER {} SA THIS TURN\n".format(6)
            current_sa_guage = current_sa_guage - 14
        # 4 SA hard cap
        if(current_sa_guage >56):
            current_sa_guage=56
        curr_message = curr_message + "adv: {}\n".format(sa_guage_adv)
        curr_message = curr_message + "as: {}\n".format(sa_guage_as)
        curr_message = curr_message + "end of turn: {} with sa gauge charge {}\n\n".format(current_turn+1, round(current_sa_guage/14,2))
        #print("end of turn: {} with sa guage charge {}".format(current_turn+1, current_sa_guage/14))
        current_turn = current_turn +1
    # SA CALC
    temp_embed = discord.Embed()
    temp_embed.color = 3066993
    temp_embed.title = "SA Calculator"
    temp_embed.description = curr_message
    await ctx.send(embed=temp_embed)
