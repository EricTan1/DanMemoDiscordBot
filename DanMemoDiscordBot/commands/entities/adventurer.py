from commands.entities.combatant import Combatant
from commands.entities.skills import AdventurerCounter
from commands.utils import getDamageBuffs, getElements


class Adventurer(Combatant):
    def __init__(
        self,
        stats: dict[str, int | float] = {
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
        current_skills_agi_mod: dict[str, list[str]] = {
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
        super().__init__(stats)

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
        self.name = name

    def get_combatSkill_agi(self, index: int) -> str:
        """index = 1-3"""
        return self.current_skills_agi_mod["combat"][index - 1]

    def add_damage(self, damage: int):
        self.current_damage += damage

    # main loop need to check skill [1,4]
    def get_combatSkill(self, index: int) -> tuple[str, list]:
        """index = 1-3"""
        return self.current_skills["combat"][index - 1]

    def get_specialSkill(self) -> tuple[str, list]:
        return self.current_skills["special"][0]

    def get_additionals(self) -> tuple[str, list]:
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

    def set_additionals(self, additional_count: int, origin_name: str):
        # only change/refresh if
        # - the new additional has more actions than are left, refreshing+overriding the current one
        # - or the new addtional comes from the SA, overriding any non-SA additionals
        if (
            additional_count > self.additionalCount
            or origin_name == (self.get_specialSkill())[0]
        ):
            self.additionalCount = additional_count
            self.additionalName = origin_name
        # else: SA additional is active and the newly activated is non-SA with at most
        # as many actions as remain on the SA, which must not override so nothing happens

    def ExtendShortenSingleEffect(self, attribute: str, turns: int, is_buff: bool):
        buffsDebuffs = self.get_boostCheckAdv(is_buff, attribute)
        if buffsDebuffs is None:
            return
        buffsDebuffs.duration += turns
        if buffsDebuffs.duration <= 0:
            self.boostCheckAdv.remove(buffsDebuffs)
            if is_buff and attribute in getDamageBuffs():
                element = attribute.replace("_attack", "")
                if element in getElements():
                    self.elementDamageBoostAdv[element] = 0
                else:
                    self.statsBoostAdv[attribute] = 0

    def ExtendReduceBuffs(self, turns: int, turnCountdown=False):
        for buffsDebuffs in self.boostCheckAdv:
            if buffsDebuffs.isbuff == True:
                # Don't change duration of regen effects, unless it's the end-of-turn countdown
                if "regen" not in buffsDebuffs.attribute or turnCountdown:
                    buffsDebuffs.duration += turns
        temp_expiry = [item for item in self.boostCheckAdv if item.duration <= 0]
        self.boostCheckAdv = [item for item in self.boostCheckAdv if item.duration > 0]

        for buffsDebuffs in temp_expiry:
            curr_attribute = buffsDebuffs.attribute
            if curr_attribute in getDamageBuffs():
                curr_element = curr_attribute.replace("_attack", "")
                if curr_element in getElements():
                    self.elementDamageBoostAdv[curr_element] = 0
                else:
                    self.statsBoostAdv[curr_attribute] = 0

    def ExtendReduceDebuffs(self, turns: int):
        for buffsDebuffs in self.boostCheckAdv:
            if buffsDebuffs.isbuff == False:
                buffsDebuffs.duration += turns
        self.boostCheckAdv = [item for item in self.boostCheckAdv if item.duration > 0]

    def get_log_effect_list(self) -> list[str]:
        result = [f"**{self.name}**"] + super().get_log_effect_list()
        if self.additionalCount > 0:
            result.append(
                f"Additional Actions: {self.additionalName}, {self.additionalCount} left"
            )
        return result

    def clearBuffs(self):
        super().clearBuffs()
        self.elementDamageBoostAdv = {
            "fire": 0,
            "water": 0,
            "thunder": 0,
            "earth": 0,
            "wind": 0,
            "light": 0,
            "dark": 0,
        }
        self.statsBoostAdv = {
            "hp": 0,
            "mp": 0,
            "strength": 0,
            "magic": 0,
            "agility": 0,
            "endurance": 0,
            "dexterity": 0,
        }
