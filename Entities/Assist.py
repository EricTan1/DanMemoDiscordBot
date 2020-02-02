class Assist:
    def __init__(self, assistid, characterid, typeid, limited,
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
        self.stars = stars
        self.splashuri = splashuri
        self.iconuri = iconuri

    def __str__(self):
        pass

class AssistSkill:
    def __init__(self, assistskillid, assistid, typeid, eleid,
                 skillname):
        ''' (AssistSkill, int, int, int, int, str) -> AssistSkill
        skillname: the name of the skill of the assist
        '''
        self.assistskillid = assistskillid
        self.assistid = assistid
        self.typeid = typeid
        self.eleid = eleid
        self.skillname = skillname

    def __str__(self):
        return self.skillname


class AssistSkillEffects:

    def __init__(self, assistskilleffectsid, assistskillid, targetid,
                 attributeid, modifierid, duration):
        ''' (AssistSkillEffects, int, int, int, int, int,
             int) -> AssistSkillEffects
             duration : some buffs/debuffs have durations
        '''
        self.assistskilleffectsid = assistskilleffectsid
        self.assistskillid = assistskill
        self.targetid = targetid
        self.attributeid = attributeid
        self.modifierid = modifierid
        self.duration = duration

    def __str__(self):
        return str(self.assistskilleffectsid)
