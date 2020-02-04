class Assist:
    def __init__(self, assistid, characterid, typeid, title,limited,
                 stars, splashuri, iconuri):
        ''' (Assist, int, int, int, bool, int, str or None, str or
             None) -> Assist
             stars : the base stars of a unit (1/2/3/4)
             limited : is the unit time-limited?
        '''
        self.assistid = assistid
        self.characterid = characterid
        self.typeid = typeid
        self.limited = limited
        self.title = title
        self.stars = stars
        self.splashuri = splashuri
        self.iconuri = iconuri

    def __str__(self):
        return self.title

class AssistSkill:
    def __init__(self, assistskillid, assistid, skillname):
        ''' (AssistSkill, int, int, int, int, str) -> AssistSkill
        skillname: the name of the skill of the assist
        '''
        self.assistskillid = assistskillid
        self.assistid = assistid
        self.skillname = skillname

    def __str__(self):
        return self.skillname


class AssistSkillEffects:

    def __init__(self, assistskilleffectsid, assistskillid, targetid,
                 attributeid, modifierid):
        ''' (AssistSkillEffects, int, int, int, int, int,
             int) -> AssistSkillEffects
             duration : some buffs/debuffs have durations
        '''
        self.assistskilleffectsid = assistskilleffectsid
        self.assistskillid = assistskillid
        self.targetid = targetid
        self.attributeid = attributeid
        self.modifierid = modifierid

    def __str__(self):
        return str(self.assistskilleffectsid)

class AssistStats:
    ''' This class is an object that represents the
    stats table in the DB
    '''
    def __init__(self, assiststatsid, assistid, attributeid, value):
        ''' (Stats, int, int, int, str) -> Stats
        value : python list but in str format of an attribute
        ex:
        attribute: Strength
        [1,2,3,4,5,6]
        [LB0,LB1,LB2,LB3,LB4,LB5]
        corresponds with limit break 0-5
        '''
        self.assiststatsid = assiststatsid
        self.assistid = assistid
        self.attributeid = attributeid
        self.value = value

    def __str__(self):
        return self.name