import json
from typing import Dict, List, Optional

from commands.utils import AssistEffect, Effect, checkBuffExistsReplace


class Combatant:
    def __init__(self, stats: Dict[str, float]):
        self.stats = stats

        # buffs and debuffs
        # append buffs to list and remove once wiped
        self.boostCheckAdv: List[Effect] = []
        self.boostCheckAst: List[AssistEffect] = []

    def set_boostCheckAdv(
        self, isbuff: bool, attribute: str, modifier: float, duration: int
    ):
        """(bool, str, int or float, int, bool) -> None
        target: self, allies, foes, foe
        attribute: strength, magic, st, aoe
        modifier: -10 ,+50
        duration: 1,2,3,4
        is_assist: is this an assist buff or not
        """
        assert isinstance(isbuff, bool)  # TODO: remove
        assert isinstance(attribute, str)
        assert isinstance(modifier, float)
        assert isinstance(duration, int)
        effect = Effect(isbuff, attribute, modifier, duration)
        checkBuffExistsReplace(self.boostCheckAdv, effect)

    def set_boostCheckAst(self, isbuff: bool, attribute: str, modifier: float):
        """(bool, str, int or float) -> None
        attribute: strength, magic, st, aoe
        modifier: -10 ,+50
        """
        assert isinstance(isbuff, bool)  # TODO: remove
        assert isinstance(attribute, str)
        assert isinstance(modifier, float)
        effect = AssistEffect(isbuff, attribute, modifier)
        checkBuffExistsReplace(self.boostCheckAst, effect)

    def clearBuffs(self):
        # take the list but all the buffs with True is removed (keep all  the isbuff==False)
        self.boostCheckAdv = [
            item for item in self.boostCheckAdv if item.isbuff == False
        ]

    def clearDebuffs(self):
        # take the list but all the buffs with True is removed (keep all  the isbuff==False)
        self.boostCheckAdv = [
            item for item in self.boostCheckAdv if item.isbuff == True
        ]

    def get_boostCheckAdv(self, isbuff: bool, attribute: str) -> Optional[Effect]:
        "returns the item in the buff/debuff list if it exists, returns NONE otherwise"
        for item in self.boostCheckAdv:
            if item.isbuff == isbuff and item.attribute == attribute:
                return item
        return None

    def get_log_effect_list(self) -> List[str]:
        ret = []
        with open("database/terms/human_readable.json", "r") as f:
            human_readable_dict = json.load(f)
        for buffsdebuffs in self.boostCheckAdv:
            if buffsdebuffs.attribute in [
                "all_damage_resist",
                "single_damage_resist",
            ]:
                modifier = -buffsdebuffs.modifier * 100
            else:
                modifier = buffsdebuffs.modifier * 100
            modifierStr = f"{modifier:.0f}" if modifier < 0 else f"+{modifier:.0f}"

            if human_readable_dict.get(buffsdebuffs.attribute) is not None:
                attribute = human_readable_dict.get(buffsdebuffs.attribute)
            else:
                attribute = buffsdebuffs.attribute

            ret.append(
                "{}% {} for {} turn(s)".format(
                    modifierStr,
                    attribute,
                    buffsdebuffs.duration,
                )
            )
        return ret
