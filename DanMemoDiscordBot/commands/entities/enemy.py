from commands.utils import getElements, getDamageDebuffs,checkBuffExistsReplace
from commands.entities.skills import AdventurerCounter
from commands.calculatorUtil import counters,counter

import asyncio

class Enemy():
    
    def __str__(self) -> str:
        #return "elemental resist\nbase: {} adv: {} ast: {}\ntype resist\nbase: {} adv: {} ast: {}\ntarget resist\nadv: {} ast: {}".format(self.elementResistDownBase,self.elementResistDownAdv,self.elementResistDownAst,self.typeResistDownBase,self.typeResistDownAdv,self.typeResistDownAst, self.targetResistDownAdv,self.targetResistDownAst )
        return "{}".format(self.boostCheckEnemyAdv)
    def __init__(self, elementResistDownBase={"fire":0,"water":0,"thunder":0,"earth":0,"wind":0,"light":0,"dark":0,"none":0},
    typeResistDownBase={"physical":0, "magic":0}, 
    stats={"hp":0,"mp":0,"strength":0, "magic":0,"agility":0,"endurance":0,"dexerity":0}):

        self.elementResistDownBase = elementResistDownBase
        self.typeResistDownBase = typeResistDownBase
        self.stats= stats

        # elemental resist down
        self.elementResistDownAdv= {"fire":0,"water":0,"thunder":0,"earth":0,"wind":0,"light":0,"dark":0,"none":0}
        self.elementResistDownAst= {"fire":0,"water":0,"thunder":0,"earth":0,"wind":0,"light":0,"dark":0,"none":0}
        
        # physical/magical resist
        self.typeResistDownAdv={"physical":0, "magic":0}
        self.typeResistDownAst={"physical":0, "magic":0}

        # target resist down
        self.targetResistDownAdv={"st":0,"aoe":0}
        self.targetResistDownAst={"st":0,"aoe":0}

        # buffs and debuffs
        # append buffs to dict and remove once wiped
        # list of dict
        # {isbuff,Attribute,Modifier,duration}
        # each list object
        #{"isbuff":False,"attribute":"strength","modifier":-45,"duration":1}
        self.boostCheckEnemyAdv=[]
        self.boostCheckEnemyAst=[]



    async def set_elementResistDownAdv(self, element:str, modifier:float):
        if(element.lower() in getElements()):
            self.elementResistDownAdv[element.lower()] = modifier

    async def set_elementResistDownAst(self, element:str, modifier:float):
        if(element.lower() in getElements()):
            self.elementResistDownAst[element.lower()] = modifier

    async def set_typeResistDownAdv(self, type:str, modifier:float):
        self.typeResistDownAdv[type.lower()] = modifier

    async def set_typeResistDownAst(self, type:str, modifier:float):
        self.typeResistDownAst[type.lower()] = modifier


    async def set_targetResistDownAdv(self, target:str, modifier:float):
        self.targetResistDownAdv[target.lower()] = modifier


    async def set_targetResistDownAst(self, target:str, modifier:float):
        self.targetResistDownAst[target.lower()] = modifier



    async def set_boostCheckEnemyAst(self,isbuff:bool,attribute:str,modifier:int,duration:int):
        ''' (bool, str, int or float, int, bool) -> None
            target: self, allies, foes, foe
            attribute: strength, magic, st, aoe
            modifier: -10 ,+50
            duration: 1,2,3,4
            is_assist: is this an assist buff or not
        '''
        tempAppend = {"isbuff":isbuff,"attribute": attribute,"modifier": modifier,"duration": duration}
        await checkBuffExistsReplace(self.boostCheckEnemyAst, tempAppend)
    async def set_boostCheckEnemyAdv(self,isbuff:bool,attribute:str,modifier:int,duration:int):
        ''' (bool, str, int or float, int, bool) -> None
            target: self, allies, foes, foe
            attribute: strength, magic, st, aoe
            modifier: -10 ,+50
            duration: 1,2,3,4
            is_assist: is this an assist buff or not
        '''
        try:
            duration = int(duration)
        except:
            pass
        tempAppend = {"isbuff":isbuff,"attribute": attribute,"modifier": modifier,"duration": duration}
        await checkBuffExistsReplace(self.boostCheckEnemyAdv, tempAppend)
    
    async def clearBuffs(self):
        # take the list but all the buffs with True is removed (keep all  the isbuff==False)
        self.boostCheckEnemyAdv = [item for item in self.boostCheckEnemyAdv if item.get("isbuff") == False]
    async def clearDebuffs(self):
        # take the list but all the buffs with True is removed (keep all  the isbuff==False)
        self.boostCheckEnemyAdv = [item for item in self.boostCheckEnemyAdv if item.get("isbuff") == True]

    async def turnOrder(self, turnOrder:int, adv_list:list, speed:int):
        ''' speed : 0 - fast, 1- normal, 2- slow
        '''
        pass

    async def turnOrderCounters(self, turnOrder:int, adv_list:list, memboost:dict, counterRate:float, speed:int, logs:dict):
        ''' speed : 0 - fast, 1- normal, 2- slow
        '''
        pass

    async def ExtendReduceBuffs(self, turns):
        for buffsDebuffs in self.boostCheckEnemyAdv:
            if(buffsDebuffs.get("isbuff") == True and isinstance(buffsDebuffs.get("duration"),int)):
                temp_duration= buffsDebuffs.get("duration") + turns
                buffsDebuffs["duration"] = temp_duration
        self.boostCheckEnemyAdv = [item for item in self.boostCheckEnemyAdv if isinstance(item.get("duration"),int) and item.get("duration") > 0]

    async def ExtendReduceDebuffs(self, turns):
        for buffsDebuffs in self.boostCheckEnemyAdv:
            if(buffsDebuffs.get("isbuff") == False and isinstance(buffsDebuffs.get("duration"),int)):
                temp_duration= buffsDebuffs.get("duration") + turns
                buffsDebuffs["duration"] = temp_duration
        tempExpiry = [item for item in self.boostCheckEnemyAdv if isinstance(item.get("duration"),int) and item.get("duration") <= 0]
        self.boostCheckEnemyAdv = [item for item in self.boostCheckEnemyAdv if isinstance(item.get("duration"),int) and item.get("duration") > 0]

        for buffsDebuffs in tempExpiry:
            curr_attribute = buffsDebuffs.get("attribute")
            if(curr_attribute in getDamageDebuffs()):
                curr_element = curr_attribute.replace("_resist","")
                if(curr_element in getElements()):
                    self.elementResistDownAdv[curr_element] = 0
                elif(curr_element == "physical" or curr_element == "magic"):
                    self.typeResistDownAdv[curr_element] = 0
                else:
                    if("single" in curr_attribute):
                        self.targetResistDownAdv["st"] = 0
                    else:
                        self.targetResistDownAdv["aoe"] = 0
    async def pop_boostCheckEnemyAdv(self,isbuff:bool,attribute:str):
        ''' (bool, str, int or float, int, bool, int) -> None
            target: self, allies, foes, foe
            attribute: strength, magic, st, aoe
            modifier: -10 ,+50
            duration: 1,2,3,4
            is_assist: is this an assist buff or not
            position : the active unit position in the party
        '''
        self.boostCheckEnemyAdv = [item for item in self.boostCheckEnemyAdv if item.get("isbuff") != isbuff and item.get("attribute") != attribute]

class Finn(Enemy):
    async def FinnClear(self, adv_list):
        #self
        self.elementResistDownAdv= {"fire":0,"water":0,"thunder":0,"earth":0,"wind":0,"light":0,"dark":0,"none":0}
        self.typeResistDownAdv={"physical":0, "magic":0}
        self.targetResistDownAdv={"st":0,"aoe":0}
        await self.clearBuffs()
        await self.clearDebuffs()
        # remove all buffs!
        for adv in adv_list:
            # adv
            adv.elementDamageBoostAdv = {"fire":0,"water":0,"thunder":0,"earth":0,"wind":0,"light":0,"dark":0}
            adv.statsBoostAdv = {"hp":0,"mp":0,"strength":0, "magic":0,"agility":0,"endurance":0,"dexerity":0}
            await adv.clearBuffs()
            await adv.clearDebuffs()

    # clear finn's debuffs from boostCheckEnemyAdv and your adv's buffs boostCheckAlliesAdv
    async def FinnStrMagBuff(self, adv_list, turns):
        # take the max of str/mag buffs
        for adv in adv_list:
            await adv.set_statsBoostAdv("strength", max(adv.statsBoostAdv.get("strength"),1.5))
            await adv.set_statsBoostAdv("magic", max(adv.statsBoostAdv.get("magic"),1.5))
            await adv.set_boostCheckAlliesAdv(True,"strength",150,turns)
            await adv.set_boostCheckAlliesAdv(True,"magic",150,turns)
        # str/mag buff
        await self.set_boostCheckEnemyAdv(True,"strength",150,turns)
        await self.set_boostCheckEnemyAdv(True,"magic",150,turns)

    async def FinnSelfEleBuff(self, element):
        await self.set_boostCheckEnemyAdv(True,"{}_attack".format(element),30,4)

    async def FinnFoesEleDebuff(self, adv_list, element):
        for adv in adv_list:
            await adv.set_boostCheckAlliesAdv(False,"{}_resist".format(element),-30,4)

    async def turnOrder(self, turnOrder:int, adv_list:list, speed:int):
        if(turnOrder in [2,6] and speed ==2):
            await self.FinnStrMagBuff(adv_list,3)
        if(turnOrder in [3,6,9,12] and speed ==0):
            await self.FinnSelfEleBuff(adv_list, "light")
        if(turnOrder in [10] and speed ==2):
            await self.FinnStrMagBuff(adv_list,5)
        if(turnOrder in [2,5,8,11] and speed ==0):
            await self.FinnSelfEleBuff("light")
        if(turnOrder in [3,7] and speed ==2):
            await self.FinnClear(adv_list)

    async def turnOrderCounters(self, turnOrder:int, adv_list:list, memboost:dict, counterRate:float, speed:int, logs:dict):
        ''' speed : 0 - fast, 1- normal, 2- slow
        '''
        ret = 0
        if(turnOrder+1 in [1,2,3,4,5,6,8,11,12,13,14] and speed==1):
            ret+=await counters(adv_list, self,memboost,counterRate,logs)
            ret+=await counters(adv_list, self,memboost,counterRate,logs)
        if(turnOrder+1 in [7,9,10,15] and speed == 1):
            ret+=await counters(adv_list, self,memboost,counterRate,logs)

        if(turnOrder+1 in [7,10,14] and speed == 0):
            ret+=await counters(adv_list, self,memboost,counterRate,logs)
        if(turnOrder+1 in [15] and speed==1):
            ret+=await counter(adv_list, self,memboost,counterRate,logs)
        return ret


class Riveria(Enemy):
    async def RiveriaPowerUp(self):
        await self.set_boostCheckEnemyAdv(True,"magic",30,4)

    # debuff remove from list boostCheckEnemyAdv
    async def RiveriaClear(self, adv_list):
        # remove all buffs!
        for adv in adv_list:
            adv.elementDamageBoostAdv = {"fire":0,"water":0,"thunder":0,"earth":0,"wind":0,"light":0,"dark":0}
            adv.statsBoostAdv = {"hp":0,"mp":0,"strength":0, "magic":0,"agility":0,"endurance":0,"dexerity":0}
            await adv.clearBuffs()

    async def RiveriaDebuff(self, adv_list, element):
        for adv in adv_list:
            await adv.set_boostCheckAlliesAdv(False,"{}_resist".format(element),-30,4)

    async def turnOrder(self, turnOrder:int, adv_list:list, speed:int):
        # debuff 1,2,4,5,7,8,9,10,11,12,13
        if(turnOrder in [0,1,3,4,6,7,8,9,10,11,12] and speed ==1):
            await self.RiveriaDebuff(adv_list, "light")
        if(turnOrder in [3,6,7,8,10,11] and speed ==1):
            await self.RiveriaPowerUp()
        if(turnOrder in [3,7] and speed ==2):
            await self.RiveriaClear(adv_list)
    
    async def turnOrderCounters(self, turnOrder:int, adv_list:list, memboost:dict, counterRate:float, speed:int,logs:dict):
        ''' speed : 0 - fast, 1- normal, 2- slow
        '''
        ret = 0
        if(turnOrder+1 in [1,5,6,10] and speed==1):
            ret+=await counters(adv_list, self,memboost,counterRate,logs)
            ret+=await counters(adv_list, self,memboost,counterRate,logs)
        
        if(turnOrder+1 in [14] and speed==1):
            ret+=await counters(adv_list, self,memboost,counterRate,logs)
            ret+=await counters(adv_list, self,memboost,counterRate,logs)
            ret+=await counters(adv_list, self,memboost,counterRate,logs)

        if(turnOrder+1 in [2,3,13] and speed == 1):
            ret+=await counters(adv_list, self,memboost,counterRate,logs)
        
        if(turnOrder+1 in [2,3,4,7,8,9,11,12,13] and speed == 0):
            ret+=await counters(adv_list, self,memboost,counterRate,logs)
        
        if(turnOrder+1 in [15] and speed == 1):
            ret+=await counter(adv_list, self,memboost,counterRate,logs)
            ret+=await counter(adv_list, self,memboost,counterRate,logs)
        return ret
        
class Ottarl(Enemy):
    async def OttarlClear(self, adv_list:list):
        # remove all buffs!
        for adv in adv_list:
            adv.elementDamageBoostAdv = {"fire":0,"water":0,"thunder":0,"earth":0,"wind":0,"light":0,"dark":0}
            adv.statsBoostAdv = {"hp":0,"mp":0,"strength":0, "magic":0,"agility":0,"endurance":0,"dexerity":0}
            await adv.clearBuffs()
    
    async def OttarlEndDebuff(self, adv_list):
        for adv in adv_list:
            await adv.set_boostCheckAlliesAdv(False,"endurance",-30,4)

    async def turnOrder(self, turnOrder:int, adv_list:list, speed:int):
        ''' turnorder: 0-14
        '''
        # start of turn 5 and start of turn 9
        if((turnOrder==3 or turnOrder==7) and speed == 2):
            await self.OttarlClear(adv_list)
        if(turnOrder in [0,2,3,4,6,7,8,11,12,13,14] and not speed == 1):
            await self.OttarlEndDebuff(adv_list)
    
    async def turnOrderCounters(self, turnOrder:int, adv_list:list, memboost:dict, counterRate:float, speed:int,logs:dict):
        ''' speed : 0 - fast, 1- normal, 2- slow
        '''
        ret = 0
        if(turnOrder+1 in [1,3,4,5,7,8,9,11,12,15] and speed==1):
            ret+=await counters(adv_list, self,memboost,counterRate,logs)
        if(turnOrder+1 in [1] and speed==1):
            ret+=await counter(adv_list, self,memboost,counterRate,logs)
            ret+=await counter(adv_list, self,memboost,counterRate,logs)
        if(turnOrder+1 in [2,6,10] and speed==1):
            ret+=await counter(adv_list, self,memboost,counterRate,logs)
            ret+=await counter(adv_list, self,memboost,counterRate,logs)
            ret+=await counter(adv_list, self,memboost,counterRate,logs)
        if(turnOrder+1 in [5,9] and speed==1):
            ret+=await counter(adv_list, self,memboost,counterRate,logs)
        
        if(turnOrder+1 in [13,14] and speed==1):
            ret+=await counters(adv_list, self,memboost,counterRate,logs)
            ret+=await counters(adv_list, self,memboost,counterRate,logs)
        return ret
        

class Revis(Enemy):
    async def RevisBuff(self):
        await self.set_boostCheckEnemyAdv(True,"strength",0.2,4)

    async def RevisAdd(self, type, type_mod):
        # type = physical/magic

        # debuffs own physical resists, take into account later magic resist debuffs
        await self.set_typeResistDownAdv(type,min(self.typeResistDownAdv.get(type), type_mod))
        await self.set_boostCheckEnemyAdv(True,"strength",0.2,4)
        await self.set_boostCheckEnemyAdv(False,"{}_resist".format(type),type_mod,4)
    
    async def RevisInitial(self,type,type_mod):
        await self.set_typeResistDownAdv(type,min(self.typeResistDownAdv.get(type), type_mod))
        await self.set_boostCheckEnemyAdv(False,"{}_resist".format(type),type_mod,4)


    async def RevisClear(self):
        self.elementResistDownAdv= {"fire":0,"water":0,"thunder":0,"earth":0,"wind":0,"light":0,"dark":0,"none":0}
        self.typeResistDownAdv={"physical":0, "magic":0}
        self.targetResistDownAdv={"st":0,"aoe":0}
        await self.clearDebuffs()
    
    async def turnOrder(self, turnOrder:int, adv_list:list, speed:int):
        ''' turnorder: 0-14
        '''
        # turn 1
        if(turnOrder==0 and speed ==0):
            await self.RevisInitial(self.debuff_type,self.debuff_mod)
        # 6 and 10
        elif((turnOrder == 5 or turnOrder == 9) and speed ==0):
            await self.RevisClear()
        # 3,7,11 both str buff and physical debuff
        elif((turnOrder == 3 or turnOrder == 7 or turnOrder == 11) and speed ==0):
            await self.RevisAdd(self.debuff_type,self.debuff_mod)
        # end of turn 11 rebuff
        if(turnOrder == 10 and speed ==2):
            await self.RevisBuff()
    
    async def turnOrderCounters(self, turnOrder:int, adv_list:list, memboost:dict, counterRate:float, speed:int,logs:dict):
            ''' speed : 0 - fast, 1- normal, 2- slow
            '''
            ret = 0
            # double aoe
            if(turnOrder+1 in [5,6,7,9,10,11] and speed==1):
                ret+=await counters(adv_list, self,memboost,counterRate,logs)
                ret+=await counters(adv_list, self,memboost,counterRate,logs)
            
            # ailment aoe
            if(turnOrder+1 in [5,6,7,8,9,10,11,12,13,14] and speed==1):
                ret+=await counters(adv_list, self,memboost,counterRate,logs)

            if(turnOrder+1 in [8,12] and speed==1):
                ret+=await counters(adv_list, self,memboost,counterRate,logs)
            
            if(turnOrder+1 in [13,14] and speed==1):
                ret+=await counters(adv_list, self,memboost,counterRate,logs)
                ret+=await counters(adv_list, self,memboost,counterRate,logs)
                ret+=await counters(adv_list, self,memboost,counterRate,logs)
            if(turnOrder+1 in [15] and speed==1):
                ret+=await counter(adv_list, self,memboost,counterRate,logs)
                ret+=await counter(adv_list, self,memboost,counterRate,logs)
            return ret

    def __init__(self, elementResistDownBase={"fire":0,"water":0,"thunder":0,"earth":0,"wind":0,"light":0,"dark":0,"none":0},
    typeResistDownBase={"physical":0, "magic":0}, 
    stats={"hp":0,"mp":0,"strength":0, "magic":0,"agility":0,"endurance":0,"dexerity":0},
    debuff_type="physical",
    debuff_mod=-0.5):
        Enemy.__init__(self,elementResistDownBase,typeResistDownBase,stats)
        self.debuff_type = debuff_type
        self.debuff_mod = debuff_mod
