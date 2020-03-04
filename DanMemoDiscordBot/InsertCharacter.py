import json
import os

import sys
sys.path.append('Entities/')

from DBcontroller import DBcontroller
from Adventurer import Adventurer,AdventurerSkill,AdventurerSkillEffects,AdventurerDevelopment, AdventurerStats
from BaseConstants import Element, Target, Type, Attribute,Modifier, Speed
from Character import Character


class AdventureC:
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
        characterid = getInsertCharacterID(adventureComplete._name,
                                           False)
    
    def insertAssist(self, assistComplete:AssistC):
        characterid = getInsertCharacterID(adventureComplete._name,
                                           False)
    
    
    
    
    
    
    
    
    def getInsertCharacterID(self, name, iscollab):
        ret = -1
        ret_list = db.getDataColumn("character","name", name)
        # check if character in, if it is then get id else insert
        if(len(ret_list) == 0):
            ret = db.insertData(Character(None, name, iscollab))
        else:
            # id is always first column
            ret = (ret_list[0])[0]
        return ret

if __name__ =="__main__":
    db = DBcontroller("localhost","root","danmemo","3306","danmemo")
    ic = InsertCharacter(db)