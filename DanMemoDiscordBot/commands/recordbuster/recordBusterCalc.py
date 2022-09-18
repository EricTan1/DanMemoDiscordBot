import ast
import configparser
from typing import Any, Dict, List, Optional, Tuple, Union, cast

import interactions
import numpy as np
from interactions.ext.files import CommandContext
from interactions.ext.wait_for import WaitForClient

from commands.cache import Cache
from commands.calculatorUtil import (
    CombineSA,
    CounterDamageFunction,
    DamageFunction,
    SADamageFunction,
    interpretSkillAdventurerAttack,
    interpretSkillAdventurerEffects,
    interpretSkillAssistEffects,
)
from commands.entities.adventurer import Adventurer
from commands.entities.assist import Assist
from commands.entities.enemy import Enemy, Finn, Gareth, Ottarl, Revis, Riveria
from commands.entities.skills import AdventurerCounter, AdventurerSkill
from commands.recordbuster.recordBusterCalcHandler import pageRBHandler
from commands.utils import getDifficultyMultiplier, getElements


async def run(
    client: WaitForClient,
    ctx: CommandContext,
    config_file: Optional[interactions.Attachment],
):
    if not config_file:
        await ctx.send(
            "For this to work, you need to download the file, edit it, and reupload it into the channel with ais bot in it via the /recordbuster-calculator command",
            files=interactions.File("RBConfig.txt"),
        )
    else:
        try:
            # to tell Discord this command may take longer than the default 3s timeout
            await ctx.defer()
            # if template attached start to verify it
            # attachment object only contains the URL, so have to download it first
            async with client._http._req._session.get(config_file.url) as request:
                contents = await request.content.read()
            contents_decode = contents.decode("utf-8")
            config = configparser.ConfigParser()
            config.read_string(contents_decode)
            # test2 =ast.literal_eval(test)
            # general settings
            # counterRate=config.getfloat("DEFAULT", "counterRate")
            original_memboost: Dict[str, Union[int, float]] = ast.literal_eval(
                config.get("DEFAULT", "memoria_boost")
            )
            try:
                memoria_turns: Dict[str, Tuple[int, int]] = ast.literal_eval(
                    config.get("DEFAULT", "memoria_turns")
                )
            except configparser.NoOptionError:
                raise CalculatorException("Please make sure you specify the duration of your memoria in the memoria_turns variable. If you don't know what this should look like, re-download the config file for an example.")

            ultRatio = config.getfloat("DEFAULT", "sa_rng")
            difficulty = config.getint("DEFAULT", "difficulty")
            # counter_RNG
            counterRate = config.getfloat("DEFAULT", "counter_rng")
            # skill_RNG
            skillRatio = config.getfloat("DEFAULT", "skill_rng")
            # units
            unit_titles = []
            ast_titles = []
            unit_stats_list = []
            unit_enable_counter = []
            for x in range(0, 6):
                unit_titles.append(config.get(f"unit{x+1}", "adventurer_title"))
                ast_titles.append(config.get(f"unit{x+1}", "assist_title"))
                unit_stats_list.append(
                    ast.literal_eval(config.get(f"unit{x+1}", "stats"))
                )
                unit_enable_counter.append(
                    config.getboolean(f"unit{x+1}", "enable_counter")
                )

            # enemy
            boss = config.get("enemy", "boss_name")
            boss_elementResistDownBase = ast.literal_eval(
                config.get("enemy", "elemental_resist")
            )
            boss_type_resist = ast.literal_eval(config.get("enemy", "type_resist"))
            boss_stats = ast.literal_eval(config.get("enemy", "stats"))

            # skillflow
            sf_list = []

            for x in range(0, 6):
                sf_list.append(ast.literal_eval(config.get("skillFlow", f"unit{x+1}")))
            skillflow = np.array(sf_list)

            # revis config
            revis_type_debuff = config.get("revis", "debuff")
            revis_type_mod = config.getfloat("revis", "debuff_modifier")

            ##############################
            # Init boss
            ##############################
            if boss.lower() == "revis":
                enemy: Enemy = Revis(
                    elementResistDownBase=boss_elementResistDownBase,
                    typeResistDownBase=boss_type_resist,
                    stats=boss_stats,
                    debuff_type=revis_type_debuff,
                    debuff_mod=revis_type_mod,
                )
            elif boss.lower() == "finn":
                enemy = Finn(
                    elementResistDownBase=boss_elementResistDownBase,
                    typeResistDownBase=boss_type_resist,
                    stats=boss_stats,
                )
            elif boss.lower() == "ottarl":
                enemy = Ottarl(
                    elementResistDownBase=boss_elementResistDownBase,
                    typeResistDownBase=boss_type_resist,
                    stats=boss_stats,
                )
            elif boss.lower() == "riveria":
                enemy = Riveria(
                    elementResistDownBase=boss_elementResistDownBase,
                    typeResistDownBase=boss_type_resist,
                    stats=boss_stats,
                )
            elif boss.lower() == "gareth":
                enemy = Gareth(
                    elementResistDownBase=boss_elementResistDownBase,
                    typeResistDownBase=boss_type_resist,
                    stats=boss_stats,
                )
            else:
                # error here?
                enemy = Enemy(
                    elementResistDownBase=boss_elementResistDownBase,
                    typeResistDownBase=boss_type_resist,
                    stats=boss_stats,
                )

            ##############################
            # Init Assists
            ##############################
            cache = Cache()
            # SELECT a.assistid, a.characterid, a.alias, a.title, a.stars, a.limited, c.name, c.iscollab
            ast_list = cache.get_all_assists()
            # SELECT assistskillid, assistid, skillname
            ast_skill = cache.get_all_assists_skills()
            # SELECT ase.assistskilleffectsid, ase.assistskillid, ase.duration, m.value as modifier, ta.name as target, a.name as attribute, assist.stars, assist.title, assist.alias, assist.limited, c.name
            ast_skill_effects = cache.get_all_assists_skills_effects()

            assist_list = []
            for assist in ast_titles:
                # parse assist titles by space
                temp_ast_title_list = assist.split(" ")
                is_mlb = False
                if len(temp_ast_title_list) > 0:
                    # its an mlb unit
                    if temp_ast_title_list[0].lower() == "mlb":
                        is_mlb = True
                        temp_ast_title_list.pop(0)
                    # rest of the title
                    temp_ast_title = " ".join(temp_ast_title_list)

                    ast_matches = [
                        x
                        for x in ast_list
                        if x.unit_label.lower() == temp_ast_title.lower()
                    ]
                    if len(ast_matches) > 0:
                        current_assist = ast_matches[0]
                        ast_skill_matches = [
                            x
                            for x in ast_skill
                            if x.assistsid == current_assist.unit_id
                        ]
                        # non mlb skill and mlb skill
                        for ast_skills in ast_skill_matches:
                            ast_skill_effects_matches = [
                                x
                                for x in ast_skill_effects
                                if x.assistskillid == ast_skills.assistsskillid
                            ]

                            if "++" in ast_skills.skillname and not (
                                "instant effect" in ast_skills.skillname
                            ):
                                if is_mlb:
                                    assist_list.append(
                                        Assist(
                                            ast_skill_effects_matches,
                                            f"[{current_assist.unit_label}] {current_assist.character_name}",
                                        )
                                    )
                            elif not is_mlb:
                                assist_list.append(
                                    Assist(
                                        ast_skill_effects_matches,
                                        f"[{current_assist.unit_label}] {current_assist.character_name}",
                                    )
                                )
                    # no assist
                    else:
                        raise CalculatorException(
                            f"Can not find assist: {temp_ast_title}"
                        )
                        # assist_list.append(Assist([],""))
                # no assist
                else:
                    raise CalculatorException("No assist found at all")
                    # assist_list.append(Assist([],""))

            ##############################
            # Init Units
            ##############################
            # loading in characters
            # unit_id, character_id, type_id, alias, unit_label, stars, is_limited, is_ascended, character_name, is_collab, type_name
            ad_list = cache.get_all_adventurers()
            # SELECT adventurerskillid, adventurerid, skillname, skilltype
            ad_skill = cache.get_all_adventurers_skills()
            # SELECT ase.AdventurerSkillEffectsid, ase.AdventurerSkillid, ase.duration, e.name AS element, m.value AS modifier, ty.name AS type, ta.name AS target, a.name AS attribute, s.name AS speed, ad.stars, ad.title, ad.alias, ad.limited, c.name
            ad_skill_effects = cache.get_all_adventurers_skills_effects()
            # SELECT addev.adventurerdevelopmentid,addev.name as development, m.value as modifier, a.name as attribute, ad.stars, ad.title, ad.alias, ad.limited, c.name
            ad_dev_effects = cache.get_all_adventurers_developments()
            # SELECT adventurerstatsid, adventurerid, advstats.attributeid, attri.name, value
            adv_stats = cache.get_all_adventurers_stats()
            ad_dev_skill_effects = (
                cache.get_all_adventurers_developments_skills_effects()
            )

            # all the units
            unit_list = []

            # organize skills into an actual list from order 1-4 (s1,s2,s3,sa)
            for unitsCounter in range(0, len(unit_titles)):
                # current_adv_json["title"]=current_adv.unit_label
                if unit_titles[unitsCounter].strip() != "":
                    adv_matches = [
                        x
                        for x in ad_list
                        if x.unit_label.lower() == unit_titles[unitsCounter].lower()
                    ]
                    if len(adv_matches) > 0:
                        curr_unit = adv_matches[0]
                        current_skills: Dict[str, List[Tuple[str, list]]] = {
                            "combat": [],
                            "special": [],
                            "additionals": [],
                        }

                        current_skills_agi_mod: Dict[str, List[str]] = {
                            "combat": [],
                            "special": [],
                            "additionals": [],
                        }
                        # get all skills related to the adventurer
                        adv_skill_matches = [
                            x for x in ad_skill if x.adventurerid == curr_unit.unit_id
                        ]

                        for adv_skills in adv_skill_matches:
                            # combine effects
                            adv_skill_effects_matches = [
                                x
                                for x in ad_skill_effects
                                if x.adventurerskillid == adv_skills.adventurerskillid
                            ]

                            adv_skill_effects_agi_matches = [
                                x
                                for x in adv_skill_effects_matches
                                if x.speed.lower() == "fast"
                            ]
                            if len(adv_skill_effects_agi_matches) > 0:
                                temp_list_agi = current_skills_agi_mod[
                                    adv_skills.skilltype
                                ]
                                temp_list_agi.append("fast")
                                current_skills_agi_mod[
                                    adv_skills.skilltype
                                ] = temp_list_agi
                            else:
                                adv_skill_effects_agi_matches = [
                                    x
                                    for x in adv_skill_effects_matches
                                    if x.speed.lower() == "slow"
                                ]
                                if len(adv_skill_effects_agi_matches) > 0:
                                    temp_list_agi = current_skills_agi_mod[
                                        adv_skills.skilltype
                                    ]
                                    temp_list_agi.append("slow")
                                    current_skills_agi_mod[
                                        adv_skills.skilltype
                                    ] = temp_list_agi
                                else:
                                    adv_skill_effects_agi_matches = [
                                        x
                                        for x in adv_skill_effects_matches
                                        if x.speed.lower() == "none"
                                    ]
                                    if len(adv_skill_effects_agi_matches) > 0:
                                        temp_list_agi = current_skills_agi_mod[
                                            adv_skills.skilltype
                                        ]
                                        temp_list_agi.append("none")
                                        current_skills_agi_mod[
                                            adv_skills.skilltype
                                        ] = temp_list_agi
                            temp_list = current_skills[adv_skills.skilltype]
                            temp_list.append(
                                (adv_skills.skillname, adv_skill_effects_matches)
                            )
                            current_skills[adv_skills.skilltype] = temp_list
                        # unit_skills.append(current_skills)
                        # development skills that boosts crit/pen dmg and counter damage
                        # counter damage
                        adv_dev_matches = [
                            x
                            for x in ad_dev_effects
                            if x.adventurerid == curr_unit.unit_id
                        ]
                        adv_dev_effects_matches = []
                        tempCounterBoost = 0.0
                        tempCritPenBoost = 0.0

                        # tempCounter
                        tempCounter_extraBoost = None
                        tempCounter_skillEffects: Optional[Tuple[str, list]] = None
                        tempCounter_element = ""
                        # tempAttack
                        tempAttack_element = ""
                        is_physical = (
                            unit_stats_list[unitsCounter]["strength"]
                            >= unit_stats_list[unitsCounter]["magic"]
                        )
                        if is_physical:
                            tempCounterAttack_type = "physical"
                        else:
                            tempCounterAttack_type = "magic"
                        # counter attack type unit_stats_list[unitsCounter]

                        for curr_adv_dev_skill in adv_dev_matches:
                            adv_dev_effects_matches = [
                                x
                                for x in ad_dev_skill_effects
                                if x.adventurerdevelopmentid
                                == curr_adv_dev_skill.adventurerdevelopmentid
                            ]

                            for curr_adv_dev_skill_effects in adv_dev_effects_matches:
                                dev_attribute_name = (
                                    curr_adv_dev_skill_effects.attribute
                                )
                                try:
                                    dev_modifier_percent = (
                                        int(curr_adv_dev_skill_effects.modifier.strip())
                                        / 100
                                    )
                                except:
                                    dev_modifier_percent = 0.0
                                # elemental counters and normal attacks check all?
                                # Water Manifestation: H || element manifestation:letter
                                # if("manifestation" in curr_adv_dev_skill.development.lower()):
                                # tempElementAttackCounter = curr_adv_dev_skill.development.lower().split(" ")[0]

                                if "countering" in dev_attribute_name.lower():
                                    for element in getElements():
                                        if (
                                            element
                                            in curr_adv_dev_skill.development.lower()
                                        ):
                                            tempCounter_element = element
                                    # check if it has other effects and record it yukina etc
                                    tempCounter_skillEffects = (
                                        "counter",
                                        adv_dev_effects_matches,
                                    )
                                if "attacking" in dev_attribute_name.lower():
                                    for element in getElements():
                                        if (
                                            element
                                            in curr_adv_dev_skill.development.lower()
                                        ):
                                            tempAttack_element = element
                                if "counter_attack" in dev_attribute_name.lower():
                                    for element in getElements():
                                        if (
                                            element
                                            in curr_adv_dev_skill.development.lower()
                                        ):
                                            tempCounter_element = element
                                            tempAttack_element = element
                                # if("attacking" in dev_attribute_name.lower()):

                                # if("will of" in curr_adv_dev_skill.development.lower()):
                                # tempElementAttackCounter = curr_adv_dev_skill.development.lower().split(" ")[2]
                                # disable counter if healing

                                # pressure skills decrease attacks
                                # ray counter extends
                                # disturbance
                                # Hierophant
                                if "per_each" in dev_attribute_name.lower():
                                    tempCounter_extraBoost = curr_adv_dev_skill_effects

                                if (
                                    "encouragement"
                                    in curr_adv_dev_skill.development.lower()
                                    or "blessing"
                                    in curr_adv_dev_skill.development.lower()
                                    or "disturbance"
                                    in curr_adv_dev_skill.development.lower()
                                    or "hierophant"
                                    in curr_adv_dev_skill.development.lower()
                                ):
                                    unit_enable_counter[unitsCounter] = False
                                # Counter Damage & counter_damage
                                if (
                                    "counter" in dev_attribute_name.lower()
                                    and "damage" in dev_attribute_name.lower()
                                ):
                                    tempCounterBoost += dev_modifier_percent
                                # Penetration Damage & penetration_damage
                                if (
                                    "penetration" in dev_attribute_name.lower()
                                    and "damage" in dev_attribute_name.lower()
                                ):
                                    tempCritPenBoost += dev_modifier_percent
                                # Critical damage & critical_damage
                                if (
                                    "critical" in dev_attribute_name.lower()
                                    and "damage" in dev_attribute_name.lower()
                                ):
                                    tempCritPenBoost += dev_modifier_percent
                                # counter extra boosts calc >:(
                        # tempCounter_noType = 0, tempAttack_noType = 0
                        if tempCounter_element == "":
                            tempCounter_noType = 1
                        else:
                            tempCounter_noType = 0

                        if tempAttack_element == "":
                            tempAttack_noType = 1
                        else:
                            tempAttack_noType = 0

                        tempCounter = AdventurerCounter(
                            target="foe",
                            extraBoost=tempCounter_extraBoost,
                            noType=tempCounter_noType,
                            type=tempCounterAttack_type,
                            element=tempCounter_element,
                        )
                        tempAttack = AdventurerCounter(
                            target="foe",
                            extraBoost=None,
                            noType=tempAttack_noType,
                            type=tempCounterAttack_type,
                            element=tempAttack_element,
                        )
                        # Create new adv object
                        unit_list.append(
                            Adventurer(
                                stats=unit_stats_list[unitsCounter],
                                counterBoost=tempCounterBoost,
                                critPenBoost=tempCritPenBoost,
                                current_skills=current_skills,
                                current_skills_agi_mod=current_skills_agi_mod,
                                turnOrder=skillflow[unitsCounter],
                                adventurerCounter=tempCounter,
                                adventurerAttack=tempAttack,
                                name=f"[{unit_titles[unitsCounter]}] {curr_unit.character_name}",
                                isCounter=unit_enable_counter[unitsCounter],
                                counterEffects=tempCounter_skillEffects,
                            )
                        )
                    else:
                        raise CalculatorException(
                            f"Can not find adventurer: {unit_titles[unitsCounter]}"
                        )
            ########################
            # Main Loop
            ########################
            # unit_list 0-5 aka 6 advs in order
            active_advs: List[Adventurer] = [
                unit_list[0],
                unit_list[1],
                unit_list[2],
                unit_list[3],
            ]  # always length 4 current active adv
            sac_counter = 0
            total_damage = 0
            logs = []

            memboost = original_memboost.copy()
            # set all current memoria boosts to 0 before first turn
            for key in memboost.keys():
                memboost[key] = 0.0

            for turn in range(0, 15):
                # logging init
                # enemy, unit{0-3}, turn
                turn_logs: Dict[str, Any] = {
                    "sa": [],
                    "combat_skills": [],
                    "counters": [],
                    "sacs": [],
                }
                logs.append(turn_logs)

                for key in memboost.keys():
                    # activate memoria boost if its starting turn matches the current turn
                    try:
                        if original_memboost[key] and memoria_turns[key][0] == turn + 1:
                            memboost[key] = original_memboost[key]
                    except KeyError:
                        raise CalculatorException(
                            "Make sure you also enter the active turns for your memoria in the memoria_turns section"
                        )
                    except ValueError:
                        raise CalculatorException(
                            "Make sure you enter memoria turns as: (<start turn>, <end turn>)"
                        )

                # assist skills first turn!!
                if turn == 0:
                    for assistCount in range(0, 4):
                        await interpretSkillAssistEffects(
                            assist_list[assistCount].skills,
                            active_advs[assistCount],
                            enemy,
                            active_advs,
                        )

                # logging buffs/debuffs
                turn_logs["turn"] = turn
                # print("Turn: {}".format(turn+1))
                turn_logs["enemy"] = str(enemy)
                for active_adv_log in range(0, len(active_advs)):
                    turn_logs[f"unit{active_adv_log}"] = str(
                        active_advs[active_adv_log]
                    )

                # SAs SA damage function, combine SA
                character_sa_list = []
                sa_counter = 0
                for active_adv in active_advs:
                    if active_adv.turnOrder[turn] == 4:
                        character_sa_list.append(1)
                        sa_counter += 1
                    else:
                        character_sa_list.append(0)
                # do the sa
                for active_adv in active_advs:
                    if active_adv.turnOrder[turn] == 4:
                        temp_adv_effects_list = await active_adv.get_specialSkill()
                        temp_adv_skill = await interpretSkillAdventurerAttack(
                            temp_adv_effects_list, active_adv, enemy
                        )
                        temp_damage = await SADamageFunction(
                            temp_adv_skill,
                            active_adv,
                            enemy,
                            memboost,
                            sa_counter,
                            ultRatio,
                        )

                        # print("{} SA damage for {}".format(active_advs[active_adv].name,int(temp_damage)))
                        temp_list_logs_sa = turn_logs["sa"]
                        temp_list_logs_sa.append(
                            f"{active_adv.name} SA damage for {temp_damage:,}"
                        )
                        turn_logs["sa"] = temp_list_logs_sa

                        await interpretSkillAdventurerEffects(
                            temp_adv_effects_list, active_adv, enemy, active_advs
                        )
                        total_damage += temp_damage
                        await active_adv.add_damage(temp_damage)

                if sa_counter > 1:
                    temp_damage = await CombineSA(active_advs, enemy, character_sa_list)
                    total_damage += temp_damage
                    temp_list_logs_sas = turn_logs["sa"]
                    temp_list_logs_sas.append(
                        f"Combined SA damage for {int(temp_damage):,}"
                    )
                    turn_logs["sa"] = temp_list_logs_sas
                # RB boss turn
                await enemy.turnOrder(turn, active_advs, 0)

                total_damage += await enemy.turnOrderCounters(
                    turn, active_advs, memboost, counterRate, 0, turn_logs
                )

                # combat skills
                # agi calculation
                # list of (temp_agi,current_speed,temp_adv_skill,active_adv)
                skills_priority_list: List[
                    Tuple[
                        float,
                        str,
                        Union[Optional[AdventurerSkill], AdventurerCounter],
                        Adventurer,
                        Tuple[str, list],
                    ]
                ] = []
                for active_adv in active_advs:
                    temp_agi: float = active_adv.stats["agility"] * (
                        1.0
                        + active_adv.statsBoostAdv["agility"]
                        + active_adv.statsBoostAst["agility"]
                    )
                    # combat
                    current_sf = active_adv.turnOrder[turn]
                    if current_sf in [0, 1, 2, 3]:
                        if current_sf in [1, 2, 3]:
                            current_speed = await active_adv.get_combatSkill_agi(
                                current_sf
                            )
                        else:
                            current_speed = "none"

                        adv_is_physical: bool = (
                            active_adv.stats["strength"] >= active_adv.stats["magic"]
                        )
                        # fast skills and agi war
                        if current_sf in [1, 2, 3]:
                            temp_adv_effects_list = await active_adv.get_combatSkill(
                                current_sf
                            )
                            temp_adv_skill = await interpretSkillAdventurerAttack(
                                temp_adv_effects_list, active_adv, enemy
                            )
                            # buff skills
                            if temp_adv_skill == None:
                                if current_speed == "fast":
                                    temp_agi *= 5.35
                                elif current_speed == "slow":
                                    temp_agi *= 0.1
                                else:
                                    temp_agi *= 1.75
                            # damage skills
                            else:
                                if current_speed == "fast":
                                    temp_agi *= 3.0
                                elif current_speed == "slow":
                                    temp_agi *= 0.01
                                else:
                                    if not adv_is_physical:
                                        temp_agi *= 0.5
                            skills_priority_list.append(
                                (
                                    temp_agi,
                                    current_speed,
                                    temp_adv_skill,
                                    active_adv,
                                    temp_adv_effects_list,
                                )
                            )
                        # auto attack
                        elif current_sf == 0:
                            if not adv_is_physical:
                                temp_agi *= 0.5

                            temp_adv_skill = active_adv.adventurerAttack
                            skills_priority_list.append(
                                (
                                    temp_agi,
                                    current_speed,
                                    temp_adv_skill,
                                    active_adv,
                                    ("", []),
                                )
                            )

                # sort the list by first element in tuple
                sorted_skills_priority_list = sorted(
                    skills_priority_list, key=lambda x: x[0], reverse=True
                )
                is_fast = True
                is_enemy_attacked = False
                for _ in range(0, len(sorted_skills_priority_list)):
                    removed_sorted_skill = sorted_skills_priority_list.pop(0)
                    if removed_sorted_skill[1] != "fast":
                        is_fast = False
                    # not fast skill then rb can go
                    if (
                        not is_fast or len(sorted_skills_priority_list) == 0
                    ) and not is_enemy_attacked:
                        await enemy.turnOrder(turn, active_advs, 1)
                        total_damage += await enemy.turnOrderCounters(
                            turn, active_advs, memboost, counterRate, 1, turn_logs
                        )
                        is_enemy_attacked = True
                        ### TODO: add instant effects

                    if (
                        isinstance(removed_sorted_skill[2], AdventurerSkill)
                        or removed_sorted_skill[2] == None
                    ):
                        cast_skill = cast(
                            Optional[AdventurerSkill], removed_sorted_skill[2]
                        )
                        temp_damage = await DamageFunction(
                            cast_skill,
                            removed_sorted_skill[3],
                            enemy,
                            memboost,
                            skillRatio,
                        )
                    elif isinstance(removed_sorted_skill[2], AdventurerCounter):
                        # no extra boosts for auto attacks
                        temp_damage = await CounterDamageFunction(
                            removed_sorted_skill[2],
                            removed_sorted_skill[3],
                            enemy,
                            memboost,
                            counterRate,
                            1,
                        )
                    temp_list_logs_combat = turn_logs["combat_skills"]
                    temp_list_logs_combat.append(
                        f"{removed_sorted_skill[3].name} skill {removed_sorted_skill[3].turnOrder[turn]} damage for {int(temp_damage):,}"
                    )
                    turn_logs["combat_skills"] = temp_list_logs_combat

                    # check if additional count == 0 so you dont attack this turn
                    perform_additional = False
                    if removed_sorted_skill[3].additionalCount > 0:
                        perform_additional = True
                        removed_sorted_skill[3].additionalCount -= 1
                    await interpretSkillAdventurerEffects(
                        removed_sorted_skill[4],
                        removed_sorted_skill[3],
                        enemy,
                        active_advs,
                    )
                    total_damage += temp_damage
                    await removed_sorted_skill[3].add_damage(temp_damage)

                    # additionals here
                    if perform_additional:
                        temp_adv_effects_list = await removed_sorted_skill[
                            3
                        ].get_current_additional()
                        temp_adv_skill = await interpretSkillAdventurerAttack(
                            temp_adv_effects_list, removed_sorted_skill[3], enemy
                        )
                        # damage
                        temp_damage = await DamageFunction(
                            temp_adv_skill,
                            removed_sorted_skill[3],
                            enemy,
                            memboost,
                            skillRatio,
                        )
                        # effects
                        await interpretSkillAdventurerEffects(
                            temp_adv_effects_list,
                            removed_sorted_skill[3],
                            enemy,
                            active_advs,
                        )
                        # logging and adding damage
                        temp_list_logs_additional = turn_logs["combat_skills"]
                        temp_list_logs_additional.append(
                            f"{removed_sorted_skill[3].name} additional damage for {temp_damage:,}"
                        )
                        turn_logs["combat_skills"] = temp_list_logs_additional
                        # damage adding
                        total_damage += temp_damage
                        await removed_sorted_skill[3].add_damage(temp_damage)

                # end of turn skills
                await enemy.turnOrder(turn, active_advs, 2)
                total_damage += await enemy.turnOrderCounters(
                    turn, active_advs, memboost, counterRate, 2, turn_logs
                )
                # if(turn+1 == 13):
                # for active_adv in active_advs:
                # print("{} with {} adv buffs".format(active_adv.name,active_adv.boostCheckAlliesAdv))

                # if(turn+1 == 2):
                # print("{} with {} adv buffs".format("Ottarl",enemy.boostCheckEnemyAdv))

                # allies tick down status buffs
                for active_adv in active_advs:
                    await active_adv.ExtendReduceBuffs(-1)
                    await active_adv.ExtendReduceDebuffs(-1)
                # enemy statuses tick down
                await enemy.ExtendReduceDebuffs(-1)
                await enemy.ExtendReduceBuffs(-1)

                # memoria expiry end of turn
                for key in memboost.keys():
                    if memboost[key] and memoria_turns[key][1] == turn + 1:
                        memboost[key] = 0.0

                # sacs
                if turn + 1 < 15 and sac_counter < 2:
                    # twince for two sacs same turn
                    for _ in range(2):
                        for i, active_adv in enumerate(active_advs):
                            # sac
                            if active_adv.turnOrder[turn + 1] == -1 and sac_counter < 2:
                                num_of_sac = len(active_advs) + sac_counter
                                temp_list_logs_sac = turn_logs["sacs"]
                                temp_list_logs_sac.append(
                                    f"{active_adv.name} leaving. {unit_list[num_of_sac].name} entering"
                                )
                                turn_logs["sacs"] = temp_list_logs_sac

                                active_advs[i] = unit_list[num_of_sac]

                                # assist
                                await interpretSkillAssistEffects(
                                    assist_list[num_of_sac].skills,
                                    unit_list[num_of_sac],
                                    enemy,
                                    active_advs,
                                )
                                sac_counter += 1
            # print('Current total damage is {}'.format(total_damage))
            # 6/8.5/10
            # print('Current total score is {}'.format(total_damage*8.5*2))
            await pageRBHandler(
                client,
                ctx,
                logs,
                total_damage,
                total_damage * getDifficultyMultiplier(difficulty) * 2,
                unit_list,
                assist_list,
            )

        except CalculatorException as e:
            await ctx.send(f"ERROR:\n```{e}```")


class CalculatorException(Exception):
    """Custom exception thrown whenever we detect an error with the inputs in the RBConfig file"""
