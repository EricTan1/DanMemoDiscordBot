import json
import os

import sys
from database.DBcontroller import DBcontroller, DatabaseEnvironment, DBConfig, EDITORS

from database.entities.Adventurer import Adventurer, AdventurerDevelopmentSkillEffects, AdventurerSkill, AdventurerSkillEffects, AdventurerDevelopment, AdventurerStats
from database.entities.BaseConstants import Element, Target, Type, Attribute, Modifier, Speed
from database.entities.Character import Character
from database.entities.Assist import AssistStats, Assist, AssistSkillEffects, AssistSkill

""" DB SETTING UP FILE json -> sql
"""


class AdventureC:
    def __init__(self, title, name, types, stars, limited, ascended, stats, skills):
        self._title = title
        self._name = name
        self._type = types
        self._stars = stars
        self._limited = limited
        self.ascended = ascended
        self.stats = stats
        self.skills = skills

class AssistC:
    def __init__(self, title, name, stars, limited, stats, skills):
        self._title = title
        self._name = name
        self._stars = stars
        self._limited = limited
        self.stats = stats
        self.skills = skills


class InsertCharacter:
    
    def __init__(self, database):
        self._db = database

    def insertAdventurer(self, adventureComplete:AdventureC):
        characterid = self.getInsertCharacterID(adventureComplete._name,
                                           False)
        typeid = self.getBaseConstants(Type(None, adventureComplete._type),False)
        adventurerid = self.getInsertAdventurerID(characterid,
                                             typeid,
                                             int(adventureComplete._limited),
                                             adventureComplete.ascended,
                                             adventureComplete._stars,
                                             None,
                                             None,
                                             adventureComplete._title)
        # stats
        stat_list = {"hp","mp","physical_attack","magic_attack","defense","strength","endurance","dexterity","agility","magic"}
        temp_list = set()
        for attributeKeys in adventureComplete.stats:
            temp_list.add(attributeKeys.lower())
            attributeid = self.getBaseConstants(Attribute(None, attributeKeys),False)
            self._db.insertData(AdventurerStats(None, adventurerid, attributeid, str(adventureComplete.stats.get(attributeKeys))))
        if(stat_list != temp_list):
            print("HEY STAT NAMED WRONG >:( FOR : "+adventureComplete._title + " " + adventureComplete._name)
            raise Exception('spam', 'eggs')
        # skills
        for skillsKeys in adventureComplete.skills:
            skillsList = adventureComplete.skills.get(skillsKeys)
            if (skillsKeys =="special"):
                adventurerskillid = self._db.insertData(AdventurerSkill(None, adventurerid, skillsList.get("name"),skillsKeys))
                self.insertAdventurerSkillEffects(adventurerskillid, skillsList.get("effects"))
            elif(skillsKeys =="combat"):
                for skills in skillsList:
                    adventurerskillid = self._db.insertData(AdventurerSkill(None, adventurerid, skills.get("name"),skillsKeys))
                    self.insertAdventurerSkillEffects(adventurerskillid, skills.get("effects"))
            elif(skillsKeys =="additionals"):
                for skills in skillsList:
                    adventurerskillid = self._db.insertData(AdventurerSkill(None, adventurerid, skills.get("name"),skillsKeys))
                    self.insertAdventurerSkillEffects(adventurerskillid, skills.get("effects"))
            # development
            else:
                for skills in skillsList:
                    adventurerdevelopmentid = self._db.insertData(AdventurerDevelopment(None, adventurerid, skills.get("name")))
                    self.insertAdventurerDevelopmentSkillEffects(adventurerdevelopmentid, skills.get("effects"))

                    #self._db.insertData(AdventurerDevelopmentSkillEffects(None, adventurerdevelopmentid, skills.get("name"), attributeid, modifierid))
            
    def insertAdventurerSkillEffects(self, adventurerskillid, skilleffectList):
        ele_list = ['light', 'wind', 'fire', 'dark', 'ice', 'water', 'earth', 'thunder']
        # AdventurerSkillEffects SET UP        
        for effects in skilleffectList:
            #Type+Element
            temp_type = effects.get("type")
            if(temp_type == None):
                temp_type = ""
            temp_element = effects.get("element")
            if(temp_element == None):
                temp_element = ""
            if(temp_type.split("_")[0] in ele_list):
                temp_split = temp_type.split("_")
                temp_element = temp_split[0]
                print(temp_type)
                if(temp_type != None and len(temp_split)==3):
                    temp_type = temp_split[1] + "_" +temp_split[2]
                #temp_index = temp_value.find("_")
                #temp_element = temp_value[0:temp_index]
                #temp_ad_ele = temp_element
                #temp_type = temp_value[temp_index+1:]
            #else:
                #temp_type = ""
                #temp_element=""
            # Element
            eleid = self.getBaseConstants(Element(None, temp_element), False)
            # Type for skills
            typeid=self.getBaseConstants(Type(None, temp_type), False)
            temp_target = effects.get("target")
            temp_attribute = effects.get("attribute")
            temp_speed = effects.get("speed")
            temp_modifier = effects.get("modifier")
            if(temp_modifier == None):
                temp_modifier = ""
            if(len(temp_modifier) > 0 and temp_modifier[len(temp_modifier)-1] == "%"):
                temp_modifier = temp_modifier[:len(temp_modifier)-1]
            targetid = self.getBaseConstants(Target(None, temp_target), False)
            attributeid = self.getBaseConstants(Attribute(None, temp_attribute), False)
            speedid = self.getBaseConstants(Speed(None, temp_speed), False)
            modifierid = self.getBaseConstants(Modifier(None, temp_modifier), True)
            # inserting effects
            self._db.insertData(AdventurerSkillEffects(None, adventurerskillid, targetid,
                 attributeid, modifierid, effects.get("duration"), typeid,eleid, speedid))

    def insertAdventurerDevelopmentSkillEffects(self, adventurerdevelopmentid, skilleffectList):
        ele_list = ['light', 'wind', 'fire', 'dark', 'ice', 'water', 'earth', 'thunder']
        # AdventurerSkillEffects SET UP        
        for effects in skilleffectList:
            #Type+Element
            temp_type = effects.get("type")
            if(temp_type == None):
                temp_type = ""
            temp_element = effects.get("element")
            if(temp_element == None):
                temp_element = ""
            if(temp_type.split("_")[0] in ele_list):
                temp_split = temp_type.split("_")
                temp_element = temp_split[0]
                print(temp_type)
                if(temp_type != None and len(temp_split)==3):
                    temp_type = temp_split[1] + "_" +temp_split[2]
                #temp_index = temp_value.find("_")
                #temp_element = temp_value[0:temp_index]
                #temp_ad_ele = temp_element
                #temp_type = temp_value[temp_index+1:]
            #else:
                #temp_type = ""
                #temp_element=""
            # Element
            eleid = self.getBaseConstants(Element(None, temp_element), False)
            # Type for skills
            typeid=self.getBaseConstants(Type(None, temp_type), False)
            temp_target = effects.get("target")
            temp_attribute = effects.get("attribute")
            temp_speed = effects.get("speed")
            temp_modifier = effects.get("modifier")
            if(temp_modifier == None):
                temp_modifier = ""
            if(len(temp_modifier) > 0 and temp_modifier[len(temp_modifier)-1] == "%"):
                temp_modifier = temp_modifier[:len(temp_modifier)-1]
            targetid = self.getBaseConstants(Target(None, temp_target), False)
            attributeid = self.getBaseConstants(Attribute(None, temp_attribute), False)
            speedid = self.getBaseConstants(Speed(None, temp_speed), False)
            modifierid = self.getBaseConstants(Modifier(None, temp_modifier), True)
            # inserting effects
            self._db.insertData(AdventurerDevelopmentSkillEffects(None, adventurerdevelopmentid, targetid,
                 attributeid, modifierid, effects.get("duration"), typeid,eleid, speedid))
    
    def insertAssist(self, assistComplete:AssistC):
        characterid = self.getInsertCharacterID(assistComplete._name,
                                           False)
        assistid = self.getInsertAssistID(characterid,
                                     int(assistComplete._limited),
                                     assistComplete._stars,
                                     None,
                                     None,
                                     assistComplete._title)
        # stats
        stat_list = {"hp","mp","physical_attack","magic_attack","defense","strength","endurance","dexterity","agility","magic"}
        temp_list = set()
        for attributeKeys in assistComplete.stats:
            temp_list.add(attributeKeys.lower())
            attributeid = self.getBaseConstants(Attribute(None, attributeKeys),False)
            self._db.insertData(AssistStats(None, assistid, attributeid, str(assistComplete.stats.get(attributeKeys))))
        if(stat_list != temp_list):
            print("HEY STAT NAMED WRONG >:( FOR : "+assistComplete._title + " " + assistComplete._name)
            raise Exception('spam', 'eggs')
        # skills
        for skills_keys in assistComplete.skills:
            for skills_list in assistComplete.skills.get(skills_keys):
                assistskillid = self._db.insertData(AssistSkill(None, assistid, skills_list.get("name"),skills_keys))
                self.insertAssistSkillEffects(assistskillid, skills_list.get("effects"))

    
    def insertAssistSkillEffects(self, assistskillid, skilleffectList):
        # assistskilleffects SET UP        
        for effects in skilleffectList:
            # Type for skills
            #typeid=self.getBaseConstants(Type(None, temp_type), False)
            temp_target = effects.get("target")
            temp_attribute = effects.get("attribute")
            temp_modifier = effects.get("modifier")
            temp_element = effects.get("element")
            temp_type = effects.get("type")
            if(temp_modifier==None):
                temp_modifier=""
            if(len(temp_modifier) > 0 and temp_modifier[len(temp_modifier)-1] == "%"):
                temp_modifier = temp_modifier[:len(temp_modifier)-1]
            targetid = self.getBaseConstants(Target(None, temp_target), False)
            attributeid = self.getBaseConstants(Attribute(None, temp_attribute), False)
            modifierid = self.getBaseConstants(Modifier(None, temp_modifier), True)
            if(temp_element == None):
                temp_element = ""
            if(temp_type == None):
                temp_type = ""

            eleid = self.getBaseConstants(Element(None, temp_element), False)
            typeid = self.getBaseConstants(Type(None, temp_type), False)

            # inserting effects
            self._db.insertData(AssistSkillEffects(None, assistskillid, targetid,
                 attributeid, modifierid, effects.get("duration"), effects.get("max_activations"),eleid,typeid))
    
    
    def getBaseConstants(self, baseConstant, isMod):
        ret = -1
        # modifier has value instead of name (b/c made more sense but now im getting punished for it lol)
        if(isMod):
            ret_list = self._db.getDataColumn(str(type(baseConstant).__name__).lower(),"value", baseConstant.value)
        else:
            ret_list = self._db.getDataColumn(str(type(baseConstant).__name__).lower(),"name", baseConstant.name)
        # check if character in, if it is then get id else insert
        if(len(ret_list) == 0):
            ret = self._db.insertData(baseConstant)
        else:
            # id is always first column
            ret = (ret_list[0])[0]
        return ret
    
    def getInsertCharacterID(self, name, iscollab):
        ret = -1
        ret_list = self._db.getDataColumn("character","name", name)
        # check if character in, if it is then get id else insert
        if(len(ret_list) == 0):
            ret = self._db.insertData(Character(None, name, iscollab))
        else:
            # id is always first column
            ret = (ret_list[0])[0]
        return ret
    
    def getInsertAdventurerID(self, characterid, typeid, limited, ascended, stars, splashuri, iconuri, title):
        ret = -1
        ret_list = self._db.getDataColumn("adventurer","title", title)
        # check if character in, if it is then get id else insert
        if(len(ret_list) == 0):
            ret = self._db.insertData(Adventurer(None, characterid, typeid,title,limited, False,
                     stars, None))
        else:
            # id is always first column
            ret = (ret_list[0])[0]
            # delete so we can insert the chara again
            if(self._db.deleteById("adventurer","adventurerid", ret)):
                ret = self._db.insertData(Adventurer(None, characterid, typeid,title,limited, False,
                     stars, None))
        return ret
    
    
    def getInsertAssistID(self, characterid,limited,stars, splashuri, iconuri, title):
        ret = -1
        ret_list = self._db.getDataColumn("assist","title", title)
        # check if character in, if it is then get id else insert
        if(len(ret_list) == 0):
            ret = self._db.insertData(Assist(None,
                                       characterid,
                                       title,
                                       limited,
                                       stars,
                                       None))
        else:
            # id is always first column
            ret = (ret_list[0])[0]
            # delete so we can insert the chara again
            if(self._db.deleteById("assist","assistid", ret)):
                ret = self._db.insertData(Assist(None,
                                       characterid,
                                       title,
                                       limited,
                                       stars,
                                       None))
        return ret

if __name__ == "__main__":
    path = "../../DB/missingad"
    db = DBcontroller(DBConfig(DatabaseEnvironment.LOCAL))
    ic = InsertCharacter(db)
    my_set = set()
    for filename in os.listdir(path):
        with open(path + '/' + filename, 'r', encoding="utf8") as f:
            if(filename != "desktop.ini"):
                print(filename)
                as_dict = json.load(f)
                if(as_dict.get("limited")== None):
                    as_dict["limited"]=False
                #temp_as = AssistC(as_dict.get("title"), as_dict.get("name"), as_dict.get("stars"), as_dict.get("limited"), as_dict.get("stats"), as_dict.get("skills"))
                #ic.insertAssist(temp_as)
                
                #(self, title, name, types, stars, limited, ascended, stats, skills)
                temp_ad = AdventureC(as_dict.get("title"), as_dict.get("name"), as_dict.get("type"),as_dict.get("stars"), as_dict.get("limited"),  True, as_dict.get("stats"), as_dict.get("skills"))
                ic.insertAdventurer(temp_ad)

async def run(dbConfig, client, ctx, *search):
    # permission checking
    if(ctx.message.author.id in EDITORS):
        db = DBcontroller(dbConfig)
        ic = InsertCharacter(db)
        # loop through all attachments and get their value
        for attach in ctx.message.attachments:
            try:
                my_json = await attach.read()
                my_json = my_json.decode('utf8')
                as_dict = json.loads(my_json)
                if(as_dict.get("limited")== None):
                    as_dict["limited"]=False
                if("assist" in search[0].lower() or "as" in search[0].lower()):
                    temp_as = AssistC(as_dict.get("title"), as_dict.get("name"), as_dict.get("stars"), as_dict.get("limited"), as_dict.get("stats"), as_dict.get("skills"))
                    ic.insertAssist(temp_as)
                elif("adventurer" in search[0].lower() or "ad" in search[0].lower()):
                    temp_ad = AdventureC(as_dict.get("title"), as_dict.get("name"), as_dict.get("type"),as_dict.get("stars"), as_dict.get("limited"),  True, as_dict.get("stats"), as_dict.get("skills"))
                    ic.insertAdventurer(temp_ad)
                await ctx.send("character(s) has been added")
            except:
                await ctx.send("Error in reading json")
        

""" async def testAd(dbConfig, client, ctx):
    db = DBcontroller(dbConfig)
    ic = InsertCharacter(db)
    for filename in os.listdir("./testJsonAdv/"):
        if filename.endswith(".json"): 
            # print(os.path.join(directory, filename))
            with open('./testJsonAdv/{}'.format(filename)) as f:
                as_dict = json.load(f)
                if(as_dict.get("limited")== None):
                    as_dict["limited"]=False
                temp_ad = AdventureC(as_dict.get("title"), as_dict.get("name"), as_dict.get("type"),as_dict.get("stars"), as_dict.get("limited"),  True, as_dict.get("stats"), as_dict.get("skills"))
                ic.insertAdventurer(temp_ad)
    await ctx.send("character(s) has been added")
async def testAs(dbConfig, client, ctx):
    db = DBcontroller(dbConfig)
    ic = InsertCharacter(db)
    for filename in os.listdir("./testJsonAs/"):
        if filename.endswith(".json"): 
            # print(os.path.join(directory, filename))
            with open('./testJsonAs/{}'.format(filename)) as f:
                as_dict = json.load(f)
                if(as_dict.get("limited")== None):
                    as_dict["limited"]=False
                temp_as = AssistC(as_dict.get("title"), as_dict.get("name"), as_dict.get("stars"), as_dict.get("limited"), as_dict.get("stats"), as_dict.get("skills"))
                ic.insertAssist(temp_as)
    await ctx.send("character(s) has been added") """