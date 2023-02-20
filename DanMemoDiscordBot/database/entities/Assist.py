from typing import Optional

from database.entities.BaseConstants import Base


class Assist(Base):
    def __init__(
        self,
        assistid: Optional[int],
        characterid: int,
        title: str,
        limited: int,
        stars: int,
        alias: Optional[str],
    ):
        """
        stars : the base stars of a unit (1/2/3/4)
        limited : is the unit regular/Time-limited/Hero Festa -> 0/1/2
        """
        self.assistid = assistid
        self.characterid = characterid
        self.limited = limited
        self.title = title
        self.stars = stars
        self.alias = str(alias)

    def __str__(self):
        return self.title


class AssistSkill(Base):
    def __init__(
        self,
        assistskillid: Optional[int],
        assistid: int,
        skillname: str,
        skilltype: str,
    ):
        self.assistskillid = assistskillid
        self.assistid = assistid
        self.skillname = skillname
        self.skilltype = skilltype

    def __str__(self):
        return self.skillname


class AssistSkillEffects(Base):
    def __init__(
        self,
        assistskilleffectsid: Optional[int],
        assistskillid: int,
        targetid: int,
        attributeid: int,
        modifierid: int,
        duration,
        maxActivations,
        elementid: int,
        typeid: int,
    ):
        """
        duration : some buffs/debuffs have durations
        """
        self.assistskilleffectsid = assistskilleffectsid
        self.assistskillid = assistskillid
        self.targetid = targetid
        self.attributeid = attributeid
        self.modifierid = modifierid
        self.duration = duration
        self.maxActivations = maxActivations
        self.elementid = elementid
        self.typeid = typeid

    def __str__(self):
        return str(self.assistskilleffectsid)


class AssistStats(Base):
    def __init__(
        self, assiststatsid: Optional[int], assistid: int, attributeid: int, value: str
    ):
        self.assiststatsid = assiststatsid
        self.assistid = assistid
        self.attributeid = attributeid
        self.value = value
