import json
import os
path = '../../database/adventurers/'
import sys
sys.path.append('../Entities/')

from DBcontroller import DBcontroller
from Adventurer import Adventurer,AdventurerSkill,AdventurerSkillEffects,AdventurerDevelopment
from BaseConstants import Element, Target, Type, Attribute,Modifier
from Character import Character, Stats

class Adventure:
    def __init__(self, title, name, types, stars, limited, ascended, stats, sa, c_skills, development):
        self._title = title
        self._name = name
        self._type = types
        self._stars = stars
        self._limited = limited
        self.ascended = ascended
        self.stats = stats
        self.sa = sa
        self.skills = c_skills
        self.development = development


db = DBcontroller("localhost","root","danmemo","3306","danmemo")
#ad_list = []
for filename in os.listdir(path):
    with open(path + '/' + filename, 'r') as f:
        ad_dict = json.load(f)
        temp_ad = Adventure(ad_dict.get("title"), ad_dict.get("name"), ad_dict.get("type"), ad_dict.get("stars"), ad_dict.get("limited"), False, ad_dict.get("stats"), ad_dict.get("skills").get("special"), ad_dict.get("skills").get("combat"), ad_dict.get("skills").get("development"))
        #Character
        if(len(db.getDataColumn("character","name",temp_ad._name))==0):
            db.insertData(Character(None, temp_ad._name,False))
        temp_ad_ele = ""
        
        # Type for adventurer
        if(len(db.getDataColumn("type","name",temp_ad._type))==0):
            db.insertData(Type(None, temp_ad._type))
            
        for skills in ad_dict.get("skills"):
            skills = ad_dict.get("skills").get(skills)
            #modifier
            temp_value = skills.get("effects").get("modifier")
            if(temp_value[len(temp_value)] == "%"):
                temp_value = temp_value[:len(temp_value)-1]
            if(len(db.getDataColumn("modifier","value",temp_value))==0):
                db.insertData(Modifier(None, temp_value))
            #Type+Element
            temp_value = skills.get("effects").get("type")
            temp_index = temp_value.find("_")
            temp_element = temp_value[0:temp_index]
            temp_ad_ele = temp_element
            temp_type = temp_value[temp_index+1:]
            print(temp_element +"-" + temp_type)
            # Element
            if(len(db.getDataColumn("element","name",temp_element))==0):
                db.insertData(Element(None, temp_element))
            # Type for skills
            if(len(db.getDataColumn("type","name",temp_type))==0):
                db.insertData(Type(None, temp_type))
            # Attribute
            temp_value = skills.get("effects").get("attribute")
            if(temp_value != None and len(db.getDataColumn("attribute","name",temp_value))==0):
                db.insertData(Attribute(None, temp_value))
            # Target
            temp_value = skills.get("effects").get("target")
            if(temp_value != None and len(db.getDataColumn("attribute","name",temp_value))==0):
                db.insertData(Attribute(None, temp_value))
        #Adventurer
        # get id's for type and character
        characterid = db.getDataColumn("character","name",temp_ad._name)[0]
        typeid = db.getDataColumn("element","name",temp_ad._type)[0]
        Adventurer(None, characterid[0], typeid[0], temp_ad._title,temp_ad._limited, False,
                 temp_ad._stars, None, None)
        adventurerid = db.getDataColumn("adventurer","title",temp_ad._title)[0]
        #Stats
        if(len(db.getDataColumn("attribute","name","hp"))==0):
            db.insertData(Attribute(None, "hp"))
        if(len(db.getDataColumn("attribute","name","mp"))==0):
            db.insertData(Attribute(None, "mp"))
        if(len(db.getDataColumn("attribute","name","physical_attack"))==0):
            db.insertData(Attribute(None, "physical_attack"))
        if(len(db.getDataColumn("attribute","name","magic_attack"))==0):
            db.insertData(Attribute(None, "magic_attack"))                   
        if(len(db.getDataColumn("attribute","name","defense"))==0):
            db.insertData(Attribute(None, "defense"))
        if(len(db.getDataColumn("attribute","name","strength"))==0):
            db.insertData(Attribute(None, "strength"))
        if(len(db.getDataColumn("attribute","name","endurance"))==0):
            db.insertData(Attribute(None, "endurance"))
        if(len(db.getDataColumn("attribute","name","dexterity"))==0):
            db.insertData(Attribute(None, "dexterity"))                          
        if(len(db.getDataColumn("attribute","name","agility"))==0):
            db.insertData(Attribute(None, "agility"))                   
        if(len(db.getDataColumn("attribute","name","magic"))==0):
            db.insertData(Attribute(None, "magic"))
        Stats(None, adventurerid[0], attributeid, temp_ad.stats.get("hp"))
        Stats(None, adventurerid[0], attributeid, temp_ad.stats.get("mp"))
        Stats(None, adventurerid[0], attributeid, temp_ad.stats.get("physical_attack"))
        Stats(None, adventurerid[0], attributeid, temp_ad.stats.get("magic_attack"))
        Stats(None, adventurerid[0], attributeid, temp_ad.stats.get("defense"))
        Stats(None, adventurerid[0], attributeid, temp_ad.stats.get("strength"))
        Stats(None, adventurerid[0], attributeid, temp_ad.stats.get("endurance"))
        Stats(None, adventurerid[0], attributeid, temp_ad.stats.get("dexterity"))
        Stats(None, adventurerid[0], attributeid, temp_ad.stats.get("agility"))
        Stats(None, adventurerid[0], attributeid, temp_ad.stats.get("magic"))
        
        
        
        #AdventurerSkill
        for skills in ad_dict.get("skills"):
            skills = ad_dict.get("skills").get(skills)
            
            temp_value = skills.get("effects").get("type")
            temp_index = temp_value.find("_")
            temp_element = temp_value[0:temp_index]
            temp_ad_ele = temp_element
            temp_type = temp_value[temp_index+1:]
            print(temp_element +"-" + temp_type)
            # Element
            temp_eleid=db.getDataColumn("element","name",temp_element)
            # Type for skills
            temp_typeid=db.getDataColumn("type","name",temp_type)
            if(skills == "special" or skills == "combat"):
                # Adventurer skill
                db.insertData(AdventurerSkill(None, adventurerid[0], temp_typeid, temp_eleid,
                         skills.get("name"),skills))
                temp_adskill=db.getDataColumn("adventurerskill","skillname",skills.get("name"))[0]
                # AdventurerSkillEffects SET UP
                temp_target = skills.get("effects").get("target")
                temp_attribute = skills.get("effects").get("attribute")
                temp_modifier = skills.get("effects").get("modifier")
                
                temp_target =db.getDataColumn("target","name",temp_target)[0]
                temp_attribute=db.getDataColumn("attribute","name",temp_attribute)[0]
                temp_modifier=db.getDataColumn("modifier","value",temp_modifier)[0]
                #AdventurerSkillEffects
                db.insertData(AdventurerSkillEffects(None, temp_adskill[0], temp_target[0],
                     temp_attribute[0], temp_modifier[0], skills.get("effects").get("duration")))
            else:
                temp_attribute = skills.get("effects").get("attribute")
                temp_modifier = skills.get("effects").get("modifier")                
                #AdventurerDevelopment                
                db.insertData(AdventurerDevelopment(None, adventurerid[0], skills.get("name"), temp_attribute,
                 temp_modifier))


                    

print(ad_list[0]._name)