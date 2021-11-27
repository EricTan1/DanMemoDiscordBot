


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

def checkBuffExistsReplace(buffDebuffList:list, buffDebuff:dict):
  ''' (list, dict) -> None
    Check the buffs/debuffs in the list and replace if attribute and target is the same and 
    if the modifier is equal or greater than the one in the list

    buffDebuffList: list of buffs or debuffs
    buffDebuff: dictionary of format
                {isbuff,attribute,modifier,duration}
                Example:{"isbuff":True","attribute":"strength","modifier":-45,"duration":1}
  '''
  pop_value = -1
  #loop through the list to find the buff
  for i in range (0, len(buffDebuffList)):
    # dictionary here
    curr_dict = buffDebuffList[i]
    # if the buff exists then check modifier
    if(curr_dict.get("attribute")== buffDebuff.get("attribute") and curr_dict.get("isbuff")== buffDebuff.get("isbuff")):
      pop_value=i

  if(pop_value==-1):
    buffDebuffList.append(buffDebuff)
  else:
    curr_dict = buffDebuffList[pop_value]
    # if the modifier of the buffdebuff is equal to greater to the one on the list then pop the list and replace it
    if(curr_dict.get("isbuff")):
      if(curr_dict.get("modifier") < buffDebuff.get("modifier")):
          buffDebuffList.pop(i)
          buffDebuffList.append(buffDebuff)
    else:
      if(curr_dict.get("modifier") > buffDebuff.get("modifier")):
        buffDebuffList.pop(i)
        buffDebuffList.append(buffDebuff)
    # if its equal check duration and replace it with the longer one
    if(curr_dict.get("modifier") == buffDebuff.get("modifier")):
      if(curr_dict.get("duration") < buffDebuff.get("duration")):
        buffDebuffList.pop(i)
        buffDebuffList.append(buffDebuff)