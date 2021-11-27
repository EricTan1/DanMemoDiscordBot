from typing import List
import numpy as np
from commands.cache import Cache


##################  
# Initialization #
##################
totalDamage=0
totalCounter=0
# damage per unit tracker
accumulateDamage=[0,0,0,0]

ultRatio = 0.0
counterRateBase = 0.0
critRateBase = 0.0
penRateBase = 0.0
bossPowerUp = 0

# list of adventurers
adv_list = []
# Printing
logprint = [1,1,1,1]
counterprint = 1
totaldamageprint = 1


##################
# RB adding buffs#
##################






##################
# RB Clear Skill #
##################

  # buff remove from list boostCheckAlliesAdv




###################
# Damage Function #
###################
def DamageFunction(
    location = 0,
    target = 'foe',
    tempBoost = 'none',
    powerCoefficient = 'low',
    extraBoost = 1, # Typical value is 1, should be 1+XX%*X
    NoType = 0, # 0 = no type counters?  1 = elemental type counters?
    type ='physical', # physical or magic attacks
    element='fire',# fire, water, earth, ....
    index_to=set() # {"strength","agi"}
    ):
  # lowercase everything
  target = target.lower()
  tempBoost = tempBoost.lower()
  powerCoefficient = powerCoefficient.lower()

  global totalDamage 
  global accumulateDamage 
  if target == 'foe':
    if tempBoost == 'none':
      tempBoostTemp = 1.0
    elif tempBoost == 'normal':   
      tempBoostTemp = 1.3
    elif tempBoost == 'normal2':   
      tempBoostTemp = 1.4     
    else:   
      tempBoostTemp = 1.6   
    if powerCoefficient == 'low':
      powerCoefficientTemp = 1.5
    elif powerCoefficient == 'mid':
      powerCoefficientTemp = 1.7
    elif powerCoefficient == 'high':
      powerCoefficientTemp = 1.9
    elif powerCoefficient == 'super':
      powerCoefficientTemp = 2.1
    elif powerCoefficient == 'magic':
      powerCoefficientTemp = 0.75
    else:
      powerCoefficientTemp = 1.0        
  else:
    if tempBoost == 'none':
      tempBoostTemp = 1.0
    elif tempBoost == 'normal':   
      tempBoostTemp = 1.4
    else:   
      tempBoostTemp = 1.7      
    if powerCoefficient == 'low':
      powerCoefficientTemp = 1.1
    elif powerCoefficient == 'mid':
      powerCoefficientTemp = 1.15
    elif powerCoefficient == 'high':
      powerCoefficientTemp = 1.2
    elif powerCoefficient == 'super':
      powerCoefficientTemp = 1.4       
  #print(memboost[location])

  # power[location]
  # powerBoostAdv[location]
  # powerBoostAst[location]
  # memboost[location] memorias
  # typeResistDownBase[location]
  # typeResistDownAdv[location]
  # typeResistDownAst[location]
  if("physical" in type):
    tempPower = power[location].get("strength")
    tempPowerBoostAdv = powerBoostAdv[location].get("strength")
    tempPowerBoostAst = powerBoostAst[location].get("strength")
    tempMemBoost = memboost.get("strength")

    tempTypeResistDownBase = typeResistDownBase.get("physical")
    tempTypeResistDownAdv = typeResistDownAdv.get("physical")
    tempTypeResistDownAst = typeResistDownAst.get("physical")


  else:
    tempPower = power[location].get("magic")
    tempPowerBoostAdv = powerBoostAdv[location].get("magic")
    tempPowerBoostAst = powerBoostAst[location].get("magic")
    tempMemBoost = memboost.get("magic")

    tempTypeResistDownBase = typeResistDownBase.get("magic")
    tempTypeResistDownAdv = typeResistDownAdv.get("magic")
    tempTypeResistDownAst = typeResistDownAst.get("magic")

  if(len(index_to) != 0):
    tempPower = 0
    tempPowerBoostAdv = 0
    tempPowerBoostAst = 0
    tempMemBoost = 0
    for index_to_attributes in index_to:
      tempPower += power[location].get(index_to_attributes)
      tempPowerBoostAdv += powerBoostAdv[location].get(index_to_attributes)
      tempPowerBoostAst += powerBoostAst[location].get(index_to_attributes)
      tempMemBoost += memboost.get(index_to_attributes)
    
  # elementResistDownBase[location]
  tempElementResistDownBase = elementResistDownBase.get(element)
  # elementResistDownAdv[location]
  tempElementResistDownAdv = elementResistDownAdv.get(element)
  # elementResistDownAst[location]
  tempElementResistDownAst = elementResistDownAst.get(element)



  # elementDamageBoostAdv[location]
  tempElementDamageBoostAdv = elementDamageBoostAdv[location].get(element)
  # elementDamageBoostAst[location]
  tempElementDamageBoostAst = elementDamageBoostAst[location].get(element)

  # critPenBoost[location] # dev skills
  # targetResistDownAdv[targetTemp]
  # targetResistDownAst[targetTemp]
  if target == 'foe':
    temptargetResistDownAdv = targetResistDownAdv.get("st")
    temptargetResistDownAst = targetResistDownAst.get("st")

  else:
    temptargetResistDownAdv = targetResistDownAdv.get("aoe")
    temptargetResistDownAst = targetResistDownAst.get("aoe")


  tempDamage = (2*tempPower*tempBoostTemp*(1+tempPowerBoostAdv+tempPowerBoostAst+tempMemBoost)-defense)*\
               (1-(1-NoType)*tempElementResistDownBase-(1-NoType)*tempElementResistDownAdv\
                -(1-NoType)*tempElementResistDownAst-tempTypeResistDownBase\
                -tempTypeResistDownAdv-tempTypeResistDownAst)*\
               (1+(1-NoType)*tempElementDamageBoostAdv+(1-NoType)*tempElementDamageBoostAst)*\
               (1+critPenBoost[location])*\
               (1-temptargetResistDownAdv-temptargetResistDownAst)*\
               powerCoefficientTemp*1.5*(extraBoost)
  totalDamage = totalDamage + tempDamage 
  accumulateDamage[location] = accumulateDamage[location] + tempDamage
  return tempDamage
def CounterDamageFunction(
    location = 0,
    target = 'foe',
    tempBoost = 'none',
    powerCoefficient = 'low',
    extraBoost = 1, # Typical value is 1, should be 1+XX%*X
    NoType = 0, # 0 = no type counters?  1 = elemental type counters?
    type ='physical', # physical or magic attacks
    element='fire' # fire, water, earth, ....

    ):
  # lowercase everything
  target = target.lower()
  tempBoost = tempBoost.lower()
  powerCoefficient = powerCoefficient.lower()

  global totalDamage 
  global accumulateDamage 
  if target == 'foe':
    if tempBoost == 'none':
      tempBoostTemp = 1.0
    elif tempBoost == 'normal':   
      tempBoostTemp = 1.3
    elif tempBoost == 'normal2':   
      tempBoostTemp = 1.4     
    else:   
      tempBoostTemp = 1.6   
    if powerCoefficient == 'low':
      powerCoefficientTemp = 1.5
    elif powerCoefficient == 'mid':
      powerCoefficientTemp = 1.7
    elif powerCoefficient == 'high':
      powerCoefficientTemp = 1.9
    elif powerCoefficient == 'super':
      powerCoefficientTemp = 2.1
    elif powerCoefficient == 'magic':
      powerCoefficientTemp = 0.75
    else:
      powerCoefficientTemp = 1.0        
  else:
    if tempBoost == 'none':
      tempBoostTemp = 1.0
    elif tempBoost == 'normal':   
      tempBoostTemp = 1.4
    else:   
      tempBoostTemp = 1.7      
    if powerCoefficient == 'low':
      powerCoefficientTemp = 1.1
    elif powerCoefficient == 'mid':
      powerCoefficientTemp = 1.15
    elif powerCoefficient == 'high':
      powerCoefficientTemp = 1.2
    elif powerCoefficient == 'super':
      powerCoefficientTemp = 1.4       
  #print(memboost[location])

  # power[location]
  # powerBoostAdv[location]
  # powerBoostAst[location]
  # memboost[location] memorias
  # typeResistDownBase[location]
  # typeResistDownAdv[location]
  # typeResistDownAst[location]
  if(type == "physical"):
    tempPower = power[location].get("strength")
    tempPowerBoostAdv = powerBoostAdv[location].get("strength")
    tempPowerBoostAst = powerBoostAst[location].get("strength")
    tempMemBoost = memboost.get("strength")

    tempTypeResistDownBase = typeResistDownBase.get("physical")
    tempTypeResistDownAdv = typeResistDownAdv.get("physical")
    tempTypeResistDownAst = typeResistDownAst.get("physical")


  else:
    tempPower = power[location].get("magic")
    tempPowerBoostAdv = powerBoostAdv[location].get("magic")
    tempPowerBoostAst = powerBoostAst[location].get("magic")
    tempMemBoost = memboost.get("magic")

    tempTypeResistDownBase = typeResistDownBase.get("magic")
    tempTypeResistDownAdv = typeResistDownAdv.get("magic")
    tempTypeResistDownAst = typeResistDownAst.get("magic")

  
  # elementResistDownBase[location]
  tempElementResistDownBase = elementResistDownBase.get(element)
  # elementResistDownAdv[location]
  tempElementResistDownAdv = elementResistDownAdv.get(element)
  # elementResistDownAst[location]
  tempElementResistDownAst = elementResistDownAst.get(element)



  # elementDamageBoostAdv[location]
  tempElementDamageBoostAdv = elementDamageBoostAdv[location].get(element)
  # elementDamageBoostAst[location]
  tempElementDamageBoostAst = elementDamageBoostAst[location].get(element)

  # critPenBoost[location] # dev skills
  # targetResistDownAdv[targetTemp]
  # targetResistDownAst[targetTemp]
  if target == 'foe':
    temptargetResistDownAdv = targetResistDownAdv.get("st")
    temptargetResistDownAst = targetResistDownAst.get("st")

  else:
    temptargetResistDownAdv = targetResistDownAdv.get("aoe")
    temptargetResistDownAst = targetResistDownAst.get("aoe")


  tempDamage = (2*tempPower*tempBoostTemp*(1+tempPowerBoostAdv+tempPowerBoostAst+tempMemBoost)-defense)*\
               (1-(1-NoType)*tempElementResistDownBase-(1-NoType)*tempElementResistDownAdv\
                -(1-NoType)*tempElementResistDownAst-tempTypeResistDownBase\
                -tempTypeResistDownAdv-tempTypeResistDownAst)*\
               (1+(1-NoType)*tempElementDamageBoostAdv+(1-NoType)*tempElementDamageBoostAst)*\
               (1+critPenBoost[location]+counterBoost[location])*\
               (1-temptargetResistDownAdv-temptargetResistDownAst)*\
               powerCoefficientTemp*1.5*(extraBoost)*counterRate
  totalDamage = totalDamage + tempDamage 
  accumulateDamage[location] = accumulateDamage[location] + tempDamage
  return tempDamage
def SADamageFunction(
    location = 0,
    target = 'Single',
    tempBoost = 'None',
    powerCoefficient = 'Low',
    extraBoost = 1, # Typical value is 1, should be 1+XX%*X
    combo = 1,
    type ='physical', # physical or magic attacks
    element='fire' # fire, water, earth, ....
    ):
  global totalDamage 
  global accumulateDamage 
  if tempBoost == 'None':
    tempBoostTemp = 1.0
  elif tempBoost == 'Normal':   
    tempBoostTemp = 1.4
  else:   
    tempBoostTemp = 1.7     
  if target == 'Single':
    if powerCoefficient == 'Low':
      powerCoefficientTemp = 1.5
    elif powerCoefficient == 'Mid':
      powerCoefficientTemp = 1.7
    elif powerCoefficient == 'High':
      powerCoefficientTemp = 1.9
    elif powerCoefficient == 'Super':
      powerCoefficientTemp = 2.1
    elif powerCoefficient == 'Ultra':
      powerCoefficientTemp = 4.0        
  else:
    if powerCoefficient == 'Low':
      powerCoefficientTemp = 1.1
    elif powerCoefficient == 'Mid':
      powerCoefficientTemp = 1.15
    elif powerCoefficient == 'High':
      powerCoefficientTemp = 1.2
    elif powerCoefficient == 'Super':
      powerCoefficientTemp = 1.4 
    elif powerCoefficient == 'Ultra':
      powerCoefficientTemp = 3.6            

  # power[location]
  # powerBoostAdv[location]
  # powerBoostAst[location]
  # memboost memorias
  # typeResistDownBase[location]
  # typeResistDownAdv[location]
  # typeResistDownAst[location]
  if(type == "physical"):
    tempPower = power[location].get("strength")
    tempPowerBoostAdv = powerBoostAdv[location].get("strength")
    tempPowerBoostAst = powerBoostAst[location].get("strength")
    tempMemBoost = memboost.get("strength")

    tempTypeResistDownBase = typeResistDownBase.get("physical")
    tempTypeResistDownAdv = typeResistDownAdv.get("physical")
    tempTypeResistDownAst = typeResistDownAst.get("physical")


  else:
    tempPower = power[location].get("magic")
    tempPowerBoostAdv = powerBoostAdv[location].get("magic")
    tempPowerBoostAst = powerBoostAst[location].get("magic")
    tempMemBoost = memboost.get("magic")

    tempTypeResistDownBase = typeResistDownBase.get("magic")
    tempTypeResistDownAdv = typeResistDownAdv.get("magic")
    tempTypeResistDownAst = typeResistDownAst.get("magic")

  
  # elementResistDownBase[location]
  tempElementResistDownBase = elementResistDownBase.get(element)
  # elementResistDownAdv[location]
  tempElementResistDownAdv = elementResistDownAdv.get(element)
  # elementResistDownAst[location]
  tempElementResistDownAst = elementResistDownAst.get(element)



  # elementDamageBoostAdv[location]
  tempElementDamageBoostAdv = elementDamageBoostAdv[location].get(element)
  # elementDamageBoostAst[location]
  tempElementDamageBoostAst = elementDamageBoostAst[location].get(element)

  # critPenBoost[location] # dev skills
  # targetResistDownAdv[targetTemp]
  # targetResistDownAst[targetTemp]
  if target == 'foe':
    temptargetResistDownAdv = targetResistDownAdv.get("st")
    temptargetResistDownAst = targetResistDownAst.get("st")

  else:
    temptargetResistDownAdv = targetResistDownAdv.get("aoe")
    temptargetResistDownAst = targetResistDownAst.get("aoe")

  tempDamage = (2*tempPower*tempBoostTemp*(1+tempPowerBoostAdv+tempPowerBoostAst+tempMemBoost)-defense)*\
               (1-tempElementResistDownBase-tempElementResistDownAdv\
                -tempElementResistDownAst-tempTypeResistDownBase\
                -tempTypeResistDownAdv-tempTypeResistDownAst)*\
               (1+tempElementDamageBoostAdv+tempElementDamageBoostAst)*\
               (1+critPenBoost[location])*\
               (1-temptargetResistDownAdv-temptargetResistDownAst)*\
               powerCoefficientTemp*1.5*(extraBoost)*(0.8+combo*0.2)*ultRatio
  totalDamage = totalDamage + tempDamage 
  accumulateDamage[location] = accumulateDamage[location] + tempDamage
  return tempDamage


'''
def AgiDamageFunction(
    location = 0,
    target = 'Single',
    tempBoost = 'None',
    powerCoefficient = 'Mid',
    extraBoost = 1, # Typical value is 1, should be 1+XX%*X    
    ):  
  global totalDamage
  global accumulateDamage
  if target == 'Single':
    targetTemp = 0   
  else:
    targetTemp = 1
  tempDamage = (2*agi*(1+agiBoostAdv+agiBoostAssist)-defense)*\
               (1-elementResistDownBase[1]-elementResistDownAdv[1]\
                -elementResistDownAst[1]-typeResistDownBase[location]\
                -typeResistDownAdv[location]-typeResistDownAst[location])*\
               (1+elementDamageBoostAdv[1]+elementDamageBoostAst[location])*\
               (1+critPenBoost[location])*\
               (1-targetResistDownAdv[targetTemp]-targetResistDownAst[targetTemp])*\
               1.7*1.95*1.5*(extraBoost)             
  totalDamage = totalDamage + tempDamage 
  accumulateDamage[location] = accumulateDamage[location] + tempDamage
  return tempDamage 
'''
#########    
# Debug #
#########
def DebugPrint():
  global elementResistDownAdv
  global typeResistDownAdv
  global elementDamageBoostAdv
  global targetResistDownAdv
  global powerBoostAdv
  print('elementResistDownAdv is:')
  print(elementResistDownAdv)
  print('typeResistDownAdv is:')
  print(typeResistDownAdv)
  print('elementDamageBoostAdv is:')
  print(elementDamageBoostAdv)
  print('targetResistDownAdv is:')
  print(targetResistDownAdv)
  print('powerBoostAdv is:')
  print(powerBoostAdv)
  print('additonalCount is:')
  print(additonalCount)  

##################    
# SA and Counter #
##################



#############
# Define RB #  
#############
# Boss
boss = 'Revis'
# Fit Parameter
# 0.96-1.04 RNG 
ultRatio = 1.00
#counterRate = 0.79
counterRate = 1
critRate = 1
penRate =1
# RB Weakness
elementResistDownBase={"fire":0,"water":0,"thunder":-0.5,"earth":-0.2,"wind":0,"light":0,"dark":0,"none":0}
typeResistDownBase={"physical":-0.1, "magic":0}
# Adv Stats
memboost = {"strength":0.00, "magic":0.06, "dex":0.00}
#power=[3079,3320,3323,3332]
#power=[3079,3320,3292,3369]
#power=[3079,3320,3125,3369]
#power=[2761,3156,3380,3389]

# including assists|| adv stat + assist stat excluding effects
power=[{"strength":270, "magic":2808}, {"strength":3380, "magic":0}, {"strength":3268, "magic":0}, {"strength":3385, "magic":0}]

#power=[2808,3380,3250,3379]
#power=[2808,3117,3388,3385]
#power=[2808,3361,3130,3404]
#power=[2778,3322-11,3300,3312+11]
#power=[2761,3419,3400,3168]
# counterBoost=[0.00, 0.60, 0.60, 0.60]
# critPenBoost=[0.06, 0.31, 0.31, 0.26]
#maxHaruMP = 823
#counterScale = 0.65
counterScale = 1
counter0Active = 0
counter1Active = 1
counter2Active = 1
counter3Active = 1

###################
# Define Strategy #  
###################
# Assist
def assistIn1():
  global powerBoostAst
  global typeResistDownAst
  global targetResistDownAst  
  global elementDamageBoostAst
  global elementResistDownAst
  global defense
  #elementResistDownAst=[-0.15, -0.15, -0.15, -0.15]
  #elementResistDownAst=[-0.0, -0.20, -0.20, -0.20]
  #targetResistDownAst=[-0.20, -0.00]
  #targetResistDownAst=[-0.20, -0.00]
  #elementDamageBoostAst=[0.00, 0.20, 0.20, 0.20]; 
  #powerBoostAst=[0.00, 0.20, 0.20, 0.20]  
  #powerBoostAst=[0.00, 0.20, 0.20, 0.20]  
  powerBoostAst=[0.00, 0.20, 0.20, 0.20] 
  #elementDamageBoostAst=[0.00, 0.20, 0.20, 0.00]; 
  #elementDamageBoostAst=[0.0, 0.20, 0.20, 0.20]; 
  #elementResistDownAst=[-0.00, -0.20, -0.20, -0.00]  
  #elementResistDownAst=[-0.00, -0.20, -0.00, -0.20]
  typeResistDownAst=[-0.00, -0.25, -0.25, -0.25] 
  #typeResistDownAst=[-0.25, -0.25, -0.25, -0.25] 
  #defense = defense*0.85
  #targetResistDownAst=[-0.00, -0.20]
  targetResistDownAst=[-0.20, -0.00]
  #elementResistDownAst=[-0.00, -0.20, -0.20, -0.20] 
  #targetResistDownAst=[-0.20, -0.00]
  #elementDamageBoostAst=[0.00, 0.20, 0.20, 0.20]
  #elementResistDownAst=[-0.00, -0.20, -0.20, -0.00]  
  #targetResistDownAst=[-0.20, -0.00]
  elementDamageBoostAst=[0.00, 0.20, 0.20, 0.20]
  #elementResistDownAst=[-0.00, -0.20, -0.20, -0.20]
  agiBoostAssist = 0.1
def assistIn2():
  global power  
  global elementResistDownAst  
  global typeResistDownAst
  global elementDamageBoostAst
  global targetResistDownAst
  global missBoost
  global powerBoostAst
  global defense
  #powerBoostAst=[0.00, 0.20, 0.15, 0.20] 
  #elementDamageBoostAst=[0.00, 0.20, 0.20, 0.00]; 
  #elementResistDownAst=[-0.00, -0.20, -0.20, -0.20]
  #typeResistDownAst=[-0.25, -0.25, -0.25, -0.25]   
  #targetResistDownAst=[-0.20, -0.00]
  #elementDamageBoostAst=[0.00, 0.20, 0.20, 0.00]
  #powerBoostAst=[0.00, 0.20, 0.15, 0.20] 
  #elementResistDownAst=[-0.00, -0.20, -0.20, -0.00] 
  #targetResistDownAst=[-0.20, -0.00]
  #targetResistDownAst=[-0.20, -0.00]
  #elementDamageBoostAst=[0.00, 0.00, 0.00, 0.20]
  #elementResistDownAst=[-0.0, -0.20, -0.20, -0.20]
  #elementDamageBoostAst=[0.00, 0.00, 0.20, 0.20]; 
  #typeResistDownAst=[-0.25, -0.25, -0.25, -0.25] 
  #elementResistDownAst=[-0.00, -0.20, -0.20, -0.20]  
  #powerBoostAst=[0.00, 0.15, 0.20, 0.15] 
  #missBoost = [0,0,0,0]
  elementResistDownAst=[-0.00, -0.20, -0.20, -0.20]
  #targetResistDownAst=[-0.20, -0.00]
  #elementResistDownAst=[-0.00, -0.00, -0.10, -0.10]   
  #targetResistDownAst=[-0.20, 0]    
  #elementResistDownAst=[-0.00, -0.20, -0.20, -0.20]  
  #defense=defense*0.65    
  #powerBoostAst=[0.00, 0.15, 0.25, 0.15]  
  #power[0]=1893;  
  return 0   
def assistIn3():
  global counterScale
  global powerBoostAst 
  global power  
  global typeResistDownAst  
  global elementResistDownAst
  global elementDamageBoostAst
  global counter0Active
  global currentHaruMP
  global counter2Active
  global counter1Active
  global counter3Active
  global targetResistDownAst
  global missBoost
  global agiBoostAssist
  #elementResistDownAst=[-0.00, -0.20, -0.20, -0.00] 
  #power[0]=2518;  
  #powerBoostAst=[0.10, 0.15, 0.10, 0.15]  
  #typeResistDownAst=[-0.25, -0.25, -0.25, -0.25]
  #powerBoostAst=[0.15, 0.15, 0.25, 0.15] 
  powerBoostAst=[0.10, 0.20, 0.20, 0.20] 
  #agiBoostAssist = 0.1
  #elementResistDownAst=[-0.00, -0.07, -0.07, -0.07]  
  #powerBoostAst=[0.10, 0.15, 0.10, 0.15] 
  #elementDamageBoostAst=[0.00, 0.20, 0.15, 0.20]
  #elementResistDownAst=[-0.00, -0.15, -0.15, -0.00]  
  #elementResistDownAst=[-0.00, -0.15, -0.15, -0.15]  
  #typeResistDownAst=[-0.25, -0.25, -0.25, -0.25] 
  #powerBoostAst=[0.00, 0.25, 0.15, 0.15]  
  #elementDamageBoostAst=[0.00, 0.20, 0.20, 0.20]; 
  #powerBoostAst=[0.15, 0.15, 0.25, 0.15]    
  #elementDamageBoostAst=[0.00, 0.20, 0.20, 0.20]; 
  #elementDamageBoostAst=[0.00, 0.20, 0.20, 0.20]; 
  #missBoost = [0,0,0,0]
  #targetResistDownAst=[-0.20, -0.0  ]
  # counter3Active = 1
  # counter1Active = 1
  # counter2Active = 1
  #counterScale = 1
  return 0 
assistInTurn = [1,2,3]
# 1,2,5

# Sac
#sac = 'WindRyu'  
#sac = 'Ais'  
sac1 = 'Ryu'
#sac1 = 'Riveria'
#sac = 'Line'
#sac = 'Alise'
#sac = 'Lyra'
#sac = 'Filvis'
#sac1 = 'Kotori'
#sac1 = 'Line'
sac = 'Ray'

# Skills
skill = np.array([
    [-1, -1,  2,  4,   1, 3, 2, 3,   1, 2, 3, 3,   2, 1, 1],
    [ 1,  3,  3,  3,   3, 3, 3, 3,   3, 2, 4, 3,   3, 3, 4],
    [ 2,  3,  3,  3,   3, 1, 3, 3,   3, 1, 3, 3,   3, 3, 3],
    [ 1,  2,  3,  3,   1, 2, 4, 3,   1, 2, 4, 3,   3, 3, 4],
    [ 3,  0,  0,  0,   0, 0, 0, 0,   0, 0, 0, 0,   0, 0, 0],
    [ 0,  2,  0,  0,   0, 0, 0, 0,   0, 0, 0, 0,   0, 0, 0]
    ]) # 5 rows for special ult (Photo etc.) 1537
""" 
skill = np.array([
    [-1, -1, -1, -1,   2, 4, 3, 3,   2, 3, 3, 3,   3, 3, 3],
    [ 1,  3,  3,  3,   3, 1, 3, 3,   3, 1, 3, 3,   3, 3, 4],
    [ 1,  2,  1,  2,   1, 2, 2, 1,   2, 2, 1, 2,   2, 2, 4],    
    [ 1,  2,  3,  3,   1, 2, 3, 3,   1, 2, 4, 3,   3, 3, 4],             
    [ 3,  0,  0,  0,   0, 0, 0, 0,   0, 0, 0, 0,   0, 0, 0], 
    [ 0,  2,  3,  4,   0, 0, 0, 0,   0, 0, 0, 0,   0, 0, 0] 
    ]) # 5 rows for special ult (Photo etc.) 1537
"""    
""" #############
# Main Loop #  
#############
# magresisthalt = 0
#currentHaruMP = maxHaruMP
totalDamageTemp = 0
for Turn in range(1,16):
  # Turn Start
  print("Turn {}:".format(int(Turn)))
  # if Turn == 13: 
  #   elementDamageBoostAdv=np.maximum([0, 1, 1, 1], elementDamageBoostAdv);  
  #if Turn == 2: missBoost[2]=1
  #if Turn == 3: missBoost[2]=0
  # if Turn == -1: 
  #   magresisthalt = 1
  # else:
  #   magresisthalt = 0
  if Turn == 7: 
    # magresisthalt = 1  2
    memboost = {"strength":0.00, "magic":0.00, "dex":0.00}
  if boss == 'Ottarl':
    if Turn == 5 or Turn == 9: OttarlClear()
  if boss == 'Riveria':
    if Turn == 5 or Turn == 9: RiveriaClear() 
    #if Turn == 12: RiveriaPowerUp()  
  if boss == 'Revis':
    if Turn == 1: RevisInitial()
    if Turn == 12: RevisPowerUp()
  if boss == 'Finn':    
    if Turn == 5 or Turn == 9: FinnClear()
    if Turn == 4 or Turn == 8 or Turn == 12: FinnAdd()    
  # Assist
  if Turn == assistInTurn[0]: assistIn1()
  if Turn == assistInTurn[1]: assistIn2()
  if Turn == assistInTurn[2]: assistIn3()    
  # SA  
  combo = np.sum(skill[:,Turn-1]==4)


  #DebugPrint()
  turnDamage = totalDamage - totalDamageTemp
  if totaldamageprint == 1:
    print('Turn {} total damage is {}'.format(Turn,np.floor(turnDamage).item()))
  totalDamageTemp = totalDamage
  #ManaRegen()
  if Turn == 15:
    print('\n')
    if logprint[0] == 1: print('{} total damage is {}'.format("PositionName0",np.floor(accumulateDamage[0]).item()))
    if logprint[1] == 1: print('{} total damage is {}'.format("PositionName1",np.floor(accumulateDamage[1]).item()))
    if logprint[2] == 1: print('{} total damage is {}'.format("PositionName2",np.floor(accumulateDamage[2]).item()))
    if logprint[3] == 1: print('{} total damage is {}'.format("PositionName3",np.floor(accumulateDamage[3]).item()))
    if totaldamageprint == 1: print('\n')
    if totaldamageprint == 1: print('Current total damage is {}'.format(np.floor(totalDamage).item()))
    if totaldamageprint == 1: print('Current total score is {}'.format(np.floor(totalDamage*10*2).item())) """




# initalization for units
def init():
  unit_titles = ['','','','']
  unit_sacs = ['', '']
  power=[{"strength":0, "magic":2808}, {"strength":3380, "magic":0}, {"strength":3268, "magic":0}, {"strength":3385, "magic":0}]
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

  # development skills that boosts crit/pen dmg and counter damage
  # counter damage
  counterBoost=[0, 0, 0, 0]
  # critpen damage
  critPenBoost=[0, 0, 0, 0]

  # organize skills into an actual list from order 1-4 (s1,s2,s3,sa)

