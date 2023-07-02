from typing import TYPE_CHECKING, Dict, List, Optional, Tuple, Union, cast

from commands.entities.skills import AdventurerSkill
from commands.utils import getAilment, getElements

if TYPE_CHECKING:
    from commands.entities.adventurer import Adventurer
    from commands.entities.assist import Assist
    from commands.entities.enemy import Enemy


def commonDamageFunction():
    pass


def DamageFunction(
    skill: Optional[AdventurerSkill],
    adventurer: "Adventurer",
    enemy: "Enemy",
    memboost: Dict[str, Union[int, float]],
    skillRng: float,
) -> int:
    if skill is None:
        return 0

    # lowercase everything
    target = skill.target.lower()
    tempBoostName = skill.tempBoost.lower()
    powerCoefficientName = skill.powerCoefficient.lower()
    powerCoefficient = 1.0

    if target == "foe":
        if tempBoostName == "none":
            tempBoost = 1.0
        elif "normal2" in tempBoostName:
            tempBoost = 1.4
        elif "normal" in tempBoostName:
            tempBoost = 1.3
        else:
            tempBoost = 1.6

        if powerCoefficientName in ["low", "lo"]:
            powerCoefficient = 1.5
        elif powerCoefficientName in ["mid", "medium"]:
            powerCoefficient = 1.7
        elif powerCoefficientName == "high":
            powerCoefficient = 1.9
        elif powerCoefficientName == "super":
            powerCoefficient = 2.1
    else:
        if tempBoostName == "none":
            tempBoost = 1.0
        elif "normal" in tempBoostName:
            tempBoost = 1.4
        else:
            tempBoost = 1.7

        if powerCoefficientName in ["low", "lo"]:
            powerCoefficient = 1.1
        elif powerCoefficientName in ["mid", "medium"]:
            powerCoefficient = 1.15
        elif powerCoefficientName == "high":
            powerCoefficient = 1.2
        elif powerCoefficientName == "super":
            powerCoefficient = 1.4

    if "physical" in skill.type:
        stat_key = "strength"
        resist_key = "physical"
    else:
        stat_key = "magic"
        resist_key = "magic"

    power = adventurer.stats[stat_key]
    powerBoostAdv = adventurer.statsBoostAdv[stat_key]
    powerBoostAst = adventurer.statsBoostAst[stat_key]
    currMemBoost = memboost[stat_key]

    typeResistDownBase = enemy.typeResistDownBase[resist_key]
    typeResistDownAdv = enemy.typeResistDownAdv[resist_key]
    typeResistDownAst = enemy.typeResistDownAst[resist_key]
    # check enemy buffs p/m resist
    typeResistBuff = enemy.get_buff_mod(f"{resist_key}_resist")

    # get strength/magic debuff
    powerDebuff = adventurer.get_boostCheckAdv(False, stat_key)
    powerBoostDebuff = 0.0
    if powerDebuff is not None:
        powerBoostDebuff = abs(powerDebuff.modifier)

    if len(skill.index_to) != 0:
        power = 0
        powerBoostAdv = 0
        powerBoostAst = 0
        currMemBoost = 0  # TODO: dis really overwritten???
        powerCoefficient = powerCoefficient * 1.96
        for index_to_attributes in skill.index_to:
            power += adventurer.stats[index_to_attributes]
            powerBoostAdv += adventurer.statsBoostAdv[index_to_attributes]
            powerBoostAst += adventurer.statsBoostAst[index_to_attributes]
            currMemBoost += memboost[index_to_attributes]

    elementBoostDebuff = 0.0
    elementResistDownBase = 0.0
    elementResistDownAdv = 0.0
    elementResistDownAst = 0.0
    elementDamageBoostAdv = 0.0
    elementDamageBoostAst = 0.0
    if skill.element != "" and skill.noType != 1:
        elementResistDownBase = enemy.elementResistDownBase[skill.element]
        elementResistDownAdv = enemy.elementResistDownAdv[skill.element]
        elementResistDownAst = enemy.elementResistDownAst[skill.element]
        elementDamageBoostAdv = adventurer.elementDamageBoostAdv[skill.element]
        if memboost.get(f"{skill.element}_attack") is not None:
            elementDamageBoostAdv += memboost[f"{skill.element}_attack"]
        # elemental damage boost from weapon
        if adventurer.stats.get(skill.element) is not None:
            elementDamageBoostAdv += adventurer.stats[skill.element]
        elementDamageBoostAst = adventurer.elementDamageBoostAst[skill.element]
        # element debuff
        eleDebuff = adventurer.get_boostCheckAdv(False, f"{skill.element}_attack")
        if eleDebuff is not None:
            elementBoostDebuff = abs(eleDebuff.modifier)

    if target == "foe":
        targetResistDownAdv = enemy.targetResistDownAdv["st"]
        targetResistDownAst = enemy.targetResistDownAst["st"]
    # foes
    else:
        targetResistDownAdv = enemy.targetResistDownAdv["aoe"]
        targetResistDownAst = enemy.targetResistDownAst["aoe"]
    enemyEnd = enemy.stats["endurance"]

    elementBaseVal = 1 - skill.noType
    powerBoost = powerBoostAdv + powerBoostAst + currMemBoost - powerBoostDebuff
    elementBoost = elementBaseVal * (
        elementDamageBoostAdv + elementDamageBoostAst - elementBoostDebuff
    )
    elementResist = elementBaseVal * (
        elementResistDownBase + elementResistDownAdv + elementResistDownAst
    )  # TODO: test if these are really just signed modifier values
    typeResist = (
        typeResistDownBase + typeResistDownAdv + typeResistDownAst + typeResistBuff
    )  # TODO: really add the buff?
    targetResist = targetResistDownAdv + targetResistDownAst
    # Critical, Penetration, Counter damage etc. boosts
    devSkillBoost = adventurer.critPenBoost

    damage = (
        max(
            2 * power * tempBoost * (1 + powerBoost) - enemyEnd,
            0,
        )
        * (1 - elementResist - typeResist)
        * (1 + elementBoost)
        * (1 + devSkillBoost + 0.06)
        * (1 - targetResist)
        * powerCoefficient
        * 1.5
        * skill.extraBoost
        * skillRng
    )
    return int(damage)


def CounterDamageFunction(
    adventurer: "Adventurer",
    enemy: "Enemy",
    memboost: Dict[str, Union[int, float]],
    counterRng: float,
    extraBoost: float,
) -> int:
    # disable counters for adventurer
    if adventurer.isCounter == False:
        return 0

    counter = adventurer.adventurerCounter

    # magic units have light element always if not specified
    if counter.element.lower() == "none" and counter.noType == 1:
        if counter.type == "magic":
            counter.element = "light"
    # lowercase everything
    target = counter.target.lower()
    tempBoost = 1.0

    if "physical" in counter.type:
        stat_key = "strength"
        resist_key = "physical"
        powerCoefficient = 1.0
    else:
        stat_key = "magic"
        resist_key = "magic"
        powerCoefficient = 0.75

    power = adventurer.stats[stat_key]
    powerBoostAdv = adventurer.statsBoostAdv[stat_key]
    powerBoostAst = adventurer.statsBoostAst[stat_key]
    currMemBoost = memboost[stat_key]

    typeResistDownBase = enemy.typeResistDownBase[resist_key]
    typeResistDownAdv = enemy.typeResistDownAdv[resist_key]
    typeResistDownAst = enemy.typeResistDownAst[resist_key]
    # check enemy buffs p/m resist
    typeResistBuff = enemy.get_buff_mod(f"{resist_key}_resist")

    # get strength/magic debuff
    powerDebuff = adventurer.get_boostCheckAdv(False, stat_key)
    powerBoostDebuff = 0.0
    if powerDebuff is not None:
        powerBoostDebuff = abs(powerDebuff.modifier)

    elementBoostDebuff = 0.0
    elementResistDownBase = 0.0
    elementResistDownAdv = 0.0
    elementResistDownAst = 0.0
    elementDamageBoostAdv = 0.0
    elementDamageBoostAst = 0.0
    if counter.element != "" and counter.noType != 1:
        elementResistDownBase = enemy.elementResistDownBase[counter.element]
        elementResistDownAdv = enemy.elementResistDownAdv[counter.element]
        elementResistDownAst = enemy.elementResistDownAst[counter.element]
        elementDamageBoostAdv = adventurer.elementDamageBoostAdv[counter.element]
        if memboost.get(f"{counter.element}_attack") is not None:
            elementDamageBoostAdv += memboost[f"{counter.element}_attack"]
        # elemental damage boost from weapon
        if adventurer.stats.get(counter.element) is not None:
            elementDamageBoostAdv += adventurer.stats[counter.element]
        elementDamageBoostAst = adventurer.elementDamageBoostAst[counter.element]
        # element debuff
        eleDebuff = adventurer.get_boostCheckAdv(False, f"{counter.element}_attack")
        if eleDebuff is not None:
            elementBoostDebuff = abs(eleDebuff.modifier)

    if target == "foe":
        targetResistDownAdv = enemy.targetResistDownAdv["st"]
        targetResistDownAst = enemy.targetResistDownAst["st"]
    # foes
    else:
        targetResistDownAdv = enemy.targetResistDownAdv["aoe"]
        targetResistDownAst = enemy.targetResistDownAst["aoe"]
    enemyEnd = enemy.stats["endurance"]

    elementBaseVal = 1 - counter.noType
    powerBoost = powerBoostAdv + powerBoostAst + currMemBoost - powerBoostDebuff
    elementBoost = elementBaseVal * (
        elementDamageBoostAdv + elementDamageBoostAst - elementBoostDebuff
    )
    elementResist = elementBaseVal * (
        elementResistDownBase + elementResistDownAdv + elementResistDownAst
    )
    typeResist = (
        typeResistDownBase + typeResistDownAdv + typeResistDownAst + typeResistBuff
    )  # TODO: really add the buff?
    targetResist = targetResistDownAdv + targetResistDownAst
    # Critical, Penetration, Counter damage etc. boosts
    devSkillBoost = adventurer.critPenBoost + adventurer.counterBoost

    damage = (
        max(
            2 * power * tempBoost * (1 + powerBoost) - enemyEnd,
            0,
        )
        * (1 - elementResist - typeResist)
        * (1 + elementBoost)
        * (1 + devSkillBoost + 0.06)
        * (1 - targetResist)
        * powerCoefficient
        * 1.5
        * extraBoost
        * counterRng
    )
    return int(damage)


def SADamageFunction(
    skill: Optional[AdventurerSkill],
    adventurer: "Adventurer",
    enemy: "Enemy",
    memboost: Dict[str, Union[int, float]],
    combo: int,
    saRng: float,
) -> int:
    """combo = int 1-4
    saRng = 0.96 - 1.04
    """
    if skill is None:
        return 0

    # lowercase everything
    target = skill.target.lower()
    tempBoostName = skill.tempBoost.lower()
    powerCoefficientName = skill.powerCoefficient.lower()
    powerCoefficient = 1.0

    if tempBoostName == "none":
        tempBoost = 1.0
    elif "normal" in tempBoostName:
        tempBoost = 1.4
    else:
        tempBoost = 1.7
    if skill.target == "foe":
        if powerCoefficientName in ["low", "lo"]:
            powerCoefficient = 1.5
        elif powerCoefficientName in ["mid", "medium"]:
            powerCoefficient = 1.7
        elif powerCoefficientName == "high":
            powerCoefficient = 1.9
        elif powerCoefficientName == "super":
            powerCoefficient = 2.1
        elif powerCoefficientName == "ultra":
            powerCoefficient = 4.0
    else:
        if powerCoefficientName in ["low", "lo"]:
            powerCoefficient = 1.1
        elif powerCoefficientName in ["mid", "medium"]:
            powerCoefficient = 1.15
        elif powerCoefficientName == "high":
            powerCoefficient = 1.2
        elif powerCoefficientName == "super":
            powerCoefficient = 1.4
        elif powerCoefficientName == "ultra":
            powerCoefficient = 3.6

    if "physical" in skill.type:
        stat_key = "strength"
        resist_key = "physical"
    else:
        stat_key = "magic"
        resist_key = "magic"

    tempPower = adventurer.stats[stat_key]
    tempPowerBoostAdv = adventurer.statsBoostAdv[stat_key]
    tempPowerBoostAst = adventurer.statsBoostAst[stat_key]
    tempMemBoost = memboost[stat_key]

    tempTypeResistDownBase = enemy.typeResistDownBase[resist_key]
    tempTypeResistDownAdv = enemy.typeResistDownAdv[resist_key]
    tempTypeResistDownAst = enemy.typeResistDownAst[resist_key]
    # check enemy buffs p/m resist
    tempTypeResistBuff = enemy.get_buff_mod(f"{resist_key}_resist")

    # get strength/magic debuff
    powerDebuff = adventurer.get_boostCheckAdv(False, stat_key)
    tempPowerBoostDebuff = 0
    if powerDebuff is not None:
        tempPowerBoostDebuff = abs(powerDebuff.modifier)
    else:
        tempPowerBoostDebuff = 0

    if len(skill.index_to) != 0:
        tempPower = 0
        tempPowerBoostAdv = 0.0
        tempPowerBoostAst = 0.0
        tempMemBoost = 0
        powerCoefficient = powerCoefficient * 1.96
        for index_to_attributes in skill.index_to:
            tempPower += adventurer.stats[index_to_attributes]
            tempPowerBoostAdv += adventurer.statsBoostAdv[index_to_attributes]
            tempPowerBoostAst += adventurer.statsBoostAst[index_to_attributes]
            tempMemBoost += memboost[index_to_attributes]
    tempElementBoostDebuff = 0.0
    if skill.element != "" and skill.noType != 1:
        # elementResistDownBase
        tempElementResistDownBase = enemy.elementResistDownBase[skill.element]
        # elementResistDownAdv
        tempElementResistDownAdv = enemy.elementResistDownAdv[skill.element]
        # elementResistDownAst
        tempElementResistDownAst = enemy.elementResistDownAst[skill.element]
        # elementDamageBoostAdv[location]

        tempElementDamageBoostAdv = adventurer.elementDamageBoostAdv[skill.element]
        if memboost.get(f"{skill.element}_attack") is not None:
            tempElementDamageBoostAdv += memboost[f"{skill.element}_attack"]
        # elemental damage boost from weapon
        if adventurer.stats.get(skill.element) is not None:
            tempElementDamageBoostAdv += cast(float, adventurer.stats[skill.element])
        # elementDamageBoostAst[location]
        tempElementDamageBoostAst = adventurer.elementDamageBoostAst[skill.element]
        # element debuff
        tempEleDebuff = adventurer.get_boostCheckAdv(False, f"{skill.element}_attack")
        if tempEleDebuff is not None:
            tempElementBoostDebuff = abs(tempEleDebuff.modifier)
    else:
        tempElementResistDownBase = 0.0
        tempElementResistDownAdv = 0.0
        tempElementResistDownAst = 0.0
        tempElementDamageBoostAdv = 0.0
        tempElementDamageBoostAst = 0.0

    # critPenBoost[location] # dev skillstempPowerBoostDebuff
    # targetResistDownAdv[targetTemp]
    # targetResistDownAst[targetTemp]
    if target == "foe":
        temptargetResistDownAdv = enemy.targetResistDownAdv["st"]
        temptargetResistDownAst = enemy.targetResistDownAst["st"]
    # foes
    else:
        temptargetResistDownAdv = enemy.targetResistDownAdv["aoe"]
        temptargetResistDownAst = enemy.targetResistDownAst["aoe"]

    temp_enemy_end = enemy.stats

    tempDamage = (
        (
            max(
                2
                * tempPower
                * tempBoost
                * (
                    1
                    + tempPowerBoostAdv
                    + tempPowerBoostAst
                    + tempMemBoost
                    - tempPowerBoostDebuff
                )
                - temp_enemy_end["endurance"],
                0,
            )
        )
        * (
            1
            - tempElementResistDownBase
            - tempElementResistDownAdv
            - tempElementResistDownAst
            - tempTypeResistDownBase
            - tempTypeResistDownAdv
            - tempTypeResistDownAst
            - tempTypeResistBuff
        )
        * (
            1
            + tempElementDamageBoostAdv
            + tempElementDamageBoostAst
            - tempElementBoostDebuff
        )
        * (1 + adventurer.critPenBoost + 0.06)
        * (1 - temptargetResistDownAdv - temptargetResistDownAst)
        * powerCoefficient
        * 1.5
        * (skill.extraBoost)
        * (0.8 + combo * 0.2)
        * saRng
    )
    # totalDamage = totalDamage + tempDamage
    # accumulateDamage[location] = accumulateDamage[location] + tempDamage
    return int(tempDamage)


def CombineSA(
    adventurerList: List["Adventurer"], enemy: "Enemy", character_list: list
) -> int:
    """(list of Adventurer, Enemy, list of boolean) -> int
    characterlist : [Char1,Char2,Char3,Char4]
      char1,char2,char3,char4 : 0 or 1
    """
    tempDamage = 0.0
    for character in range(0, 4):
        isPhysical = (
            adventurerList[character].stats["magic"]
            <= adventurerList[character].stats["strength"]
        )

        tempPower = max(
            adventurerList[character].stats["strength"],
            adventurerList[character].stats["magic"],
        )

        if isPhysical:
            temp_type = "physical"
            tempPowerBoostAdv = adventurerList[character].statsBoostAdv["strength"]
            tempPowerBoostAst = adventurerList[character].statsBoostAst["strength"]
            # get str debuff
            tempStrDebuff = adventurerList[character].get_boostCheckAdv(
                False, "strength"
            )
            if tempStrDebuff is not None:
                tempPowerBoostDebuff = abs(tempStrDebuff.modifier)
            else:
                tempPowerBoostDebuff = 0
        else:
            temp_type = "magic"
            tempPowerBoostAdv = adventurerList[character].statsBoostAdv["magic"]
            tempPowerBoostAst = adventurerList[character].statsBoostAst["magic"]
            # get magic debuff
            tempMagDebuff = adventurerList[character].get_boostCheckAdv(False, "magic")
            if tempMagDebuff is not None:
                tempPowerBoostDebuff = abs(tempMagDebuff.modifier)
            else:
                tempPowerBoostDebuff = 0
        tempDamage = tempDamage + (
            character_list[character]
            * (
                1.16
                * tempPower
                * (1 + tempPowerBoostAdv + tempPowerBoostAst - tempPowerBoostDebuff)
            )
        )

    tempDamage = (
        (max(tempDamage - enemy.stats["endurance"], 0))
        * (1 - enemy.typeResistDownAdv[temp_type] - enemy.typeResistDownAst[temp_type])
        * (1 - enemy.targetResistDownAdv["aoe"] - enemy.targetResistDownAst["aoe"])
        * 3.7
        * 1.5
    )
    print(f"Combine SA damage is {int(tempDamage)}")
    return int(tempDamage)


def interpretExtraBoostWrapper(
    skillEffect, adventurer: "Adventurer", enemy: "Enemy"
) -> float:
    # This wrapper is used to make "per each regen" type skills be interpreted
    # as both a "per each hp regen" and "per each mp regen" effect

    temp_list = skillEffect.attribute.split("_")
    if "regen" in temp_list and not "hp" in temp_list and not "mp" in temp_list:
        skillEffect.attribute = skillEffect.attribute.replace("regen", "hp_regen")
        extra_boosts_multiplier = interpretExtraBoost(skillEffect, adventurer, enemy)
        skillEffect.attribute = skillEffect.attribute.replace("hp_regen", "mp_regen")
        extra_boosts_multiplier += interpretExtraBoost(skillEffect, adventurer, enemy)
    else:
        extra_boosts_multiplier = interpretExtraBoost(skillEffect, adventurer, enemy)
    return extra_boosts_multiplier


def interpretExtraBoost(skillEffect, adventurer: "Adventurer", enemy: "Enemy") -> float:
    """(adventurerSkillEffect) -> float
    takes in a skill effect with attribute exists of "per_each" then parse it and return the extra boosts multiplier

    return: extra boosts multiplier
        for extraBoost
        {
            "modifier": "+40",
            "target": "skill",
            "attribute": "per_each_self_fire_attack_buff",

            # per_each = extraboost
            # target = self/target
            # attribute = inbtw
            # buff/debuff
            "speed": "None"
        },
    """
    extra_boosts_modifier_value = 0.0
    temp_list: list = skillEffect.attribute.split("_")
    # per each
    temp_list = temp_list[2:]
    try:
        temp_list.remove("skill")
    except:
        pass

    if temp_list[0] == "self":
        effect_lists = [adventurer.boostCheckAdv, adventurer.boostCheckAst]
    else:
        effect_lists = [enemy.boostCheckAdv, enemy.boostCheckAst]
    temp_list = temp_list[1:]
    attribute = "_".join(temp_list[: len(temp_list) - 1])
    attribute_type = temp_list[-1]

    for effect_list in effect_lists:
        for selfBuffs in effect_list:
            if selfBuffs.isbuff == (attribute_type == "buff"):
                if selfBuffs.attribute == attribute:
                    extra_boosts_modifier_value += (
                        int(skillEffect.modifier.strip()) / 100
                    )

    print(extra_boosts_modifier_value)
    return extra_boosts_modifier_value


def interpretSkillAdventurerAttack(
    skillEffectsWithName: Tuple[str, list], adventurer: "Adventurer", enemy: "Enemy"
) -> Optional[AdventurerSkill]:
    """(list of skillEffects, Adventurer, Enemy) -> AdventurerSkill or None
    None if there are no damage related effects
    AdventurerSkill if there is a damage related effect
    """
    # for index_to maybe list  {"modifier": "End. & Mag.", "target": "skill", "attribute": "indexed_to","speed": "None" }

    # test if skill effects empty
    if skillEffectsWithName:
        _, skillEffects = skillEffectsWithName
    else:
        skillEffects = []

    damage_skills = [
        x
        for x in skillEffects
        if x.attribute.lower().strip() == "damage"
        or (
            (x.element is not None and x.element != "")
            and (x.type == "physical_attack" or x.type == "magic_attack")
        )
    ]
    if len(damage_skills) > 0:
        damage_skill = damage_skills[0]
        # do the damage first if attribute == element and modifier== high/medium etc, type = attack
        index_to_effects = [
            x for x in skillEffects if x.attribute.lower().strip() == "indexed_to"
        ]
        index_to_modifier = set()
        # modifier is the index_to target
        for index_to_effect in index_to_effects:
            # "attribute" index_to
            index_to_modifier.add(index_to_effect.modifier)
        """
    For temp boosts
    {
        "modifier": "normal2_str",
        "target": "skill",
        "attribute": "temp_boost",
    }
    """
        temp_boost_effects = [
            x for x in skillEffects if x.attribute.lower().strip() == "temp_boost"
        ]
        if len(temp_boost_effects) > 0:
            temp_boost_mod = temp_boost_effects[0].modifier
        else:
            temp_boost_mod = "none"

        # loop through the variables to check if attribute exists
        extra_boosts_effects = [
            x for x in skillEffects if "per_each" in x.attribute.lower().strip()
        ]
        extra_boosts_value = 1.0
        # for example str/mag debuff
        if len(extra_boosts_effects) > 0:
            for extra_boosts in extra_boosts_effects:
                temp_extra_boosts = interpretExtraBoostWrapper(
                    extra_boosts, adventurer, enemy
                )
                extra_boosts_value = extra_boosts_value + temp_extra_boosts
        # SELECT ase.AdventurerSkillEffectsid, ase.AdventurerSkillid, ase.duration, e.name AS element, m.value AS modifier, ty.name AS type, ta.name AS target, a.name AS attribute, s.name AS speed, ad.stars, ad.title, ad.alias, ad.limited, c.name
        ret = AdventurerSkill(
            damage_skill.target,
            temp_boost_mod,
            damage_skill.modifier,
            extra_boosts_value,
            0,
            damage_skill.type,
            damage_skill.element,
            index_to_modifier,
        )
        return ret
    else:
        return None


def interpretSkillAdventurerEffects(
    skillEffectsWithName: Tuple[str, list],
    adventurer: "Adventurer",
    enemy: "Enemy",
    adv_list: List["Adventurer"],
):
    # test if skill effects empty
    if skillEffectsWithName:
        skillName, skillEffects = skillEffectsWithName
    else:
        skillEffects = []

    # go through the effects
    for skillEffect in skillEffects:
        if skillEffect.attribute is None:
            continue

        curr_attribute = skillEffect.attribute.strip().lower()

        try:
            curr_modifier = int(skillEffect.modifier) / 100
        except:
            curr_modifier = skillEffect.modifier

        current_target = skillEffect.target.strip()
        if current_target == "self":
            target_list = [adventurer]
        elif current_target == "allies":
            target_list = adv_list
        else:
            target_list = []

        # st/aoe resist down
        if curr_attribute in ["all_damage_resist", "single_damage_resist"]:
            if current_target in ["self", "allies"]:
                for curr_adv in target_list:
                    curr_adv.set_boostCheckAdv(
                        curr_modifier >= 0,
                        curr_attribute,
                        curr_modifier,
                        int(skillEffect.duration),
                    )
            elif current_target in ["foe", "foes"]:
                if curr_attribute == "single_damage_resist":
                    stat_key = "st"
                elif curr_attribute == "all_damage_resist":
                    stat_key = "aoe"
                temp_min = min(enemy.targetResistDownAdv[stat_key], curr_modifier)
                enemy.targetResistDownAdv[stat_key] = temp_min
                enemy.set_boostCheckAdv(
                    False, curr_attribute, curr_modifier, int(skillEffect.duration)
                )
        # physical/magic resist down
        elif curr_attribute in ["physical_resist", "magic_resist"]:
            if current_target in ["self", "allies"]:
                for curr_adv in target_list:
                    curr_adv.set_boostCheckAdv(
                        curr_modifier >= 0,
                        curr_attribute,
                        curr_modifier,
                        int(skillEffect.duration),
                    )
            elif current_target in ["foe", "foes"]:
                if curr_attribute == "physical_resist":
                    stat_key = "physical"
                elif curr_attribute == "magic_resist":
                    stat_key = "magic"
                temp_min = min(enemy.typeResistDownAdv[stat_key], curr_modifier)
                enemy.typeResistDownAdv[stat_key] = temp_min
                enemy.set_boostCheckAdv(
                    False, curr_attribute, curr_modifier, int(skillEffect.duration)
                )
        # STAT buffs including str/mag buffs
        elif curr_attribute in [
            "strength",
            "magic",
            "endurance",
            "dexterity",
            "agility",
        ]:
            if current_target in ["self", "allies"]:
                for curr_adv in target_list:
                    temp_max = max(
                        curr_adv.statsBoostAdv[curr_attribute.strip()], curr_modifier
                    )
                    curr_adv.statsBoostAdv[curr_attribute.strip()] = temp_max
                    curr_adv.set_boostCheckAdv(
                        curr_modifier >= 0,
                        curr_attribute,
                        curr_modifier,
                        int(skillEffect.duration),
                    )
            elif current_target in ["foe", "foes"]:
                enemy.set_boostCheckAdv(
                    False, curr_attribute, curr_modifier, int(skillEffect.duration)
                )
        # element Resist & elemental buffs Down
        elif curr_attribute in [f"{element}_attack" for element in getElements()]:
            if current_target in ["self", "allies"]:
                curr_element = curr_attribute.replace("_attack", "")
                for curr_adv in target_list:
                    temp_max = max(
                        curr_adv.elementDamageBoostAdv[curr_element],
                        curr_modifier,
                    )
                    curr_adv.elementDamageBoostAdv[curr_element] = temp_max
                    curr_adv.set_boostCheckAdv(
                        curr_modifier >= 0,
                        curr_attribute,
                        curr_modifier,
                        int(skillEffect.duration),
                    )
        elif curr_attribute in [f"{element}_resist" for element in getElements()]:
            if current_target in ["foe", "foes"]:
                curr_element = curr_attribute.replace("_resist", "")
                temp_min = min(enemy.elementResistDownAdv[curr_element], curr_modifier)
                enemy.elementResistDownAdv[curr_element] = temp_min
                enemy.set_boostCheckAdv(
                    False, curr_attribute, curr_modifier, int(skillEffect.duration)
                )
        # status buff/debuff extension/shortening
        elif curr_attribute == "status_debuff" and skillEffect.duration is not None:
            temp_duration = int(skillEffect.duration)
            if current_target in ["self", "allies"]:
                for curr_adv in target_list:
                    curr_adv.ExtendReduceDebuffs(temp_duration)
            elif current_target in ["foe", "foes"]:
                enemy.ExtendReduceDebuffs(temp_duration)
        elif curr_attribute == "status_buff" and skillEffect.duration is not None:
            temp_duration = int(skillEffect.duration)
            if current_target in ["self", "allies"]:
                for curr_adv in target_list:
                    curr_adv.ExtendReduceBuffs(temp_duration)
            elif current_target in ["foe", "foes"]:
                enemy.ExtendReduceBuffs(temp_duration)
        # single effect extension/shortening
        elif curr_attribute.endswith("_debuffs") or curr_attribute.endswith("_buffs"):
            is_buff = not curr_attribute.endswith("_debuffs")
            attribute = curr_attribute.replace("_debuffs", "")
            attribute = attribute.replace("_buffs", "")
            temp_duration = int(skillEffect.duration)
            if current_target in ["self", "allies"]:
                for curr_adv in target_list:
                    curr_adv.ExtendShortenSingleEffect(
                        attribute, temp_duration, is_buff
                    )
            elif current_target in ["foe", "foes"]:
                enemy.ExtendShortenSingleEffect(attribute, temp_duration, is_buff)

        # additional refresh
        elif curr_attribute == "additional_action":
            if current_target == "self":
                adventurer.set_additionals(int(skillEffect.duration), skillName)
        # removal skills
        elif "removal_no_assist" in curr_attribute:
            is_buff = not ("debuff" in curr_attribute)

            temp_list = curr_attribute.replace("removal_no_assist", "").split("_")
            try:
                temp_list.remove("buff")
            except:
                pass
            try:
                temp_list.remove("debuff")
            except:
                pass
            temp_attribute = " ".join(temp_list).strip()
            if current_target in ["self", "allies"]:
                for curr_adv in target_list:
                    curr_adv.pop_boostCheckAdv(is_buff, temp_attribute)
            elif current_target in ["foe", "foes"]:
                enemy.pop_boostCheckAdv(is_buff, temp_attribute)
        else:
            NumberTypes = (int, float)
            print(curr_attribute)
            if isinstance(curr_modifier, NumberTypes) and curr_attribute in [
                "sa_gauge_charge",
                "critical_rate",
                "penetration_rate",
                "counter_rate",
                "guard_rate",
                "heal_modifier",
                "hp_regen",
            ]:
                if current_target in ["foe", "foes"]:
                    # boostCheckEnemyAppend
                    enemy.set_boostCheckAdv(
                        curr_modifier >= 0,
                        curr_attribute,
                        curr_modifier,
                        int(skillEffect.duration),
                    )
                # ally exists for a heal but doesn't matter here because its a heal. but maybe in the future??
                if current_target in ["self", "allies"]:
                    # boostCheckAllyAppend
                    for curr_adv in target_list:
                        curr_adv.set_boostCheckAdv(
                            curr_modifier >= 0,
                            curr_attribute,
                            curr_modifier,
                            int(skillEffect.duration),
                        )


def interpretSkillAssistEffects(
    skillEffects, adventurer: "Adventurer", enemy: "Enemy", adv_list: list
):
    # go through the effects
    for skillEffect in skillEffects:
        curr_attribute = skillEffect.attribute
        if curr_attribute is not None:
            curr_attribute = curr_attribute.strip().lower()
            try:
                curr_modifier = int(skillEffect.modifier) / 100
            except:
                curr_modifier = skillEffect.modifier

            # st/aoe resist down
            if curr_attribute == "all_damage_resist":
                if skillEffect.target.strip() == "self":
                    adventurer.set_boostCheckAst(
                        curr_modifier >= 0,
                        curr_attribute,
                        curr_modifier,
                    )
                elif skillEffect.target.strip() == "allies":
                    for curr_adv in adv_list:
                        curr_adv.set_boostCheckAst(
                            curr_modifier >= 0,
                            curr_attribute,
                            curr_modifier,
                        )
                elif (
                    skillEffect.target.strip() == "foe"
                    or skillEffect.target.strip() == "foes"
                ):
                    temp_min = min(enemy.targetResistDownAst["aoe"], curr_modifier)
                    enemy.targetResistDownAst["aoe"] = temp_min
                    enemy.set_boostCheckAst(False, curr_attribute, curr_modifier)
            elif curr_attribute == "single_damage_resist":
                if skillEffect.target.strip() == "self":
                    adventurer.set_boostCheckAst(
                        curr_modifier >= 0,
                        curr_attribute,
                        curr_modifier,
                    )
                elif skillEffect.target.strip() == "allies":
                    for curr_adv in adv_list:
                        curr_adv.set_boostCheckAst(
                            curr_modifier >= 0,
                            curr_attribute,
                            curr_modifier,
                        )
                elif (
                    skillEffect.target.strip() == "foe"
                    or skillEffect.target.strip() == "foes"
                ):
                    temp_min = min(enemy.targetResistDownAst["st"], curr_modifier)
                    enemy.targetResistDownAst["st"] = temp_min
                    enemy.set_boostCheckAst(False, curr_attribute, curr_modifier)
            # physical/magic resist down
            elif curr_attribute == "physical_resist":
                if skillEffect.target.strip() == "self":
                    adventurer.set_boostCheckAst(
                        curr_modifier >= 0,
                        curr_attribute,
                        curr_modifier,
                    )
                elif skillEffect.target.strip() == "allies":
                    for curr_adv in adv_list:
                        curr_adv.set_boostCheckAst(
                            curr_modifier >= 0,
                            curr_attribute,
                            curr_modifier,
                        )
                elif (
                    skillEffect.target.strip() == "foe"
                    or skillEffect.target.strip() == "foes"
                ):
                    temp_min = min(enemy.typeResistDownAst["physical"], curr_modifier)
                    enemy.typeResistDownAst["physical"] = temp_min
                    enemy.set_boostCheckAst(False, curr_attribute, curr_modifier)
            elif curr_attribute == "magic_resist":
                if skillEffect.target.strip() == "self":
                    adventurer.set_boostCheckAst(
                        curr_modifier >= 0,
                        curr_attribute,
                        curr_modifier,
                    )
                elif skillEffect.target.strip() == "allies":
                    for curr_adv in adv_list:
                        curr_adv.set_boostCheckAst(
                            curr_modifier >= 0,
                            curr_attribute,
                            curr_modifier,
                        )
                elif (
                    skillEffect.target.strip() == "foe"
                    or skillEffect.target.strip() == "foes"
                ):
                    temp_min = min(enemy.typeResistDownAst["magic"], curr_modifier)
                    enemy.typeResistDownAst["magic"] = temp_min
                    enemy.set_boostCheckAst(False, curr_attribute, curr_modifier)
            # STATS || str/mag buffs
            elif curr_attribute in [
                "strength",
                "magic",
                "endurance",
                "dexterity",
                "agility",
            ]:
                if skillEffect.target.strip() == "self":
                    temp_max = max(
                        adventurer.statsBoostAst[curr_attribute.strip()], curr_modifier
                    )
                    adventurer.statsBoostAst[curr_attribute.strip()] = temp_max
                    adventurer.set_boostCheckAst(
                        curr_modifier >= 0,
                        curr_attribute,
                        curr_modifier,
                    )
                elif skillEffect.target.strip() == "allies":
                    for curr_adv in adv_list:
                        temp_max = max(
                            curr_adv.statsBoostAst[curr_attribute.strip()],
                            curr_modifier,
                        )
                        curr_adv.statsBoostAst[curr_attribute.strip()] = temp_max
                        curr_adv.set_boostCheckAst(
                            curr_modifier >= 0,
                            curr_attribute,
                            curr_modifier,
                        )
                elif (
                    skillEffect.target.strip() == "foe"
                    or skillEffect.target.strip() == "foes"
                ):
                    enemy.set_boostCheckAst(False, curr_attribute, curr_modifier)
            # element Resist & elemental buffs Down
            for curr_element in getElements():
                if curr_element in curr_attribute and "attack" in curr_attribute:
                    if skillEffect.target.strip() == "self":
                        temp_max = max(
                            adventurer.elementDamageBoostAst[curr_element],
                            curr_modifier,
                        )
                        adventurer.elementDamageBoostAst[curr_element] = temp_max
                        adventurer.set_boostCheckAst(
                            curr_modifier >= 0,
                            curr_attribute,
                            curr_modifier,
                        )
                    elif skillEffect.target.strip() == "allies":
                        for curr_adv in adv_list:
                            temp_max = max(
                                curr_adv.elementDamageBoostAst[curr_element],
                                curr_modifier,
                            )
                            curr_adv.elementDamageBoostAst[curr_element] = temp_max
                            curr_adv.set_boostCheckAst(
                                curr_modifier >= 0,
                                curr_attribute,
                                curr_modifier,
                            )
                elif curr_element in curr_attribute and "resist" in curr_attribute:
                    if (
                        skillEffect.target.strip() == "foe"
                        or skillEffect.target.strip() == "foes"
                    ):
                        temp_min = min(
                            enemy.elementResistDownAst[curr_element], curr_modifier
                        )
                        enemy.elementResistDownAst[curr_element] = temp_min
                        enemy.set_boostCheckAst(False, curr_attribute, curr_modifier)

            if "status" in curr_attribute and "debuff" in curr_attribute:
                temp_duration = int(skillEffect.duration)
                if skillEffect.target.strip() == "self":
                    adventurer.ExtendReduceDebuffs(temp_duration)
                elif skillEffect.target.strip() == "allies":
                    for curr_adv in adv_list:
                        curr_adv.ExtendReduceDebuffs(temp_duration)
                elif (
                    skillEffect.target.strip() == "foe"
                    or skillEffect.target.strip() == "foes"
                ):
                    enemy.ExtendReduceDebuffs(temp_duration)
            # status buff / debuffs extends/reduction
            elif "status" in curr_attribute and "buff" in curr_attribute:
                temp_duration = int(skillEffect.duration)
                if skillEffect.target.strip() == "self":
                    adventurer.ExtendReduceBuffs(temp_duration)
                elif skillEffect.target.strip() == "allies":
                    for curr_adv in adv_list:
                        curr_adv.ExtendReduceBuffs(temp_duration)
                elif (
                    skillEffect.target.strip() == "foe"
                    or skillEffect.target.strip() == "foes"
                ):
                    enemy.ExtendReduceBuffs(temp_duration)
            # single effect extension/shortening
            elif curr_attribute.endswith("_debuffs") or curr_attribute.endswith(
                "_buffs"
            ):
                is_buff = not curr_attribute.endswith("_debuffs")
                attribute = curr_attribute.replace("_debuffs", "")
                attribute = attribute.replace("_buffs", "")
                temp_duration = int(skillEffect.duration)
                if skillEffect.target.strip() in ["self", "allies"]:
                    target_list = (
                        [adventurer]
                        if skillEffect.target.strip() == "self"
                        else adv_list
                    )
                    for curr_adv in target_list:
                        curr_adv.ExtendShortenSingleEffect(
                            attribute, temp_duration, is_buff
                        )
                elif skillEffect.target.strip() in ["foe", "foes"]:
                    enemy.ExtendShortenSingleEffect(attribute, temp_duration, is_buff)
            else:
                NumberTypes = (int, float)
                if (
                    isinstance(curr_modifier, NumberTypes)
                    and curr_attribute is not None
                    and curr_attribute != "none"
                    and not curr_attribute in getAilment()
                ):
                    if (
                        skillEffect.target.strip() == "foe"
                        or skillEffect.target.strip() == "foes"
                    ):
                        # boostCheckEnemyAppend
                        enemy.set_boostCheckAst(
                            curr_modifier >= 0,
                            curr_attribute,
                            curr_modifier,
                        )
                    # ally exists for a heal but doesn't matter here because its a heal. but maybe in the future??
                    if skillEffect.target.strip() == "allies":
                        # boostCheckAllyAppend
                        for curr_adv in adv_list:
                            curr_adv.set_boostCheckAst(
                                curr_modifier >= 0,
                                curr_attribute,
                                curr_modifier,
                            )
                    if skillEffect.target.strip() == "self":
                        adventurer.set_boostCheckAst(
                            curr_modifier >= 0,
                            curr_attribute,
                            curr_modifier,
                        )


def counter(
    assist_list: List["Assist"],
    adv_list: List["Adventurer"],
    enemy: "Enemy",
    memboost: dict,
    counterRng: float,
    react_on_st: bool,
    logs: dict,
) -> int:
    ret = 0
    if react_on_st:
        ret = interpretInstantEffects(
            assist_list, adv_list, enemy, memboost, counterRng, logs
        )
    # take the avg
    # loop through and take the avg
    for adv in adv_list:
        temp_extra_boost = 1.0
        if adv.adventurerCounter.extraBoost is not None:
            temp_extra_boost += interpretExtraBoostWrapper(
                adv.adventurerCounter.extraBoost, adv, enemy
            )

        temp_counter_damage = int(
            CounterDamageFunction(
                adventurer=adv,
                enemy=enemy,
                memboost=memboost,
                counterRng=counterRng,
                extraBoost=temp_extra_boost,
            )
            * 0.25
        )
        adv.add_damage(temp_counter_damage)
        ret += temp_counter_damage
        # interpret the effects of counters
        interpretSkillAdventurerEffects(adv.counterEffects, adv, enemy, adv_list)

    logs["counters"].append(f"average single counter damage for {ret:,}")

    return ret


def counters(
    assist_list: List["Assist"],
    adv_list: List["Adventurer"],
    enemy: "Enemy",
    memboost: Dict[str, Union[int, float]],
    counterRng: float,
    logs: Dict[str, List[str]],
) -> int:
    ret = interpretInstantEffects(
        assist_list, adv_list, enemy, memboost, counterRng, logs
    )

    # take the avg
    # loop through and take the avg
    for adv in adv_list:
        # create adventurerCounter
        temp_extra_boost = 1.0
        if adv.adventurerCounter.extraBoost is not None:
            temp_extra_boost += interpretExtraBoostWrapper(
                adv.adventurerCounter.extraBoost, adv, enemy
            )
        temp_counter_damage = CounterDamageFunction(
            adventurer=adv,
            enemy=enemy,
            memboost=memboost,
            counterRng=counterRng,
            extraBoost=temp_extra_boost,
        )
        adv.add_damage(temp_counter_damage)
        logs["counters"].append(
            f"{adv.name} counter damage for {temp_counter_damage:,}"
        )
        ret += temp_counter_damage
        # interpret the effects of counters
        interpretSkillAdventurerEffects(adv.counterEffects, adv, enemy, adv_list)
    return ret


def interpretInstantEffects(
    assist_list: List["Assist"],
    adventurer_list: List["Adventurer"],
    enemy: "Enemy",
    memoria_boost: Dict[str, Union[int, float]],
    counter_rate: float,
    logs: Dict[str, List[str]],
) -> int:
    ret = 0
    for unit_num, assist in enumerate(assist_list):
        if (
            assist.instant_effects
            and assist.total_activations < assist.max_activations
            and assist.current_turn_activations < assist.activations_per_turn
        ):
            assist.total_activations += 1
            assist.current_turn_activations += 1

            current_adventurer = adventurer_list[unit_num]
            skill_tuple = ("instant_effect", assist.instant_effects)
            attack_skill = interpretSkillAdventurerAttack(
                skill_tuple, current_adventurer, enemy
            )
            damage = DamageFunction(
                attack_skill, current_adventurer, enemy, memoria_boost, counter_rate
            )
            interpretSkillAdventurerEffects(
                skill_tuple, current_adventurer, enemy, adventurer_list
            )

            logs["instant_actions"].append(f"{assist.name} instant action triggered")

            if damage > 0:
                ret += damage
                current_adventurer.add_damage(damage)
                logs["counters"].append(
                    f"{assist.name} used instant action, damage for {damage:,}"
                )

    return ret
