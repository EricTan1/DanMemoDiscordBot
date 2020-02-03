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
        Adventurer(None, characterid[0], typeid[0], temp_ad._limited, False,
                 temp_ad._stars, None, None)
        
        #AdventurerSkill
        AdventurerSkill()
        #AdventurerSkillEffects
        AdventurerSkillEffects()
        #AdventurerDevelopment
        AdventurerDevelopment()
        #Stats
        Stats()

print(ad_list[0]._name)