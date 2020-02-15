class Adventurer:
    def __init__(self, adventurerid:int, characterid:int, typeid:int, title:str,limited:bool, ascended:bool,
                 stars:int, splashuri:str, iconuri:str):
        ''' (Adventurer, int, int, int, bool, bool, int, str or None, str or
             None) -> Adventurer
             stars : the base stars of a unit (1/2/3/4)
             limited : is the unit time-limited?
             ascended : does the unit have hero ascension?
        '''
        self.adventurerid = int(adventurerid)
        self.characterid = int(characterid)
        self.title = str(title)
        self.typeid = int(typeid)
        self.limited = bool(limited)
        self.ascended = bool(ascended)
        self.stars = int(stars)
        self.splashuri = str(splashuri)
        self.iconuri = str(iconuri)

    def __str__(self):
        return self.title
    
class AdventurerSkill:
    def __init__(self, adventurerskillid:int, adventurerid:int,
                 skillname:str,skilltype:str):
        ''' (AdventurerSkill, int, int,str, str) -> AdventurerSkill
        skillname: the name of the skill of the adventurer
        '''
        self.adventurerskillid = int(adventurerskillid)
        self.adventurerid = int(adventurerid)
        self.skillname = str(skillname)
        self.skilltype = str(skilltype)

    def __str__(self):
        return self.skillname


class AdventurerSkillEffects:

    def __init__(self, adventurerskilleffectsid:int, adventurerskillid:int, targetid:int,
                 attributeid:int, modifierid:int, duration, typeid:int,eleid:int):
        ''' (AdventurerSkillEffects, int, int, int, int, int,
             int) -> AdventurerSkillEffects
             duration : some buffs/debuffs have durations
        '''
        self.adventurerskilleffectsid = int(adventurerskilleffectsid)
        self.adventurerskillid = int(adventurerskillid)
        self.targetid = int(targetid)
        self.attributeid = int(attributeid)
        self.modifierid = int(modifierid)
        self.duration = duration
        self.typeid=int(typeid)
        self.eleid=int(eleid)

    def __str__(self):
        return str(self.adventurerskilleffectsid)


class AdventurerDevelopment:
    def __init__(self, adventurerdevelopmentid:int, adventurerid:int, name:str, attributeid:int,
                 modifierid:int):
        ''' (AdventurerDevelopment, int, int, str, int,
             int) -> AdventurerDevelopment
             name : name of the development skill
        '''
        self.adventurerdevelopmentid = int(adventurerdevelopmentid)
        self.adventurerid = int(adventurerid)
        self.name = str(name)
        self.attributeid = int(attributeid)
        self.modifierid = int(modifierid)
        
    def __str__(self):
        ''' Placeholder for now we will add modifier and attribute after?
        '''
        return self.name

class AdventurerStats:
    ''' This class is an object that represents the
    stats table in the DB
    '''
    def __init__(self, adventurerstatsid:int, adventurerid:int, attributeid:int, value:str):
        ''' (Stats, int, int, int, str) -> Stats
        value : python list but in str format of an attribute
        ex:
        attribute: Strength
        [1,2,3,4,5,6]
        [LB0,LB1,LB2,LB3,LB4,LB5]
        corresponds with limit break 0-5
        '''
        self.adventurerstatsid = int(adventurerstatsid)
        self.adventurerid = int(adventurerid)
        self.attributeid = int(attributeid)
        self.value = str(value)

    def __str__(self):
        return self.name