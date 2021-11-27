# -*- coding: utf-8 -*-
"""
Created on Thu Jan 28 00:53:39 2021

@author: lobsterbird
"""

import numpy as np
#import sys

##################  
# Initialization #
##################
totalDamage=0
totalCounter=0
accumulateDamage=[0,0,0,0]
elementResistDownBase=[0, 0, 0, 0]
elementResistDownAdv=[0, 0, 0, 0]
elementResistDownAst=[0, 0, 0, 0]
typeResistDownBase=[0, 0, 0, 0]
typeResistDownAdv=[0, 0, 0, 0]
typeResistDownAst=[0, 0, 0, 0]
elementDamageBoostAdv=[0, 0, 0, 0]
elementDamageBoostAst=[0, 0, 0, 0]
targetResistDownAdv=[0, 0]
targetResistDownAst=[0, 0]
powerBoostAdv=[0, 0, 0, 0]
powerBoostAst=[0, 0, 0, 0]
ultRatio = 0.0
counterRateBase = 0.0
critRateBase = 0.0
penRateBase = 0.0
bossPowerUp = 0
# Adv Stats
power=[0,0,0,0]
counterBoost=[0, 0, 0, 0.0]
critPenBoost=[0, 0, 0, 0]
chaseCount=[0,0,0,0]
maxHaruMP = 0
currentHaruMP = 0
# AssistsIn
targetResistDownAst=[-0.0, -0.0]
elementDamageBoostAst=[0.0, 0.0, 0.0, 0.0]
powerBoostAst=[0.0, 0.0, 0.0, 0.0]
typeResistDownAst=[-0.0, -0.0, -0.0, -0.0]
elementResistDownAst=[-0.0, -0.0, -0.0, -0.0]
# Special Parameter
missBoost = [0,0,0,0]
defense = 100
# Printing
logprint = [1,1,1,1]
counterprint = 1
totaldamageprint = 1
##################  
# RB Clear Skill #
##################
def RevisPowerUp():
  global bossPowerUp
  bossPowerUp = 1
def RiveriaPowerUp():
  global bossPowerUp
  bossPowerUp = 1  
def RevisAdd():
  global typeResistDownAdv
  global bossPowerUp
  typeResistDownAdv=np.minimum([-0.0, -0.7, -0.7, -0.7],typeResistDownAdv)
  bossPowerUp = 1
def RevisInitial():
  global typeResistDownAdv
  typeResistDownAdv=np.minimum([-0.0, -0.7, -0.7, -0.7],typeResistDownAdv)
  #print(typeResistDownAdv)
def RevisClear():
  global elementResistDownAdv
  global typeResistDownAdv
  global targetResistDownAdv
  elementResistDownAdv=[0, 0, 0, 0]
  typeResistDownAdv=[0, 0, 0, 0]
  targetResistDownAdv=[0, 0]
def RiveriaClear():
  global elementDamageBoostAdv
  global powerBoostAdv
  elementDamageBoostAdv=[0, 0, 0, 0]
  powerBoostAdv=[0, 0, 0, 0]  
def FinnClear():
  global elementResistDownAdv
  global typeResistDownAdv
  global targetResistDownAdv  
  global elementDamageBoostAdv
  global powerBoostAdv
  elementResistDownAdv=[0, 0, 0, 0]
  typeResistDownAdv=[0, 0, 0, 0]
  targetResistDownAdv=[0, 0]
  elementDamageBoostAdv=[0, 0, 0, 0]
  powerBoostAdv=[0, 0, 0, 0]  
def FinnAdd():
  global powerBoostAdv  
  global bossPowerUp
  powerBoostAdv=[1.5, 1.5, 1.5, 1.5]
  bossPowerUp = 2  
def OttarlClear():
  global elementDamageBoostAdv
  global powerBoostAdv
  elementDamageBoostAdv=[0, 0, 0, 0]
  powerBoostAdv=[0, 0, 0, 0]    
def Clear1():
  global elementDamageBoostAdv
  global powerBoostAdv
  elementDamageBoostAdv[0]=0
  powerBoostAdv[0]=0  
def ManaRegen():
  global currentHaruMP
  global maxHaruMP
  currentHaruMP = min(currentHaruMP+25,maxHaruMP)
def magresistbreak():
  global typeResistDownAdv
  typeResistDownAdv=[-0.0, -0.0, -0.0, -0.0]
###################
# Damage Function #
###################
def DamageFunction(
    location = 0,
    target = 'Single',
    tempBoost = 'None',
    powerCoefficient = 'Low',
    extraBoost = 1, # Typical value is 1, should be 1+XX%*X
    NoType = 0
    ):
  global totalDamage 
  global accumulateDamage 
  if target == 'Single':
    targetTemp = 0
    if tempBoost == 'None':
      tempBoostTemp = 1.0
    elif tempBoost == 'Normal':   
      tempBoostTemp = 1.3
    elif tempBoost == 'Normal2':   
      tempBoostTemp = 1.4     
    else:   
      tempBoostTemp = 1.6   
    if powerCoefficient == 'Low':
      powerCoefficientTemp = 1.5
    elif powerCoefficient == 'Mid':
      powerCoefficientTemp = 1.7
    elif powerCoefficient == 'High':
      powerCoefficientTemp = 1.9
    elif powerCoefficient == 'Super':
      powerCoefficientTemp = 2.1
    elif powerCoefficient == 'Magic':
      powerCoefficientTemp = 0.75
    else:
      powerCoefficientTemp = 1.0        
  else:
    targetTemp = 1
    if tempBoost == 'None':
      tempBoostTemp = 1.0
    elif tempBoost == 'Normal':   
      tempBoostTemp = 1.4
    else:   
      tempBoostTemp = 1.7      
    if powerCoefficient == 'Low':
      powerCoefficientTemp = 1.1
    elif powerCoefficient == 'Mid':
      powerCoefficientTemp = 1.15
    elif powerCoefficient == 'High':
      powerCoefficientTemp = 1.2
    elif powerCoefficient == 'Super':
      powerCoefficientTemp = 1.4            
  tempDamage = (2*power[location]*tempBoostTemp*(1+powerBoostAdv[location]+powerBoostAst[location])-defense)*\
               (1-(1-NoType)*elementResistDownBase[location]-(1-NoType)*elementResistDownAdv[location]\
                -(1-NoType)*elementResistDownAst[location]-typeResistDownBase[location]\
                -typeResistDownAdv[location]-typeResistDownAst[location])*\
               (1+(1-NoType)*elementDamageBoostAdv[location]+(1-NoType)*elementDamageBoostAst[location])*\
               (1+critPenBoost[location])*\
               (1-targetResistDownAdv[targetTemp]-targetResistDownAst[targetTemp])*\
               powerCoefficientTemp*1.5*(extraBoost)
  totalDamage = totalDamage + tempDamage 
  accumulateDamage[location] = accumulateDamage[location] + tempDamage
  return tempDamage
def CounterDamageFunction(
    location = 0,
    target = 'Single',
    tempBoost = 'None',
    powerCoefficient = 'Low',
    extraBoost = 1, # Typical value is 1, should be 1+XX%*X
    NoType = 0
    ):
  global totalDamage 
  global accumulateDamage 
  if target == 'Single':
    targetTemp = 0
    if tempBoost == 'None':
      tempBoostTemp = 1.0
    elif tempBoost == 'Normal':   
      tempBoostTemp = 1.3
    else:   
      tempBoostTemp = 1.6   
    if powerCoefficient == 'Low':
      powerCoefficientTemp = 1.5
    elif powerCoefficient == 'Mid':
      powerCoefficientTemp = 1.7
    elif powerCoefficient == 'High':
      powerCoefficientTemp = 1.9
    elif powerCoefficient == 'Super':
      powerCoefficientTemp = 2.1
    elif powerCoefficient == 'Magic': # Magic Normal Attach/Counter
      powerCoefficientTemp = 0.75
    else:
      powerCoefficientTemp = 1.0        
  else:
    targetTemp = 1
    if tempBoost == 'None':
      tempBoostTemp = 1.0
    elif tempBoost == 'Normal':   
      tempBoostTemp = 1.4
    else:   
      tempBoostTemp = 1.7      
    if powerCoefficient == 'Low':
      powerCoefficientTemp = 1.1
    elif powerCoefficient == 'Mid':
      powerCoefficientTemp = 1.15
    elif powerCoefficient == 'High':
      powerCoefficientTemp = 1.2
    elif powerCoefficient == 'Super':
      powerCoefficientTemp = 1.4            
  tempDamage = (2*power[location]*tempBoostTemp*(1+powerBoostAdv[location]+powerBoostAst[location])-defense)*\
               (1-(1-NoType)*elementResistDownBase[location]-(1-NoType)*elementResistDownAdv[location]\
                -(1-NoType)*elementResistDownAst[location]-typeResistDownBase[location]\
                -typeResistDownAdv[location]-typeResistDownAst[location])*\
               (1+(1-NoType)*elementDamageBoostAdv[location]+(1-NoType)*elementDamageBoostAst[location])*\
               (1+critPenBoost[location]+counterBoost[location])*\
               (1-targetResistDownAdv[targetTemp]-targetResistDownAst[targetTemp])*\
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
    targetTemp = 0
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
    targetTemp = 1    
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
  tempDamage = (2*power[location]*tempBoostTemp*(1+powerBoostAdv[location]+powerBoostAst[location])-defense)*\
               (1-elementResistDownBase[location]-elementResistDownAdv[location]\
                -elementResistDownAst[location]-typeResistDownBase[location]\
                -typeResistDownAdv[location]-typeResistDownAst[location])*\
               (1+elementDamageBoostAdv[location]+elementDamageBoostAst[location])*\
               (1+critPenBoost[location])*\
               (1-targetResistDownAdv[targetTemp]-targetResistDownAst[targetTemp])*\
               powerCoefficientTemp*1.5*(extraBoost)*(0.8+combo*0.2)*ultRatio 
  totalDamage = totalDamage + tempDamage 
  accumulateDamage[location] = accumulateDamage[location] + tempDamage
  return tempDamage
def OverwriteDamageFunction(
    location = 0,
    target = 'Single',
    tempBoost = 'None',
    powerCoefficient = 'Low',
    extraBoost = 1, # Typical value is 1, should be 1+XX%*X
    ):
  global totalDamage 
  global accumulateDamage 
  if target == 'Single':
    targetTemp = 0
    if tempBoost == 'None':
      tempBoostTemp = 1.0
    elif tempBoost == 'Normal':   
      tempBoostTemp = 1.3
    elif tempBoost == 'Normal2':   
      tempBoostTemp = 1.4     
    else:   
      tempBoostTemp = 1.6   
    if powerCoefficient == 'Low':
      powerCoefficientTemp = 1.5
    elif powerCoefficient == 'Mid':
      powerCoefficientTemp = 1.7
    elif powerCoefficient == 'High':
      powerCoefficientTemp = 1.9
    elif powerCoefficient == 'Super':
      powerCoefficientTemp = 2.1
    elif powerCoefficient == 'Magic':
      powerCoefficientTemp = 0.75
    else:
      powerCoefficientTemp = 1.0        
  else:
    targetTemp = 1
    if tempBoost == 'None':
      tempBoostTemp = 1.0
    elif tempBoost == 'Normal':   
      tempBoostTemp = 1.4
    else:   
      tempBoostTemp = 1.7      
    if powerCoefficient == 'Low':
      powerCoefficientTemp = 1.1
    elif powerCoefficient == 'Mid':
      powerCoefficientTemp = 1.15
    elif powerCoefficient == 'High':
      powerCoefficientTemp = 1.2
    elif powerCoefficient == 'Super':
      powerCoefficientTemp = 1.4     
  """       
  tempDamage = (2*power[location]*tempBoostTemp*(1+powerBoostAdv[location]+powerBoostAst[location])-defense)*\
               (1-elementResistDownBase[location]-elementResistDownAdv[location]\
                -elementResistDownAst[location]-typeResistDownBase[location]\
                -typeResistDownAdv[location]-typeResistDownAst[location])*\
               (1+elementDamageBoostAdv[location]+elementDamageBoostAst[location])*\
               (1+critPenBoost[location])*\
               (1-targetResistDownAdv[targetTemp]-targetResistDownAst[targetTemp])*\
               powerCoefficientTemp*1.5*(extraBoost)
  """
  tempDamage = (2*power[location]*tempBoostTemp*(1+powerBoostAdv[location]+powerBoostAst[location])-defense)*\
               (1-elementResistDownBase[1]-elementResistDownAdv[1]\
                -elementResistDownAst[1]-typeResistDownBase[location]\
                -typeResistDownAdv[location]-typeResistDownAst[location])*\
               (1+elementDamageBoostAdv[1]+elementDamageBoostAst[location])*\
               (1+critPenBoost[location])*\
               (1-targetResistDownAdv[targetTemp]-targetResistDownAst[targetTemp])*\
               powerCoefficientTemp*1.5*(extraBoost)             
  totalDamage = totalDamage + tempDamage 
  accumulateDamage[location] = accumulateDamage[location] + tempDamage
  return tempDamage
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
  print('chaseCount is:')
  print(chaseCount)  
    
########    
# Haru #
########  
def HaruS1():
  global totalDamage
  global accumulateDamage  
  global typeResistDownAdv
  tempDamage = DamageFunction(
      location = 0,
      target = 'AOE',
      tempBoost = 'None',
      powerCoefficient = 'Mid',
      extraBoost = 1,
      )
  if logprint[0] == 1:
    print('Haru S1 damage is {}'.format(np.floor(tempDamage).item()))         
def HaruS2():
  return 0  
def HaruS3():
  global totalDamage
  global accumulateDamage  
  global typeResistDownAdv
  tempDamage = DamageFunction(
      location = 0,
      target = 'AOE',
      tempBoost = 'None',
      powerCoefficient = 'Super',
      extraBoost = 1,
      )
  if logprint[0] == 1:
    print('Haru S3 damage is {}'.format(np.floor(tempDamage).item()))   
def HaruSA(combo=0):  
  global powerBoostAdv
  powerBoostAdv=np.maximum([1.2, 1.2, 1.2, 1.2], powerBoostAdv)

########    
# Bell #
########
def BellS1():
  global totalDamage
  global accumulateDamage  
  global typeResistDownAdv
  tempDamage = DamageFunction(
      location = 1,
      target = 'AOE',
      tempBoost = 'None',
      powerCoefficient = 'Mid',
      extraBoost = 1,
      )
  if logprint[1] == 1:
    print('Bell S1 damage is {}'.format(np.floor(tempDamage).item()))         
  typeResistDownAdv=np.minimum([-0.40, -0.40, -0.40, -0.40],typeResistDownAdv)
  BellChase()
  chaseCount[1] = 3   
def BellS2():
  global elementDamageBoostAdv
  global powerBoostAdv
  global totalDamage
  global accumulateDamage    
  tempDamage = DamageFunction(
      location = 1,
      target = 'AOE',
      tempBoost = 'None',
      powerCoefficient = 'High',
      extraBoost = 1,
      )
  if logprint[1] == 1:
    print('Bell S2 damage is {}'.format(np.floor(tempDamage).item()))     
  elementDamageBoostAdv=np.maximum([0.0, 0.70, 0.0, 0.0], elementDamageBoostAdv)
  powerBoostAdv=np.maximum([0.0, 0.70, 0.0, 0.0], powerBoostAdv)  
  BellChase()
def BellS3():
  global totalDamage
  global accumulateDamage  
  tempDamage = DamageFunction(
      location = 1,
      target = 'Single',
      tempBoost = 'None',
      powerCoefficient = 'Super',
      extraBoost = 2.6,
      )
  if logprint[1] == 1:
    print('Bell S3 damage is {}'.format(np.floor(tempDamage).item()))  
  BellChase()  
def BellSA(Combo=1):
  global elementDamageBoostAdv
  global totalDamage  
  global accumulateDamage
  tempDamage = SADamageFunction(
    location = 1,
    target = 'AOE',
    tempBoost = 'Great',
    powerCoefficient = 'Ultra',
    extraBoost = 1.0,
    combo = Combo,
    )            
  if logprint[1] == 1:
    print('Bell SA damage is {}'.format(np.floor(tempDamage).item()))     
  elementDamageBoostAdv=np.maximum([0.0, 1.0, 1.0, 1.0], elementDamageBoostAdv)    
def BellChase():
  global chaseCount
  global totalDamage
  global accumulateDamage  
  if chaseCount[1] > 0.5:
    tempDamage = DamageFunction(
      location = 1,
      target = 'AOE',
      tempBoost = 'None',
      powerCoefficient = 'Mid',
      extraBoost = 1,
      )
    if logprint[1] == 1:
      print('Bell chase damage is {}'.format(np.floor(tempDamage).item()))
    chaseCount[1] = chaseCount[1] - 1  

########    
# Welf #
######## 
def WelfS1(): 
  global elementDamageBoostAdv
  global powerBoostAdv  
  global totalDamage 
  global accumulateDamage  
  global targetResistDownAdv
  tempDamage = DamageFunction(
      location = 2,
      target = 'Single',
      tempBoost = 'None',
      powerCoefficient = 'Mid',
      extraBoost = 1,
      )
  if logprint[2] == 1:
    print('Welf S1 damage is {}'.format(np.floor(tempDamage).item())) 
  powerBoostAdv=np.maximum([0.0, 0.0, 1.0, 0.0], powerBoostAdv);    
  targetResistDownAdv=np.minimum([-0.25, -0.0],targetResistDownAdv)  
  WelfChase()     
def WelfS2():   
  global totalDamage 
  global accumulateDamage  
  global elementDamageBoostAdv
  tempDamage = DamageFunction(
      location = 2,
      target = 'Single',
      tempBoost = 'Normal',
      powerCoefficient = 'High',
      extraBoost = 1,
      )
  if logprint[2] == 1:
    print('Welf S2 damage is {}'.format(np.floor(tempDamage).item()))
  elementDamageBoostAdv=np.maximum([0.0, 0.0, 0.6, 0.0], elementDamageBoostAdv)   
  WelfChase() 
  chaseCount[2] = 3 
def WelfS3():   
  global powerBoostAdv    
  global totalDamage 
  global accumulateDamage  
  tempDamage = DamageFunction(
      location = 2,
      target = 'Single',
      tempBoost = 'None',
      powerCoefficient = 'Super',
      extraBoost = 2.6,
      )
  if logprint[2] == 1:
    print('Welf S3 damage is {}'.format(np.floor(tempDamage).item()))
  WelfChase() 
def WelfSA(Combo=1):
  global totalDamage  
  global accumulateDamage
  global elementDamageBoostAdv
  global powerBoostAdv  
  tempDamage = SADamageFunction(
    location = 2,
    target = 'Single',
    tempBoost = 'Great',
    powerCoefficient = 'Ultra',
    extraBoost = 1,
    combo = Combo,
    )            
  if logprint[2] == 1:
    print('Welf SA damage is {}'.format(np.floor(tempDamage).item()))
  powerBoostAdv=np.maximum([0.75, 0.75, 0.75, 0.75], powerBoostAdv);  
  elementDamageBoostAdv=np.maximum([0.0, 0.75, 0.75, 0.75], elementDamageBoostAdv)    
def WelfChase():
  global chaseCount
  global totalDamage
  global accumulateDamage  
  if chaseCount[2] > 0.5:
    tempDamage = DamageFunction(
      location = 2,
      target = 'Single',
      tempBoost = 'None',
      powerCoefficient = 'Mid',
      extraBoost = 1,
      )
    if logprint[2] == 1:
      print('Welf chase damage is {}'.format(np.floor(tempDamage).item()))
    chaseCount[2] = chaseCount[2] - 1   
    
########    
# Finn #
########
def FinnS1():
  global powerBoostAdv
  global elementDamageBoostAdv
  powerBoostAdv=np.maximum([0, 0.0, 0.0, 0.65], powerBoostAdv);
  elementDamageBoostAdv=np.maximum([0, 0.0, 0.0, 0.65], elementDamageBoostAdv);  
  FinnChase() 
  chaseCount[3]=3    
def FinnS2():
  global totalDamage
  global elementResistDownAdv
  global typeResistDownAdv
  tempDamage = DamageFunction(
      location = 3,
      target = 'Single',
      tempBoost = 'None',
      powerCoefficient = 'Mid',
      extraBoost = 1
      )
  if logprint[3] == 1:
    print('Finn S3 damage is {}'.format(np.floor(tempDamage).item()))     
  elementResistDownAdv=np.minimum([0, -0.3, -0.3, -0.3],elementResistDownAdv)
  typeResistDownAdv=np.minimum([-0.0, -0.3, -0.3, -0.3],typeResistDownAdv); 
  FinnChase() 
def FinnS3():
  global totalDamage
  global elementDamageBoostAdv 
  tempDamage = DamageFunction(
      location = 3,
      target = 'Single',
      tempBoost = 'Normal',
      powerCoefficient = 'Super',
      extraBoost = 1
      )  
  if logprint[3] == 1:
    print('Finn S3 damage is {}'.format(np.floor(tempDamage).item()))
  FinnChase() 
def FinnSA(Combo=1):
  global totalDamage
  global elementResistDownAdv
  global typeResistDownAdv  
  tempDamage = SADamageFunction(
    location = 3,
    target = 'Single',
    tempBoost = 'None',
    powerCoefficient = 'Ultra',
    extraBoost = 1.9,
    combo = Combo,
    )     
  if logprint[3] == 1:
    print('Finn SA damage is {}'.format(np.floor(tempDamage).item()))
def FinnChase():
  global totalDamage
  global accumulateDamage  
  if chaseCount[3] > 0.5:  
    tempDamage = DamageFunction(
      location = 3,
      target = 'Single',
      tempBoost = 'None',
      powerCoefficient = 'Low',
      extraBoost = 1
      )
    if logprint[3] == 1:
      print('Finn chase damage is {}'.format(np.floor(tempDamage).item()))
    chaseCount[3]=chaseCount[3]-1       
    
"""   
#########    
# Aisha #
#########
def AishaS1():
  global powerBoostAdv
  global elementDamageBoostAdv  
  global totalDamage
  tempDamage = DamageFunction(
      location = 2,
      target = 'Single',
      tempBoost = 'None',
      powerCoefficient = 'Low',
      extraBoost = 1
      )
  print('Aisha S1 damage is {}'.format(np.floor(tempDamage).item()))  
  powerBoostAdv=np.maximum([0.0, 0.0, 0.7, 0.0], powerBoostAdv);  
  elementDamageBoostAdv=np.maximum([0, 0.0, 0.7, 0.0],elementDamageBoostAdv)  
def AishaS2(): 
  global totalDamage  
  tempDamage = DamageFunction(
      location = 2,
      target = 'Single',
      tempBoost = 'None',
      powerCoefficient = 'Mid',
      extraBoost = 1
      )
  print('Aisha S2 damage is {}'.format(np.floor(tempDamage).item()))
def AishaS3(): 
  global totalDamage  
  tempDamage = DamageFunction(
      location = 2,
      target = 'Single',
      tempBoost = 'Normal',
      powerCoefficient = 'Super',
      extraBoost = 2.7
      )
  print('Aisha S3 damage is {}'.format(np.floor(tempDamage).item()))
  powerBoostAdv[2]=0
def AishaSA(Combo=1):
  global totalDamage
  global targetResistDownAdv
  tempDamage = SADamageFunction(
    location = 2,
    target = 'Single',
    tempBoost = 'None',
    powerCoefficient = 'Ultra',
    extraBoost = 2.7,
    combo = Combo,
    )   
  print('Aisha SA damage is {}'.format(np.floor(tempDamage).item()))
  targetResistDownAdv=np.minimum([-0.25, -0.0],targetResistDownAdv) 

############    
# Haruhime #
############
def HaruS1(): 
  global elementDamageBoostAdv
  global powerBoostAdv 
  global currentHaruMP  
  currentHaruMP = currentHaruMP-40    
  if currentHaruMP < 0:
    print('!!!Error!!! Running out of MP')
    sys.exit()
  elementDamageBoostAdv=np.maximum([0, 0.6, 0.0, 0.0], elementDamageBoostAdv)
  powerBoostAdv=np.maximum([0.0, 0.6, 0.0, 0.0], powerBoostAdv) 
def HaruS2(): 
  global totalDamage
  global elementResistDownAdv
  global typeResistDownAdv
  global targetResistDownAdv
  global currentHaruMP  
  global accumulateDamage  
  currentHaruMP = currentHaruMP-153  
  if currentHaruMP < 0:
    print('!!!Error!!! Running out of MP')  
    sys.exit()   
  tempDamage = DamageFunction(
      location = 1,
      target = 'Single',
      tempBoost = 'None',
      powerCoefficient = 'High',
      extraBoost = 1,
      )
  print('Haru S2 damage is {}'.format(np.floor(tempDamage).item()))     
  elementResistDownAdv=np.minimum([-0.35, -0.35, 0.0, -0.0],elementResistDownAdv)
  typeResistDownAdv=np.minimum([-0.35, -0.35, -0.35, -0.35],typeResistDownAdv)  
  targetResistDownAdv=np.minimum([-0.2, 0],targetResistDownAdv)    
def HaruS3(): 
  global totalDamage
  global currentHaruMP
  global accumulateDamage
  currentHaruMP = currentHaruMP-10   
  if currentHaruMP < 0:
    print('!!!Error!!! Running out of MP')  
    sys.exit()   
  tempDamage = DamageFunction(
      location = 1,
      target = 'Single',
      tempBoost = 'None',
      powerCoefficient = 'Mid',
      extraBoost = (1.23-0.23*currentHaruMP/maxHaruMP),
      )
  print('Haru S3 damage is {}'.format(np.floor(tempDamage).item()))    
  currentHaruMP = maxHaruMP 
def HaruSA(Combo=1):
  global totalDamage  
  global accumulateDamage
  tempDamage = SADamageFunction(
    location = 1,
    target = 'Single',
    tempBoost = 'None',
    powerCoefficient = 'Ultra',
    extraBoost = 2.6-0.4*missBoost[1],
    combo = Combo,
    )            
  print('Haru SA damage is {}'.format(np.floor(tempDamage).item()))

########    
# Lena #
######## 
def LenaChase(): 
  global chaseCount
  global totalDamage
  global accumulateDamage  
  if chaseCount[2] > 0.5:
    tempDamage = DamageFunction(
      location = 2,
      target = 'Single',
      tempBoost = 'None',
      powerCoefficient = 'Low',
      extraBoost = 1,
      )
    print('Lena chase damage is {}'.format(np.floor(tempDamage).item()))
    chaseCount[2] = chaseCount[2] - 1   
def LenaS1(): 
  global elementDamageBoostAdv
  global powerBoostAdv  
  powerBoostAdv=np.maximum([0.0, 0.0, 0.6, 0.0], powerBoostAdv);  
  elementDamageBoostAdv=np.maximum([0.0, 0.0, 0.6, 0.0], elementDamageBoostAdv)  
  LenaChase()     
  chaseCount[2]=3   
def LenaS2():   
  global elementResistDownAdv
  global typeResistDownAdv
  global totalDamage 
  global accumulateDamage  
  tempDamage = DamageFunction(
      location = 2,
      target = 'Single',
      tempBoost = 'None',
      powerCoefficient = 'High',
      extraBoost = 1,
      )
  print('Lena S2 damage is {}'.format(np.floor(tempDamage).item()))     
  typeResistDownAdv=np.minimum([-0.35, -0.35, -0.35, -0.35],typeResistDownAdv)   
  elementResistDownAdv=np.minimum([-0.00, -0.00, -0.35, -0.00],elementResistDownAdv) 
  LenaChase()        
def LenaS3():   
  global powerBoostAdv    
  global totalDamage 
  global accumulateDamage  
  tempDamage = DamageFunction(
      location = 2,
      target = 'Single',
      tempBoost = 'None',
      powerCoefficient = 'Super',
      extraBoost = 2.6,
      )
  print('Lena S3 damage is {}'.format(np.floor(tempDamage).item()))    
  powerBoostAdv[2]=0
  LenaChase()  
def LenaSA(Combo=1):
  global elementResistDownAdv  
  global totalDamage  
  global accumulateDamage
  global elementDamageBoostAdv
  global powerBoostAdv  
  tempDamage = SADamageFunction(
    location = 2,
    target = 'Single',
    tempBoost = 'None',
    powerCoefficient = 'Ultra',
    extraBoost = 2.6,
    combo = Combo,
    )            
  print('Lena SA damage is {}'.format(np.floor(tempDamage).item()))
  elementResistDownAdv=np.minimum([-0.00, -0.00, -0.50, -0.00],elementResistDownAdv)     

##########    
# Hestia #
##########
def HestiaS1():
  global elementDamageBoostAdv  
  elementDamageBoostAdv=np.maximum([0, 0.0, 0.0, 1.0],elementDamageBoostAdv) 
  HestiaChase()
  chaseCount[3]=3     
def HestiaS2(): 
  global totalDamage  
  global typeResistDownAdv
  global powerBoostAdv
  tempDamage = DamageFunction(
      location = 3,
      target = 'Single',
      tempBoost = 'Normal',
      powerCoefficient = 'Mid',
      extraBoost = 1
      )
  print('Hestia S2 damage is {}'.format(np.floor(tempDamage).item()))
  typeResistDownAdv=np.minimum([-0.35, -0.35, -0.35, -0.35],typeResistDownAdv);   
  powerBoostAdv=np.maximum([0.0, 0.0, 0.0, 0.5], powerBoostAdv);
  HestiaChase()    
def HestiaS3(): 
  global totalDamage  
  tempDamage = DamageFunction(
      location = 3,
      target = 'Single',
      tempBoost = 'None',
      powerCoefficient = 'High',
      extraBoost = 2.7
      )
  print('Hestia S3 damage is {}'.format(np.floor(tempDamage).item()))
  if magresisthalt == 1:
    magresistbreak()
  HestiaChase()      
def HestiaSA(Combo=1):
  global totalDamage
  tempDamage = SADamageFunction(
    location = 3,
    target = 'Single',
    tempBoost = 'None',
    powerCoefficient = 'Ultra',
    extraBoost = 1,
    combo = Combo,
    )   
  print('Hestia SA damage is {}'.format(np.floor(tempDamage).item()))
def HestiaChase():
  global totalDamage
  if chaseCount[3] > 0.5:  
    tempDamage = DamageFunction(
      location = 3,
      target = 'Single',
      tempBoost = 'None',
      powerCoefficient = 'Low',
      extraBoost = 1
      )
    print('Hestia chase damage is {}'.format(np.floor(tempDamage).item()))    
    chaseCount[3]=chaseCount[3]-1 

#########    
# Tiona #
#########
def TionaChase(): 
  global chaseCount
  global totalDamage
  global accumulateDamage  
  if chaseCount[2] > 0.5:
    tempDamage = DamageFunction(
      location = 2,
      target = 'Single',
      tempBoost = 'None',
      powerCoefficient = 'Low',
      extraBoost = 1,
      )
    print('Tiona chase damage is {}'.format(np.floor(tempDamage).item()))
    chaseCount[2] = chaseCount[2] - 1     
def TionaS1():
  global powerBoostAdv
  global elementDamageBoostAdv
  global chaseCount    
  powerBoostAdv=np.maximum([0, 0.0, 0.65, 0], powerBoostAdv);
  elementDamageBoostAdv=np.maximum([0, 0.0, 0.65, 0], elementDamageBoostAdv);  
  TionaChase() 
  chaseCount[2]=3      
def TionaS2():
  global bossPowerUp  
  global totalDamage 
  global accumulateDamage  
  tempDamage = DamageFunction(
      location = 2,
      target = 'Single',
      tempBoost = 'None',
      powerCoefficient = 'High',
      extraBoost = 1+bossPowerUp*1.2,
      )
  print('Tiona S2 damage is {}'.format(np.floor(tempDamage).item()))       
  bossPowerUp = 0
  TionaChase() 
def TionaS3():
  global elementResistDownAdv
  global typeResistDownAdv  
  global totalDamage 
  global accumulateDamage  
  tempDamage = DamageFunction(
      location = 2,
      target = 'Single',
      tempBoost = 'None',
      powerCoefficient = 'Super',
      extraBoost = 1,
      )
  print('Tiona S3 damage is {}'.format(np.floor(tempDamage).item()))       
  elementResistDownAdv=np.minimum([-0.0, -0.0, -0.35, -0.0],elementResistDownAdv)
  typeResistDownAdv=np.minimum([-0.35, -0.35, -0.35, -0.35],typeResistDownAdv)    
  TionaChase() 
def TionaSA(Combo=1):
  global bossPowerUp    
  global totalDamage  
  global accumulateDamage
  tempDamage = SADamageFunction(
    location = 2,
    target = 'Single',
    tempBoost = 'None',
    powerCoefficient = 'Ultra',
    extraBoost = 1.0+bossPowerUp*1.5,
    combo = Combo,
    )            
  print('Tiona SA damage is {}'.format(np.floor(tempDamage).item()))     
  bossPowerUp = 0

##########    
# Ottarl #
##########
def OttarlS1():
  global powerBoostAdv
  global elementDamageBoostAdv  
  powerBoostAdv=np.maximum([0.0, 0.75, 0, 0], powerBoostAdv);  
  elementDamageBoostAdv=np.maximum([0, 0.75, 0, 0.0],elementDamageBoostAdv)  
  OttarlChase()
  chaseCount[1]=3    
def OttarlS2(): 
  global totalDamage  
  global elementResistDownAdv
  global typeResistDownAdv
  tempDamage = DamageFunction(
      location = 1,
      target = 'Single',
      tempBoost = 'None',
      powerCoefficient = 'High',
      extraBoost = 1
      )
  print('Ottarl S2 damage is {}'.format(np.floor(tempDamage).item()))
  elementResistDownAdv=np.minimum([-0.0, -0.35, -0.35, -0.35],elementResistDownAdv)  
  typeResistDownAdv=np.minimum([-0.0, -0.35, -0.35, -0.0],typeResistDownAdv); 
  OttarlChase()
def OttarlS3(): 
  global totalDamage  
  tempDamage = DamageFunction(
      location = 1,
      target = 'Single',
      tempBoost = 'Normal',
      powerCoefficient = 'Super',
      extraBoost = 1
      )
  print('Ottarl S3 damage is {}'.format(np.floor(tempDamage).item()))
  OttarlChase()
def OttarlSA(Combo=1):
  global totalDamage
  tempDamage = SADamageFunction(
    location = 1,
    target = 'Single',
    tempBoost = 'None',
    powerCoefficient = 'Ultra',
    extraBoost = 2.4,
    combo = Combo,
    )   
  print('Ottarl SA damage is {}'.format(np.floor(tempDamage).item()))
def OttarlChase():
  global totalDamage
  if chaseCount[1] > 0.5:  
    tempDamage = DamageFunction(
      location = 1,
      target = 'Single',
      tempBoost = 'None',
      powerCoefficient = 'Low',
      extraBoost = 1
      )
    print('Ottarl chase damage is {}'.format(np.floor(tempDamage).item()))    
    chaseCount[1]=chaseCount[1]-1 
    
#######    
# Ray #
#######  
def RayS1():
  global chaseCount  
  RayChase() 
  chaseCount[0]=3    
def RayS2():
  global totalDamage 
  global accumulateDamage  
  tempDamage = DamageFunction(
      location = 0,
      target = 'Single',
      tempBoost = 'None',
      powerCoefficient = 'High',
      extraBoost = 1,
      )
  print('Ray S2 damage is {}'.format(np.floor(tempDamage).item()))  
  RayChase()     
def RayS3():
  global powerBoostAdv
  powerBoostAdv=np.maximum([0.3, 0.0, 0.0, 0.3], powerBoostAdv)  
  RayChase()
def RaySA(combo=0):  
  global powerBoostAdv
  global elementDamageBoostAdv  
  powerBoostAdv=np.maximum([0.9, 0.9, 0.9, 0.9], powerBoostAdv)
  elementDamageBoostAdv=np.maximum([1.0, 0.0, 0.0, 0.0], elementDamageBoostAdv)  
def RayChase():
  global chaseCount
  global totalDamage
  global accumulateDamage  
  if chaseCount[0] > 0.5:
    tempDamage = DamageFunction(
      location = 0,
      target = 'Single',
      tempBoost = 'None',
      powerCoefficient = 'Low',
      extraBoost = 1,
      )
    print('Ray chase damage is {}'.format(np.floor(tempDamage).item()))
    chaseCount[0] = chaseCount[0] - 1
  
#########    
# Aisha #
#########
def AishaS1():
  global totalDamage
  global accumulateDamage  
  tempDamage = DamageFunction(
      location = 2,
      target = 'AOE',
      tempBoost = 'None',
      powerCoefficient = 'Super',
      extraBoost = 1,
      )
  print('Aisha S2 damage is {}'.format(np.floor(tempDamage).item()))         
def AishaS2():
  global elementDamageBoostAdv
  global powerBoostAdv
  global totalDamage
  global accumulateDamage    
  tempDamage = DamageFunction(
      location = 2,
      target = 'AOE',
      tempBoost = 'None',
      powerCoefficient = 'Mid',
      extraBoost = 1,
      )
  print('Aisha S2 damage is {}'.format(np.floor(tempDamage).item()))     
  elementDamageBoostAdv=np.maximum([0.4, 0.4, 0.4, 0.4], elementDamageBoostAdv)
  powerBoostAdv=np.maximum([0.35, 0.35, 0.35, 0.35], powerBoostAdv)  
def AishaS3():
  global totalDamage
  global accumulateDamage  
  tempDamage = DamageFunction(
      location = 1,
      target = 'Single',
      tempBoost = 'Normal',
      powerCoefficient = 'High',
      extraBoost = 1,
      )
  print('Aisha S3 damage is {}'.format(np.floor(tempDamage).item()))      
def AishaSA(Combo=1):
  global elementDamageBoostAdv
  global totalDamage  
  global accumulateDamage
  tempDamage = SADamageFunction(
    location = 1,
    target = 'AOE',
    tempBoost = 'Great',
    powerCoefficient = 'Ultra',
    extraBoost = 1.0,
    combo = Combo,
    )            
  print('Aisha SA damage is {}'.format(np.floor(tempDamage).item()))     
  elementDamageBoostAdv=np.maximum([1.0, 1.0, 1.0, 1.0], elementDamageBoostAdv)    
############    
# Haruhime #
############
def HaruS0():  
  global totalDamage 
  global accumulateDamage  
  tempDamage = OverwriteDamageFunction(
      location = 0,
      target = 'Single',
      tempBoost = 'None',
      powerCoefficient = 'Magic',
      extraBoost = 1,
      )
  print('Haru Normal Attack damage is {}'.format(np.floor(tempDamage).item()))    
def HaruS1():  
  global totalDamage 
  global accumulateDamage  
  tempDamage = DamageFunction(
      location = 0,
      target = 'AOE',
      tempBoost = 'None',
      powerCoefficient = 'Mid',
      extraBoost = 1,
      )
  print('Haru S1 damage is {}'.format(np.floor(tempDamage).item()))  
def HaruSA(combo=0):  
  global powerBoostAdv
  powerBoostAdv=np.maximum([1, 1, 1, 1], powerBoostAdv);

##########    
# Gareth #
##########
def GarethS1():
  global elementResistDownAdv
  global elementDamageBoostAdv
  global totalDamage
  tempDamage = DamageFunction(
      location = 1,
      target = 'Single',
      tempBoost = 'None',
      powerCoefficient = 'Mid',
      extraBoost = 1
      )
  print('Gareth S1 damage is {}'.format(np.floor(tempDamage).item()))    
  elementDamageBoostAdv=np.maximum([0, 0.9, 0, 0.0],elementDamageBoostAdv)  
  elementResistDownAdv=np.minimum([0, -0.4, -0.4, -0.4],elementResistDownAdv)  
def GarethS2(): 
  global totalDamage  
  tempDamage = DamageFunction(
      location = 1,
      target = 'Single',
      tempBoost = 'Normal',
      powerCoefficient = 'High',
      extraBoost = 1
      )
  print('Gareth S2 damage is {}'.format(np.floor(tempDamage).item()))
def GarethS3():
  global totalDamage
  tempDamage = DamageFunction(
      location = 1,
      target = 'Single',
      tempBoost = 'None',
      powerCoefficient = 'Super',
      extraBoost = 2.2
      )
  print('Gareth S3 damage is {}'.format(np.floor(tempDamage).item()))     
def GarethSA(Combo=1):
  global totalDamage
  global elementResistDownAdv  
  tempDamage = SADamageFunction(
    location = 1,
    target = 'Single',
    tempBoost = 'Normal',
    powerCoefficient = 'Ultra',
    extraBoost = 1,
    combo = Combo,
    )   
  print('Gareth SA damage is {}'.format(np.floor(tempDamage).item()))
  elementResistDownAdv=np.minimum([0, -0.6, -0.6, -0.6],elementResistDownAdv)   
  
#########    
# Tione #
#########   
def TioneS1():
  global totalDamage 
  tempDamage = DamageFunction(
      location = 2,
      target = 'AOE',
      tempBoost = 'Normal',
      powerCoefficient = 'High',
      extraBoost = 1
      )
  print('Tione S1 damage is {}'.format(np.floor(tempDamage).item()))     
def TioneS2():
  global totalDamage
  global powerBoostAdv
  global elementDamageBoostAdv
  global typeResistDownAdv
  tempDamage = DamageFunction(
      location = 2,
      target = 'AOE',
      tempBoost = 'None',
      powerCoefficient = 'Super',
      extraBoost = 1
      )
  print('Tione S2 damage is {}'.format(np.floor(tempDamage).item()))     
  powerBoostAdv=np.maximum([0, 0.0, 0.6, 0], powerBoostAdv);
  elementDamageBoostAdv=np.maximum([0, 0.0, 0.6, 0], elementDamageBoostAdv);      
  typeResistDownAdv=np.minimum([-0.0, -0.3, -0.3, -0.0],typeResistDownAdv); 
def TioneS3():
  global totalDamage
  global elementDamageBoostAdv 
  tempDamage = DamageFunction(
      location = 2,
      target = 'Single',
      tempBoost = 'None',
      powerCoefficient = 'High',
      extraBoost = 1.8
      )  
  print('Tione S3 damage is {}'.format(np.floor(tempDamage).item()))
def TioneSA(Combo=1):
  global totalDamage
  global typeResistDownAdv  
  tempDamage = SADamageFunction(
    location = 2,
    target = 'AOE',
    tempBoost = 'High',
    powerCoefficient = 'Ultra',
    extraBoost = 1,
    combo = Combo,
    )     
  print('Tione SA damage is {}'.format(np.floor(tempDamage).item()))
  typeResistDownAdv=np.minimum([-0.0, -0.6, -0.6, -0.0],typeResistDownAdv); 
##########    
# Lefiya #
##########
def LefiyaS1():
  global powerBoostAdv
  global chaseCount
  powerBoostAdv=np.maximum([0, 0.0, 0.0, 0.9], powerBoostAdv);
  LefiyaChase()
  chaseCount[3]=4  
def LefiyaS2(): 
  global targetResistDownAdv
  global elementDamageBoostAdv
  targetResistDownAdv=np.minimum([-0.2, -0.0],targetResistDownAdv)
  elementDamageBoostAdv=np.maximum([0.0, 0.0, 0.0, 0.75], elementDamageBoostAdv);   
  LefiyaChase()     
def LefiyaS3():
  global totalDamage
  tempDamage = DamageFunction(
      location = 3,
      target = 'Single',
      tempBoost = 'Normal',
      powerCoefficient = 'Super',
      extraBoost = 1.8
      )
  print('Lefiya S3 damage is {}'.format(np.floor(tempDamage).item()))     
  LefiyaChase()
def LefiyaSA(Combo=1):
  global totalDamage
  global elementResistDownAdv  
  tempDamage = SADamageFunction(
    location = 3,
    target = 'Single',
    tempBoost = 'None',
    powerCoefficient = 'Ultra',
    extraBoost = 2.6,
    combo = Combo,
    )   
  print('Lefiya SA damage is {}'.format(np.floor(tempDamage).item()))
def LefiyaChase():
  global totalDamage
  global accumulateDamage  
  if chaseCount[3] > 0.5:  
    tempDamage = DamageFunction(
      location = 3,
      target = 'Single',
      tempBoost = 'None',
      powerCoefficient = 'Low',
      extraBoost = 1
      )
    print('Lefiya chase damage is {}'.format(np.floor(tempDamage).item()))    
    chaseCount[3]=chaseCount[3]-1 
#########    
# Tione #
#########
def TionaS1():
  global elementResistDownAdv
  global chaseCount
  elementResistDownAdv=np.minimum([0, -0.0, -0.35, -0.35],elementResistDownAdv)    
  TionaChase() 
  chaseCount[2]=3  
def TionaS2():
  global totalDamage
  global powerBoostAdv
  global elementDamageBoostAdv
  tempDamage = DamageFunction(
      location = 2,
      target = 'AOE',
      tempBoost = 'None',
      powerCoefficient = 'Super',
      extraBoost = 1
      )
  print('Tiona S2 damage is {}'.format(np.floor(tempDamage).item()))    
  powerBoostAdv=np.maximum([0, 0.0, 0.6, 0], powerBoostAdv);
  elementDamageBoostAdv=np.maximum([0, 0.0, 0.6, 0], elementDamageBoostAdv);      
def TionaS3():
  global totalDamage
  global elementDamageBoostAdv 
  tempDamage = DamageFunction(
      location = 2,
      target = 'Single',
      tempBoost = 'None',
      powerCoefficient = 'High',
      extraBoost = 1.8
      )  
  print('Tiona S3 damage is {}'.format(np.floor(tempDamage).item()))    
def TionaSA(Combo=1):
  global totalDamage
  tempDamage = SADamageFunction(
    location = 2,
    target = 'AOE',
    tempBoost = 'High',
    powerCoefficient = 'Ultra',
    extraBoost = 1,
    combo = Combo,
    )     
  print('Tiona SA damage is {}'.format(np.floor(tempDamage).item()))    
def TionaChase():
  global totalDamage
  global accumulateDamage  
  if chaseCount[2] > 0.5:  
    tempDamage = DamageFunction(
      location = 2,
      target = 'AOE',
      tempBoost = 'None',
      powerCoefficient = 'Low',
      extraBoost = 1
      )
    print('Tiona chase damage is {}'.format(np.floor(tempDamage).item()))    
    chaseCount[2]=chaseCount[2]-1
    
########    
# Anya #
########  
def AnyaS1(): 
  global elementDamageBoostAdv
  global powerBoostAdv  
  powerBoostAdv=np.maximum([0.0, 0.6, 0.0, 0.0], powerBoostAdv);  
  elementDamageBoostAdv=np.maximum([0.0, 0.6, 0.0, 0.0], elementDamageBoostAdv)  
def AnyaS2(): 
  global elementResistDownAdv
  global typeResistDownAdv
  global totalDamage 
  global accumulateDamage  
  tempDamage = DamageFunction(
      location = 1,
      target = 'Single',
      tempBoost = 'None',
      powerCoefficient = 'High',
      extraBoost = 1,
      )
  print('Anya S2 damage is {}'.format(np.floor(tempDamage).item()))    
  typeResistDownAdv=np.minimum([-0.00, -0.30, -0.30, -0.30],typeResistDownAdv)   
  elementResistDownAdv=np.minimum([-0.00, -0.30, -0.00, -0.00],elementResistDownAdv)  
def AnyaS3():
  global totalDamage 
  global accumulateDamage  
  tempDamage = DamageFunction(
      location = 1,
      target = 'Single',
      tempBoost = 'None',
      powerCoefficient = 'Super',
      extraBoost = 1,
      )
  print('Anya S3 damage is {}'.format(np.floor(tempDamage).item()))          
def AnyaSA(Combo=1):
  global totalDamage  
  global accumulateDamage
  global elementDamageBoostAdv
  global powerBoostAdv  
  tempDamage = SADamageFunction(
    location = 1,
    target = 'Single',
    tempBoost = 'None',
    powerCoefficient = 'Ultra',
    extraBoost = 2.3,
    combo = Combo,
    )            
  print('Anya SA damage is {}'.format(np.floor(tempDamage).item()))    
  powerBoostAdv=np.maximum([0.0, 0.9, 0.0, 0.0], powerBoostAdv);  
  elementDamageBoostAdv=np.maximum([0.0, 0.9, 0., 0.0], elementDamageBoostAdv)   
def TioneS1():
  global totalDamage 
  tempDamage = DamageFunction(
      location = 2,
      target = 'AOE',
      tempBoost = 'Normal',
      powerCoefficient = 'High',
      extraBoost = 1
      )
  print('Tione S1 damage is {}'.format(np.floor(tempDamage).item()))     
def TioneS2():
  global totalDamage
  global powerBoostAdv
  global elementDamageBoostAdv
  global typeResistDownAdv
  tempDamage = DamageFunction(
      location = 2,
      target = 'AOE',
      tempBoost = 'None',
      powerCoefficient = 'Super',
      extraBoost = 1
      )
  print('Tione S2 damage is {}'.format(np.floor(tempDamage).item()))     
  powerBoostAdv=np.maximum([0, 0.0, 0.6, 0], powerBoostAdv);
  elementDamageBoostAdv=np.maximum([0, 0.0, 0.6, 0], elementDamageBoostAdv);      
  typeResistDownAdv=np.minimum([-0.0, -0.3, -0.3, -0.3],typeResistDownAdv); 
def TioneS3():
  global totalDamage
  global elementDamageBoostAdv 
  tempDamage = DamageFunction(
      location = 2,
      target = 'Single',
      tempBoost = 'None',
      powerCoefficient = 'High',
      extraBoost = 1.8
      )  
  print('Tione S3 damage is {}'.format(np.floor(tempDamage).item()))
def TioneSA(Combo=1):
  global totalDamage
  global typeResistDownAdv  
  tempDamage = SADamageFunction(
    location = 2,
    target = 'AOE',
    tempBoost = 'High',
    powerCoefficient = 'Ultra',
    extraBoost = 1,
    combo = Combo,
    )     
  print('Tione SA damage is {}'.format(np.floor(tempDamage).item()))
  typeResistDownAdv=np.minimum([-0.0, -0.6, -0.6, -0.6],typeResistDownAdv);   
##########    
# Ais #
##########
def Ais2S1():
  return 0
def Ais2S2():
  global totalDamage
  global targetResistDownAdv
  tempDamage = DamageFunction(
      location = 1,
      target = 'Single',
      tempBoost = 'None',
      powerCoefficient = 'High',
      extraBoost = 1.8
      )  
  print('Ais2 S2 damage is {}'.format(np.floor(tempDamage).item())))  
  return 0
def Ais2S3():
  global totalDamage
  global targetResistDownAdv
  tempDamage = DamageFunction(
      location = 1,
      target = 'AOE',
      tempBoost = 'None',
      powerCoefficient = 'Super',
      extraBoost = 2
      )  
  print('Ais2 S3 damage is {}'.format(np.floor(tempDamage).item())))
  targetResistDownAdv=np.minimum([-0.2, -0.2],targetResistDownAdv) 
def Ais2SA(Combo=1):
  global totalDamage
  global elementResistDownAdv  
  tempDamage = SADamageFunction(
    location = 1,
    target = 'AOE',
    tempBoost = 'Normal',
    powerCoefficient = 'Ultra',
    extraBoost = 1,
    combo = Combo,
    )   
  print('Ais2 SA damage is {}'.format(np.floor(tempDamage).item())))
  
##########    
# Filvis #
##########
def FilvisS1():
  global powerBoostAdv
  global elementDamageBoostAdv
  powerBoostAdv=np.maximum([0, 0.6, 0.0, 0], powerBoostAdv);
  elementDamageBoostAdv=np.maximum([0, 0.6, 0.0, 0], elementDamageBoostAdv);  
  FilvisChase() 
  chaseCount[1]=3    
def FilvisS2():
  global totalDamage
  global elementResistDownAdv
  global typeResistDownAdv
  tempDamage = DamageFunction(
      location = 1,
      target = 'AOE',
      tempBoost = 'None',
      powerCoefficient = 'High',
      extraBoost = 1
      )
  print('Filvis S2 damage is {}'.format(np.floor(tempDamage).item()))     
  elementResistDownAdv=np.minimum([0, -0.3, -0.3, -0.3],elementResistDownAdv)
  typeResistDownAdv=np.minimum([-0.3, -0.3, -0.3, -0.3],typeResistDownAdv); 
  FilvisChase() 
def FilvisS3():
  global totalDamage
  global elementDamageBoostAdv 
  tempDamage = DamageFunction(
      location = 1,
      target = 'Single',
      tempBoost = 'High',
      powerCoefficient = 'High',
      extraBoost = 1
      )  
  print('Filvis S3 damage is {}'.format(np.floor(tempDamage).item())))
  FilvisChase() 
def FilvisSA(Combo=1):
  global totalDamage
  global elementResistDownAdv
  global typeResistDownAdv  
  tempDamage = SADamageFunction(
    location = 1,
    target = 'AOE',
    tempBoost = 'High',
    powerCoefficient = 'Ultra',
    extraBoost = 1,
    combo = Combo,
    )     
  print('Filvis SA damage is {}'.format(np.floor(tempDamage).item())))
  elementResistDownAdv=np.minimum([0, -0.5, -0.5, -0.5],elementResistDownAdv)
  typeResistDownAdv=np.minimum([-0.5, -0.5, -0.0, -0.5],typeResistDownAdv); 
def FilvisChase():
  global totalDamage
  global accumulateDamage  
  if chaseCount[1] > 0.5:  
    tempDamage = DamageFunction(
      location = 1,
      target = 'AOE',
      tempBoost = 'None',
      powerCoefficient = 'Low',
      extraBoost = 1
      )
    print('Filvis chase damage is {}'.format(np.floor(tempDamage).item())))
    chaseCount[1]=chaseCount[1]-1
    
########    
# Finn #
########
def FinnS1():
  global powerBoostAdv
  global elementDamageBoostAdv
  powerBoostAdv=np.maximum([0, 0.0, 0.65, 0], powerBoostAdv);
  elementDamageBoostAdv=np.maximum([0, 0.0, 0.65, 0], elementDamageBoostAdv);  
  FinnChase() 
  chaseCount[2]=3    
def FinnS2():
  global totalDamage
  global elementResistDownAdv
  global typeResistDownAdv
  tempDamage = DamageFunction(
      location = 2,
      target = 'Single',
      tempBoost = 'None',
      powerCoefficient = 'Mid',
      extraBoost = 1
      )
  print('Finn S2 damage is {}'.format(np.floor(tempDamage).item()))     
  elementResistDownAdv=np.minimum([0, -0.3, -0.3, -0.3],elementResistDownAdv)
  typeResistDownAdv=np.minimum([-0.0, -0.0, -0.3, -0.0],typeResistDownAdv); 
  FinnChase() 
def FinnS3():
  global totalDamage
  global elementDamageBoostAdv 
  tempDamage = DamageFunction(
      location = 2,
      target = 'Single',
      tempBoost = 'Normal',
      powerCoefficient = 'Super',
      extraBoost = 1
      )  
  print('Finn S3 damage is {}'.format(np.floor(tempDamage).item())))
  FinnChase() 
def FinnSA(Combo=1):
  global totalDamage
  global elementResistDownAdv
  global typeResistDownAdv  
  tempDamage = SADamageFunction(
    location = 2,
    target = 'Single',
    tempBoost = 'None',
    powerCoefficient = 'Ultra',
    extraBoost = 2.2,
    combo = Combo,
    )     
  print('Finn SA damage is {}'.format(np.floor(tempDamage).item())))
def FinnChase():
  global totalDamage
  global accumulateDamage  
  if chaseCount[2] > 0.5:  
    tempDamage = DamageFunction(
      location = 2,
      target = 'Single',
      tempBoost = 'None',
      powerCoefficient = 'Low',
      extraBoost = 1
      )
    print('Finn chase damage is {}'.format(np.floor(tempDamage).item())))
    chaseCount[2]=chaseCount[2]-1   
    
###########    
# Riveria #
###########
def RiveriaS1():
  global elementDamageBoostAdv
  elementDamageBoostAdv=np.maximum([0, 0, 0, 1],elementDamageBoostAdv)
  RiveriaChase() 
  chaseCount[3]=3     
def RiveriaS2(): 
  global totalDamage  
  global accumulateDamage
  tempDamage = DamageFunction(
      location = 3,
      target = 'Single',
      tempBoost = 'Normal',
      powerCoefficient = 'Super',
      extraBoost = 1
      )
  print('Riveria S2 damage is {}'.format(np.floor(tempDamage).item())))  
  RiveriaChase()   
def RiveriaS3():
  global totalDamage
  global accumulateDamage  
  global powerBoostAdv
  tempDamage = DamageFunction(
      location = 3,
      target = 'Single',
      tempBoost = 'None',
      powerCoefficient = 'High',
      extraBoost = 1
      )
  print('Riveria S3 damage is {}'.format(np.floor(tempDamage).item()))     
  powerBoostAdv=np.maximum([0, 0, 0.0, 0.5],powerBoostAdv)
  RiveriaChase()   
def RiveriaSA(Combo=1):
  global totalDamage
  global accumulateDamage  
  tempDamage = SADamageFunction(
    location = 3,
    target = 'Single',
    tempBoost = 'None',
    powerCoefficient = 'Ultra',
    extraBoost = 2.4,
    combo = Combo,
    )   
  print('Riveria SA damage is {}'.format(np.floor(tempDamage).item())))
def RiveriaChase():
  global totalDamage
  global accumulateDamage  
  if chaseCount[3] > 0.5:  
    tempDamage = DamageFunction(
      location = 3,
      target = 'Single',
      tempBoost = 'None',
      powerCoefficient = 'Low',
      extraBoost = 1
      )
    print('Riveria chase damage is {}'.format(np.floor(tempDamage).item())))
    chaseCount[3]=chaseCount[3]-1      

#######    
# Ryu #
#######    
def RyuS0():
  global totalDamage
  global accumulateDamage  
  tempDamage = DamageFunction(
      location = 1,
      target = 'Single',
      tempBoost = 'None',
      powerCoefficient = 'Magic',
      extraBoost = 1,
      NoType = 1      
      )
  print('Ryu normal attack damage is {}'.format(np.floor(tempDamage).item())))
def RyuS1():
  global totalDamage
  global elementDamageBoostAdv
  global powerBoostAdv
  global targetResistDownAdv
  global accumulateDamage  
  tempDamage = DamageFunction(
      location = 1,
      target = 'Single',
      tempBoost = 'None',
      powerCoefficient = 'Mid',
      extraBoost = 1
      )
  print('Ryu S1 damage is {}'.format(np.floor(tempDamage).item())))  
  elementDamageBoostAdv=np.maximum([0.0, 0.6, 0.0, 0.0], elementDamageBoostAdv)
  powerBoostAdv=np.maximum([0.0, 0.6, 0.0, 0.0], powerBoostAdv)
  targetResistDownAdv=np.minimum([-0.2, 0],targetResistDownAdv)   
def RyuS2():
  global totalDamage  
  global accumulateDamage  
  tempDamage = DamageFunction(
      location = 1,
      target = 'Single',
      tempBoost = 'Normal',
      powerCoefficient = 'Super',
      extraBoost = 1
      )
  print('Ryu S2 damage is {}'.format(np.floor(tempDamage).item())))
def RyuS3():
  global totalDamage  
  global accumulateDamage  
  tempDamage = DamageFunction(
      location = 1,
      target = 'Single',
      tempBoost = 'None',
      powerCoefficient = 'High',
      extraBoost = 2.7
      )
  print('Ryu S3 damage is {}'.format(np.floor(tempDamage).item())))
def RyuSA(Combo=1): 
  global totalDamage
  global accumulateDamage  
  global targetResistDownAdv  
  tempDamage = SADamageFunction(
    location = 1,
    target = 'Single',
    tempBoost = 'None',
    powerCoefficient = 'Ultra',
    extraBoost = 1,
    combo = Combo,
    )   
  print('Ryu SA damage is {}'.format(np.floor(tempDamage).item())))
  targetResistDownAdv=np.minimum([-0.25, -0.25],targetResistDownAdv)  
  
##########    
# Filvis #
##########
def FilvisS1():
  global powerBoostAdv
  global elementDamageBoostAdv
  powerBoostAdv=np.maximum([0, 0.0, 0.6, 0], powerBoostAdv);
  elementDamageBoostAdv=np.maximum([0, 0.0, 0.6, 0], elementDamageBoostAdv);  
  FilvisChase() 
  chaseCount[2]=3    
def FilvisS2():
  global totalDamage
  global elementResistDownAdv
  global typeResistDownAdv
  tempDamage = DamageFunction(
      location = 2,
      target = 'AOE',
      tempBoost = 'None',
      powerCoefficient = 'High',
      extraBoost = 1
      )
  print('Filvis S2 damage is {}'.format(np.floor(tempDamage).item()))     
  elementResistDownAdv=np.minimum([0, -0.3, -0.3, -0.3],elementResistDownAdv)
  typeResistDownAdv=np.minimum([-0.3, -0.3, -0.3, -0.3],typeResistDownAdv); 
  FilvisChase() 
def FilvisS3():
  global totalDamage
  global elementDamageBoostAdv 
  tempDamage = DamageFunction(
      location = 2,
      target = 'Single',
      tempBoost = 'High',
      powerCoefficient = 'High',
      extraBoost = 1
      )  
  print('Filvis S3 damage is {}'.format(np.floor(tempDamage).item())))
  FilvisChase() 
def FilvisSA(Combo=1):
  global totalDamage
  global elementResistDownAdv
  global typeResistDownAdv  
  tempDamage = SADamageFunction(
    location = 2,
    target = 'AOE',
    tempBoost = 'High',
    powerCoefficient = 'Ultra',
    extraBoost = 1,
    combo = Combo,
    )     
  print('Filvis SA damage is {}'.format(np.floor(tempDamage).item())))
  elementResistDownAdv=np.minimum([0, -0.5, -0.5, -0.5],elementResistDownAdv)
  typeResistDownAdv=np.minimum([-0.5, -0.5, -0.5, -0.5],typeResistDownAdv); 
def FilvisChase():
  global totalDamage
  global accumulateDamage  
  if chaseCount[2] > 0.5:  
    tempDamage = DamageFunction(
      location = 2,
      target = 'AOE',
      tempBoost = 'None',
      powerCoefficient = 'Low',
      extraBoost = 1
      )
    print('Filvis chase damage is {}'.format(np.floor(tempDamage).item())))
    chaseCount[2]=chaseCount[2]-1   
############    
# Haruhime #
############
def SSHaruS1(): 
  global elementDamageBoostAdv
  global powerBoostAdv  
  powerBoostAdv=np.maximum([0.3, 0.3, 0.6, 0.0], powerBoostAdv);  
  elementDamageBoostAdv=np.maximum([0.0, 0.3, 0.6, 0.3], elementDamageBoostAdv)  
def SSHaruS2():   
  global targetResistDownAdv
  targetResistDownAdv=np.minimum([-0.20, -0.00],targetResistDownAdv)   
def SSHaruS3():   
  global powerBoostAdv    
  global totalDamage 
  global accumulateDamage  
  tempDamage = DamageFunction(
      location = 2,
      target = 'Single',
      tempBoost = 'None',
      powerCoefficient = 'Super',
      extraBoost = 1.8,
      )
  print('Haru S3 damage is {}'.format(np.floor(tempDamage).item()))    
def SSHaruSA(Combo=1):
  global totalDamage  
  global accumulateDamage
  global elementDamageBoostAdv
  tempDamage = SADamageFunction(
    location = 2,
    target = 'Single',
    tempBoost = 'None',
    powerCoefficient = 'Ultra',
    extraBoost = 2.6,
    combo = Combo,
    )            
  print('Haru SA damage is {}'.format(np.floor(tempDamage).item()))    
  elementDamageBoostAdv=np.maximum([0.0, 0.8, 0.8, 0.8], elementDamageBoostAdv)   
  
########    
# Lily #
########  
def LilyChase(): 
  global chaseCount
  global totalDamage
  global accumulateDamage  
  if chaseCount[3] > 0.5:
    tempDamage = DamageFunction(
      location = 3,
      target = 'Single',
      tempBoost = 'None',
      powerCoefficient = 'Low',
      extraBoost = 1,
      )
    print('Lily chase damage is {}'.format(np.floor(tempDamage).item())))
    chaseCount[3] = chaseCount[3] - 1     
def LilyS1(): 
  global elementResistDownAdv
  elementResistDownAdv=np.minimum([-0.00, -0.40, -0.40, -0.40],elementResistDownAdv)  
  LilyChase() 
  chaseCount[3]=3   
def LilyS2(): 
  global elementDamageBoostAdv
  global powerBoostAdv
  global totalDamage 
  global accumulateDamage  
  tempDamage = DamageFunction(
      location = 3,
      target = 'Single',
      tempBoost = 'Normal',
      powerCoefficient = 'Mid',
      extraBoost = 1,
      )
  print('Lily S2 damage is {}'.format(np.floor(tempDamage).item())))  
  powerBoostAdv=np.maximum([0.0, 0.0, 0.0, 0.6], powerBoostAdv);  
  elementDamageBoostAdv=np.maximum([0.0, 0.0, 0.0, 0.6], elementDamageBoostAdv)
  LilyChase() 
def LilyS3(): 
  global elementDamageBoostAdv
  global totalDamage 
  global accumulateDamage  
  tempDamage = DamageFunction(
      location = 3,
      target = 'Single',
      tempBoost = 'None',
      powerCoefficient = 'Super',
      extraBoost = 2.2,
      )
  print('Lily S3 damage is {}'.format(np.floor(tempDamage).item()))    
  LilyChase() 
def LilySA(Combo=1):
  global totalDamage  
  global accumulateDamage
  tempDamage = SADamageFunction(
    location = 3,
    target = 'Single',
    tempBoost = 'Normal',
    powerCoefficient = 'Ultra',
    extraBoost = 1,
    combo = Combo,
    )            
  print('Lily SA damage is {}'.format(np.floor(tempDamage).item()))    
########    
# Anya #
########  
def AnyaS1(): 
  global elementDamageBoostAdv
  global powerBoostAdv  
  powerBoostAdv=np.maximum([0.0, 0.0, 0.6, 0.0], powerBoostAdv);  
  elementDamageBoostAdv=np.maximum([0.0, 0.0, 0.6, 0.0], elementDamageBoostAdv)  
def AnyaS2(): 
  global elementResistDownAdv
  global typeResistDownAdv
  global totalDamage 
  global accumulateDamage  
  tempDamage = DamageFunction(
      location = 2,
      target = 'Single',
      tempBoost = 'None',
      powerCoefficient = 'High',
      extraBoost = 1,
      )
  print('Anya S2 damage is {}'.format(np.floor(tempDamage).item()))     
  typeResistDownAdv=np.minimum([-0.00, -0.00, -0.30, -0.30],typeResistDownAdv)   
  elementResistDownAdv=np.minimum([-0.00, -0.30, -0.30, -0.30],elementResistDownAdv)  
def AnyaS3():
  global totalDamage 
  global accumulateDamage  
  tempDamage = DamageFunction(
      location = 2,
      target = 'Super',
      tempBoost = 'None',
      powerCoefficient = 'High',
      extraBoost = 1,
      )
  print('Anya S3 damage is {}'.format(np.floor(tempDamage).item()))       
def AnyaSA(Combo=1):
  global totalDamage  
  global accumulateDamage
  global elementDamageBoostAdv
  global powerBoostAdv  
  tempDamage = SADamageFunction(
    location = 2,
    target = 'Single',
    tempBoost = 'None',
    powerCoefficient = 'Ultra',
    extraBoost = 2.3,
    combo = Combo,
    )            
  print('Anya SA damage is {}'.format(np.floor(tempDamage).item()))) 
  powerBoostAdv=np.maximum([0.0, 0.0, 0.9, 0.0], powerBoostAdv);  
  elementDamageBoostAdv=np.maximum([0.0, 0.0, 0.9, 0.0], elementDamageBoostAdv)      
 
###########    
# Riveria #
###########  
def RiveriaS1(): 
  global elementResistDownAdv
  global typeResistDownAdv  
  global totalDamage 
  global accumulateDamage  
  tempDamage = DamageFunction(
      location = 1,
      target = 'Single',
      tempBoost = 'None',
      powerCoefficient = 'Mid',
      extraBoost = 1,
      )
  print('Riveria S1 damage is {}'.format(np.floor(tempDamage).item())))  
  elementResistDownAdv=np.minimum([-0.30, -0.30, -0.30, -0.30],elementResistDownAdv)
  typeResistDownAdv=np.minimum([-0.30, -0.30, -0.30, -0.30],typeResistDownAdv)    
def RiveriaS2():  
  global elementDamageBoostAdv
  global powerBoostAdv 
  global totalDamage 
  global accumulateDamage  
  tempDamage = DamageFunction(
      location = 1,
      target = 'Single',
      tempBoost = 'None',
      powerCoefficient = 'High',
      extraBoost = 1,
      )
  print('Riveria S2 damage is {}'.format(np.floor(tempDamage).item())))  
  elementDamageBoostAdv=np.maximum([0, 0.7, 0.0, 0.0], elementDamageBoostAdv)
  powerBoostAdv=np.maximum([0.0, 0.7, 0.0, 0.0], powerBoostAdv) 
def RiveriaS3():  
  global totalDamage 
  global accumulateDamage  
  tempDamage = DamageFunction(
      location = 1,
      target = 'Single',
      tempBoost = 'Normal',
      powerCoefficient = 'Super',
      extraBoost = 1,
      )
  print('Riveria S3 damage is {}'.format(np.floor(tempDamage).item()))     
def RiveriaSA(Combo=1):
  global totalDamage  
  global accumulateDamage
  tempDamage = SADamageFunction(
    location = 1,
    target = 'Single',
    tempBoost = 'None',
    powerCoefficient = 'Ultra',
    extraBoost = 3.0-0.5*missBoost[1],
    combo = Combo,
    )            
  print('Riveria SA damage is {}'.format(np.floor(tempDamage).item()))    

#######    
# Ray #
#######  
def RayS1():
  global chaseCount  
  RayChase() 
  chaseCount[0]=3    
def RayS2():
  global totalDamage 
  global accumulateDamage  
  tempDamage = DamageFunction(
      location = 0,
      target = 'Single',
      tempBoost = 'None',
      powerCoefficient = 'High',
      extraBoost = 1,
      )
  print('Ray S2 damage is {}'.format(np.floor(tempDamage).item())))  
  RayChase()     
def RayS3():
  global powerBoostAdv
  powerBoostAdv=np.maximum([0.3, 0.3, 0.3, 0.3], powerBoostAdv)  
  RayChase()
def RaySA(combo=0):  
  global powerBoostAdv
  global elementDamageBoostAdv  
  powerBoostAdv=np.maximum([0.9, 0.9, 0.9, 0.9], powerBoostAdv)
  elementDamageBoostAdv=np.maximum([1.0, 0.0, 0.0, 0.0], elementDamageBoostAdv)  
def RayChase():
  global chaseCount
  global totalDamage
  global accumulateDamage  
  if chaseCount[0] > 0.5:
    tempDamage = DamageFunction(
      location = 0,
      target = 'Single',
      tempBoost = 'None',
      powerCoefficient = 'Low',
      extraBoost = 1,
      )
    print('Ray chase damage is {}'.format(np.floor(tempDamage).item())))
    chaseCount[0] = chaseCount[0] - 1    
###########    
# Riveria #
###########
def RiveriaS1():
  global elementDamageBoostAdv
  elementDamageBoostAdv=np.maximum([0, 1, 0, 0],elementDamageBoostAdv)
  RiveriaChase() 
  chaseCount[1]=3     
def RiveriaS2(): 
  global totalDamage  
  global accumulateDamage
  tempDamage = DamageFunction(
      location = 1,
      target = 'Single',
      tempBoost = 'Normal',
      powerCoefficient = 'Super',
      extraBoost = 1
      )
  print('Riveria S2 damage is {}'.format(np.floor(tempDamage).item())))  
  RiveriaChase()   
def RiveriaS3():
  global totalDamage
  global accumulateDamage  
  global powerBoostAdv
  tempDamage = DamageFunction(
      location = 2,
      target = 'Single',
      tempBoost = 'None',
      powerCoefficient = 'High',
      extraBoost = 1
      )
  print('Riveria S3 damage is {}'.format(np.floor(tempDamage).item()))     
  powerBoostAdv=np.maximum([0, 0.5, 0.0, 0],powerBoostAdv)
  RiveriaChase()   
def RiveriaSA(Combo=1):
  global totalDamage
  global accumulateDamage  
  tempDamage = SADamageFunction(
    location = 1,
    target = 'Single',
    tempBoost = 'None',
    powerCoefficient = 'Ultra',
    extraBoost = 2.4,
    combo = Combo,
    )   
  print('Riveria SA damage is {}'.format(np.floor(tempDamage).item())))
def RiveriaChase():
  global totalDamage
  global accumulateDamage  
  if chaseCount[1] > 0.5:  
    tempDamage = DamageFunction(
      location = 1,
      target = 'Single',
      tempBoost = 'None',
      powerCoefficient = 'Low',
      extraBoost = 1
      )
    print('Riveria chase damage is {}'.format(np.floor(tempDamage).item())))
    chaseCount[1]=chaseCount[1]-1     
#######    
# Ray #
#######  
def RayS1():
  global chaseCount  
  RayChase() 
  chaseCount[0]=3    
def RayS2():
  global totalDamage 
  global accumulateDamage  
  tempDamage = DamageFunction(
      location = 0,
      target = 'Single',
      tempBoost = 'None',
      powerCoefficient = 'High',
      extraBoost = 1,
      )
  print('Ray S2 damage is {}'.format(np.floor(tempDamage).item())))  
  RayChase()     
def RayS3():
  global powerBoostAdv
  powerBoostAdv=np.maximum([0.3, 0.3, 0.3, 0.3], powerBoostAdv)  
  RayChase()
def RaySA(combo=0):  
  global powerBoostAdv
  global elementDamageBoostAdv  
  powerBoostAdv=np.maximum([0.9, 0.9, 0.9, 0.9], powerBoostAdv)
  elementDamageBoostAdv=np.maximum([1.0, 1.0, 0.0, 0.0], elementDamageBoostAdv)  
def RayChase():
  global chaseCount
  global totalDamage
  global accumulateDamage  
  if chaseCount[0] > 0.5:
    tempDamage = DamageFunction(
      location = 0,
      target = 'Single',
      tempBoost = 'None',
      powerCoefficient = 'Low',
      extraBoost = 1,
      )
    print('Ray chase damage is {}'.format(np.floor(tempDamage).item())))
    chaseCount[0] = chaseCount[0] - 1   
########    
# Welf #
########  
def WelfS1(): 
  global elementDamageBoostAdv
  global powerBoostAdv   
  elementDamageBoostAdv=np.maximum([0.3, 0.3, 0.3, 0.3], elementDamageBoostAdv)
  powerBoostAdv=np.maximum([0.3, 0.3, 0.3, 0.3], powerBoostAdv) 
def WelfS2(): 
  global targetResistDownAdv
  global totalDamage 
  global accumulateDamage  
  tempDamage = DamageFunction(
      location = 3,
      target = 'AOE',
      tempBoost = 'None',
      powerCoefficient = 'High',
      extraBoost = 1,
      )
  print('Welf S2 damage is {}'.format(np.floor(tempDamage).item()))     
  targetResistDownAdv=np.minimum([-0.2, -0.2],targetResistDownAdv)   
def WelfS3():
  global totalDamage 
  global accumulateDamage  
  tempDamage = DamageFunction(
      location = 3,
      target = 'Single',
      tempBoost = 'Normal2',
      powerCoefficient = 'Super',
      extraBoost = 1,
      )
  print('Welf S3 damage is {}'.format(np.floor(tempDamage).item())))
def WelfSA(Combo=1):
  global totalDamage  
  global accumulateDamage
  global bossPowerUp      
  tempDamage = SADamageFunction(
    location = 3,
    target = 'Single',
    tempBoost = 'None',
    powerCoefficient = 'Ultra',
    extraBoost = 2.6-0.5*missBoost[3],
    combo = Combo,
    )            
  print('Welf SA damage is {}'.format(np.floor(tempDamage).item()))      
  bossPowerUp = 0    

############    
# Haruhime #
############
def HaruSA(combo=0):  
  global powerBoostAdv
  powerBoostAdv=np.maximum([1, 1, 1, 1], powerBoostAdv);
##########    
# Lefiya #
##########
def LefiyaS1():
  global powerBoostAdv
  global elementDamageBoostAdv
  powerBoostAdv=np.maximum([0, 0.6, 0, 0], powerBoostAdv);
  elementDamageBoostAdv=np.maximum([0, 0.6, 0, 0], elementDamageBoostAdv);  
def LefiyaS2():
  global totalDamage
  global elementResistDownAdv
  global typeResistDownAdv
  tempDamage = DamageFunction(
      location = 1,
      target = 'Single',
      tempBoost = 'None',
      powerCoefficient = 'High',
      extraBoost = 1
      )
  print('Lefiya S2 damage is {}'.format(np.floor(tempDamage).item()))     
  elementResistDownAdv=np.minimum([0, -0.3, -0.3, -0.3],elementResistDownAdv)
  typeResistDownAdv=np.minimum([-0.3, -0.3, -0.3, -0.3],typeResistDownAdv); 
def LefiyaS3():
  global totalDamage
  global elementDamageBoostAdv 
  tempDamage = DamageFunction(
      location = 1,
      target = 'Single',
      tempBoost = 'None',
      powerCoefficient = 'Super',
      extraBoost = 2.2
      )  
  print('Lefiya S3 damage is {}'.format(np.floor(tempDamage).item())))
  elementDamageBoostAdv[1]=0;
def LefiyaSA(Combo=1):
  global totalDamage
  global elementResistDownAdv
  tempDamage = SADamageFunction(
    location = 1,
    target = 'Single',
    tempBoost = 'None',
    powerCoefficient = 'Ultra',
    extraBoost = 2.4,
    combo = Combo,
    )     
  print('Lefiya SA damage is {}'.format(np.floor(tempDamage).item())))
  elementResistDownAdv=np.minimum([0, -0.5, -0.5, -0.5],elementResistDownAdv)
"""

##################    
# SA and Counter #
##################
def CombineSA(Char1,Char2,Char3,Char4):
  global totalDamage
  tempDamage = (Char1*(1.16*power[0]*(1+powerBoostAdv[0]+powerBoostAst[0]))+
                Char2*(1.16*power[1]*(1+powerBoostAdv[1]+powerBoostAst[1]))+
                Char3*(1.16*power[2]*(1+powerBoostAdv[2]+powerBoostAst[2]))+
                Char4*(1.16*power[3]*(1+powerBoostAdv[3]+powerBoostAst[3]))-
                defense)*\
                (1-typeResistDownAdv[0]-typeResistDownAst[0])*\
                (1-targetResistDownAdv[1]-targetResistDownAst[1])*\
                3.7*1.5
  print('Combine SA damage is {}'.format(np.floor(tempDamage).item()))
  totalDamage = totalDamage + np.floor(tempDamage).item()  
def Counter(notIn=[0,0,0,0]):
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
    print('Haru average single counter damage is {}'.format(np.floor(tempDamage).item()))
  tempDamage = CounterDamageFunction(
      location = 1,
      target = 'Single',
      tempBoost = 'None',
      powerCoefficient = 'Physic',
      extraBoost = 0.25*(1-notIn[1])*(counterScale)*counter1Active    
      )            
  if logprint[1] == 1 and counterprint == 1:
    print('Bell average single counter damage is {}'.format(np.floor(tempDamage).item()))
  tempDamage = CounterDamageFunction(
      location = 2,
      target = 'Single',
      tempBoost = 'None',
      powerCoefficient = 'Physic',
      extraBoost = 0.25*(1-notIn[2])*1*counter2Active             
      )
  if logprint[2] == 1 and counterprint == 1:
    print('Welf average single counter damage is {}'.format(np.floor(tempDamage).item()))
  tempDamage = CounterDamageFunction(
      location = 3,
      target = 'Single',
      tempBoost = 'None',
      powerCoefficient = 'Physic',
      extraBoost = 0.25*(1-notIn[3])*counterScale         
      )  
  if logprint[3] == 1 and counterprint == 1:
    print('Finn average single counter damage is {}'.format(np.floor(tempDamage).item()))
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
    print('Haru counter damage is {}'.format(np.floor(tempDamage).item()))
  tempDamage = CounterDamageFunction(
      location = 1,
      target = 'Single',
      tempBoost = 'None',
      powerCoefficient = 'Physic',
      extraBoost = (1-notIn[1])*(counterScale)*counter1Active        
      ) 
  if logprint[1] == 1 and counterprint == 1:
    print('Bell counter damage is {}'.format(np.floor(tempDamage).item()))
  tempDamage = CounterDamageFunction(
      location = 2,
      target = 'Single',
      tempBoost = 'None',
      powerCoefficient = 'Physic',
      extraBoost = (1-notIn[2])*1*counter2Active           
      )  
  if logprint[2] == 1 and counterprint == 1:
    print('Welf counter damage is {}'.format(np.floor(tempDamage).item()))
  tempDamage = CounterDamageFunction(
      location = 3,
      target = 'Single',
      tempBoost = 'None',
      powerCoefficient = 'Physic',
      extraBoost = (1-notIn[3])*counterScale     
      )  
  if logprint[3] == 1 and counterprint == 1:
    print('Finn counter damage is {}'.format(np.floor(tempDamage).item()))

########    
# Sacs #
########
def ArcherS1():
  global elementDamageBoostAdv
  elementDamageBoostAdv=np.maximum([0, 0.25, 0.25, 0.25], elementDamageBoostAdv);    
def LyraS1():
  global typeResistDownAdv
  typeResistDownAdv=np.minimum([-0.35, -0.35, -0.35, -0.35],typeResistDownAdv)   
def AliseS1():
  global elementResistDownAdv
  elementResistDownAdv=np.minimum([-0.40, -0.40, -0.40, -0.40],elementResistDownAdv)      
def WindRyuS3():
  global elementResistDownAdv
  elementResistDownAdv=np.minimum([-0.25, -0.0, -0.0, -0.0],elementResistDownAdv)    
def AnnakittyS1():
  global targetResistDownAdv
  targetResistDownAdv=np.minimum([-0.2, -0.2],targetResistDownAdv)    
def NazaS1():
  global targetResistDownAdv
  targetResistDownAdv=np.minimum([-0.25, -0.0],targetResistDownAdv)      
# def OttarlS2(): 
#   global typeResistDownAdv
#   typeResistDownAdv=np.minimum([0, -0.35, -0.0, -0.35],typeResistDownAdv) 
def ArdeeS2():
  global typeResistDownAdv
  typeResistDownAdv=np.minimum([-0.3, -0.3, -0.3, -0.3],typeResistDownAdv)  
def AisS1():
  global elementResistDownAdv
  elementResistDownAdv=np.minimum([-0.0, -0.0, -0.35, -0.35],elementResistDownAdv) 
def WindHaruS2(): 
  global elementResistDownAdv
  global typeResistDownAdv
  global targetResistDownAdv
  elementResistDownAdv=np.minimum([-0.0, -0.0, 0.0, 0.0],elementResistDownAdv)
  typeResistDownAdv=np.minimum([-0.35, -0.35, -0.0, -0.35],typeResistDownAdv)  
  targetResistDownAdv=np.minimum([-0.2, 0],targetResistDownAdv)      
"""  
def FinnS1():
  global elementResistDownAdv
  elementResistDownAdv=np.minimum([-0.40, -0.40, -0.0, -0.0],elementResistDownAdv)    
"""  
def PhotoSA(Combo=1):  
  global typeResistDownAdv
  global targetResistDownAdv
  typeResistDownAdv=np.minimum([-0.35, -0.35, -0.35, -0.35],elementResistDownAdv)
  targetResistDownAdv=np.minimum([-0.35, -0.35],targetResistDownAdv)
"""  
def FilvisS2():
  global elementResistDownAdv
  global typeResistDownAdv
  elementResistDownAdv=np.minimum([-0.30, -0.30, -0.30, -0.30],elementResistDownAdv)
  typeResistDownAdv=np.minimum([-0.30, -0.30, -0.30, -0.30],typeResistDownAdv)    
def FilvisS1():
  global elementResistDownAdv
  global typeResistDownAdv
  global totalDamage
  global accumulateDamage  
  tempDamage = DamageFunction(
      location = 0,
      target = 'AOE',
      tempBoost = 'None',
      powerCoefficient = 'Mid',
      extraBoost = 1,
      )
  print('Filvis S1 damage is {}'.format(np.floor(tempDamage).item()))       
  elementResistDownAdv=np.minimum([-0.25, -0.25, -0.25, -0.25],elementResistDownAdv)
  typeResistDownAdv=np.minimum([-0.25, -0.25, -0.25, -0.25],typeResistDownAdv)    
def FilvisSA(Combo=1):
  global elementResistDownAdv
  global typeResistDownAdv
  elementResistDownAdv=np.minimum([-0.00, -0.50, -0.50, -0.50],elementResistDownAdv)
  typeResistDownAdv=np.minimum([-0.50, -0.50, -0.50, -0.50],typeResistDownAdv)
"""  
def YuriS2():     
  global elementResistDownAdv  
  elementResistDownAdv=np.minimum([-0.0, -0.0, -0.0, -0.4],elementResistDownAdv)
def WieneS1():     
  global powerBoostAdv  
  powerBoostAdv=np.maximum([0.4, 0.4, 0.4, 0.4], powerBoostAdv);    
  print('Wiene S1 damage is {}'.format(np.floor(0).item()))  
def WieneS2():  
  global targetResistDownAdv
  targetResistDownAdv=np.minimum([-0.20, -0.20],targetResistDownAdv)  
  print('Wiene S2 damage is {}'.format(np.floor(0).item()))    
def WieneSA(Combo=1):  
  global targetResistDownAdv
  targetResistDownAdv=np.minimum([-0.50, -0.50],targetResistDownAdv)
  print('Wiene SA damage is {}'.format(np.floor(0).item())) 
# def HaruSA(combo=0):  
#   global powerBoostAdv
#   powerBoostAdv=np.maximum([0, 1.2, 1.2, 1.2], powerBoostAdv);  
"""  
def KotoriS3(Combo=1):  
  global targetResistDownAdv
  targetResistDownAdv=np.minimum([-0.2, -0.0],targetResistDownAdv)    
def AishaS2():
  global elementDamageBoostAdv
  global powerBoostAdv
  elementDamageBoostAdv=np.maximum([0.4, 0.0, 0.4, 0.4], elementDamageBoostAdv)
  powerBoostAdv=np.maximum([0.35, 0.0, 0.35, 0.35], powerBoostAdv)   
def AishaSA(Combo=1):
  global elementDamageBoostAdv
  elementDamageBoostAdv=np.maximum([1.0, 0.0, 1.0, 1.0], elementDamageBoostAdv)
"""   
  
  
#############
# Define RB #  
#############
# Boss
boss = 'Riveria'
# Fit Parameter
ultRatio = 1.00
#counterRate = 0.79
counterRate = 1.0
critRate = 1
penRate =1
# RB Weakness
elementResistDownBase=[-0.20, -0.50, -0.50, -0.50];
typeResistDownBase=[0.0, -0.20, -0.20, -0.20];
# Adv Stats

power=[1902,3324,3394,3313];
power=[2600,3363,3394,3274];
# power=[2600,3363,3388,3111];
# power=[2600,3363,3161,3338];
# power=[2600,3161,3388,3313];
#power=[1902,3363,3394,3274];
#power=[1902,3388,3400,3084];
#power=[3293,3297,3299,3309];
counterBoost=[0.00, 0.00, 0.60, 0.00];
critPenBoost=[0.06, 0.06, 0.06, 0.26];
#maxHaruMP = 823
counterScale = 0.80
#counterScale = 0.968
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
  elementResistDownAst=[-0.15, -0.15, -0.15, -0.15]
  targetResistDownAst=[-0.20, 0.0]
  #elementDamageBoostAst=[0.00, 0.20, 0.20, 0.20]; 
  powerBoostAst=[0.00, 0.20, 0.20, 0.20]  
  #powerBoostAst=[0.00, 0.15, 0.15, 0.15]  
  elementDamageBoostAst=[0.0, 0.00, 0.00, 0.00]; 
  typeResistDownAst=[-0.00, -0.20, -0.20, -0.20] 
  #defense = defense*0.85
def assistIn2():
  global power  
  global elementResistDownAst  
  global typeResistDownAst
  global elementDamageBoostAst
  global targetResistDownAst
  elementDamageBoostAst=[0.00, 0.20, 0.20, 0.20]; 
  #targetResistDownAst=[-0.20, 0.0]
  #elementResistDownAst=[-0.00, -0.00, -0.10, -0.10]   
  #targetResistDownAst=[-0.20, 0]    
  #elementResistDownAst=[-0.00, -0.20, -0.20, -0.20]      
  #power[0]=1893;  
  return 0   
def assistIn3():
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
  #power[0]=2518;  
  #powerBoostAst=[0.15, 0.20, 0.20, 0.15]  
  #typeResistDownAst=[-0.15, -0.15, -0.15, -0.15]
  #elementResistDownAst=[-0.00, -0.20, -0.20, -0.20]  
  powerBoostAst=[0.10, 0.20, 0.20, 0.20]  
  #elementDamageBoostAst=[0.00, 0.20, 0.20, 0.20]; 
  #powerBoostAst=[0.10, 0.15, 0.15, 0.15]    
  #elementDamageBoostAst=[0.15, 0.15, 0.15, 0.15]; 
  #elementDamageBoostAst=[0.20, 0.20, 0.0, 0.00]; 
  counter3Active = 1
  counter1Active = 1
  counter2Active = 1
  return 0 
assistInTurn = [1,2,5]  
# Sac
#sac = 'WindRyu'  
#sac = 'Ais'  
#sac = 'Aisha'
#sac = 'Line'
#sac = 'Alise'
#sac = 'Lyra'
#sac = 'Filvis'
#sac1 = 'Kotori'
sac1 = 'Line'
sac = 'Wiene'
# Skills
skill = np.array([
    [-1, -1, -1, -1,   1, 2, 1, 3,   1, 4, 2, 3,   3, 3, 3],
    [ 2,  1,  3,  3,   2, 3, 3, 3,   1, 4, 3, 3,   3, 3, 3],
    [ 1,  2,  3,  2,   1, 2, 3, 3,   2, 3, 3, 2,   3, 3, 3],    
    [ 1,  2,  3,  3,   1, 3, 3, 3,   1, 3, 3, 3,   3, 4, 4],       
    [ 0,  1,  3,  4,   0, 0, 0, 0,   0, 0, 0, 0,   0, 0, 0], 
    [ 1,  0,  0,  0,   0, 0, 0, 0,   0, 0, 0, 0,   0, 0, 0] 
    ]) # 5 rows for special ult (Photo etc.) 1279.62
#2133_2132_3323_334
#2132_3123_3323_334
#2132_3123_3233_334
""" 
skill = np.array([
    [-1, -1, -1, -1,   1, 3, 3, 3,   1, 3, 4, 3,   1, 2, 2],
    [ 2,  3,  3,  3,   3, 1, 4, 3,   3, 1, 3, 3,   3, 3, 3],
    [ 2,  1,  3,  2,   3, 1, 2, 3,   3, 2, 3, 3,   3, 3, 4],    
    [ 1,  2,  3,  1,   3, 2, 1, 3,   3, 2, 1, 3,   3, 3, 4],       
    [ 0,  2,  1,  4,   0, 0, 0, 0,   0, 0, 0, 0,   0, 0, 0], 
    [ 3,  0,  0,  0,   0, 0, 0, 0,   0, 0, 0, 0,   0, 0, 0] 
    ]) # 5 rows for special ult (Photo etc.) 1279.62
skill = np.array([
    [-1, -1, -1, -1,   1, 3, 3, 3,   1, 3, 4, 3,   1, 2, 2],
    [ 2,  3,  3,  3,   3, 1, 4, 3,   3, 1, 3, 3,   3, 3, 3],
    [ 1,  2,  3,  3,   2, 1, 3, 2,   3, 3, 2, 3,   3, 3, 4],    
    [ 1,  2,  3,  1,   3, 2, 1, 3,   3, 2, 1, 3,   3, 3, 4],       
    [ 0,  2,  1,  4,   0, 0, 0, 0,   0, 0, 0, 0,   0, 0, 0], 
    [ 3,  0,  0,  0,   0, 0, 0, 0,   0, 0, 0, 0,   0, 0, 0] 
    ]) # 5 rows for special ult (Photo etc.) 1279.62
skill = np.array([
    [-1, -1, -1, -1,   1, 3, 3, 3,   1, 3, 4, 3,   1, 2, 2],
    [ 2,  3,  3,  3,   3, 1, 4, 3,   3, 1, 3, 3,   3, 3, 3],
    [ 2,  1,  3,  2,   3, 1, 2, 3,   3, 2, 3, 3,   3, 3, 4],    
    [ 1,  2,  3,  1,   3, 2, 1, 3,   3, 2, 1, 3,   3, 3, 4],       
    [ 0,  2,  1,  4,   0, 0, 0, 0,   0, 0, 0, 0,   0, 0, 0], 
    [ 3,  0,  0,  0,   0, 0, 0, 0,   0, 0, 0, 0,   0, 0, 0] 
    ]) # 5 rows for special ult (Photo etc.) 1279.62
skill = np.array([
    [-1, -1, -1, -1,   1, 3, 3, 3,   1, 2, 4, 3,   1, 3, 2],
    [ 2,  3,  3,  3,   3, 1, 4, 3,   3, 1, 3, 3,   3, 3, 3],
    [ 2,  1,  3,  2,   3, 1, 2, 3,   3, 2, 3, 3,   2, 3, 3],    
    [ 1,  2,  3,  3,   1, 2, 3, 3,   1, 2, 3, 3,   3, 4, 4],       
    [ 0,  2,  1,  4,   0, 0, 0, 0,   0, 0, 0, 0,   0, 0, 0], 
    [ 3,  0,  0,  0,   0, 0, 0, 0,   0, 0, 0, 0,   0, 0, 0] 
    ]) # 5 rows for special ult (Photo etc.) 1279.62
skill = np.array([
    [-1, -1, -1, -1,   1, 3, 3, 3,   1, 2, 4, 3,   1, 3, 2],
    [ 2,  3,  3,  3,   3, 1, 4, 3,   3, 1, 3, 3,   3, 3, 3],
    [ 1,  2,  3,  3,   3, 1, 2, 3,   3, 2, 3, 2,   3, 3, 3],    
    [ 1,  2,  3,  3,   1, 2, 3, 3,   1, 2, 3, 3,   3, 4, 4],       
    [ 0,  2,  1,  4,   0, 0, 0, 0,   0, 0, 0, 0,   0, 0, 0], 
    [ 3,  0,  0,  0,   0, 0, 0, 0,   0, 0, 0, 0,   0, 0, 0] 
    ]) # 5 rows for special ult (Photo etc.) 1279.41
skill = np.array([
    [-1, -1, -1, -1,   1, 3, 3, 3,   1, 2, 4, 3,   1, 3, 2],
    [ 2,  3,  3,  3,   3, 1, 4, 3,   3, 1, 3, 3,   3, 3, 3],
    [ 1,  2,  3,  3,   2, 1, 3, 2,   3, 3, 2, 3,   3, 3, 4],    
    [ 1,  2,  3,  3,   1, 2, 3, 3,   1, 2, 3, 1,   3, 3, 4],       
    [ 0,  2,  1,  4,   0, 0, 0, 0,   0, 0, 0, 0,   0, 0, 0], 
    [ 3,  0,  0,  0,   0, 0, 0, 0,   0, 0, 0, 0,   0, 0, 0] 
    ]) # 5 rows for special ult (Photo etc.) 1279.62
skill = np.array([
    [-1, -1, -1, -1,   1, 3, 3, 3,   1, 2, 4, 3,   1, 3, 2],
    [ 2,  3,  3,  3,   3, 1, 4, 3,   3, 1, 3, 3,   3, 3, 3],
    [ 1,  2,  3,  3,   2, 1, 3, 2,   3, 3, 2, 3,   3, 3, 3],    
    [ 1,  2,  3,  3,   1, 2, 3, 3,   1, 2, 3, 3,   3, 4, 4],       
    [ 0,  2,  1,  4,   0, 0, 0, 0,   0, 0, 0, 0,   0, 0, 0], 
    [ 3,  0,  0,  0,   0, 0, 0, 0,   0, 0, 0, 0,   0, 0, 0] 
    ]) # 5 rows for special ult (Photo etc.) 687
skill = np.array([
    [-1, -1, -1, -1,   1, 3, 3, 3,   1, 2, 4, 3,   1, 3, 2],
    [ 2,  1,  3,  3,   3, 1, 4, 3,   3, 1, 3, 3,   3, 3, 3],
    [ 1,  2,  3,  3,   3, 1, 2, 3,   3, 2, 3, 3,   3, 3, 3],    
    [ 1,  2,  3,  1,   3, 2, 1, 3,   3, 2, 1, 3,   3, 4, 4],       
    [ 0,  2,  1,  4,   0, 0, 0, 0,   0, 0, 0, 0,   0, 0, 0], 
    [ 3,  0,  0,  0,   0, 0, 0, 0,   0, 0, 0, 0,   0, 0, 0] 
    ]) # 5 rows for special ult (Photo etc.) 687
skill = np.array([
    [-1, -1, -1, -1,   1, 3, 3, 3,   1, 2, 4, 3,   1, 3, 2],
    [ 2,  1,  3,  3,   3, 1, 4, 3,   3, 1, 3, 3,   3, 3, 3],
    [ 1,  2,  3,  3,   3, 1, 2, 3,   3, 2, 3, 3,   3, 3, 3],    
    [ 2,  1,  3,  3,   1, 2, 3, 3,   1, 2, 3, 3,   3, 4, 4],       
    [ 0,  2,  1,  4,   0, 0, 0, 0,   0, 0, 0, 0,   0, 0, 0], 
    [ 3,  0,  0,  0,   0, 0, 0, 0,   0, 0, 0, 0,   0, 0, 0] 
    ]) # 5 rows for special ult (Photo etc.) 687
skill = np.array([
    [-1, -1, -1, -1,   1, 3, 3, 3,   1, 2, 4, 3,   1, 3, 2],
    [ 2,  1,  3,  3,   3, 1, 4, 3,   3, 1, 3, 3,   3, 3, 3],
    [ 1,  2,  3,  3,   3, 1, 2, 3,   3, 2, 3, 3,   3, 3, 3],    
    [ 1,  2,  3,  1,   3, 2, 1, 3,   3, 2, 1, 3,   3, 4, 4],       
    [ 0,  2,  1,  4,   0, 0, 0, 0,   0, 0, 0, 0,   0, 0, 0], 
    [ 3,  0,  0,  0,   0, 0, 0, 0,   0, 0, 0, 0,   0, 0, 0] 
    ]) # 5 rows for special ult (Photo etc.) 687
skill = np.array([
    [-1, -1, -1, -1,   1, 3, 2, 3,   3, 2, 4, 3,   3, 3, 3],
    [ 2,  1,  3,  3,   3, 1, 4, 3,   3, 1, 3, 3,   3, 3, 3],
    [ 1,  2,  3,  3,   3, 1, 2, 3,   3, 2, 3, 3,   3, 3, 3],    
    [ 2,  1,  3,  3,   1, 2, 3, 1,   3, 3, 1, 3,   3, 4, 4],       
    [ 0,  2,  1,  4,   0, 0, 0, 0,   0, 0, 0, 0,   0, 0, 0], 
    [ 3,  0,  0,  0,   0, 0, 0, 0,   0, 0, 0, 0,   0, 0, 0] 
    ]) # 5 rows for special ult (Photo etc.) 687
skill = np.array([
    [ 3,  2,  2,  1,   3, 4, 2, 1,   3, 4, 2, 1,   3, 2, 2],
    [ 1,  2,  2,  2,   1, 3, 2, 2,   1, 4, 2, 2,   3, 4, 4],
    [-1, -1, -1,  3,   1, 2, 2, 2,   1, 3, 2, 2,   1, 3, 3],    
    [ 1,  2,  3,  3,   1, 3, 3, 3,   1, 3, 3, 3,   3, 3, 3],       
    [ 0,  1,  4,  0,   0, 0, 0, 0,   0, 0, 0, 0,   0, 0, 0], 
    [ 2,  0,  0,  0,   0, 0, 0, 0,   0, 0, 0, 0,   0, 0, 0] 
    ]) # 5 rows for special ult (Photo etc.) 835
skill = np.array([
    [ 3,  2,  2,  1,   3, 4, 2, 1,   4, 3, 2, 1,   2, 3, 2],
    [ 1,  2,  2,  2,   1, 3, 2, 2,   1, 2, 2, 3,   4, 4, 4],
    [-1, -1, -1,  2,   1, 3, 2, 2,   1, 2, 2, 2,   1, 3, 3],    
    [ 1,  2,  3,  3,   1, 3, 3, 3,   1, 3, 3, 3,   3, 3, 3],       
    [ 0,  1,  4,  0,   0, 0, 0, 0,   0, 0, 0, 0,   0, 0, 0], 
    [ 2,  0,  0,  0,   0, 0, 0, 0,   0, 0, 0, 0,   0, 0, 0] 
    ]) # 5 rows for special ult (Photo etc.) 829  
skill = np.array([
    [ 3,  2,  2,  1,   3, 2, 2, 1,   3, 4, 2, 1,   3, 2, 2],
    [ 1,  2,  2,  2,   1, 3, 2, 2,   1, 4, 2, 2,   3, 4, 4],
    [-1, -1, -1,  2,   1, 3, 2, 2,   1, 4, 2, 2,   3, 3, 3],    
    [ 1,  2,  3,  3,   1, 3, 3, 3,   1, 3, 3, 3,   3, 3, 3],       
    [ 0,  1,  4,  0,   0, 0, 0, 0,   0, 0, 0, 0,   0, 0, 0], 
    [ 2,  0,  0,  0,   0, 0, 0, 0,   0, 0, 0, 0,   0, 0, 0] 
    ]) # 5 rows for special ult (Photo etc.) 827
"""    
#############
# Main Loop #  
#############
magresisthalt = 0
currentHaruMP = maxHaruMP
totalDamageTemp = 0
for Turn in range(1,16):
  # Turn Start
  print("Turn {}:".format(int(Turn)))
  # if Turn == 13: 
  #   elementDamageBoostAdv=np.maximum([0, 1, 1, 1], elementDamageBoostAdv);    
  if Turn == -1: 
    magresisthalt = 1
  else:
    magresisthalt = 0
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
  if skill[0][Turn-1]==4: WieneSA(combo)  
  if sac == 'Wiene' and skill[4][Turn-1]==4: WieneSA(combo)   
  # if sac1 == 'Haru' and skill[4][Turn-1]==4: HaruSA(combo)   
  if skill[0][Turn-1]==4: HaruSA(combo)   
  # if skill[2][Turn-1]==4: TionaSA(combo) 
  if skill[1][Turn-1]==4: BellSA(combo) 
  if skill[2][Turn-1]==4: WelfSA(combo)   
  if skill[3][Turn-1]==4: FinnSA(combo)    
  #if skill[4][Turn-1]==4: WieneSA(combo)  
  # if skill[2][Turn-1]==4: TioneSA(combo)    
  # if skill[1][Turn-1]==4: GarethSA(combo)    
  # if skill[2][Turn-1]==4: ArgonautSA(combo)   
  # if skill[3][Turn-1]==4: LefiyaSA(combo)
  # if skill[2][Turn-1]==4: TioneSA(combo)    
  # if skill[1][Turn-1]==4: Ais2SA(combo)    
  # if skill[1][Turn-1]==4: RyuSA(combo)
  # if skill[4][Turn-1]==4: WieneSA(combo)  
  if combo > 1.5: CombineSA(int(skill[0][Turn-1]==4),
                            int(skill[1][Turn-1]==4),
                            int(skill[2][Turn-1]==4),
                            int(skill[3][Turn-1]==4))
  if boss == 'Revis':
    if Turn == 6 or Turn == 10: 
      RevisClear()  
    elif Turn == 4 or Turn == 8 or Turn == 12: 
      RevisAdd() 
  # Fast+No damage\    
  # if skill[2][Turn-1]==1: ArgonautS1()     
  if skill[0][Turn-1]==2: HaruS2()  
  # Fast 
  if skill[0][Turn-1]==1: HaruS1()  
  if skill[1][Turn-1]==2: BellS2() 
  if skill[2][Turn-1]==1: WelfS1() 
  # if skill[2][Turn-1]==2: AishaS2()      
  # if skill[1][Turn-1]==2: OttarlS2() 
  # if skill[2][Turn-1]==2: LenaS2()  
  # if skill[1][Turn-1]==2: HaruS2()  
  # if skill[3][Turn-1]==2: HestiaS2()     
  # if skill[1][Turn-1]==1: TioneS1()      
  # if skill[0][Turn-1]==1: HaruS1()     
  if boss == 'Finn':  
    if Turn == 2 or Turn == 3 or Turn == 7 or Turn == 10 or Turn == 11 or\
    Turn == 13 or Turn == 14:
        Counters(skill[:,Turn-1]==-1)   
  # No damage 
  if skill[3][Turn-1]==1: FinnS1() 
  # if skill[0][Turn-1]==1: WieneS1()  
  # if skill[0][Turn-1]==1: RayS1()   
  # if skill[0][Turn-1]==3: RayS3()   
  # if skill[2][Turn-1]==1: LenaS1()   
  # if skill[2][Turn-1]==1: TionaS1()   
  # if skill[1][Turn-1]==1: HaruS1()   
  # if skill[1][Turn-1]==1: OttarlS1()   
  # if skill[3][Turn-1]==1: HestiaS1()   
  # if skill[3][Turn-1]==1: LefiyaS1()   
  # if skill[3][Turn-2]==2: LefiyaS2()   
  # if skill[4][Turn-1]==1: WieneS1()    
  # Boss fast attack
  if boss == 'Ottarl':
    if Turn == 2 or Turn == 6 or Turn == 10:
      Counter(skill[:,Turn-1]==-1)
      Counter(skill[:,Turn-1]==-1)
      Counter(skill[:,Turn-1]==-1)   
    if Turn == 3 or Turn == 7 or Turn == 11:
      Counters(skill[:,Turn-1]==-1)  
  if boss == 'Riveria':
    if Turn == 4 or Turn == 7 or Turn == 8 or Turn == 11 or Turn == 12:
      Counters(skill[:,Turn-1]==-1)          
    elif Turn == 15:
      Counter(skill[:,Turn-1]==-1)
      Counter(skill[:,Turn-1]==-1)
  if boss == 'Revis':  
    if Turn == 4 or Turn == 5 or Turn == 6 or Turn == 7 or Turn == 8 or\
    Turn == 9 or Turn == 10 or Turn == 11 or Turn == 12:    
        Counters(skill[:,Turn-1]==-1)
    elif Turn == 13 or Turn == 14:
        Counters(skill[:,Turn-1]==-1)
        Counters(skill[:,Turn-1]==-1)                      
  # Phy Normal 
  if skill[1][Turn-1]==1: BellS1()  
  if skill[1][Turn-1]==3: BellS3() 
  if skill[3][Turn-1]==2: FinnS2() 
  if skill[2][Turn-1]==2: WelfS2() 
  if skill[2][Turn-1]==3: WelfS3() 
  if sac1 == 'Ais' and skill[5][Turn-1]==1: AisS1()     
  # if skill[1][Turn-1]==3: OttarlS3() 
  # if skill[5][Turn-1]==2: YuriS2()    
  # if skill[5][Turn-1]==1: NazaS1()    
  # if skill[0][Turn-1]==2: WieneS2()    
  # if skill[2][Turn-1]==2: TioneS2()     
  # if skill[2][Turn-1]==3: TioneS3() 
  # if skill[1][Turn-1]==1: GarethS1() 
  # if skill[1][Turn-1]==2: GarethS2() 
  # if skill[1][Turn-1]==3: GarethS3()  
  # if skill[2][Turn-1]==2: ArgonautS2() 
  # if skill[2][Turn-1]==3: ArgonautS3()    
  # if skill[4][Turn-1]==2: WieneS2()  
  # if skill[1][Turn-1]==2: Ais2S2() 
  # if skill[1][Turn-1]==3: Ais2S3()   
  # if skill[1][Turn-1]==3: KotoriS3()   
  # if skill[2][Turn-1]==2: FinnS2()    
  if sac == 'Wiene' and skill[4][Turn-1]==2: WieneS2()  
  if boss == 'Finn':  
    if Turn == 2 or Turn == 3 or Turn == 7 or Turn == 9 or Turn == 10 or\
    Turn == 11:
        Counters(skill[:,Turn-1]==-1)   
    elif Turn == 1 or Turn == 4 or Turn == 5 or Turn == 6 or Turn == 8 or\
    Turn == 12 or Turn == 13 or Turn == 14:
        Counters(skill[:,Turn-1]==-1)  
        Counters(skill[:,Turn-1]==-1)     
    elif Turn == 15:
      Counters(skill[:,Turn-1]==-1)         
      Counter(skill[:,Turn-1]==-1)    
  if boss == 'Riveria':
    if Turn == 7 or Turn == 8 or Turn == 9 or Turn == 11 or Turn == 12:
      RiveriaPowerUp()
  # Mag Normal   
  if skill[0][Turn-1]==3: HaruS3()  
  # if skill[0][Turn-1]==2: RayS2()  
  # if skill[2][Turn-1]==2: TionaS2() 
  # if skill[2][Turn-1]==3: TionaS3()  
  # if skill[1][Turn-1]==3: HaruS3() 
  # if skill[3][Turn-1]==3: LefiyaS3()
  # Boss normal attack  
  if boss == 'Riveria':
    if Turn == 4:
      RiveriaPowerUp()  
  if boss == 'Revis':  
    if Turn == 4 or Turn == 8 or Turn == 12:
        Counters(skill[:,Turn-1]==-1)   
    elif Turn == 5 or Turn == 6 or Turn == 7 or Turn == 9 or Turn == 10 or\
    Turn == 11 or Turn == 13 or Turn == 14:      
        Counters(skill[:,Turn-1]==-1)  
        Counters(skill[:,Turn-1]==-1)          
  if boss == 'Ottarl':
    if Turn == 1:
      Counter(skill[:,Turn-1]==-1)
      Counter(skill[:,Turn-1]==-1)  
    if Turn == 5 or Turn == 9:
      Counter(skill[:,Turn-1]==-1)
    if Turn == 1 or Turn == 4 or Turn == 5 or Turn == 8 or Turn == 9 or Turn == 12 or Turn == 15:  
      Counters(skill[:,Turn-1]==-1)   
    if Turn == 13 or Turn == 14:  
      Counters(skill[:,Turn-1]==-1)     
      Counters(skill[:,Turn-1]==-1)
  if boss == 'Riveria':
    if Turn == 1 or Turn == 3 or Turn == 9:
      Counters(skill[:,Turn-1]==-1)       
    elif Turn == 5 or Turn == 6 or Turn == 10 or Turn == 13:
      Counters(skill[:,Turn-1]==-1)     
      Counters(skill[:,Turn-1]==-1)    
    elif Turn == 14:
      Counters(skill[:,Turn-1]==-1)     
      Counters(skill[:,Turn-1]==-1)
      Counters(skill[:,Turn-1]==-1)
  if boss == 'Revis':
    if Turn == 15:
      Counter(skill[:,Turn-1]==-1)
      Counter(skill[:,Turn-1]==-1)        
  # Slow   
  if skill[3][Turn-1]==3: FinnS3() 
  # if skill[2][Turn-1]==1: AishaS1()    
  # if skill[2][Turn-1]==3: AishaS3()  
  # if skill[2][Turn-1]==3: LenaS3()  
  # if skill[3][Turn-1]==3: HestiaS3()
  # if skill[0][Turn-1]==3: WieneS3()              
  # if skill[0][Turn-1]==2: WieneS2()  
  # if skill[2][Turn-1]==3: FinnS3()  
  # if skill[3][Turn-1]==2: RiveriaS2()
  # if skill[1][Turn-1]==3: RyuS3()
  #if Turn == 12 or Turn == 13: magresistbreak()
  # DebugPrint()
  turnDamage = totalDamage - totalDamageTemp
  if totaldamageprint == 1:
    print('Turn {} total damage is {}'.format(Turn,np.floor(turnDamage).item()))
  totalDamageTemp = totalDamage
  ManaRegen()
  if Turn == 15:
    print('\n')
    if logprint[0] == 1: print('Wiene total damage is {}'.format(np.floor(accumulateDamage[0]).item()))
    if logprint[1] == 1: print('Bell total damage is {}'.format(np.floor(accumulateDamage[1]).item()))
    if logprint[2] == 1: print('Welf total damage is {}'.format(np.floor(accumulateDamage[2]).item()))
    if logprint[3] == 1: print('Finn total damage is {}'.format(np.floor(accumulateDamage[3]).item()))
    if totaldamageprint == 1: print('\n')
    if totaldamageprint == 1: print('Current total damage is {}'.format(np.floor(totalDamage).item()))
    if totaldamageprint == 1: print('Current total score is {}'.format(np.floor(totalDamage*8.5*2).item()))




