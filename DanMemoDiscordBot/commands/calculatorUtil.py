
#from commands.entities.adventurer import Adventurer

#from commands.entities.enemy import Enemy
from commands.entities.skills import AdventurerSkill,AdventurerCounter
import numpy as np
from commands.utils import getElements, getAilment

async def DamageFunction(skill:AdventurerSkill,adventurer,enemy, memboost:dict,skillRatio):
  ''' (AdventurerSkill, Adventurer, Enemy, dict, int) -> float
  memboost: {"strength":0.00, "magic":0.06, "dex":0.00}
  '''
  if(skill != None):
    # lowercase everything
    target = skill.target.lower()
    tempBoost = skill.tempBoost.lower()
    powerCoefficient = skill.powerCoefficient.lower()
    powerCoefficientTemp = 1.0

    if target == 'foe':
      if tempBoost == 'none':
        tempBoostTemp = 1.0
      elif 'normal2' in tempBoost:
        tempBoostTemp = 1.4  
      elif 'normal' in tempBoost:
        tempBoostTemp = 1.3   
      else:   
        tempBoostTemp = 1.6   
      if powerCoefficient == 'low' or powerCoefficient == 'lo':
        powerCoefficientTemp = 1.5
      elif powerCoefficient == 'mid' or powerCoefficient =='medium':
        powerCoefficientTemp = 1.7
      elif powerCoefficient == 'high':
        powerCoefficientTemp = 1.9
      elif powerCoefficient == 'super':
        powerCoefficientTemp = 2.1
      elif powerCoefficient == 'magic':
        powerCoefficientTemp = 0.75
    else:
      if tempBoost == 'none':
        tempBoostTemp = 1.0
      elif tempBoost == 'normal':   
        tempBoostTemp = 1.4
      else:   
        tempBoostTemp = 1.7      
      if powerCoefficient == 'low' or powerCoefficient == 'lo':
        powerCoefficientTemp = 1.1
      elif powerCoefficient == 'mid' or powerCoefficient == 'medium':
        powerCoefficientTemp = 1.15
      elif powerCoefficient == 'high':
        powerCoefficientTemp = 1.2
      elif powerCoefficient == 'super':
        powerCoefficientTemp = 1.4       

    # power[location]
    # powerBoostAdv[location]
    # powerBoostAst[location]
    # memboost[location] memorias
    # typeResistDownBase[location]
    # typeResistDownAdv[location]
    # typeResistDownAst[location]
    if("physical" in skill.type):
      tempPower = adventurer.stats.get("strength")
      tempPowerBoostAdv = adventurer.statsBoostAdv.get("strength")
      tempPowerBoostAst = adventurer.statsBoostAst.get("strength")
      tempMemBoost = memboost.get("strength")

      tempTypeResistDownBase = enemy.typeResistDownBase.get("physical")
      tempTypeResistDownAdv = enemy.typeResistDownAdv.get("physical")
      tempTypeResistDownAst = enemy.typeResistDownAst.get("physical")


    else:
      tempPower = adventurer.stats.get("magic")
      tempPowerBoostAdv = adventurer.statsBoostAdv.get("magic")
      tempPowerBoostAst = adventurer.statsBoostAst.get("magic")
      tempMemBoost = memboost.get("magic")

      tempTypeResistDownBase = enemy.typeResistDownBase.get("magic")
      tempTypeResistDownAdv = enemy.typeResistDownAdv.get("magic")
      tempTypeResistDownAst = enemy.typeResistDownAst.get("magic")

    if(len(skill.index_to) != 0):
      tempPower = 0
      tempPowerBoostAdv = 0
      tempPowerBoostAst = 0
      tempMemBoost = 0
      powerCoefficientTemp = powerCoefficientTemp *1.96
      for index_to_attributes in skill.index_to:
        tempPower += adventurer.stats.get(index_to_attributes)
        tempPowerBoostAdv += adventurer.statsBoostAdv.get(index_to_attributes)
        tempPowerBoostAst += adventurer.statsBoostAst.get(index_to_attributes)
        tempMemBoost += memboost.get(index_to_attributes)
    if(skill.element != "" and skill.noType !=1):
      # elementResistDownBase
      tempElementResistDownBase = enemy.elementResistDownBase.get(skill.element)
      # elementResistDownAdv
      tempElementResistDownAdv = enemy.elementResistDownAdv.get(skill.element)
      # elementResistDownAst
      tempElementResistDownAst = enemy.elementResistDownAst.get(skill.element)
      # elementDamageBoostAdv[location]
      tempElementDamageBoostAdv = adventurer.elementDamageBoostAdv.get(skill.element)
      if(memboost.get("{}_attack".format(skill.element)) != None):
        tempElementDamageBoostAdv+=memboost.get("{}_attack".format(skill.element))
      # elementDamageBoostAst[location]
      tempElementDamageBoostAst = adventurer.elementDamageBoostAst.get(skill.element)
    else:
      tempElementResistDownBase=0
      tempElementResistDownAdv=0
      tempElementResistDownAst=0
      tempElementDamageBoostAdv=0
      tempElementDamageBoostAst=0

    # critPenBoost[location] # dev skills
    # targetResistDownAdv[targetTemp]
    # targetResistDownAst[targetTemp]
    if target == 'foe':
      temptargetResistDownAdv = enemy.targetResistDownAdv.get("st")
      temptargetResistDownAst = enemy.targetResistDownAst.get("st")
    # foes
    else:
      temptargetResistDownAdv = enemy.targetResistDownAdv.get("aoe")
      temptargetResistDownAst = enemy.targetResistDownAst.get("aoe")
    temp_enemy_end = enemy.stats

    tempDamage = ((max(2*tempPower*tempBoostTemp*(1+tempPowerBoostAdv+tempPowerBoostAst+tempMemBoost)-temp_enemy_end.get("endurance"),0))*\
                (1-(1-skill.noType)*tempElementResistDownBase-(1-skill.noType)*tempElementResistDownAdv\
                  -(1-skill.noType)*tempElementResistDownAst-tempTypeResistDownBase\
                  -tempTypeResistDownAdv-tempTypeResistDownAst)*\
                (1+(1-skill.noType)*tempElementDamageBoostAdv+(1-skill.noType)*tempElementDamageBoostAst)*\
                (1+adventurer.critPenBoost + 0.06)*\
                (1-temptargetResistDownAdv-temptargetResistDownAst)*\
                powerCoefficientTemp*1.5*(skill.extraBoost))*skillRatio
    #totalDamage = totalDamage + tempDamage 
    #accumulateDamage[location] = accumulateDamage[location] + tempDamage
    return np.floor(tempDamage).item()
  else:
    return 0
async def CounterDamageFunction(counter:AdventurerCounter,adventurer,enemy, memboost:dict, counterRate:int, extra_boost:int):
  ''' (AdventurerSkill, Adventurer, Enemy, dict) -> float
  memboost: {"strength":0.00, "magic":0.06, "dex":0.00}
  '''
  # disable counters for adventurer
  if(adventurer.isCounter == False):
    return 0
  # magic units have light element always if not specified
  if(counter.element.lower() == "none" and counter.noType == 1):
    if(counter.type == "magic"):
      counter.element = "light"
  # lowercase everything
  target = counter.target.lower()
  tempBoostTemp = 1.0
  # power[location]
  # powerBoostAdv[location]
  # powerBoostAst[location]
  # memboost[location] memorias
  # typeResistDownBase[location]
  # typeResistDownAdv[location]
  # typeResistDownAst[location]
  if("physical" in counter.type):
    powerCoefficientTemp = 1.0   
    tempPower = adventurer.stats.get("strength")
    tempPowerBoostAdv = adventurer.statsBoostAdv.get("strength")
    tempPowerBoostAst = adventurer.statsBoostAst.get("strength")
    tempMemBoost = memboost.get("strength")
    tempTypeResistDownBase = enemy.typeResistDownBase.get("physical")
    tempTypeResistDownAdv = enemy.typeResistDownAdv.get("physical")
    tempTypeResistDownAst = enemy.typeResistDownAst.get("physical")
  else:
    powerCoefficientTemp = 0.75
    tempPower = adventurer.stats.get("magic")
    tempPowerBoostAdv = adventurer.statsBoostAdv.get("magic")
    tempPowerBoostAst = adventurer.statsBoostAst.get("magic")
    tempMemBoost = memboost.get("magic")

    tempTypeResistDownBase = enemy.typeResistDownBase.get("magic")
    tempTypeResistDownAdv = enemy.typeResistDownAdv.get("magic")
    tempTypeResistDownAst = enemy.typeResistDownAst.get("magic")

  if(counter.element != "" and counter.noType !=1):
    # elementResistDownBase
    tempElementResistDownBase = enemy.elementResistDownBase.get(counter.element)
    # elementResistDownAdv
    tempElementResistDownAdv = enemy.elementResistDownAdv.get(counter.element)
    # elementResistDownAst
    tempElementResistDownAst = enemy.elementResistDownAst.get(counter.element)
    # elementDamageBoostAdv[location]
    tempElementDamageBoostAdv = adventurer.elementDamageBoostAdv.get(counter.element)
    if(memboost.get("{}_attack".format(counter.element)) != None):
        tempElementDamageBoostAdv+=memboost.get("{}_attack".format(counter.element))
    # elementDamageBoostAst[location]
    tempElementDamageBoostAst = adventurer.elementDamageBoostAst.get(counter.element)
  else:
    tempElementResistDownBase=0
    tempElementResistDownAdv=0
    tempElementResistDownAst=0
    tempElementDamageBoostAdv=0
    tempElementDamageBoostAst=0

  # critPenBoost[location] # dev skills
  # targetResistDownAdv[targetTemp]
  # targetResistDownAst[targetTemp]
  if target == 'foe':
    temptargetResistDownAdv = enemy.targetResistDownAdv.get("st")
    temptargetResistDownAst = enemy.targetResistDownAst.get("st")
  # foes
  else:
    temptargetResistDownAdv = enemy.targetResistDownAdv.get("aoe")
    temptargetResistDownAst = enemy.targetResistDownAst.get("aoe")
  temp_enemy_end = enemy.stats

  tempDamage = ((max(2*tempPower*tempBoostTemp*(1+tempPowerBoostAdv+tempPowerBoostAst+tempMemBoost)-temp_enemy_end.get("endurance"),0))*\
               (1-(1-counter.noType)*tempElementResistDownBase-(1-counter.noType)*tempElementResistDownAdv\
                -(1-counter.noType)*tempElementResistDownAst-tempTypeResistDownBase\
                -tempTypeResistDownAdv-tempTypeResistDownAst)*\
               (1+(1-counter.noType)*tempElementDamageBoostAdv+(1-counter.noType)*tempElementDamageBoostAst)*\
               (1+adventurer.critPenBoost+adventurer.counterBoost + 0.06)*\
               (1-temptargetResistDownAdv-temptargetResistDownAst)*\
               powerCoefficientTemp*1.5*(extra_boost))*counterRate
  #totalDamage = totalDamage + tempDamage 
  #accumulateDamage[location] = accumulateDamage[location] + tempDamage
  #if(tempDamage > 0):
    #print("{} counter damage for {}".format(adventurer.name,tempDamage))
  return np.floor(tempDamage).item()
async def SADamageFunction(skill:AdventurerSkill,adventurer,enemy, memboost:dict, combo:int,ultRatio:int):
  ''' combo = int 1-4
      ultRatio = 0.96 - 1.04
  '''
  if(skill != None):
    # lowercase everything
    target = skill.target.lower()
    tempBoost = skill.tempBoost.lower()
    powerCoefficient = skill.powerCoefficient.lower()
    powerCoefficientTemp = 1
    if tempBoost == 'none':
      tempBoostTemp = 1.0
    elif 'normal' in tempBoost:   
      tempBoostTemp = 1.4
    else:   
      tempBoostTemp = 1.7     
    if skill.target == 'foe':
      if powerCoefficient == 'low' or powerCoefficient =='lo':
        powerCoefficientTemp = 1.5
      elif powerCoefficient == 'mid' or powerCoefficient == 'mid':
        powerCoefficientTemp = 1.7
      elif powerCoefficient == 'high':
        powerCoefficientTemp = 1.9
      elif powerCoefficient == 'super':
        powerCoefficientTemp = 2.1
      elif powerCoefficient == 'ultra':
        powerCoefficientTemp = 4.0        
    else:
      if powerCoefficient == 'low' or powerCoefficient =='lo':
        powerCoefficientTemp = 1.1
      elif powerCoefficient == 'mid' or powerCoefficient =='medium':
        powerCoefficientTemp = 1.15
      elif powerCoefficient == 'high':
        powerCoefficientTemp = 1.2
      elif powerCoefficient == 'super':
        powerCoefficientTemp = 1.4 
      elif powerCoefficient == 'ultra':
        powerCoefficientTemp = 3.6            

    # power[location]
    # powerBoostAdv[location]
    # powerBoostAst[location]
    # memboost[location] memorias
    # typeResistDownBase[location]
    # typeResistDownAdv[location]
    # typeResistDownAst[location]
    if("physical" in skill.type):
      tempPower = adventurer.stats.get("strength")
      tempPowerBoostAdv = adventurer.statsBoostAdv.get("strength")
      tempPowerBoostAst = adventurer.statsBoostAst.get("strength")
      tempMemBoost = memboost.get("strength")

      tempTypeResistDownBase = enemy.typeResistDownBase.get("physical")
      tempTypeResistDownAdv = enemy.typeResistDownAdv.get("physical")
      tempTypeResistDownAst = enemy.typeResistDownAst.get("physical")


    else:
      tempPower = adventurer.stats.get("magic")
      tempPowerBoostAdv = adventurer.statsBoostAdv.get("magic")
      tempPowerBoostAst = adventurer.statsBoostAst.get("magic")
      tempMemBoost = memboost.get("magic")

      tempTypeResistDownBase = enemy.typeResistDownBase.get("magic")
      tempTypeResistDownAdv = enemy.typeResistDownAdv.get("magic")
      tempTypeResistDownAst = enemy.typeResistDownAst.get("magic")

    if(len(skill.index_to) != 0):
      tempPower = 0
      tempPowerBoostAdv = 0
      tempPowerBoostAst = 0
      tempMemBoost = 0
      powerCoefficientTemp = powerCoefficientTemp *1.96
      for index_to_attributes in skill.index_to:
        tempPower += adventurer.stats.get(index_to_attributes)
        tempPowerBoostAdv += adventurer.statsBoostAdv.get(index_to_attributes)
        tempPowerBoostAst += adventurer.statsBoostAst.get(index_to_attributes)
        tempMemBoost += memboost.get(index_to_attributes)
    if(skill.element != "" and skill.noType !=1):
      # elementResistDownBase
      tempElementResistDownBase = enemy.elementResistDownBase.get(skill.element)
      # elementResistDownAdv
      tempElementResistDownAdv = enemy.elementResistDownAdv.get(skill.element)
      # elementResistDownAst
      tempElementResistDownAst = enemy.elementResistDownAst.get(skill.element)
      # elementDamageBoostAdv[location]
      
      tempElementDamageBoostAdv = adventurer.elementDamageBoostAdv.get(skill.element)
      if(memboost.get("{}_attack".format(skill.element)) != None):
        tempElementDamageBoostAdv+=memboost.get("{}_attack".format(skill.element))
      # elementDamageBoostAst[location]
      tempElementDamageBoostAst = adventurer.elementDamageBoostAst.get(skill.element)
    else:
      tempElementResistDownBase=0
      tempElementResistDownAdv=0
      tempElementResistDownAst=0
      tempElementDamageBoostAdv=0
      tempElementDamageBoostAst=0

    # critPenBoost[location] # dev skills
    # targetResistDownAdv[targetTemp]
    # targetResistDownAst[targetTemp]
    if target == 'foe':
      temptargetResistDownAdv = enemy.targetResistDownAdv.get("st")
      temptargetResistDownAst = enemy.targetResistDownAst.get("st")
    # foes
    else:
      temptargetResistDownAdv = enemy.targetResistDownAdv.get("aoe")
      temptargetResistDownAst = enemy.targetResistDownAst.get("aoe")

    temp_enemy_end = enemy.stats


    tempDamage = (max(2*tempPower*tempBoostTemp*(1+tempPowerBoostAdv+tempPowerBoostAst+tempMemBoost)-temp_enemy_end.get("endurance"),0))*\
                (1-tempElementResistDownBase-tempElementResistDownAdv\
                  -tempElementResistDownAst-tempTypeResistDownBase\
                  -tempTypeResistDownAdv-tempTypeResistDownAst)*\
                (1+tempElementDamageBoostAdv+tempElementDamageBoostAst)*\
                (1+adventurer.critPenBoost+ 0.06)*\
                (1-temptargetResistDownAdv-temptargetResistDownAst)*\
                powerCoefficientTemp*1.5*(skill.extraBoost)*(0.8+combo*0.2)*ultRatio
    #totalDamage = totalDamage + tempDamage 
    #accumulateDamage[location] = accumulateDamage[location] + tempDamage
    return np.floor(tempDamage).item()
  else:
    return 0

async def CombineSA(adventurerList:list,enemy, character_list:list):
  ''' (list of Adventurer, Enemy, list of boolean) -> int
  characterlist : [Char1,Char2,Char3,Char4]
    char1,char2,char3,char4 : 0 or 1
  '''
  tempDamage = 0
  for character in range(0,4):
    isPhysical=adventurerList[character].stats.get("magic") <= adventurerList[character].stats.get("strength")
    
    tempPower = max(adventurerList[character].stats.get("strength"),adventurerList[character].stats.get("magic"))
    
    if(isPhysical):
      temp_type = "physical"
      tempPowerBoostAdv =adventurerList[character].statsBoostAdv.get("strength")
      tempPowerBoostAst =adventurerList[character].statsBoostAst.get("strength")
    else:
      temp_type = "magic"
      tempPowerBoostAdv =adventurerList[character].statsBoostAdv.get("magic")
      tempPowerBoostAst =adventurerList[character].statsBoostAst.get("magic")
    tempDamage= tempDamage + (character_list[character]*(1.16*tempPower*(1+tempPowerBoostAdv+tempPowerBoostAst)))

  tempDamage = (max(tempDamage-enemy.stats.get("endurance"),0))*\
                (1-enemy.typeResistDownAdv.get(temp_type)-enemy.typeResistDownAst.get(temp_type))*\
                (1-enemy.targetResistDownAdv.get("aoe")-enemy.targetResistDownAst.get("aoe"))*\
                3.7*1.5
  print('Combine SA damage is {}'.format(np.floor(tempDamage).item()))
  #totalDamage = totalDamage + np.floor(tempDamage).item()
  return np.floor(tempDamage).item()

""" def Counter(notIn=[0,0,0,0]):
  global totalDamage
  global accumulateDamage  
  tempDamage = CounterDamageFunction(
      location = 0,
      target = 'Single',
      tempBoost = 'None',
      powerCoefficient = 'Magic',
      extraBoost = 0.25*counter0Active*counterScale,
      NoType = 1          
      )
  if logprint[0] == 1 and counterprint == 1:
    print('{} average single counter damage is {}'.format("PositionName0",np.floor(tempDamage).item()))
  tempDamage = CounterDamageFunction(
      location = 1,
      target = 'Single',
      tempBoost = 'None',
      powerCoefficient = 'Physic',
      extraBoost = 0.25*(1-notIn[1])*(counterScale)*counter1Active    
      )            
  if logprint[1] == 1 and counterprint == 1:
    print('{} average single counter damage is {}'.format("PositionName1",np.floor(tempDamage).item()))
  tempDamage = CounterDamageFunction(
      location = 2,
      target = 'Single',
      tempBoost = 'None',
      powerCoefficient = 'Physic',
      extraBoost = 0.25*(1-notIn[2])*1*counter2Active
      )
  if logprint[2] == 1 and counterprint == 1:
    print('{} average single counter damage is {}'.format("PositionName2",np.floor(tempDamage).item()))
  tempDamage = CounterDamageFunction(
      location = 3,
      target = 'Single',
      tempBoost = 'None',
      powerCoefficient = 'Physic',
      extraBoost = 0.25*(1-notIn[3])*counterScale     
      )  
  if logprint[3] == 1 and counterprint == 1:
    print('{} average single counter damage is {}'.format("PositionName3",np.floor(tempDamage).item()))
def Counters(notIn=[0,0,0,0]):
  global totalDamage
  global accumulateDamage
  tempDamage = CounterDamageFunction(
      location = 0,
      target = 'Single',
      tempBoost = 'None',
      powerCoefficient = 'Magic',
      extraBoost = counter0Active*counterScale,
      NoType = 1  
      )               
  if logprint[0] == 1 and counterprint == 1:
    print('{} counter damage is {}'.format("PositionName0",np.floor(tempDamage).item()))
  tempDamage = CounterDamageFunction(
      location = 1,
      target = 'Single',
      tempBoost = 'None',
      powerCoefficient = 'Physic',
      extraBoost = (1-notIn[1])*(counterScale)*counter1Active        
      ) 
  if logprint[1] == 1 and counterprint == 1:
    print('{} counter damage is {}'.format("PositionName1",np.floor(tempDamage).item()))
  tempDamage = CounterDamageFunction(
      location = 2,
      target = 'Single',
      tempBoost = 'None',
      powerCoefficient = 'Physic',
      extraBoost = (1-notIn[2])*1*counter2Active            
      )  
  if logprint[2] == 1 and counterprint == 1:
    print('{} counter damage is {}'.format("PositionName2",np.floor(tempDamage).item()))
  tempDamage = CounterDamageFunction(
      location = 3,
      target = 'Single',
      tempBoost = 'None',
      powerCoefficient = 'Physic',
      extraBoost = (1-notIn[3])*counterScale   
      )  
  if logprint[3] == 1 and counterprint == 1:
    print('{} counter damage is {}'.format("PositionName3",np.floor(tempDamage).item()))

 """

async def interpretExtraBoost(skillEffect, adventurer, enemy):
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

async def interpretSkillAdventurerAttack(skillEffects, adventurer, enemy):
  ''' (list of skillEffects, Adventurer, Enemy) -> AdventurerSkill or None
    None if there are no damage related effects
    AdventurerSkill if there is a damage related effect
  '''
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
          temp_extra_boosts = await interpretExtraBoost(extra_boosts, adventurer, enemy)
          extra_boosts_value = extra_boosts_value + temp_extra_boosts
    #SELECT ase.AdventurerSkillEffectsid, ase.AdventurerSkillid, ase.duration, e.name AS element, m.value AS modifier, ty.name AS type, ta.name AS target, a.name AS attribute, s.name AS speed, ad.stars, ad.title, ad.alias, ad.limited, c.name
    ret = AdventurerSkill(target=damage_skill.target,tempBoost=temp_boost_mod,powerCoefficient=damage_skill.modifier,extraBoost=extra_boosts_value,noType=0,type=damage_skill.type,element=damage_skill.element,index_to=index_to_modifier)
    return ret
  else:
    return None

async def interpretSkillAdventurerEffects(skillEffects, adventurer, enemy, adv_list:list):
  ''' (list of skilleffects, Adventurer, Enemy, list of Adventurer)
  '''
  # go through the effects
  for skillEffect in skillEffects:
    curr_attribute = skillEffect.attribute
    if(curr_attribute != None):
      curr_attribute = curr_attribute.strip().lower()
      try:
        curr_modifier = int(skillEffect.modifier)/100
      except:
        curr_modifier = skillEffect.modifier
      
      # st/aoe resist down
      if(curr_attribute=="all_damage_resist"):
        if(skillEffect.target.strip() == "self"):
          await adventurer.set_boostCheckAlliesAdv(curr_modifier>=0,curr_attribute,curr_modifier,skillEffect.duration)
        elif(skillEffect.target.strip() == "allies"):
          for curr_adv in adv_list:
            await curr_adv.set_boostCheckAlliesAdv(curr_modifier>=0,curr_attribute,curr_modifier,skillEffect.duration)
        elif(skillEffect.target.strip() == "foe" or skillEffect.target.strip() == "foes"):
          temp_min = min(enemy.targetResistDownAdv.get("aoe"), curr_modifier)
          enemy.targetResistDownAdv["aoe"] = temp_min
          await enemy.set_boostCheckEnemyAdv(False,curr_attribute,curr_modifier,skillEffect.duration)
      elif(curr_attribute=="single_damage_resist"):
        if(skillEffect.target.strip() == "self"):
          await adventurer.set_boostCheckAlliesAdv(curr_modifier>=0,curr_attribute,curr_modifier,skillEffect.duration)
        elif(skillEffect.target.strip() == "allies"):
          for curr_adv in adv_list:
            await curr_adv.set_boostCheckAlliesAdv(curr_modifier>=0,curr_attribute,curr_modifier,skillEffect.duration)
        elif(skillEffect.target.strip() == "foe" or skillEffect.target.strip() == "foes"):
          temp_min = min(enemy.targetResistDownAdv.get("st"), curr_modifier)
          enemy.targetResistDownAdv["st"] = temp_min
          await enemy.set_boostCheckEnemyAdv(False,curr_attribute,curr_modifier,skillEffect.duration)
      # physical/magic resist down
      elif(curr_attribute=="physical_resist"):
        if(skillEffect.target.strip() == "self"):
          await adventurer.set_boostCheckAlliesAdv(curr_modifier>=0,curr_attribute,curr_modifier,skillEffect.duration)
        elif(skillEffect.target.strip() == "allies"):
          for curr_adv in adv_list:
            await curr_adv.set_boostCheckAlliesAdv(curr_modifier>=0,curr_attribute,curr_modifier,skillEffect.duration)
        elif(skillEffect.target.strip() == "foe" or skillEffect.target.strip() == "foes"):
          temp_min = min(enemy.typeResistDownAdv.get("physical"), curr_modifier)
          enemy.typeResistDownAdv["physical"] = temp_min
          await enemy.set_boostCheckEnemyAdv(False,curr_attribute,curr_modifier,skillEffect.duration)
      elif(curr_attribute=="magic_resist"):
        if(skillEffect.target.strip() == "self"):
          await adventurer.set_boostCheckAlliesAdv(curr_modifier>=0,curr_attribute,curr_modifier,skillEffect.duration)
        elif(skillEffect.target.strip() == "allies"):
          for curr_adv in adv_list:
            await curr_adv.set_boostCheckAlliesAdv(curr_modifier>=0,curr_attribute,curr_modifier,skillEffect.duration)
        elif(skillEffect.target.strip() == "foe" or skillEffect.target.strip() == "foes"):
          temp_min = min(enemy.typeResistDownAdv.get("magic"), curr_modifier)
          enemy.typeResistDownAdv["magic"] = temp_min
          await enemy.set_boostCheckEnemyAdv(False,curr_attribute,curr_modifier,skillEffect.duration)
      # STAT buffs including str/mag buffs
      elif(curr_attribute in ["strength","magic","endurance","dexterity","agility"]):
        if(skillEffect.target.strip() == "self"):
          temp_max = max(adventurer.statsBoostAdv.get(curr_attribute.strip()), curr_modifier)
          adventurer.statsBoostAdv[curr_attribute.strip()] = temp_max
          await adventurer.set_boostCheckAlliesAdv(curr_modifier>=0,curr_attribute,curr_modifier,skillEffect.duration)
        elif(skillEffect.target.strip() == "allies"):
          for curr_adv in adv_list:
            temp_max = max(curr_adv.statsBoostAdv.get(curr_attribute.strip()), curr_modifier)
            curr_adv.statsBoostAdv[curr_attribute.strip()] = temp_max
            await curr_adv.set_boostCheckAlliesAdv(curr_modifier>=0,curr_attribute,curr_modifier,skillEffect.duration)
        elif(skillEffect.target.strip() == "foe" or skillEffect.target.strip() == "foes"):
          await enemy.set_boostCheckEnemyAdv(False,curr_attribute,curr_modifier,skillEffect.duration)
      # element Resist & elemental buffs Down
      for curr_element in getElements():
        if(curr_element in curr_attribute and "attack" in curr_attribute):
          if(skillEffect.target.strip() == "self"):
              temp_max = max(adventurer.elementDamageBoostAdv.get(curr_element), curr_modifier)
              adventurer.elementDamageBoostAdv[curr_element] = temp_max
              await adventurer.set_boostCheckAlliesAdv(curr_modifier>=0,curr_attribute,curr_modifier,skillEffect.duration)
          elif(skillEffect.target.strip() == "allies"):
            for curr_adv in adv_list:
              temp_max = max(curr_adv.elementDamageBoostAdv.get(curr_element), curr_modifier)
              curr_adv.elementDamageBoostAdv[curr_element] = temp_max
              await curr_adv.set_boostCheckAlliesAdv(curr_modifier>=0,curr_attribute,curr_modifier,skillEffect.duration)
        elif(curr_element in curr_attribute and "resist" in curr_attribute):
          if(skillEffect.target.strip() == "foe" or skillEffect.target.strip() == "foes"):
            temp_min = min(enemy.elementResistDownAdv.get(curr_element), curr_modifier)
            enemy.elementResistDownAdv[curr_element] = temp_min
            await enemy.set_boostCheckEnemyAdv(False,curr_attribute,curr_modifier,skillEffect.duration)
      # removal status_debuffs / status_buffs 
      if("status" in curr_attribute and "debuff" in curr_attribute and skillEffect.duration != None):
        temp_duration = int(skillEffect.duration)
        if(skillEffect.target.strip() == "self"):
          await adventurer.ExtendReduceDebuffs(temp_duration)
        elif(skillEffect.target.strip() == "allies"):
          for curr_adv in adv_list:
            await curr_adv.ExtendReduceDebuffs(temp_duration)
        elif(skillEffect.target.strip() == "foe" or skillEffect.target.strip() == "foes"):
          await enemy.ExtendReduceDebuffs(temp_duration)
      # status buff / debuffs extends/reduction
      elif("status" in curr_attribute and "buff" in curr_attribute and skillEffect.duration != None):
        temp_duration = int(skillEffect.duration)
        if(skillEffect.target.strip() == "self"):
          await adventurer.ExtendReduceBuffs(temp_duration)
        elif(skillEffect.target.strip() == "allies"):
          for curr_adv in adv_list:
            await curr_adv.ExtendReduceBuffs(temp_duration)
        elif(skillEffect.target.strip() == "foe" or skillEffect.target.strip() == "foes"):
          await enemy.ExtendReduceBuffs(temp_duration)

      # status buff removal and status debuff removal add

      # additional refresh
      if(curr_attribute == "additional_action"):
        if(skillEffect.target.strip() == "self"):
          await adventurer.set_additionalCount(int(skillEffect.duration))
      # removal skills
      elif("removal_no_assist" in curr_attribute):
        is_buff = not("debuff" in curr_attribute)

  

        temp_list = curr_attribute.replace("removal_no_assist","").split("_")
        try:
          temp_list.remove("buff")
        except:
          pass
        try:
          temp_list.remove("debuff")
        except:
          pass
        temp_attribute = " ".join(temp_list).strip()
        if(skillEffect.target.strip() == "self"):
          await adventurer.pop_boostCheckAlliesAdv(is_buff, temp_attribute)
        elif(skillEffect.target.strip() == "allies"):
          for curr_adv in adv_list:
            await curr_adv.pop_boostCheckAlliesAdv(is_buff, temp_attribute)
        elif(skillEffect.target.strip() == "foe" or skillEffect.target.strip() == "foes"):
          await enemy.pop_boostCheckEnemyAdv(is_buff, temp_attribute)
      else:
        NumberTypes = (int, float)
        if(isinstance(curr_modifier,NumberTypes) and curr_attribute != None and curr_attribute != "none" and not curr_attribute in getAilment()):
          if(skillEffect.target.strip() == "foe" or skillEffect.target.strip() == "foes"):
            #boostCheckEnemyAppend
            await enemy.set_boostCheckEnemyAdv(curr_modifier>=0,curr_attribute,curr_modifier,skillEffect.duration)
          # ally exists for a heal but doesn't matter here because its a heal. but maybe in the future??
          if(skillEffect.target.strip() == "allies"):
            #boostCheckAllyAppend
            for curr_adv in adv_list:
              await curr_adv.set_boostCheckAlliesAdv(curr_modifier>=0,curr_attribute,curr_modifier,skillEffect.duration)
          if(skillEffect.target.strip() == "self"):
            await adventurer.set_boostCheckAlliesAdv(curr_modifier>=0,curr_attribute,curr_modifier,skillEffect.duration)

async def interpretSkillAssistEffects(skillEffects, adventurer, enemy, adv_list:list):
  ''' (list of skilleffects, Adventurer, Enemy, list of Adventurer)
  '''
  # go through the effects
  for skillEffect in skillEffects:
    curr_attribute = skillEffect.attribute
    if(curr_attribute != None):
      curr_attribute = curr_attribute.strip().lower()
      try:
        curr_modifier = int(skillEffect.modifier)/100
      except:
        curr_modifier = skillEffect.modifier
      
      # st/aoe resist down
      if(curr_attribute=="all_damage_resist"):
        if(skillEffect.target.strip() == "self"):
          await adventurer.set_boostCheckAlliesAst(curr_modifier>=0,curr_attribute,curr_modifier,skillEffect.duration)
        elif(skillEffect.target.strip() == "allies"):
          for curr_adv in adv_list:
            await curr_adv.set_boostCheckAlliesAst(curr_modifier>=0,curr_attribute,curr_modifier,skillEffect.duration)
        elif(skillEffect.target.strip() == "foe" or skillEffect.target.strip() == "foes"):
          temp_min = min(enemy.targetResistDownAst.get("aoe"), curr_modifier)
          enemy.targetResistDownAst["aoe"] = temp_min
          await enemy.set_boostCheckEnemyAst(False,curr_attribute,curr_modifier,skillEffect.duration)
      elif(curr_attribute=="single_damage_resist"):
        if(skillEffect.target.strip() == "self"):
          await adventurer.set_boostCheckAlliesAst(curr_modifier>=0,curr_attribute,curr_modifier,skillEffect.duration)
        elif(skillEffect.target.strip() == "allies"):
          for curr_adv in adv_list:
            await curr_adv.set_boostCheckAlliesAst(curr_modifier>=0,curr_attribute,curr_modifier,skillEffect.duration)
        elif(skillEffect.target.strip() == "foe" or skillEffect.target.strip() == "foes"):
          temp_min = min(enemy.targetResistDownAst.get("st"), curr_modifier)
          enemy.targetResistDownAst["st"] = temp_min
          await enemy.set_boostCheckEnemyAst(False,curr_attribute,curr_modifier,skillEffect.duration)
      # physical/magic resist down
      elif(curr_attribute=="physical_resist"):
        if(skillEffect.target.strip() == "self"):
          await adventurer.set_boostCheckAlliesAst(curr_modifier>=0,curr_attribute,curr_modifier,skillEffect.duration)
        elif(skillEffect.target.strip() == "allies"):
          for curr_adv in adv_list:
            await curr_adv.set_boostCheckAlliesAst(curr_modifier>=0,curr_attribute,curr_modifier,skillEffect.duration)
        elif(skillEffect.target.strip() == "foe" or skillEffect.target.strip() == "foes"):
          temp_min = min(enemy.typeResistDownAst.get("physical"), curr_modifier)
          enemy.typeResistDownAst["physical"] = temp_min
          await enemy.set_boostCheckEnemyAst(False,curr_attribute,curr_modifier,skillEffect.duration)
      elif(curr_attribute=="magic_resist"):
        if(skillEffect.target.strip() == "self"):
          await adventurer.set_boostCheckAlliesAst(curr_modifier>=0,curr_attribute,curr_modifier,skillEffect.duration)
        elif(skillEffect.target.strip() == "allies"):
          for curr_adv in adv_list:
            await curr_adv.set_boostCheckAlliesAst(curr_modifier>=0,curr_attribute,curr_modifier,skillEffect.duration)
        elif(skillEffect.target.strip() == "foe" or skillEffect.target.strip() == "foes"):
          temp_min = min(enemy.typeResistDownAst.get("magic"), curr_modifier)
          enemy.typeResistDownAst["magic"] = temp_min
          await enemy.set_boostCheckEnemyAst(False,curr_attribute,curr_modifier,skillEffect.duration)
      # STATS || str/mag buffs
      elif(curr_attribute in ["strength","magic","endurance","dexterity","agility"]):
        if(skillEffect.target.strip() == "self"):
          temp_max = max(adventurer.statsBoostAst.get(curr_attribute.strip()), curr_modifier)
          adventurer.statsBoostAst[curr_attribute.strip()] = temp_max
          await adventurer.set_boostCheckAlliesAst(curr_modifier>=0,curr_attribute,curr_modifier,skillEffect.duration)
        elif(skillEffect.target.strip() == "allies"):
          for curr_adv in adv_list:
            temp_max = max(curr_adv.statsBoostAst.get(curr_attribute.strip()), curr_modifier)
            curr_adv.statsBoostAst[curr_attribute.strip()] = temp_max
            await curr_adv.set_boostCheckAlliesAst(curr_modifier>=0,curr_attribute,curr_modifier,skillEffect.duration)
        elif(skillEffect.target.strip() == "foe" or skillEffect.target.strip() == "foes"):
          await enemy.set_boostCheckEnemyAst(False,curr_attribute,curr_modifier,skillEffect.duration)
      # element Resist & elemental buffs Down
      for curr_element in getElements():
        if(curr_element in curr_attribute and "attack" in curr_attribute):
          if(skillEffect.target.strip() == "self"):
              temp_max = max(adventurer.elementDamageBoostAst.get(curr_element), curr_modifier)
              adventurer.elementDamageBoostAst[curr_element] = temp_max
              await adventurer.set_boostCheckAlliesAst(curr_modifier>=0,curr_attribute,curr_modifier,skillEffect.duration)
          elif(skillEffect.target.strip() == "allies"):
            for curr_adv in adv_list:
              temp_max = max(curr_adv.elementDamageBoostAst.get(curr_element), curr_modifier)
              curr_adv.elementDamageBoostAst[curr_element] = temp_max
              await curr_adv.set_boostCheckAlliesAst(curr_modifier>=0,curr_attribute,curr_modifier,skillEffect.duration)
        elif(curr_element in curr_attribute and "resist" in curr_attribute):
          if(skillEffect.target.strip() == "foe" or skillEffect.target.strip() == "foes"):
            temp_min = min(enemy.elementResistDownAst.get(curr_element), curr_modifier)
            enemy.elementResistDownAst[curr_element] = temp_min
            await enemy.set_boostCheckEnemyAst(False,curr_attribute,curr_modifier,skillEffect.duration)
      
      if("status" in curr_attribute and "debuff" in curr_attribute):
        temp_duration = int(skillEffect.duration)
        if(skillEffect.target.strip() == "self"):
          await adventurer.ExtendReduceDebuffs(temp_duration)
        elif(skillEffect.target.strip() == "allies"):
          for curr_adv in adv_list:
            await curr_adv.ExtendReduceDebuffs(temp_duration)
        elif(skillEffect.target.strip() == "foe" or skillEffect.target.strip() == "foes"):
          await enemy.ExtendReduceDebuffs(temp_duration)
      # status buff / debuffs extends/reduction
      elif("status" in curr_attribute and "buff" in curr_attribute):
        temp_duration = int(skillEffect.duration)
        if(skillEffect.target.strip() == "self"):
          await adventurer.ExtendReduceBuffs(temp_duration)
        elif(skillEffect.target.strip() == "allies"):
          for curr_adv in adv_list:
            await curr_adv.ExtendReduceBuffs(temp_duration)
        elif(skillEffect.target.strip() == "foe" or skillEffect.target.strip() == "foes"):
          await enemy.ExtendReduceBuffs(temp_duration)
      else:
        NumberTypes = (int, float)
        if(isinstance(curr_modifier,NumberTypes) and curr_attribute != None and curr_attribute != "none" and not curr_attribute in getAilment()):
          if(skillEffect.target.strip() == "foe" or skillEffect.target.strip() == "foes"):
            #boostCheckEnemyAppend
            await enemy.set_boostCheckEnemyAst(curr_modifier>=0,curr_attribute,curr_modifier,skillEffect.duration)
          # ally exists for a heal but doesn't matter here because its a heal. but maybe in the future??
          if(skillEffect.target.strip() == "allies"):
            #boostCheckAllyAppend
            for curr_adv in adv_list:
              await curr_adv.set_boostCheckAlliesAst(curr_modifier>=0,curr_attribute,curr_modifier,skillEffect.duration)
          if(skillEffect.target.strip() == "self"):
            await adventurer.set_boostCheckAlliesAst(curr_modifier>=0,curr_attribute,curr_modifier,skillEffect.duration)

async def counter(adv_list, enemy, memboost:dict, counterRate:float,logs:dict):
  ret = 0
  # take the avg
  # loop through and take the avg
  for adv in adv_list:

    temp_adv_counter= adv.adventurerCounter
    temp_extra_boost = 1
    if(adv.adventurerCounter.extraBoost != None):
      temp_extra_boost_value = await interpretExtraBoost(adv.adventurerCounter.extraBoost, adv, enemy)
      temp_extra_boost += temp_extra_boost_value

    temp_counter_damage = await CounterDamageFunction(counter=temp_adv_counter,adventurer=adv,enemy=enemy,memboost=memboost,counterRate=counterRate,extra_boost=temp_extra_boost)*0.25
    await adv.add_damage(temp_counter_damage)
    ret += temp_counter_damage
    # interpret the effects of counters
    await interpretSkillAdventurerEffects(adv.counterEffects,adv,enemy,adv_list)

  temp_list_logs = logs.get("counters")
  temp_list_logs.append("average single counter damage for {:,}".format(int(ret)))
  logs["counters"] = temp_list_logs

  
  return ret
    
async def counters(adv_list, enemy, memboost:dict, counterRate:float, logs:dict):
  ret = 0
  # take the avg
  # loop through and take the avg
  for adv in adv_list:
    # create adventurerCounter
  
    temp_adv_counter= adv.adventurerCounter
    temp_extra_boost = 1
    if(adv.adventurerCounter.extraBoost != None):
      temp_extra_boost_value = await interpretExtraBoost(adv.adventurerCounter.extraBoost, adv, enemy)
      temp_extra_boost += temp_extra_boost_value
    temp_counter_damage = await CounterDamageFunction(counter=temp_adv_counter,adventurer=adv,enemy=enemy,memboost=memboost,counterRate=counterRate,extra_boost=temp_extra_boost)
    await adv.add_damage(temp_counter_damage)
    temp_list_logs = logs.get("counters")
    temp_list_logs.append("{} counter damage for {:,}".format(adv.name,int(temp_counter_damage)))
    logs["counters"] = temp_list_logs
    ret += temp_counter_damage
    # interpret the effects of counters
    await interpretSkillAdventurerEffects(adv.counterEffects,adv,enemy,adv_list)
  return ret