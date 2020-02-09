class Adventurer:
    def __init__(self, adventurerid, characterid, typeid, title,limited, ascended,
                 stars, splashuri, iconuri):
        ''' (Adventurer, int, int, int, bool, bool, int, str or None, str or
             None) -> Adventurer
             stars : the base stars of a unit (1/2/3/4)
             limited : is the unit time-limited?
             ascended : does the unit have hero ascension?
        '''
        self.adventurerid = adventurerid
        self.characterid = characterid
        self.title = title
        self.typeid = typeid
        self.limited = limited
        self.ascended = ascended
        self.stars = stars
        self.splashuri = splashuri
        self.iconuri = iconuri

    def __str__(self):
        return self.title
    
class AdventurerSkill:
    def __init__(self, adventurerskillid, adventurerid,
                 skillname,skilltype):
        ''' (AdventurerSkill, int, int, int, int, str) -> AdventurerSkill
        skillname: the name of the skill of the adventurer
        '''
        self.adventurerskillid = adventurerskillid
        self.adventurerid = adventurerid
        self.skillname = skillname
        self.skilltype = skilltype

    def __str__(self):
        return self.skillname


class AdventurerSkillEffects:

    def __init__(self, adventurerskilleffectsid, adventurerskillid, targetid,
                 attributeid, modifierid, duration, typeid,eleid):
        ''' (AdventurerSkillEffects, int, int, int, int, int,
             int) -> AdventurerSkillEffects
             duration : some buffs/debuffs have durations
        '''
        self.adventurerskilleffectsid = adventurerskilleffectsid
        self.adventurerskillid = adventurerskillid
        self.targetid = targetid
        self.attributeid = attributeid
        self.modifierid = modifierid
        self.duration = duration
        self.typeid=typeid
        self.eleid=eleid

    def __str__(self):
        return str(self.adventurerskilleffectsid)


class AdventurerDevelopment:
    def __init__(self, adventurerdevelopmentid, adventurerid, name, attributeid,
                 modifierid):
        ''' (AdventurerDevelopment, int, int, str, int,
             int) -> AdventurerDevelopment
             name : name of the development skill
        '''
        self.adventurerdevelopmentid = adventurerdevelopmentid
        self.adventurerid = adventurerid
        self.name = name
        self.attributeid = attributeid
        self.modifierid = modifierid
        
    def __str__(self):
        ''' Placeholder for now we will add modifier and attribute after?
        '''
        return self.name

class AdventurerStats:
    ''' This class is an object that represents the
    stats table in the DB
    '''
    def __init__(self, adventurerstatsid, adventurerid, attributeid, value):
        ''' (Stats, int, int, int, str) -> Stats
        value : python list but in str format of an attribute
        ex:
        attribute: Strength
        [1,2,3,4,5,6]
        [LB0,LB1,LB2,LB3,LB4,LB5]
        corresponds with limit break 0-5
        '''
        self.adventurerstatsid = adventurerstatsid
        self.adventurerid = adventurerid
        self.attributeid = attributeid
        self.value = value

    def __str__(self):
        return self.name