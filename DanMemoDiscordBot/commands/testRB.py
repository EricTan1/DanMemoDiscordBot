import discord
import asyncio
import json
import sys
import os
import aiohttp
from discord.ext import commands
from PIL import Image
import io
from urllib.parse import urlparse
import itertools

from commands.utils import get_emoji,HeroAscensionStatsP,HeroAscensionStatsB,HeroAscensionStatsM,Status, HeroAscensionStatsD, HeroAscensionStatsH, getDefaultEmoji, getElements
from database.DBcontroller import DBcontroller
from database.entities.Adventurer import Adventurer, AdventurerSkill, AdventurerSkillEffects, AdventurerDevelopment, AdventurerStats
from database.entities.BaseConstants import Element, Target, Type, Attribute, Modifier

from commands.cache import Cache
from commands.record_buster_calc import DamageFunction, boostCheckEnemyAppend, boostCheckAlliesAppend
import numpy as np
elementResistDownBase = {"fire":0,"water":0,"thunder":0,"earth":-0.2,"wind":0,"light":0,"dark":0,"none":0}
elementResistDownAdv= {"fire":0,"water":0,"thunder":0,"earth":0,"wind":0,"light":0,"dark":0,"none":0}
elementResistDownAst= {"fire":0,"water":0,"thunder":0,"earth":0,"wind":0,"light":0,"dark":0,"none":0}
# current 4 active party members
elementDamageBoostAdv=[
{"fire":0,"water":0,"thunder":0,"earth":0,"wind":0,"light":0,"dark":0},
{"fire":0,"water":0,"thunder":0,"earth":0,"wind":0,"light":0,"dark":0},
{"fire":0,"water":0,"thunder":0,"earth":0,"wind":0,"light":0,"dark":0},
{"fire":0,"water":0,"thunder":0,"earth":0,"wind":0,"light":0,"dark":0}]

elementDamageBoostAst=[
{"fire":0,"water":0,"thunder":0,"earth":0,"wind":0,"light":0,"dark":0},
{"fire":0,"water":0,"thunder":0,"earth":0,"wind":0,"light":0,"dark":0},
{"fire":0,"water":0,"thunder":0,"earth":0,"wind":0,"light":0,"dark":0},
{"fire":0,"water":0,"thunder":0,"earth":0,"wind":0,"light":0,"dark":0}]


# initalization for units
async def run(client, ctx):
    # 1 , 2, 3, 4, sac1, sac2
    unit_titles = ['Wondering Man','deathly dance','dazzling elf','Aschenputtel',"twilight supporter", "Drakguard's Will"]
    unit_skills = []
    power=[{"strength":2400, "magic":2808, "agility":0}, {"strength":3380, "magic":0,"agility":0}, {"strength":3268, "magic":0,"agility":0}, {"strength":3385, "magic":0,"agility":0}]
    # generally 1,2
    # could also be 1,1 for double sac or 1,4 for wiene
    # END of turn?
    unit_sacs_swap_turn =[1,4]
    skillflow = np.array([
        [-1, -1,  2,  4,   1, 3, 2, 3,   1, 2, 3, 3,   2, 1, 1], # unit 1
        [ 1,  3,  3,  3,   3, 3, 3, 3,   3, 2, 4, 3,   3, 3, 4], # unit 2
        [ 2,  3,  3,  3,   3, 1, 3, 3,   3, 1, 3, 3,   3, 3, 3], # unit 3
        [ 1,  2,  3,  3,   1, 2, 4, 3,   1, 2, 4, 3,   3, 3, 4], # unit 4
        [ 3,  0,  0,  0,   0, 0, 0, 0,   0, 0, 0, 0,   0, 0, 0], # sac 1
        [ 0,  2,  0,  0,   0, 0, 0, 0,   0, 0, 0, 0,   0, 0, 0]]) # sac 2 


    counterBoost=[0, 0, 0, 0, 0, 0]
    critPenBoost=[0, 0, 0, 0, 0, 0]
    
    #loading in characters
    cache = Cache()
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



    # organize skills into an actual list from order 1-4 (s1,s2,s3,sa)
    for unitsCounter in range(0,4):
        #current_adv_json["title"]=current_adv.unit_label
        if(unit_titles[unitsCounter].strip() != ""):
            adv_matches = [x for x in ad_list if x.unit_label.lower() == unit_titles[unitsCounter].lower()]
            if(len(adv_matches) > 0):
                curr_unit = adv_matches[0]
                current_skills = {"combat": [], "special":[], "additionals": []}
                # get all skills related to the adventurer
                adv_skill_matches = [x for x in ad_skill if x.adventurerid == curr_unit.unit_id]

                for adv_skills in adv_skill_matches:
                    # combine effects
                    adv_skill_effects_matches = [x for x in ad_skill_effects if x.adventurerskillid == adv_skills.adventurerskillid]
                    #print(adv_skill_effects_matches)
                    temp_list = current_skills.get(adv_skills.skilltype)
                    temp_list.append(adv_skill_effects_matches)
                    #print(temp_list)
                    current_skills[adv_skills.skilltype] = temp_list
                    #print(current_skills)        
                unit_skills.append(current_skills)
                # development skills that boosts crit/pen dmg and counter damage
                # counter damage
                adv_dev_matches = [x for x in ad_dev_effects if x.adventurerid == curr_unit.unit_id]
                for curr_adv_dev_skill in adv_dev_matches:
                    dev_attribute_name = curr_adv_dev_skill.attribute
                    #print("modifier: {} modifier type: {}".format(curr_adv_dev_skill.modifier,type(curr_adv_dev_skill.modifier)))
                    try:
                        dev_modifier_percent = int(curr_adv_dev_skill.modifier.strip())/100
                    except:
                        dev_modifier_percent=0
                    # critpen damage

                    # Counter Damage & counter_damage
                    if("counter" in dev_attribute_name.lower() and "damage" in dev_attribute_name.lower()):
                        counterBoost[unitsCounter]+= dev_modifier_percent
                    # Penetration Damage & penetration_damage
                    if("penetration" in dev_attribute_name.lower() and "damage" in dev_attribute_name.lower()):
                        critPenBoost[unitsCounter]+= dev_modifier_percent
                    # Critical damage & critical_damage
                    if("critical" in dev_attribute_name.lower() and "damage" in dev_attribute_name.lower()):
                        critPenBoost[unitsCounter]+= dev_modifier_percent

    await interpretSkillAdventurer(unit_skills[0].get("combat")[0])

   
async def interpretSkillAdventurer(skillEffects, location = 0):
    # for index_to maybe list  {"modifier": "End. & Mag.", "target": "skill", "attribute": "indexed_to","speed": "None" }
    
    damage_skill = [x for x in skillEffects if x.attribute.lower().strip()=="damage" or ((x.element!=None or x.element!="") and (x.type=="physical_attack" or x.type=="magic_attack"))]
    if(len(damage_skill) > 0):
        damage_skill = damage_skill[0]
        # do the damage first if attribute == element and modifier== high/medium etc, type = attack
        index_to_effects = [x for x in skillEffects if x.attribute.lower().strip()=="indexed_to"]
        index_to_modifier=set()
        # modifier is the index_to target
        for index_to_effect in index_to_effects:
            # "attribute" index_to
            index_to_modifier.add(index_to_effect.modifier)
        '''
        For temp boosts
        {
            "modifier": "normal2_str",
            "target": "skill",
            "attribute": "temp_boost",
        }
        '''
        temp_boost_effects = [x for x in skillEffects if x.attribute.lower().strip()=="temp_boost"]
        if(len(temp_boost_effects) > 0):
            temp_boost_mod = temp_boost_effects[0].modifier
        else:
            temp_boost_mod='none'
        
        # loop through the variables to check if attribute exists
        extra_boosts_effects = [x for x in skillEffects if "per_each" in x.attribute.lower().strip()]
        extra_boosts_value = 1
        # for example str/mag debuff
        if(len(extra_boosts_effects) > 0):
            for extra_boosts in extra_boosts_effects:
                extra_boosts_value = extra_boosts_value + interpretExtraBoost(extra_boosts, location)
        print(extra_boosts_value)
    #SELECT ase.AdventurerSkillEffectsid, ase.AdventurerSkillid, ase.duration, e.name AS element, m.value AS modifier, ty.name AS type, ta.name AS target, a.name AS attribute, s.name AS speed, ad.stars, ad.title, ad.alias, ad.limited, c.name

        # do main damage calc based on attribute
        temp_damage = DamageFunction(
            location = location,
            target = damage_skill.target,
            tempBoost = temp_boost_mod,
            powerCoefficient = damage_skill.modifier,
            extraBoost = extra_boosts_value, # Typical value is 1, should be 1+XX%*X
            NoType = 0, # 0 = no type counters?  1 = elemental type counters?
            type =damage_skill.type, # physical or magic attacks
            element=damage_skill.element,
            index_to=index_to_modifier # fire, water, earth, ....
        )
        print(temp_damage)


    # go through the effects
    for skillEffect in skillEffects:
        curr_attribute = skillEffect.attribute
        if(curr_attribute != None):
            # st/aoe resist down
            if(curr_attribute=="all_damage_resist"):
                pass
            elif(curr_attribute=="single_damage_resist"):
                pass
            # physical/magic resist down
            elif(curr_attribute.strip()=="physical_resist"):
                pass
            elif(curr_attribute.strip()=="magic_resist"):
                pass
            # str/mag buffs
            elif(curr_attribute.strip()=="strength"):
                # check self or allies
                pass
            elif(curr_attribute.strip()=="magic"):
                # check self or allies
                pass
            # element Resist & elemental buffs Down
            for curr_element in getElements():
                if(curr_element in curr_attribute and "attack" in curr_attribute):
                    if(curr_attribute.target.strip() == "self"):
                        temp_max = max(elementDamageBoostAdv[location].get(curr_element), int(skillEffect.modifier))
                        elementDamageBoostAdv[location][curr_element] = temp_max
                    elif(curr_attribute.target.strip() == "allies"):
                        for unitLocation in range(4):
                            temp_max = max(elementDamageBoostAdv[unitLocation].get(curr_element), int(skillEffect.modifier))
                            elementDamageBoostAdv[unitLocation][curr_element] = temp_max
                elif(curr_element in curr_attribute and "resist" in curr_attribute):
                    if(curr_attribute.target.strip() == "foe" or curr_attribute.target.strip() == "foes"):
                        temp_min = min(elementResistDownAdv.get(curr_element), int(skillEffect.modifier))
                        elementResistDownAdv[curr_element] = temp_min
            # status buff extends 
            if("status" in curr_attribute.strip() and ("buff" in curr_attribute.strip() or "debuff" in curr_attribute.strip())):
                pass
            # (maybe lyd extension for example)

            # removal skills
            elif("removal_no_assist" in curr_attribute.strip()):
                pass
            else:
                if(curr_attribute.target.strip() == "foe" or curr_attribute.target.strip() == "foes"):
                    #boostCheckEnemyAppend
                    pass
                # ally exists for a heal but doesn't matter here because its a heal. but maybe in the future??
                if(curr_attribute.target.strip() == "allies"):
                    #boostCheckAllyAppend
                    pass
                if(curr_attribute.target.strip() == "self"):
                    pass
            # update boost check arrays
    pass
    #print("counterBoost: {}".format(counterBoost))
    #print("critPenBoost: {}".format(critPenBoost))
    #print(unit_skills)



# append buffs to dict and remove once wiped
# list of dict
# {isbuff,Attribute,Modifier,duration}
# each list object
#{"isbuff":False,"attribute":"strength","modifier":-45,"duration":1}
# boostCheckEnemyAdv=[]
# boostCheckEnemyAst=[]

# boostCheckAlliesAdv=[[],[],[],[]]
# boostCheckAlliesAst=[[],[],[],[]]
boostCheckEnemyAdv=[]
boostCheckEnemyAst=[]

boostCheckAlliesAdv=[[],[],[],[]]
boostCheckAlliesAst=[[{"isbuff":True,"attribute":"critical_rate","modifier":-45,"duration":1},{"isbuff":True,"attribute":"strength","modifier":-45,"duration":1}],[],[],[]]

def interpretExtraBoost(skillEffect, location):
    ''' (adventurerSkillEffect) -> float
    takes in a skill effect with attribute exists of "per_each" then parse it and return the extra boosts multiplier

    return: extra boosts multiplier
        for extraBoost
        {
            "modifier": "+40",
            "target": "skill",
            "attribute": "per_each_self_fire_attack_buff",

            # per_each = extraboost
            # target = self/target
            # attribute = inbtw
            # buff/debuff
            "speed": "None"
        },
        # each list object
        #{"isbuff":False,"attribute":"strength","modifier":-45,"duration":1}
    '''
    extra_boosts_modifier_value = 0
    temp_list = skillEffect.attribute.split("_")
    # per each
    temp_list = temp_list[2:]
    try:
        temp_list.remove("skill")
    except:
        pass
    target=temp_list[0]
    temp_list = temp_list[1:]
    attribute = "_".join(temp_list[:len(temp_list)-1])
    attribute_type = temp_list[-1]
    print(target)
    print(attribute)
    print(attribute_type)

    if(target == "self"):
        #boostCheckAlliesAdv
        for selfBuffsAdv in boostCheckAlliesAdv[location]:
            if(selfBuffsAdv.get('isbuff') == (attribute_type == "buff")):
                if(selfBuffsAdv.get('attribute') == attribute):
                    extra_boosts_modifier_value = extra_boosts_modifier_value + int(skillEffect.modifier.strip())/100
        #boostCheckAlliesAst
        for selfBuffsAst in boostCheckAlliesAst[location]:
            if(selfBuffsAst.get('isbuff') == (attribute_type == "buff")):
                if(selfBuffsAst.get('attribute') == attribute):
                    extra_boosts_modifier_value = extra_boosts_modifier_value + int(skillEffect.modifier.strip())/100
    #target aka foes/foe
    else:
        for selfBuffsAdv in boostCheckEnemyAdv:
            if(selfBuffsAdv.get('isbuff') == (attribute_type == "buff")):
                if(selfBuffsAdv.get('attribute') == attribute):
                    extra_boosts_modifier_value = extra_boosts_modifier_value + int(skillEffect.modifier.strip())/100
        #boostCheckAlliesAst
        for selfBuffsAst in boostCheckEnemyAst:
            if(selfBuffsAst.get('isbuff') == (attribute_type == "buff")):
                if(selfBuffsAst.get('attribute') == attribute):
                    extra_boosts_modifier_value = extra_boosts_modifier_value + int(skillEffect.modifier.strip())/100
    print(extra_boosts_modifier_value)
    return extra_boosts_modifier_value

    