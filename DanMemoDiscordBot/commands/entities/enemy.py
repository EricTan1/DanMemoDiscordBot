from typing import TYPE_CHECKING

from commands.calculatorUtil import counter, counters
from commands.entities.combatant import Combatant
from commands.utils import getDamageDebuffs, getElements

if TYPE_CHECKING:
    from commands.entities.adventurer import Adventurer
    from commands.entities.assist import Assist


class Enemy(Combatant):
    def __init__(
        self,
        elementResistDownBase: dict[str, float] = {
            "fire": 0.0,
            "water": 0.0,
            "thunder": 0.0,
            "earth": 0.0,
            "wind": 0.0,
            "light": 0.0,
            "dark": 0.0,
            "none": 0.0,
        },
        typeResistDownBase: dict[str, float] = {"physical": 0.0, "magic": 0.0},
        stats: dict[str, int] = {
            "hp": 0,
            "mp": 0,
            "strength": 0,
            "magic": 0,
            "agility": 0,
            "endurance": 0,
            "dexterity": 0,
        },
    ):
        super().__init__(stats)

        self.elementResistDownBase = elementResistDownBase
        self.typeResistDownBase = typeResistDownBase

        # elemental resist down
        self.elementResistDownAdv = {
            "fire": 0.0,
            "water": 0.0,
            "thunder": 0.0,
            "earth": 0.0,
            "wind": 0.0,
            "light": 0.0,
            "dark": 0.0,
            "none": 0.0,
        }
        self.elementResistDownAst = {
            "fire": 0.0,
            "water": 0.0,
            "thunder": 0.0,
            "earth": 0.0,
            "wind": 0.0,
            "light": 0.0,
            "dark": 0.0,
            "none": 0.0,
        }

        # physical/magical resist
        self.typeResistDownAdv = {"physical": 0.0, "magic": 0.0}
        self.typeResistDownAst = {"physical": 0.0, "magic": 0.0}

        # target resist down
        self.targetResistDownAdv = {"st": 0.0, "aoe": 0.0}
        self.targetResistDownAst = {"st": 0.0, "aoe": 0.0}

    def set_elementResistDownAdv(self, element: str, modifier: float):
        if element.lower() in getElements():
            self.elementResistDownAdv[element.lower()] = modifier

    def set_elementResistDownAst(self, element: str, modifier: float):
        if element.lower() in getElements():
            self.elementResistDownAst[element.lower()] = modifier

    def set_typeResistDownAdv(self, type: str, modifier: float):
        self.typeResistDownAdv[type.lower()] = modifier

    def set_typeResistDownAst(self, type: str, modifier: float):
        self.typeResistDownAst[type.lower()] = modifier

    def set_targetResistDownAdv(self, target: str, modifier: float):
        self.targetResistDownAdv[target.lower()] = modifier

    def set_targetResistDownAst(self, target: str, modifier: float):
        self.targetResistDownAst[target.lower()] = modifier

    def turnOrder(self, turnOrder: int, adv_list: list, speed: int):
        """speed : 0 - fast, 1- normal, 2- slow"""
        pass

    def turnOrderCounters(
        self,
        turnOrder: int,
        adv_list: list["Adventurer"],
        assist_list: list["Assist"],
        memboost: dict[str, int | float],
        counterRate: float,
        react_on_st: bool,
        speed: int,
        logs: dict[str, list[str]],
    ):
        """speed : 0 - fast, 1- normal, 2- slow"""
        pass

    def ExtendShortenSingleEffect(self, attribute: str, turns: int, is_buff: bool):
        buffsDebuffs = self.get_boostCheckAdv(is_buff, attribute)
        if buffsDebuffs is None:
            return
        buffsDebuffs.duration += turns
        if buffsDebuffs.duration <= 0:
            self.boostCheckAdv.remove(buffsDebuffs)
            if not is_buff and attribute in getDamageDebuffs():
                curr_element = attribute.replace("_resist", "")
                if curr_element in getElements():
                    self.elementResistDownAdv[curr_element] = 0
                elif curr_element in ["physical", "magic"]:
                    self.typeResistDownAdv[curr_element] = 0
                else:
                    if "single" in attribute:
                        self.targetResistDownAdv["st"] = 0
                    else:
                        self.targetResistDownAdv["aoe"] = 0

    def ExtendReduceBuffs(self, turns: int):
        for buffsDebuffs in self.boostCheckAdv:
            if buffsDebuffs.isbuff:
                buffsDebuffs.duration += turns
        self.boostCheckAdv = [item for item in self.boostCheckAdv if item.duration > 0]

    def ExtendReduceDebuffs(self, turns: int):
        for buffsDebuffs in self.boostCheckAdv:
            if not buffsDebuffs.isbuff:
                buffsDebuffs.duration += turns
        tempExpiry = [item for item in self.boostCheckAdv if item.duration <= 0]
        self.boostCheckAdv = [item for item in self.boostCheckAdv if item.duration > 0]

        for buffsDebuffs in tempExpiry:
            curr_attribute = buffsDebuffs.attribute
            if curr_attribute in getDamageDebuffs():
                curr_element = curr_attribute.replace("_resist", "")
                if curr_element in getElements():
                    self.elementResistDownAdv[curr_element] = 0
                elif curr_element == "physical" or curr_element == "magic":
                    self.typeResistDownAdv[curr_element] = 0
                else:
                    if "single" in curr_attribute:
                        self.targetResistDownAdv["st"] = 0
                    else:
                        self.targetResistDownAdv["aoe"] = 0

    def get_buff_mod(self, buffName: str):
        ret = [
            item
            for item in self.boostCheckAdv
            if item.isbuff == True and item.attribute == buffName
        ]
        if len(ret) == 1:
            return ret[0].modifier
        else:
            # 0
            return 0


class Finn(Enemy):
    def FinnClear(self, adv_list):
        # self
        self.elementResistDownAdv = {
            "fire": 0,
            "water": 0,
            "thunder": 0,
            "earth": 0,
            "wind": 0,
            "light": 0,
            "dark": 0,
            "none": 0,
        }
        self.typeResistDownAdv = {"physical": 0, "magic": 0}
        self.targetResistDownAdv = {"st": 0, "aoe": 0}
        self.clearBuffs()
        self.clearDebuffs()
        # remove all buffs!
        for adv in adv_list:
            adv.clearBuffs()
            adv.clearDebuffs()

    # clear Finn's debuffs from boostCheckAdv and your adv's buffs boostCheckAdv
    def FinnStrMagBuff(self, adv_list: list["Adventurer"], turns: int):
        # take the max of str/mag buffs
        for adv in adv_list:
            adv.set_statsBoostAdv("strength", max(adv.statsBoostAdv["strength"], 1.5))
            adv.set_statsBoostAdv("magic", max(adv.statsBoostAdv["magic"], 1.5))
            adv.set_boostCheckAdv(True, "strength", 1.5, turns)
            adv.set_boostCheckAdv(True, "magic", 1.5, turns)
        # str/mag buff
        self.set_boostCheckAdv(True, "strength", 1.5, turns)
        self.set_boostCheckAdv(True, "magic", 1.5, turns)

    def FinnSelfEleBuff(self, element):
        self.set_boostCheckAdv(True, f"{element}_attack", 0.3, 4)

    def FinnFoesEleDebuff(self, adv_list, element):
        for adv in adv_list:
            adv.set_boostCheckAdv(False, f"{element}_resist", -0.3, 4)

    def turnOrder(self, turnOrder: int, adv_list: list, speed: int):
        if turnOrder in [2, 6] and speed == 2:
            self.FinnStrMagBuff(adv_list, 3)
        if turnOrder in [3, 6, 9, 12] and speed == 0:
            self.FinnSelfEleBuff("light")
        if turnOrder in [10] and speed == 2:
            self.FinnStrMagBuff(adv_list, 5)
        if turnOrder in [2, 5, 8, 11] and speed == 0:
            self.FinnSelfEleBuff("light")
        if turnOrder in [3, 7] and speed == 2:
            self.FinnClear(adv_list)

    def turnOrderCounters(
        self,
        turnOrder: int,
        adv_list: list["Adventurer"],
        assist_list: list["Assist"],
        memboost: dict[str, int | float],
        counterRng: float,
        react_on_st: bool,
        speed: int,
        logs: dict[str, list[str]],
    ):
        """speed : 0 - fast, 1- normal, 2- slow"""
        ret = 0
        if turnOrder + 1 in [1, 2, 3, 4, 5, 6, 8, 11, 12, 13, 14] and speed == 1:
            ret += counters(assist_list, adv_list, self, memboost, counterRng, logs)
            ret += counters(assist_list, adv_list, self, memboost, counterRng, logs)
        if turnOrder + 1 in [7, 9, 10, 15] and speed == 1:
            ret += counters(assist_list, adv_list, self, memboost, counterRng, logs)

        if turnOrder + 1 in [7, 10, 14] and speed == 0:
            ret += counters(assist_list, adv_list, self, memboost, counterRng, logs)
        if turnOrder + 1 in [15] and speed == 1:
            ret += counter(
                assist_list, adv_list, self, memboost, counterRng, react_on_st, logs
            )
        return ret


class Riveria(Enemy):
    def RiveriaPowerUp(self):
        self.set_boostCheckAdv(True, "magic", 0.30, 4)

    # debuff remove from list boostCheckAdv
    def RiveriaClear(self, adv_list):
        # remove all buffs!
        for adv in adv_list:
            adv.clearBuffs()

    def RiveriaDebuff(self, adv_list, element):
        for adv in adv_list:
            adv.set_boostCheckAdv(False, f"{element}_resist", -0.30, 4)

    def turnOrder(self, turnOrder: int, adv_list: list, speed: int):
        # debuff 1,2,4,5,7,8,9,10,11,12,13
        if turnOrder in [0, 1, 3, 4, 6, 7, 8, 9, 10, 11, 12] and speed == 1:
            self.RiveriaDebuff(adv_list, "light")
        if turnOrder in [3, 6, 7, 8, 10, 11] and speed == 1:
            self.RiveriaPowerUp()
        if turnOrder in [3, 7] and speed == 2:
            self.RiveriaClear(adv_list)

    def turnOrderCounters(
        self,
        turnOrder: int,
        adv_list: list["Adventurer"],
        assist_list: list["Assist"],
        memboost: dict[str, int | float],
        counterRng: float,
        react_on_st: bool,
        speed: int,
        logs: dict[str, list[str]],
    ):
        """speed : 0 - fast, 1- normal, 2- slow"""
        ret = 0
        if turnOrder + 1 in [1, 5, 6, 10] and speed == 1:
            ret += counters(assist_list, adv_list, self, memboost, counterRng, logs)
            ret += counters(assist_list, adv_list, self, memboost, counterRng, logs)

        if turnOrder + 1 in [14] and speed == 1:
            ret += counters(assist_list, adv_list, self, memboost, counterRng, logs)
            ret += counters(assist_list, adv_list, self, memboost, counterRng, logs)
            ret += counters(assist_list, adv_list, self, memboost, counterRng, logs)

        if turnOrder + 1 in [2, 3, 13] and speed == 1:
            ret += counters(assist_list, adv_list, self, memboost, counterRng, logs)

        if turnOrder + 1 in [2, 3, 4, 7, 8, 9, 11, 12, 13] and speed == 0:
            ret += counters(assist_list, adv_list, self, memboost, counterRng, logs)

        if turnOrder + 1 in [15] and speed == 1:
            ret += counter(
                assist_list, adv_list, self, memboost, counterRng, react_on_st, logs
            )
            ret += counter(
                assist_list, adv_list, self, memboost, counterRng, react_on_st, logs
            )
        return ret


class Gareth(Enemy):
    def GarethSelfBuff(self):
        self.set_boostCheckAdv(True, "physical_resist", 0.30, 4)
        self.set_boostCheckAdv(True, "magic_resist", 0.30, 4)
        self.set_boostCheckAdv(True, "counter_rate", 1.1, 4)

        # need to set actual calcs

    def GarethDebuff(self, adv_list):
        for adv in adv_list:
            adv.set_boostCheckAdv(False, "light_resist", -0.3, 4)

    def GarethClearBuffs(self, adv_list: list):
        # remove all buffs!
        for adv in adv_list:
            adv.clearBuffs()

    def GarethClearDebuffs(self):
        self.elementResistDownAdv = {
            "fire": 0,
            "water": 0,
            "thunder": 0,
            "earth": 0,
            "wind": 0,
            "light": 0,
            "dark": 0,
            "none": 0,
        }
        self.typeResistDownAdv = {"physical": 0, "magic": 0}
        self.targetResistDownAdv = {"st": 0, "aoe": 0}
        self.clearDebuffs()

    def clearDebuffs(self):
        # take the list but all the buffs with True is removed (keep all  the isbuff==False)
        self.boostCheckAdv = [
            item for item in self.boostCheckAdv if item.isbuff == True
        ]

    def turnOrder(self, turnOrder: int, adv_list: list, speed: int):
        """speed : 0 - fast, 1- normal, 2- slow"""
        if turnOrder + 1 in [6] and speed == 2:
            self.GarethClearBuffs(adv_list)
        if turnOrder + 1 in [10] and speed == 2:
            self.GarethClearDebuffs()
        if turnOrder + 1 in [4, 9] and speed == 2:
            self.GarethDebuff(adv_list)
        if turnOrder + 1 in [3, 9] and speed == 2:
            self.GarethSelfBuff()

    def turnOrderCounters(
        self,
        turnOrder: int,
        adv_list: list["Adventurer"],
        assist_list: list["Assist"],
        memboost: dict[str, int | float],
        counterRng: float,
        react_on_st: bool,
        speed: int,
        logs: dict[str, list[str]],
    ):
        """speed : 0 - fast, 1- normal, 2- slow"""
        ret = 0
        if turnOrder + 1 in [1, 15] and speed == 1:
            ret += counter(
                assist_list, adv_list, self, memboost, counterRng, react_on_st, logs
            )
            ret += counter(
                assist_list, adv_list, self, memboost, counterRng, react_on_st, logs
            )
        if turnOrder + 1 in [2] and speed == 1:
            ret += counter(
                assist_list, adv_list, self, memboost, counterRng, react_on_st, logs
            )
            ret += counters(assist_list, adv_list, self, memboost, counterRng, logs)

        if turnOrder + 1 in [6, 7, 11, 12] and speed == 1:
            ret += counters(assist_list, adv_list, self, memboost, counterRng, logs)
            ret += counter(
                assist_list, adv_list, self, memboost, counterRng, react_on_st, logs
            )

        if turnOrder + 1 in [3, 5, 8, 10, 13] and speed == 1:
            ret += counters(assist_list, adv_list, self, memboost, counterRng, logs)
            ret += counters(assist_list, adv_list, self, memboost, counterRng, logs)

        if turnOrder + 1 in [4, 9] and speed == 1:
            ret += counters(assist_list, adv_list, self, memboost, counterRng, logs)

        if turnOrder + 1 in [14] and speed == 1:
            ret += counters(assist_list, adv_list, self, memboost, counterRng, logs)
            ret += counters(assist_list, adv_list, self, memboost, counterRng, logs)
            ret += counters(assist_list, adv_list, self, memboost, counterRng, logs)

        return ret


class Ottarl(Enemy):
    def OttarlClear(self, adv_list: list["Adventurer"]):
        # remove all buffs!
        for adv in adv_list:
            adv.clearBuffs()

    def OttarlEndDebuff(self, adv_list):
        for adv in adv_list:
            adv.set_boostCheckAdv(False, "endurance", -0.3, 4)

    def turnOrder(self, turnOrder: int, adv_list: list, speed: int):
        """turnorder: 0-14"""
        # start of turn 5 and start of turn 9
        if (turnOrder == 3 or turnOrder == 7) and speed == 2:
            self.OttarlClear(adv_list)
        if turnOrder in [0, 2, 3, 4, 6, 7, 8, 11, 12, 13, 14] and not speed == 1:
            self.OttarlEndDebuff(adv_list)

    def turnOrderCounters(
        self,
        turnOrder: int,
        adv_list: list["Adventurer"],
        assist_list: list["Assist"],
        memboost: dict[str, int | float],
        counterRng: float,
        react_on_st: bool,
        speed: int,
        logs: dict[str, list[str]],
    ):
        """speed : 0 - fast, 1- normal, 2- slow"""
        ret = 0
        if turnOrder + 1 in [1, 3, 4, 5, 7, 8, 9, 11, 12, 15] and speed == 1:
            ret += counters(assist_list, adv_list, self, memboost, counterRng, logs)
        if turnOrder + 1 in [1] and speed == 1:
            ret += counter(
                assist_list, adv_list, self, memboost, counterRng, react_on_st, logs
            )
            ret += counter(
                assist_list, adv_list, self, memboost, counterRng, react_on_st, logs
            )
        if turnOrder + 1 in [2, 6, 10] and speed == 1:
            ret += counter(
                assist_list, adv_list, self, memboost, counterRng, react_on_st, logs
            )
            ret += counter(
                assist_list, adv_list, self, memboost, counterRng, react_on_st, logs
            )
            ret += counter(
                assist_list, adv_list, self, memboost, counterRng, react_on_st, logs
            )
        if turnOrder + 1 in [5, 9] and speed == 1:
            ret += counter(
                assist_list, adv_list, self, memboost, counterRng, react_on_st, logs
            )

        if turnOrder + 1 in [13, 14] and speed == 1:
            ret += counters(assist_list, adv_list, self, memboost, counterRng, logs)
            ret += counters(assist_list, adv_list, self, memboost, counterRng, logs)
        return ret


class Revis(Enemy):
    def RevisBuff(self):
        self.set_boostCheckAdv(True, "strength", 0.2, 4)

    def RevisAdd(self, type, type_mod):
        # type = physical/magic

        # debuffs own physical resists, take into account later magic resist debuffs
        self.set_typeResistDownAdv(type, min(self.typeResistDownAdv[type], type_mod))
        self.set_boostCheckAdv(True, "strength", 0.2, 4)
        self.set_boostCheckAdv(False, f"{type}_resist", type_mod, 4)

    def RevisInitial(self, type, type_mod):
        self.set_typeResistDownAdv(type, min(self.typeResistDownAdv[type], type_mod))
        self.set_boostCheckAdv(False, f"{type}_resist", type_mod, 4)

    def RevisClear(self):
        self.elementResistDownAdv = {
            "fire": 0,
            "water": 0,
            "thunder": 0,
            "earth": 0,
            "wind": 0,
            "light": 0,
            "dark": 0,
            "none": 0,
        }
        self.typeResistDownAdv = {"physical": 0, "magic": 0}
        self.targetResistDownAdv = {"st": 0, "aoe": 0}
        self.clearDebuffs()

    def turnOrder(self, turnOrder: int, adv_list: list, speed: int):
        """turnorder: 0-14"""
        # turn 1
        if turnOrder == 0 and speed == 0:
            self.RevisInitial(self.debuff_type, self.debuff_mod)
        # 6 and 10
        elif (turnOrder == 5 or turnOrder == 9) and speed == 0:
            self.RevisClear()
        # 4,8,12 both str buff and physical debuff
        elif (turnOrder == 3 or turnOrder == 7 or turnOrder == 11) and speed == 0:
            self.RevisAdd(self.debuff_type, self.debuff_mod)
        # end of turn 11 rebuff
        if turnOrder == 10 and speed == 2:
            self.RevisBuff()

    def turnOrderCounters(
        self,
        turnOrder: int,
        adv_list: list["Adventurer"],
        assist_list: list["Assist"],
        memboost: dict[str, int | float],
        counterRng: float,
        react_on_st: bool,
        speed: int,
        logs: dict[str, list[str]],
    ):
        """speed : 0 - fast, 1- normal, 2- slow"""
        ret = 0
        # double aoe
        if turnOrder + 1 in [5, 6, 7, 9, 10, 11] and speed == 1:
            ret += counters(assist_list, adv_list, self, memboost, counterRng, logs)
            ret += counters(assist_list, adv_list, self, memboost, counterRng, logs)

        # ailment aoe
        if turnOrder + 1 in [5, 6, 7, 8, 9, 10, 11, 12, 13, 14] and speed == 1:
            ret += counters(assist_list, adv_list, self, memboost, counterRng, logs)

        if turnOrder + 1 in [8, 12] and speed == 1:
            ret += counters(assist_list, adv_list, self, memboost, counterRng, logs)

        if turnOrder + 1 in [13, 14] and speed == 1:
            ret += counters(assist_list, adv_list, self, memboost, counterRng, logs)
            ret += counters(assist_list, adv_list, self, memboost, counterRng, logs)
            ret += counters(assist_list, adv_list, self, memboost, counterRng, logs)
        if turnOrder + 1 in [15] and speed == 1:
            ret += counter(
                assist_list, adv_list, self, memboost, counterRng, react_on_st, logs
            )
            ret += counter(
                assist_list, adv_list, self, memboost, counterRng, react_on_st, logs
            )
        return ret

    def __init__(
        self,
        elementResistDownBase={
            "fire": 0,
            "water": 0,
            "thunder": 0,
            "earth": 0,
            "wind": 0,
            "light": 0,
            "dark": 0,
            "none": 0,
        },
        typeResistDownBase={"physical": 0, "magic": 0},
        stats={
            "hp": 0,
            "mp": 0,
            "strength": 0,
            "magic": 0,
            "agility": 0,
            "endurance": 0,
            "dexterity": 0,
        },
        debuff_type="physical",
        debuff_mod=-0.5,
    ):
        Enemy.__init__(self, elementResistDownBase, typeResistDownBase, stats)
        self.debuff_type = debuff_type
        self.debuff_mod = debuff_mod
