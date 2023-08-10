import json
from typing import Mapping

from commands.utils import AssistEffect, Effect, checkBuffExistsReplace


class Combatant:
    def __init__(self, stats: Mapping[str, int | float]):
        self.stats = stats

        # track active buffs and debuffs by source
        self.boostCheckAdv: list[Effect] = []
        self.boostCheckAst: list[AssistEffect] = []

    def set_boostCheckAdv(
        self, isbuff: bool, attribute: str, modifier: float, duration: int
    ):
        effect = Effect(isbuff, attribute, modifier, duration)
        checkBuffExistsReplace(self.boostCheckAdv, effect)

    def set_boostCheckAst(self, isbuff: bool, attribute: str, modifier: float):
        effect = AssistEffect(isbuff, attribute, modifier)
        checkBuffExistsReplace(self.boostCheckAst, effect)

    def pop_boostCheckAdv(self, isbuff: bool, attribute: str):
        self.boostCheckAdv = [
            item
            for item in self.boostCheckAdv
            if item.isbuff != isbuff or item.attribute != attribute
        ]

    def clearBuffs(self):
        # take the list but all the buffs with True is removed (keep all the isbuff==False)
        self.boostCheckAdv = [
            item
            for item in self.boostCheckAdv
            if item.isbuff == False or "regen" in item.attribute
        ]

    def clearDebuffs(self):
        # take the list but all the buffs with True is removed (keep all the isbuff==False)
        self.boostCheckAdv = [
            item for item in self.boostCheckAdv if item.isbuff == True
        ]

    def get_boostCheckAdv(self, isbuff: bool, attribute: str) -> Effect | None:
        "returns the item in the buff/debuff list if it exists, returns NONE otherwise"
        for item in self.boostCheckAdv:
            if item.isbuff == isbuff and item.attribute == attribute:
                return item
        return None

    def get_log_effect_list(self) -> list[str]:
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
                f"{modifierStr}% {attribute} for {buffsdebuffs.duration} turn(s)"
            )
        return ret
