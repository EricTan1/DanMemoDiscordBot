from commands.utils import getElements, getDamageBuffs, getStats,checkBuffExistsReplace
from commands.entities.skills import AdventurerCounter
import json

class Adventurer():
    def __str__(self) -> str:
        ret = "**{}**:\n".format(self.name)
        with open('database/terms/human_readable.json', 'r') as f:
            human_readable_dict = json.load(f)
        # return "**{}**\nElement Boost:\nadv:{}\nast:{}\nStats Boost:\nadv:{}\nast:{}".format(self.name,self.elementDamageBoostAdv,self.elementDamageBoostAst,self.statsBoostAdv,self.statsBoostAst)
        # loop through all buffs/debuffs
        for buffsdebuffs in self.boostCheckAlliesAdv:
            if(human_readable_dict.get(buffsdebuffs.get("attribute"))!= None):
                #duration
                ret+="{:.0f}% {} for {} turns\n".format(float(buffsdebuffs.get("modifier"))*100,human_readable_dict.get(buffsdebuffs.get("attribute")), buffsdebuffs.get("duration"))
            else:
                ret+="{:.0f}% {} for {} turns\n".format(float(buffsdebuffs.get("modifier"))*100,buffsdebuffs.get("attribute"), buffsdebuffs.get("duration"))
        return ret
    
    # 
    #if(self.human_readable_dict.get(temp_target)!= None):
    #            temp_target=self.human_readable_dict.get(temp_target)


    def __init__(self, 
    stats = {"hp":0,"mp":0,"strength":0, "magic":0,"agility":0,"endurance":0,"dexterity":0}, 
    counterBoost=0, 
    critPenBoost=0, 
    current_skills={"combat": [], "special":[], "additionals": []},
    current_skills_agi_mod= {"combat": [], "special":[], "additionals": []},
    turnOrder = [0]*15,
    adventurerCounter = AdventurerCounter(target="foe",extraBoost="",noType=0,type="physical",element = ""),
    adventurerAttack = AdventurerCounter(target="foe",extraBoost="",noType=0,type="physical",element = ""),
    name ="",
    isCounter=True,
    counterEffects=[]):
        ''' (self, dict, float, float) -> Adventurer
        is_physical = adv.stats.get("strength")>=adv.stats.get("magic")
    if(is_physical):
      temp_type = "physical"
    else:
      temp_type = "magic"
    temp_noType = adv.elementAttackCounter == "None"

    temp_adv_counter= AdventurerCounter(target="foe",extraBoost=1,noType=int(temp_noType),type=temp_type,element = adv.elementAttackCounter)
        '''
        self.stats = stats
        self.counterBoost = counterBoost
        self.critPenBoost= critPenBoost
        self.current_skills = current_skills
        self.current_skills_agi_mod= current_skills_agi_mod
        self.turnOrder = turnOrder
        self.adventurerCounter = adventurerCounter
        self.adventurerAttack= adventurerAttack
        # element attack
        self.elementDamageBoostAdv = {"fire":0,"water":0,"thunder":0,"earth":0,"wind":0,"light":0,"dark":0}
        self.elementDamageBoostAst = {"fire":0,"water":0,"thunder":0,"earth":0,"wind":0,"light":0,"dark":0}
        # str/mag boosts
        self.statsBoostAdv={"hp":0,"mp":0,"strength":0, "magic":0,"agility":0,"endurance":0,"dexterity":0}
        self.statsBoostAst={"hp":0,"mp":0,"strength":0, "magic":0,"agility":0,"endurance":0,"dexterity":0}
        # additionals count
        self.additionalCount=0
        # adv damage
        self.current_damage = 0
        self.isCounter=isCounter
        self.counterEffects = counterEffects
        # buffs and debuffs
        # append buffs to dict and remove once wiped
        # list of dict
        # {isbuff,Attribute,Modifier,duration}
        # each list object
        #{"isbuff":False,"attribute":"strength","modifier":-45,"duration":1}
        self.boostCheckAlliesAdv=[]
        self.boostCheckAlliesAst=[]
        self.name=name
        
    async def get_combatSkill_agi(self, index:int):
        ''' index = 1-3
        '''
        return self.current_skills_agi_mod.get("combat")[index-1]

    async def add_damage(self, damage:int):
        self.current_damage += damage


    # main loop need to check skill [1,4]
    async def get_combatSkill(self, index:int):
        ''' index = 1-3
        '''
        return self.current_skills.get("combat")[index-1]
    
    async def get_specialSkill(self):
        return self.current_skills.get("special")[0]

    async def get_additionals(self):
        return self.current_skills.get("additionals")[0]

    async def set_statsBoostAdv(self, stat:str, modifier:float):
        self.statsBoostAdv[stat.lower()] = modifier

    async def set_statsBoostAst(self, stat:str, modifier:float):
        self.statsBoostAst[stat.lower()] = modifier
    
    async def set_elementDamageBoostAdv(self, element:str, modifier:float):
        if(element.lower() in getElements()):
            self.elementDamageBoostAdv[element.lower()] = modifier
    async def set_elementDamageBoostAst(self, element:str, modifier:float):
        if(element.lower() in getElements()):
            self.elementDamageBoostAst[element.lower()] = modifier
    
    async def set_boostCheckAlliesAdv(self,isbuff:bool,attribute:str,modifier:int,duration:int):
        ''' (bool, str, int or float, int, bool, int) -> None
            target: self, allies, foes, foe
            attribute: strength, magic, st, aoe
            modifier: -10 ,+50
            duration: 1,2,3,4
            is_assist: is this an assist buff or not
            position : the active unit position in the party
        '''
        try:
            duration = int(duration)
        except:
            pass
        tempAppend = {"isbuff":isbuff,"attribute": attribute,"modifier": modifier,"duration": duration}
        await checkBuffExistsReplace(self.boostCheckAlliesAdv, tempAppend)
    
    async def set_boostCheckAlliesAst(self,isbuff:bool,attribute:str,modifier:int,duration:int):
        ''' (bool, str, int or float, int, bool, int) -> None
            target: self, allies, foes, foe
            attribute: strength, magic, st, aoe
            modifier: -10 ,+50
            duration: 1,2,3,4
            is_assist: is this an assist buff or not
            position : the active unit position in the party
        '''
        tempAppend = {"isbuff":isbuff,"attribute": attribute,"modifier": modifier,"duration": duration}
        await checkBuffExistsReplace(self.boostCheckAlliesAst, tempAppend)

    

    async def set_additionalCount(self,additionalCount:int):
        self.additionalCount = additionalCount

    async def clearBuffs(self):
        # take the list but all the buffs with True is removed (keep all  the isbuff==False)
        self.boostCheckAlliesAdv = [item for item in self.boostCheckAlliesAdv if item.get("isbuff") == False]
    async def clearDebuffs(self):
        # take the list but all the buffs with True is removed (keep all  the isbuff==False)
        self.boostCheckAlliesAdv = [item for item in self.boostCheckAlliesAdv if item.get("isbuff") == True]

    async def ExtendReduceBuffs(self, turns):
        for buffsDebuffs in self.boostCheckAlliesAdv:
            if(buffsDebuffs.get("isbuff") == True and isinstance(buffsDebuffs.get("duration"),int)):
                temp_duration= buffsDebuffs.get("duration") + turns
                buffsDebuffs["duration"] = temp_duration
        temp_expiry = [item for item in self.boostCheckAlliesAdv if isinstance(item.get("duration"),int) and item.get("duration") <= 0]
        self.boostCheckAlliesAdv = [item for item in self.boostCheckAlliesAdv if isinstance(item.get("duration"),int) and item.get("duration") > 0]
        

        for buffsDebuffs in temp_expiry:
            curr_attribute = buffsDebuffs.get("attribute")
            if buffsDebuffs.get("attribute") in getDamageBuffs():
                curr_element = curr_attribute.replace("_attack","")
                if (curr_element in getElements()):
                    self.elementDamageBoostAdv[curr_element] = 0
                else:
                    self.statsBoostAdv[curr_attribute] = 0


    async def ExtendReduceDebuffs(self, turns):
        for buffsDebuffs in self.boostCheckAlliesAdv:
            if(buffsDebuffs.get("isbuff") == False and isinstance(buffsDebuffs.get("duration"),int)):
                temp_duration= buffsDebuffs.get("duration") + turns
                buffsDebuffs["duration"] = temp_duration
        self.boostCheckAlliesAdv = [item for item in self.boostCheckAlliesAdv if isinstance(item.get("duration"),int) and item.get("duration") > 0]
    

    async def pop_boostCheckAlliesAdv(self,isbuff:bool,attribute:str):
        ''' (bool, str, int or float, int, bool, int) -> None
            target: self, allies, foes, foe
            attribute: strength, magic, st, aoe
            modifier: -10 ,+50
            duration: 1,2,3,4
            is_assist: is this an assist buff or not
            position : the active unit position in the party
        '''
        self.boostCheckAlliesAdv = [item for item in self.boostCheckAlliesAdv if not(item.get("isbuff") == isbuff and item.get("attribute") == attribute)]
        # remove from actual thing

        if attribute in getDamageBuffs():
            curr_element = attribute.replace("_attack","")
            if (curr_element in getElements()):
                self.elementDamageBoostAdv[curr_element] = 0
            else:
                self.statsBoostAdv[attribute] = 0