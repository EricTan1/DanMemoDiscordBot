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
from commands.entities.enemy import Enemy

from commands.utils import getElements

from commands.cache import Cache
from commands.calculatorUtil import DamageFunction
import numpy as np

from commands.entities.adventurer import Adventurer


##################  
# Initialization #
##################
totalDamage=0
totalCounter=0
# damage per unit tracker
accumulateDamage=[0,0,0,0]
# Printing
logprint = [1,1,1,1]
counterprint = 1
totaldamageprint = 1

##################################################
#############
# Define RB #  
#############
# Boss
boss = 'Revis'
# 0.96-1.04 RNG 
ultRatio = 1.00
counterRate = 1
critRate = 1
penRate =1
ultRatio = 0.0
counterRateBase = 0.0
critRateBase = 0.0
penRateBase = 0.0
# memoria
memboost = {"strength":0.00, "magic":0.06, "dex":0.00}
# toggle counters
counterScale = 1
counter0Active = 0
counter1Active = 1
counter2Active = 1
counter3Active = 1

# initalization for units
async def run(client, ctx):
    pass

    #await interpretSkillAdventurer(unit_skills[0].get("combat")[0])
''' interpretSkillAdventurerAttack -> Skill
    interpretSkillAdventurerEffect -> Apply effects straight up
'''
   
async def interpretSkillAdventurer(skillEffects, adventurer:Adventurer, enemy:Enemy):
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
                extra_boosts_value = extra_boosts_value + interpretExtraBoost(extra_boosts, adventurer, enemy)
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

async def interpretExtraBoost(skillEffect, adventurer:Adventurer, enemy:Enemy):
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
        for selfBuffsAdv in adventurer.boostCheckAlliesAdv:
            if(selfBuffsAdv.get('isbuff') == (attribute_type == "buff")):
                if(selfBuffsAdv.get('attribute') == attribute):
                    extra_boosts_modifier_value = extra_boosts_modifier_value + int(skillEffect.modifier.strip())/100
        #boostCheckAlliesAst
        for selfBuffsAst in adventurer.boostCheckAlliesAst:
            if(selfBuffsAst.get('isbuff') == (attribute_type == "buff")):
                if(selfBuffsAst.get('attribute') == attribute):
                    extra_boosts_modifier_value = extra_boosts_modifier_value + int(skillEffect.modifier.strip())/100
    #target aka foes/foe
    else:
        for selfBuffsAdv in enemy.boostCheckEnemyAdv:
            if(selfBuffsAdv.get('isbuff') == (attribute_type == "buff")):
                if(selfBuffsAdv.get('attribute') == attribute):
                    extra_boosts_modifier_value = extra_boosts_modifier_value + int(skillEffect.modifier.strip())/100
        #boostCheckAlliesAst
        for selfBuffsAst in enemy.boostCheckEnemyAst:
            if(selfBuffsAst.get('isbuff') == (attribute_type == "buff")):
                if(selfBuffsAst.get('attribute') == attribute):
                    extra_boosts_modifier_value = extra_boosts_modifier_value + int(skillEffect.modifier.strip())/100
    print(extra_boosts_modifier_value)
    return extra_boosts_modifier_value


'''
if(curr_attribute.target.strip() == "self"):
    temp_max = max(adventurer.elementDamageBoostAdv.get(curr_element), int(skillEffect.modifier))
    adventurer.elementDamageBoostAdv[curr_element] = temp_max
    await adventurer.set_boostCheckAlliesAdv(True,curr_attribute,skillEffect.modifier,skillEffect.duration)
elif(curr_attribute.target.strip() == "allies"):
    for curr_adv in adv_list:
        temp_max = max(curr_adv.elementDamageBoostAdv.get(curr_element), int(skillEffect.modifier))
        curr_adv.elementDamageBoostAdv[curr_element] = temp_max
        await curr_adv.set_boostCheckAlliesAdv(True,curr_attribute,skillEffect.modifier,skillEffect.duration)
elif(curr_attribute.target.strip() == "foe" or curr_attribute.target.strip() == "foes"):
    temp_min = min(enemy.elementResistDownAdv.get(), int(skillEffect.modifier))
    enemy.elementResistDownAdv[curr_element] = temp_min
    await enemy.set_boostCheckEnemyAdv(False,curr_attribute,skillEffect.modifier,skillEffect.duration)

'''