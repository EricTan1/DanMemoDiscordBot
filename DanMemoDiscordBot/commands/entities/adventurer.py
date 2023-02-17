import json
from typing import Any, Dict, List, Optional, Tuple, Union

from commands.entities.skills import AdventurerCounter
from commands.utils import checkBuffExistsReplace, getDamageBuffs, getElements


class Adventurer:
    def __init__(
        self,
        stats: Dict[str, Union[int, float]] = {
            "hp": 0,
            "mp": 0,
            "strength": 0,
            "magic": 0,
            "agility": 0,
            "endurance": 0,
            "dexterity": 0,
            "fire": 0.0,
            "water": 0.0,
            "thunder": 0.0,
            "earth": 0.0,
            "wind": 0.0,
            "light": 0.0,
            "dark": 0.0,
        },
        counterBoost=0,
        critPenBoost=0,
        current_skills={"combat": [], "special": [], "additionals": []},
        current_skills_agi_mod: Dict[str, List[str]] = {
            "combat": [],
            "special": [],
            "additionals": [],
        },
        turnOrder=[0] * 15,
        adventurerCounter=AdventurerCounter(
            target="foe", extraBoost="", noType=0, type="physical", element=""
        ),
        adventurerAttack=AdventurerCounter(
            target="foe", extraBoost="", noType=0, type="physical", element=""
        ),
        name="",
        isCounter=True,
        counterEffects=[],
    ):
        self.stats = stats
        self.counterBoost = counterBoost
        self.critPenBoost = critPenBoost
        self.current_skills = current_skills
        self.current_skills_agi_mod = current_skills_agi_mod
        self.turnOrder = turnOrder
        self.adventurerCounter = adventurerCounter
        self.adventurerAttack = adventurerAttack
        # element attack
        self.elementDamageBoostAdv = {
            "fire": 0.0,
            "water": 0.0,
            "thunder": 0.0,
            "earth": 0.0,
            "wind": 0.0,
            "light": 0.0,
            "dark": 0.0,
        }
        self.elementDamageBoostAst = {
            "fire": 0.0,
            "water": 0.0,
            "thunder": 0.0,
            "earth": 0.0,
            "wind": 0.0,
            "light": 0.0,
            "dark": 0.0,
        }
        # str/mag boosts
        self.statsBoostAdv = {
            "hp": 0.0,
            "mp": 0.0,
            "strength": 0.0,
            "magic": 0.0,
            "agility": 0.0,
            "endurance": 0.0,
            "dexterity": 0.0,
        }
        self.statsBoostAst = {
            "hp": 0.0,
            "mp": 0.0,
            "strength": 0.0,
            "magic": 0.0,
            "agility": 0.0,
            "endurance": 0.0,
            "dexterity": 0.0,
        }
        # additionals count
        self.additionalName = ""
        self.additionalCount = 0
        # adv damage
        self.current_damage = 0
        self.isCounter = isCounter
        self.counterEffects = counterEffects
        # buffs and debuffs
        # append buffs to dict and remove once wiped
        # list of dict
        # {isbuff,Attribute,Modifier,duration}
        # each list object
        # {"isbuff":False,"attribute":"strength","modifier":-45,"duration":1}
        self.boostCheckAlliesAdv: List[Dict[str, Any]] = []
        self.boostCheckAlliesAst: List[Dict[str, Any]] = []
        self.name = name

    def get_combatSkill_agi(self, index: int) -> str:
        """index = 1-3"""
        return self.current_skills_agi_mod["combat"][index - 1]

    def add_damage(self, damage: int):
        self.current_damage += damage

    # main loop need to check skill [1,4]
    def get_combatSkill(self, index: int) -> Tuple[str, list]:
        """index = 1-3"""
        return self.current_skills["combat"][index - 1]

    def get_specialSkill(self) -> Tuple[str, list]:
        return self.current_skills["special"][0]

    def get_additionals(self) -> Tuple[str, list]:
        return self.current_skills["additionals"]

    def get_current_additional(self):
        additionals = self.get_additionals()
        for aa in additionals:
            if aa[0] == self.additionalName:
                return aa
        # if no additional with matching name was found, we assume the unit has only one AA and it wasn't named
        return additionals[0]

    def set_statsBoostAdv(self, stat: str, modifier: float):
        self.statsBoostAdv[stat.lower()] = modifier

    def set_statsBoostAst(self, stat: str, modifier: float):
        self.statsBoostAst[stat.lower()] = modifier

    def set_elementDamageBoostAdv(self, element: str, modifier: float):
        if element.lower() in getElements():
            self.elementDamageBoostAdv[element.lower()] = modifier

    def set_elementDamageBoostAst(self, element: str, modifier: float):
        if element.lower() in getElements():
            self.elementDamageBoostAst[element.lower()] = modifier

    def set_boostCheckAlliesAdv(
        self, isbuff: bool, attribute: str, modifier: float, duration: int
    ):
        """(bool, str, int or float, int, bool, int) -> None
        target: self, allies, foes, foe
        attribute: strength, magic, st, aoe
        modifier: -10 ,+50
        duration: 1,2,3,4
        is_assist: is this an assist buff or not
        position : the active unit position in the party
        """
        try:
            duration = int(duration)
        except:
            pass
        tempAppend = {
            "isbuff": isbuff,
            "attribute": attribute,
            "modifier": modifier,
            "duration": duration,
        }
        checkBuffExistsReplace(self.boostCheckAlliesAdv, tempAppend)

    def set_boostCheckAlliesAst(
        self, isbuff: bool, attribute: str, modifier: float, duration: int
    ):
        """(bool, str, int or float, int, bool, int) -> None
        target: self, allies, foes, foe
        attribute: strength, magic, st, aoe
        modifier: -10 ,+50
        duration: 1,2,3,4
        is_assist: is this an assist buff or not
        position : the active unit position in the party
        """
        tempAppend = {
            "isbuff": isbuff,
            "attribute": attribute,
            "modifier": modifier,
            "duration": duration,
        }
        checkBuffExistsReplace(self.boostCheckAlliesAst, tempAppend)

    def set_additionals(self, additional_count: int, origin_name: str):
        # only change/refresh if
        # - the current additional action is already empty, or
        # - the same additional is added, meaning it'll just be refreshed
        # - the new addtional comes from the SA, overriding any non-SA additionals
        if (
            self.additionalCount == 0
            or origin_name == self.additionalName
            or origin_name == (self.get_specialSkill())[0]
        ):
            self.additionalCount = additional_count
            self.additionalName = origin_name
        # else: SA additional is active and the newly activated is non-SA, which must not override so nothing happens

    def clearBuffs(self):
        # take the list but all the buffs with True is removed (keep all  the isbuff==False)
        self.boostCheckAlliesAdv = [
            item for item in self.boostCheckAlliesAdv if item.get("isbuff") == False
        ]

    def clearDebuffs(self):
        # take the list but all the buffs with True is removed (keep all  the isbuff==False)
        self.boostCheckAlliesAdv = [
            item for item in self.boostCheckAlliesAdv if item.get("isbuff") == True
        ]

    def ExtendShortenSingleEffect(self, attribute: str, turns: int, is_buff: bool):
        buffsDebuffs = self.get_boostCheckAlliesAdv(is_buff, attribute)
        if buffsDebuffs is None:
            return
        buffsDebuffs["duration"] += turns
        if buffsDebuffs["duration"] <= 0:
            self.boostCheckAlliesAdv.remove(buffsDebuffs)
            if is_buff and attribute in getDamageBuffs():
                element = attribute.replace("_attack", "")
                if element in getElements():
                    self.elementDamageBoostAdv[element] = 0
                else:
                    self.statsBoostAdv[attribute] = 0

    def ExtendReduceBuffs(self, turns):
        for buffsDebuffs in self.boostCheckAlliesAdv:
            if buffsDebuffs.get("isbuff") == True and isinstance(
                buffsDebuffs.get("duration"), int
            ):
                buffsDebuffs["duration"] += turns
        temp_expiry = [
            item
            for item in self.boostCheckAlliesAdv
            if isinstance(item.get("duration"), int) and item.get("duration") <= 0
        ]
        self.boostCheckAlliesAdv = [
            item
            for item in self.boostCheckAlliesAdv
            if isinstance(item.get("duration"), int) and item.get("duration") > 0
        ]

        for buffsDebuffs in temp_expiry:
            curr_attribute = buffsDebuffs.get("attribute")
            if curr_attribute in getDamageBuffs():
                curr_element = curr_attribute.replace("_attack", "")
                if curr_element in getElements():
                    self.elementDamageBoostAdv[curr_element] = 0
                else:
                    self.statsBoostAdv[curr_attribute] = 0

    def ExtendReduceDebuffs(self, turns):
        for buffsDebuffs in self.boostCheckAlliesAdv:
            if buffsDebuffs.get("isbuff") == False and isinstance(
                buffsDebuffs.get("duration"), int
            ):
                temp_duration = buffsDebuffs.get("duration") + turns
                buffsDebuffs["duration"] = temp_duration
        self.boostCheckAlliesAdv = [
            item
            for item in self.boostCheckAlliesAdv
            if isinstance(item.get("duration"), int) and item.get("duration") > 0
        ]

    def get_boostCheckAlliesAdv(
        self, isbuff: bool, attribute: str
    ) -> Optional[Dict[str, Any]]:
        "returns the item in the buff/debuff list if it exists, returns NONE otherwise"
        for item in self.boostCheckAlliesAdv:
            if item.get("isbuff") == isbuff and item.get("attribute") == attribute:
                return item
        return None

    def pop_boostCheckAlliesAdv(self, isbuff: bool, attribute: str):
        """(bool, str, int or float, int, bool, int) -> None
        target: self, allies, foes, foe
        attribute: strength, magic, st, aoe
        modifier: -10 ,+50
        duration: 1,2,3,4
        is_assist: is this an assist buff or not
        position : the active unit position in the party
        """
        self.boostCheckAlliesAdv = [
            item
            for item in self.boostCheckAlliesAdv
            if not (item.get("isbuff") == isbuff and item.get("attribute") == attribute)
        ]

    def get_log_effect_list(self) -> List[str]:
        ret = [f"**{self.name}**"]
        with open("database/terms/human_readable.json", "r") as f:
            human_readable_dict = json.load(f)
        for buffsdebuffs in self.boostCheckAlliesAdv:
            if buffsdebuffs["attribute"] in [
                "all_damage_resist",
                "single_damage_resist",
            ]:
                modifier = -buffsdebuffs["modifier"] * 100
            else:
                modifier = buffsdebuffs["modifier"] * 100
            modifierStr = f"{modifier:.0f}" if modifier < 0 else f"+{modifier:.0f}"

            if human_readable_dict.get(buffsdebuffs["attribute"]) != None:
                attribute = human_readable_dict.get(buffsdebuffs["attribute"])
            else:
                attribute = buffsdebuffs["attribute"]

            ret.append(
                "{}% {} for {} turn(s)".format(
                    modifierStr,
                    attribute,
                    buffsdebuffs.get("duration"),
                )
            )
        return ret
