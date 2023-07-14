class AdventurerSkill:
    def __init__(
        self,
        target="foe",
        tempBoost="None",
        powerCoefficient="Low",
        extraBoost=1,
        noType=0,
        type="physical",
        element="",
        index_to=[],
    ):
        """(self, str, float, str, float, boolean, str, str, list of str)
        target: foes,foe
        tempBoost: normal, normal2, great
        powerCoefficient: Hi, Lo, Super, Ultra, ....
        extraBoost: 1 + x%/100 per each skills
        NoType: does it have an element? Older units don't have elements
        type: physical or magic attack
        element: wind, fire, water, earth, ....
        index_to: the scaling of an ability (thunder daph scales to agility)
        """
        self.target = target
        self.tempBoost = tempBoost
        self.powerCoefficient = powerCoefficient
        self.extraBoost = extraBoost
        self.noType = noType
        self.type = type
        self.element = element
        self.index_to = index_to


class AdventurerCounter:
    def __init__(
        self, target="foe", extraBoost="", noType=0, type="physical", element=""
    ):
        """(self, str, float, str, float, boolean, str, str, list of str)
        target: foes,foe
        NoType: does it have an element? Older units don't have elements
        type: physical or magic attack
        element: wind, fire, water, earth, ....
        """
        self.target = target
        self.noType = noType
        self.type = type
        self.element = element
        # str per_each_attribute_buff/debuff
        self.extraBoost = extraBoost


# "Dummy" class used so we can schedule Enemy Attacks among adventurer actions in rbcalc
class EnemyAttack:
    pass
