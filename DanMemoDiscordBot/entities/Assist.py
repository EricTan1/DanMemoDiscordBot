from BaseConstants import Base

class Assist(Base):
    def __init__(self, assistid, characterid:int, title:str,limited:bool,
                 stars:int, alias:str):
        ''' (Assist, int, int, int, bool, int, str or None, str or
             None) -> Assist
             stars : the base stars of a unit (1/2/3/4)
             limited : is the unit time-limited?
        '''
        self.assistid = assistid
        self.characterid = int(characterid)
        self.limited = bool(limited)
        self.title = str(title)
        self.stars = int(stars)
        self.alias = str(alias)

    def __str__(self):
        return self.title

class AssistSkill(Base):
    def __init__(self, assistskillid, assistid:int, skillname:str):
        ''' (AssistSkill, int, int, int, int, str) -> AssistSkill
        skillname: the name of the skill of the assist
        '''
        self.assistskillid = assistskillid
        self.assistid = int(assistid)
        self.skillname = str(skillname)

    def __str__(self):
        return self.skillname


class AssistSkillEffects(Base):

    def __init__(self, assistskilleffectsid, assistskillid:int, targetid:int,
                 attributeid:int, modifierid:int, duration):
        ''' (AssistSkillEffects, int, int, int, int, int,
             int) -> AssistSkillEffects
             duration : some buffs/debuffs have durations
        '''
        self.assistskilleffectsid = assistskilleffectsid
        self.assistskillid = int(assistskillid)
        self.targetid = int(targetid)
        self.attributeid = int(attributeid)
        self.modifierid = int(modifierid)
        self.duration = duration

    def __str__(self):
        return str(self.assistskilleffectsid)

class AssistStats(Base):
    ''' This class is an object that represents the
    stats table in the DB
    '''
    def __init__(self, assiststatsid, assistid:int, attributeid:int, value):
        ''' (Stats, int, int, int, str) -> Stats
        value : python list but in str format of an attribute
        ex:
        attribute: Strength
        [1,2,3,4,5,6]
        [LB0,LB1,LB2,LB3,LB4,LB5]
        corresponds with limit break 0-5
        '''
        self.assiststatsid = assiststatsid
        self.assistid = int(assistid)
        self.attributeid = int(attributeid)
        self.value = value

    def __str__(self):
        return self.name