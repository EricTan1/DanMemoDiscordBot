from discord.ext import commands
import discord
from commands.utils import getElements
from commands.cache import Cache
from commands.calculatorUtil import DamageFunction,CounterDamageFunction,SADamageFunction,CombineSA,interpretSkillAdventurerAttack,interpretSkillAdventurerEffects,interpretSkillAssistEffects
import numpy as np
from commands.entities.adventurer import Adventurer
from commands.entities.assist import Assist

from commands.entities.enemy import Enemy, Revis, Finn, Ottarl, Riveria
from commands.entities.skills import AdventurerSkill, AdventurerCounter


async def run(client, ctx):
    # user sets
    ##############################
    # Init boss
    ##############################
    boss = 'Revis'
    if(boss.lower() == "revis"):
        enemy = Revis(elementResistDownBase={"fire":0,"water":0,"thunder":0,"earth":0,"wind":0,"light":0,"dark":0,"none":0},
        typeResistDownBase={"physical":0, "magic":0}, 
        stats={"hp":0,"mp":0,"strength":0, "magic":0,"agility":0,"endurance":100,"dexerity":0})
    elif(boss.lower() == "finn"):
        enemy = Finn(elementResistDownBase={"fire":0,"water":0,"thunder":0,"earth":0,"wind":0,"light":0,"dark":0,"none":0},
        typeResistDownBase={"physical":0, "magic":0}, 
        stats={"hp":0,"mp":0,"strength":0, "magic":0,"agility":0,"endurance":700,"dexerity":0})
    elif(boss.lower() == "ottarl"):
        enemy = Ottarl(elementResistDownBase={"fire":0,"water":0,"thunder":0,"earth":0,"wind":0,"light":0,"dark":0,"none":0},
        typeResistDownBase={"physical":0, "magic":0}, 
        stats={"hp":0,"mp":0,"strength":0, "magic":0,"agility":0,"endurance":100,"dexerity":0})
    elif(boss.lower() == "riveria"):
        enemy = Riveria(elementResistDownBase={"fire":0,"water":0,"thunder":0,"earth":0,"wind":0,"light":0,"dark":0,"none":0},
        typeResistDownBase={"physical":0, "magic":0}, 
        stats={"hp":0,"mp":0,"strength":0, "magic":0,"agility":0,"endurance":100,"dexerity":0})
    else:
        enemy = Enemy(elementResistDownBase={"fire":0,"water":0,"thunder":0,"earth":0,"wind":0,"light":0,"dark":0,"none":0},
        typeResistDownBase={"physical":0, "magic":0}, 
        stats={"hp":0,"mp":0,"strength":0, "magic":0,"agility":0,"endurance":0,"dexerity":0})

    # 0.96-1.04 RNG 
    ultRatio = 1.00
    counterRate = 1
    critRate = 1
    penRate =1
    ultRatio = 0.0
    counterRateBase = 0.0
    critRateBase = 0.0
    penRateBase = 0.0
    memboost = {"hp":0,"mp":0,"strength":0, "magic":0,"agility":0,"endurance":0,"dexerity":0}
    # 1, 2, 3, 4, 5 ,6
    # sacs can be any order just list in SF
    unit_titles = ['Wondering Man','deathly dance','dazzling elf','Aschenputtel',"twilight supporter", "Drakguard's Will"]
    ast_titles = ["mlb Key Strategist","","","","",""]
    unit_sacs_swap_turn =[1,4]

    # skillflow[row][column] = skillflow[unit][turn] = skillflow[0-5][0-14]
    skillflow = np.array([
        [ 2,  0,  0,  0,   0, 0, 0, 0,   0, 0, 0, 0,   0, 0, 0], # unit 1
        [ 1,  3,  3,  3,   3, 3, 3, 3,   3, 2, 4, 3,   3, 3, 4], # unit 2
        [ 2,  3,  3,  3,   3, 1, 3, 3,   3, 1, 3, 3,   3, 3, 3], # unit 3
        [ 1,  2,  3,  3,   1, 2, 4, 3,   1, 2, 4, 3,   3, 3, 4], # unit 4
        [ 0,  2,  0,  0,   0, 0, 0, 0,   0, 0, 0, 0,   0, 0, 0], # unit 5
        [-1, -1,  2,  4,   1, 3, 2, 3,   1, 2, 3, 3,   2, 1, 1]]) # unit 6

    ##############################
    # Init Assists
    ##############################
    cache = Cache()
    #SELECT a.assistid, a.characterid, a.alias, a.title, a.stars, a.limited, c.name, c.iscollab
    ast_list = cache.get_all_assists()
    # SELECT assistskillid, assistid, skillname
    ast_skill = cache.get_all_assists_skills()
    #SELECT ase.assistskilleffectsid, ase.assistskillid, ase.duration, m.value as modifier, ta.name as target, a.name as attribute, assist.stars, assist.title, assist.alias, assist.limited, c.name
    ast_skill_effects = cache.get_all_adventurers_skills_effects()
    
    assist_list = []
    for assist in ast_titles:
        # parse assist titles by space
        temp_ast_title_list = assist.split(' ')
        is_mlb = False
        if(len(temp_ast_title_list) > 0):
            # its an mlb unit
            if(temp_ast_title_list[0].lower() == "mlb"):
                is_mlb = True
                temp_ast_title_list.pop(0)
            # rest of the title
            temp_ast_title = " ".join(temp_ast_title_list)

            ast_matches = [x for x in ast_list if x.title.lower() == temp_ast_title.lower()]
            if(len(ast_matches) > 0):
                current_assist = ast_matches[0]
                ast_skill_matches = [x for x in ast_skill if x.assistid == current_assist.assistid]
                ast_skill_effects = dict()
                # non mlb skill and mlb skill
                for ast_skill in ast_skill_matches:
                    ast_skill_effects_matches = [x for x in ast_skill_effects if x.assistskillid == ast_skill.assistskillid]
                    
                    if("++" in ast_skill.skillname):
                        if(is_mlb):
                            assist_list.append(Assist(ast_skill_effects_matches))
                    else:
                        assist_list.append(Assist(ast_skill_effects_matches))
            # no assist
            else:
                assist_list.append(Assist([]))
        # no assist
        else:
            assist_list.append(Assist([]))



    ##############################
    # Init Units
    ##############################
    #loading in characters
    # unit_id, character_id, type_id, alias, unit_label, stars, is_limited, is_ascended, character_name, is_collab, type_name
    ad_list = cache.get_all_adventurers()
    #SELECT adventurerskillid, adventurerid, skillname, skilltype
    ad_skill = cache.get_all_adventurers_skills()
    #SELECT ase.AdventurerSkillEffectsid, ase.AdventurerSkillid, ase.duration, e.name AS element, m.value AS modifier, ty.name AS type, ta.name AS target, a.name AS attribute, s.name AS speed, ad.stars, ad.title, ad.alias, ad.limited, c.name
    ad_skill_effects=cache.get_all_adventurers_skills_effects()
    #SELECT addev.adventurerdevelopmentid,addev.name as development, m.value as modifier, a.name as attribute, ad.stars, ad.title, ad.alias, ad.limited, c.name
    ad_dev_effects = cache.get_all_adventurers_developments()
    #SELECT adventurerstatsid, adventurerid, advstats.attributeid, attri.name, value
    adv_stats = cache.get_all_adventurers_stats()

    # all the units
    unit_list=[]

    # organize skills into an actual list from order 1-4 (s1,s2,s3,sa)
    for unitsCounter in range(0,len(unit_titles)):
        #current_adv_json["title"]=current_adv.unit_label
        if(unit_titles[unitsCounter].strip() != ""):
            adv_matches = [x for x in ad_list if x.unit_label.lower() == unit_titles[unitsCounter].lower()]
            if(len(adv_matches) > 0):
                curr_unit = adv_matches[0]
                current_skills = {"combat": [], "special":[], "additionals": []}
                
                current_skills_agi_mod = {"combat": [], "special":[], "additionals": []}
                # get all skills related to the adventurer
                adv_skill_matches = [x for x in ad_skill if x.adventurerid == curr_unit.unit_id]

                for adv_skills in adv_skill_matches:
                    # combine effects
                    adv_skill_effects_matches = [x for x in ad_skill_effects if x.adventurerskillid == adv_skills.adventurerskillid]

                    adv_skill_effects_agi_matches = [x for x in ad_skill_effects if x.speed.lower() == "fast"]
                    if(len(adv_skill_effects_agi_matches)>0):
                        temp_list_agi = current_skills_agi_mod.get(adv_skills.skilltype)
                        temp_list_agi.append("fast")
                        current_skills_agi_mod[adv_skills.skilltype] = temp_list_agi
                    else:
                        adv_skill_effects_agi_matches = [x for x in ad_skill_effects if x.speed.lower() == "slow"]
                        if(len(adv_skill_effects_agi_matches)>0):
                            temp_list_agi = current_skills_agi_mod.get(adv_skills.skilltype)
                            temp_list_agi.append("slow")
                            current_skills_agi_mod[adv_skills.skilltype] = temp_list_agi
                        else:
                            adv_skill_effects_agi_matches = [x for x in ad_skill_effects if x.speed.lower() == "none"]
                            if(len(adv_skill_effects_agi_matches)>0):
                                temp_list_agi = current_skills_agi_mod.get(adv_skills.skilltype)
                                temp_list_agi.append("none")
                                current_skills_agi_mod[adv_skills.skilltype] = temp_list_agi
                    #print(adv_skill_effects_matches)
                    temp_list = current_skills.get(adv_skills.skilltype)
                    temp_list.append(adv_skill_effects_matches)
                    #print(temp_list)
                    current_skills[adv_skills.skilltype] = temp_list
                    #print(current_skills)        
                #unit_skills.append(current_skills)
                # development skills that boosts crit/pen dmg and counter damage
                # counter damage
                adv_dev_matches = [x for x in ad_dev_effects if x.adventurerid == curr_unit.unit_id]
                tempCounterBoost = 0
                tempCritPenBoost= 0
                tempElementAttackCounter = "None"
                for curr_adv_dev_skill in adv_dev_matches:
                    dev_attribute_name = curr_adv_dev_skill.attribute
                    #print("modifier: {} modifier type: {}".format(curr_adv_dev_skill.modifier,type(curr_adv_dev_skill.modifier)))
                    try:
                        dev_modifier_percent = int(curr_adv_dev_skill.modifier.strip())/100
                    except:
                        dev_modifier_percent=0
                    # elemental counters and normal attacks
                    # Water Manifestation: H || element manifestation:letter
                    if("manifestation" in curr_adv_dev_skill.name.lower()):
                        tempElementAttackCounter = curr_adv_dev_skill.name.lower().split(" ")[0]

                    # Counter Damage & counter_damage
                    if("counter" in dev_attribute_name.lower() and "damage" in dev_attribute_name.lower()):
                        tempCounterBoost+= dev_modifier_percent
                    # Penetration Damage & penetration_damage
                    if("penetration" in dev_attribute_name.lower() and "damage" in dev_attribute_name.lower()):
                        tempCritPenBoost+= dev_modifier_percent
                    # Critical damage & critical_damage
                    if("critical" in dev_attribute_name.lower() and "damage" in dev_attribute_name.lower()):
                        tempCritPenBoost+= dev_modifier_percent
                    # counter extra boosts calc >:(
                # Create new adv object
                unit_list.append(Adventurer(stats = {"hp":0,"mp":0,"strength":0, "magic":0,"agility":0,"endurance":0,"dexerity":0}, 
                                    counterBoost=tempCounterBoost, 
                                    critPenBoost=tempCritPenBoost, 
                                    current_skills=current_skills,
                                    current_skills_agi_mod = current_skills_agi_mod, 
                                    turnOrder = skillflow[unitsCounter],
                                    elementAttackCounter=tempElementAttackCounter))
    ########################
    # Main Loop
    ########################
    # unit_list 0-5 aka 6 advs in order
    active_advs= [unit_list[0],unit_list[1],unit_list[2],unit_list[3]] # always length 4 current active adv
    sac_counter = 0
    total_damage = 0
    for turn in range(0, 15):
        # assist skills first turn!!
        if(turn == 0):
            for assistCount in range(0,4):
                interpretSkillAssistEffects(assist_list[assistCount].skills,active_advs[assistCount],enemy,active_advs)

        # SADamageFunction(skill:AdventurerSkill,adventurer:Adventurer,enemy:Enemy, memboost:dict, combo:int,ultRatio:int)
        # CombineSA(adventurerList:list,enemy:Enemy, character_list:list):
        # SAs SA damage function, combine SA
        character_sa_list = []
        sa_counter = 0
        for active_adv in range(0, len(active_advs)):
            if(active_advs[active_adv].get_turnOrder()[turn] == 4):
                character_sa_list.append(1)
                sa_counter+=1
            else:
                character_sa_list.append(0)
        # do the sa
        for active_adv in range(0, len(active_advs)):
            if(active_advs[active_adv].get_turnOrder()[turn] == 4):
                temp_adv_effects_list = active_advs[active_adv].get_specialSkill()
                temp_adv_skill = interpretSkillAdventurerAttack(temp_adv_effects_list,active_advs[active_adv],enemy)
                temp_damage = SADamageFunction(temp_adv_skill,active_advs[active_adv],enemy,memboost,sa_counter,ultRatio)
                total_damage += temp_damage
                active_advs[active_adv].add_damage(temp_damage)
        
        total_damage += CombineSA(active_advs,enemy,character_sa_list)
        # RB boss turn
        enemy.turnOrder(turn,active_adv, 0)

        #AdventurerCounter ???

        # agi calculation
        # ("agi","skill","adv")
        skills_priority_list = []
        for active_adv in active_advs:
            temp_agi = active_adv.get_stats().get("agility") * (1 + active_adv.get_statsBoostAdv().get("agility") + active_adv.get_statsBoostAst().get("agility"))
            # combat
            current_sf= active_adv.get_turnOrder()[turn]
            current_speed = active_adv.get_combatSkill_agi(current_sf)

            is_physical = active_adv.get_stats().get("strength")>=active_adv.get_stats().get("magic")
             # fast skills and agi war
            if(current_sf in [1,2,3]):
                temp_adv_effects_list = active_adv.get_combatSkill(current_sf)
                temp_adv_skill = interpretSkillAdventurerAttack(temp_adv_effects_list,active_advs[active_adv],enemy)
                temp_damage = SADamageFunction(temp_adv_skill,active_advs[active_adv],enemy,memboost,sa_counter,ultRatio)
                # interpret skills
                interpretSkillAdventurerEffects(temp_adv_effects_list,active_advs[active_adv],enemy,active_advs)
                # buff skills
                if(temp_damage == None):
                    if(current_speed== "fast"):
                        temp_agi = temp_agi * 5.35
                    elif(current_speed =="slow"):
                        temp_agi = temp_agi * 0.1
                    else:
                        temp_agi = temp_agi*1.75
                # damage skills
                else:
                    if(current_speed== "fast"):
                        temp_agi = temp_agi*3
                    elif(current_speed =="slow"):
                        temp_agi = temp_agi * 0.01
                    else:
                        if(not is_physical):
                            temp_agi = temp_agi *0.5
                skills_priority_list.append((temp_agi,current_speed,temp_adv_skill,active_adv))
            # auto attack
            elif(current_sf == 0):
                if(is_physical):
                    temp_type = "physical"
                else:
                    temp_agi = temp_agi *0.5
                    temp_type= "magic"
                temp_adv_skill = AdventurerSkill(powerCoefficient="physical",noType=0,type=temp_type,element=active_adv.elementAttackCounter)
                skills_priority_list.append((temp_agi,current_speed,temp_adv_skill,active_adv))

        sorted_skills_priority_list = sorted(skills_priority_list, key=lambda x: x[0], reverse=True)
        is_fast =True
        is_enemy_attacked = False
        # sort the list by first element in tuple
        for sorted_skills_counter in range(0,len(sorted_skills_priority_list)):
            removed_sorted_skill = sorted_skills_priority_list.pop(0)
            if(removed_sorted_skill[1] != "fast"):
                is_fast = False
            # not fast skill then rb can go
            if(not is_fast and not is_enemy_attacked):
                enemy.turnOrder(turn,active_adv, 1)
                is_enemy_attacked = True
            temp_damage = DamageFunction(removed_sorted_skill[2],removed_sorted_skill[3],enemy,memboost)
            interpretSkillAdventurerEffects(removed_sorted_skill[2],removed_sorted_skill[3],enemy,active_advs)
            total_damage += temp_damage
            removed_sorted_skill[3].add_damage(temp_damage)
        # end of turn skills
        enemy.turnOrder(turn,active_adv, 2)

        
        # sacs
        if(turn +1 < 15 and sac_counter < 2):
            for active_adv in range(0, len(active_advs)):
                # sac
                if(active_advs[active_adv].get_turnOrder()[turn+1] == -1 and sac_counter < 2):
                    active_advs[active_adv] = unit_list[len(active_advs)+sac_counter]
                    # assist
                    interpretSkillAssistEffects(assist_list[len(active_advs)+sac_counter].skills,unit_list[len(active_advs)+sac_counter],enemy,active_advs)
                    sac_counter+=1
    print('Current total damage is {}'.format(total_damage))
    print('Current total score is {}'.format(total_damage*10*2))