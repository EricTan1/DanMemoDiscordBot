from database.entities.BaseConstants import Base

class Adventurer(Base):
    def __init__(self, adventurerid, characterid:int, typeid:int, title:str,limited:bool, ascended:bool,
                 stars:int, alias:str):
        ''' (Adventurer, int, int, int, bool, bool, int, str or None, str or
             None) -> Adventurer
             stars : the base stars of a unit (1/2/3/4)
             limited : is the unit time-limited?
             ascended : does the unit have hero ascension?
        '''
        self.adventurerid = adventurerid
        self.characterid = int(characterid)
        self.title = str(title)
        self.typeid = int(typeid)
        self.limited = bool(limited)
        self.ascended = bool(ascended)
        self.stars = int(stars)
        self.alias = str(alias)

    def __str__(self):
        return self.title
    
class AdventurerSkill(Base):
    def __init__(self, adventurerskillid, adventurerid:int,
                 skillname:str,skilltype:str):
        ''' (AdventurerSkill, int, int,str, str) -> AdventurerSkill
        skillname: the name of the skill of the adventurer
        '''
        self.adventurerskillid = adventurerskillid
        self.adventurerid = int(adventurerid)
        self.skillname = str(skillname)
        self.skilltype = str(skilltype)

    def __str__(self):
        return self.skillname


class AdventurerSkillEffects(Base):

    def __init__(self, adventurerskilleffectsid, adventurerskillid:int, targetid:int,
                 attributeid:int, modifierid:int, duration, typeid:int,eleid:int, speedid):
        ''' (AdventurerSkillEffects, int, int, int, int, int,
             int) -> AdventurerSkillEffects
             duration : some buffs/debuffs have durations
        '''
        self.adventurerskilleffectsid = adventurerskilleffectsid
        self.adventurerskillid = int(adventurerskillid)
        self.targetid = int(targetid)
        self.attributeid = int(attributeid)
        self.modifierid = int(modifierid)
        self.duration = duration
        self.typeid=int(typeid)
        self.eleid=int(eleid)
        self.speedid=speedid

    def __str__(self):
        return str(self.adventurerskilleffectsid)


class AdventurerDevelopment(Base):
    def __init__(self, adventurerdevelopmentid, adventurerid:int, name:str):
        ''' (AdventurerDevelopment, int, int, str, int,
             int) -> AdventurerDevelopment
             name : name of the development skill
        '''
        self.adventurerdevelopmentid = adventurerdevelopmentid
        self.adventurerid = int(adventurerid)
        self.name = str(name)
        #self.attributeid = int(attributeid)
        #self.modifierid = int(modifierid)
    
class AdventurerDevelopmentSkillEffects(Base):
    def __init__(self, adventurerdevelopmentskilleffectsid,adventurerdevelopmentid, targetid:int, attributeid:int,
                 modifierid:int, duration, typeid:int, eleid: int, speedid):
        ''' (AdventurerDevelopment, int, int, str, int,
             int) -> AdventurerDevelopment
             name : name of the development skill
        '''
        self.adventurerdevelopmentskilleffectsid = adventurerdevelopmentskilleffectsid
        self.adventurerdevelopmentid = adventurerdevelopmentid
        self.attributeid = int(attributeid)
        self.modifierid = int(modifierid)
        self.targetid = targetid
        self.duration = duration
        self.typeid = typeid
        self.eleid = eleid
        self.speedid = speedid

        
    def __str__(self):
        ''' Placeholder for now we will add modifier and attribute after?
        '''
        return self.name

class AdventurerStats(Base):
    ''' This class is an object that represents the
    stats table in the DB
    '''
    def __init__(self, adventurerstatsid, adventurerid:int, attributeid:int, value:str):
        ''' (Stats, int, int, int, str) -> Stats
        value : python list but in str format of an attribute
        ex:
        attribute: Strength
        [1,2,3,4,5,6]
        [LB0,LB1,LB2,LB3,LB4,LB5]
        corresponds with limit break 0-5
        '''
        self.adventurerstatsid = adventurerstatsid
        self.adventurerid = int(adventurerid)
        self.attributeid = int(attributeid)
        self.value = str(value)

    def __str__(self):
        return self.name