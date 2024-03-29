import ast
import configparser
from typing import cast

from aiohttp import ClientSession
from interactions import Attachment, Client, File, SlashContext

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
from commands.entities.skills import AdventurerCounter, AdventurerSkill, EnemyAttack
from commands.recordbuster.recordBusterCalcHandler import pageRBHandler
from commands.utils import getDifficultyMultiplier, getElements


async def run(
    client: Client,
    ctx: SlashContext,
    config_file: Attachment | None,
):
    if not config_file:
        await ctx.send(
            "For this to work, you need to download the file, edit it, and reupload it into the channel with ais bot in it via the /recordbuster-calculator command",
            files=File("RBConfig.txt"),
        )
    else:
        try:
            # if template attached start to verify it
            # attachment object only contains the URL, so have to download it first
            async with ClientSession() as session:
                async with session.get(config_file.url) as resp:
                    contents = await resp.text()
            config = configparser.ConfigParser()
            config.read_string(contents)
            # general settings
            original_memboost: dict[str, int | float] = ast.literal_eval(
                config.get("DEFAULT", "memoria_boost")
            )
            try:
                memoria_turns: dict[str, tuple[int, int]] = ast.literal_eval(
                    config.get("DEFAULT", "memoria_turns")
                )
            except configparser.NoOptionError:
                raise CalculatorException(
                    "Please make sure you specify the duration of your memoria in the memoria_turns variable. If you don't know what this should look like, re-download the config file for an example."
                )

            saRng = config.getfloat("DEFAULT", "sa_rng")
            difficulty = config.getint("DEFAULT", "difficulty")
            # counter_RNG
            counterRng = config.getfloat("DEFAULT", "counter_rng")
            # skill_RNG
            skillRng = config.getfloat("DEFAULT", "skill_rng")
            try:
                react_on_st = config.getboolean("DEFAULT", "react_on_st")
            except configparser.NoOptionError:
                raise CalculatorException(
                    "Please make sure to specify the 'react_on_st' option in the DEFAULT section"
                )
            except ValueError:
                raise CalculatorException(
                    "Please make sure you set 'react_on_st' to either True or False"
                )
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
            skillflows = []

            for x in range(0, 6):
                skillflows.append(
                    ast.literal_eval(config.get("skillFlow", f"unit{x+1}"))
                )

            # revis config
            revis_type_debuff = config.get("revis", "debuff")
            revis_type_mod = config.getfloat("revis", "debuff_modifier")

            ##############################
            # Init boss
            ##############################
            match boss.lower():
                case "revis":
                    enemy: Enemy = Revis(
                        elementResistDownBase=boss_elementResistDownBase,
                        typeResistDownBase=boss_type_resist,
                        stats=boss_stats,
                        debuff_type=revis_type_debuff,
                        debuff_mod=revis_type_mod,
                    )
                case "finn":
                    enemy = Finn(
                        elementResistDownBase=boss_elementResistDownBase,
                        typeResistDownBase=boss_type_resist,
                        stats=boss_stats,
                    )
                case "ottarl":
                    enemy = Ottarl(
                        elementResistDownBase=boss_elementResistDownBase,
                        typeResistDownBase=boss_type_resist,
                        stats=boss_stats,
                    )
                case "riveria":
                    enemy = Riveria(
                        elementResistDownBase=boss_elementResistDownBase,
                        typeResistDownBase=boss_type_resist,
                        stats=boss_stats,
                    )
                case "gareth":
                    enemy = Gareth(
                        elementResistDownBase=boss_elementResistDownBase,
                        typeResistDownBase=boss_type_resist,
                        stats=boss_stats,
                    )
                case _:  # error here?
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
            for assist_title in ast_titles:
                # parse assist titles by space
                temp_ast_title_list = assist_title.split(" ")
                is_mlb = False
                if len(temp_ast_title_list) > 0:
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
                        skill_effects = []
                        instant_effects = []
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
                                    skill_effects = ast_skill_effects_matches
                            elif (
                                not is_mlb
                                and not "instant effect" in ast_skills.skillname
                            ):
                                skill_effects = ast_skill_effects_matches
                            elif "instant effect" in ast_skills.skillname:
                                instant_effects = ast_skill_effects_matches

                        assist_list.append(
                            Assist(
                                f"[{current_assist.unit_label}] {current_assist.character_name}",
                                skill_effects,
                                instant_effects,
                            )
                        )

                    # no assist
                    else:
                        raise CalculatorException(
                            f"Cannot find assist: {temp_ast_title}"
                        )
                # no assist
                else:
                    raise CalculatorException("No assist found at all")

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
            ad_dev_skill_effects = (
                cache.get_all_adventurers_developments_skills_effects()
            )

            unit_list = []

            # organize skills into an actual list from order 1-4 (s1,s2,s3,sa)
            for unitsCounter in range(0, len(unit_titles)):
                if unit_titles[unitsCounter].strip() != "":
                    adv_matches = [
                        x
                        for x in ad_list
                        if x.unit_label.lower() == unit_titles[unitsCounter].lower()
                    ]
                    if len(adv_matches) > 0:
                        curr_unit = adv_matches[0]
                        current_skills: dict[str, list[tuple[str, list]]] = {
                            "combat": [],
                            "special": [],
                            "additionals": [],
                        }

                        current_skills_agi_mod: dict[str, list[str]] = {
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
                        # development skills that boosts crit/pen dmg and counter damage
                        adv_dev_matches = [
                            x
                            for x in ad_dev_effects
                            if x.adventurerid == curr_unit.unit_id
                        ]
                        adv_dev_effects_matches = []
                        tempCounterBoost = 0.0
                        tempCritPenBoost = 0.0

                        tempCounter_extraBoost = None
                        tempCounter_skillEffects: tuple[str, list] | None = None
                        tempCounter_element = ""

                        tempAttack_element = ""
                        is_physical = (
                            unit_stats_list[unitsCounter]["strength"]
                            >= unit_stats_list[unitsCounter]["magic"]
                        )
                        if is_physical:
                            tempCounterAttack_type = "physical"
                        else:
                            tempCounterAttack_type = "magic"

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

                                # if("will of" in curr_adv_dev_skill.development.lower()):
                                # tempElementAttackCounter = curr_adv_dev_skill.development.lower().split(" ")[2]

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
                        tempCounter_noType = 0
                        if tempCounter_element == "":
                            tempCounter_noType = 1

                        tempAttack_noType = 0
                        if tempAttack_element == "":
                            tempAttack_noType = 1

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
                                turnOrder=skillflows[unitsCounter],
                                adventurerCounter=tempCounter,
                                adventurerAttack=tempAttack,
                                name=f"[{unit_titles[unitsCounter]}] {curr_unit.character_name}",
                                isCounter=unit_enable_counter[unitsCounter],
                                counterEffects=tempCounter_skillEffects,
                            )
                        )
                    else:
                        raise CalculatorException(
                            f"Cannot find adventurer: {unit_titles[unitsCounter]}"
                        )
            ########################
            # Main Loop
            ########################
            # unit_list 0-5 aka 6 advs in order
            # always length 4 current active adv
            active_advs: list[Adventurer] = unit_list[0:4]
            active_assists: list[Assist] = assist_list[0:4]
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
                turn_logs: dict[str, list[str]] = {
                    "sa": [],
                    "combat_skills": [],
                    "instant_actions": [],
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
                    for assist_number in range(4):
                        interpretSkillAssistEffects(
                            assist_list[assist_number].skills,
                            active_advs[assist_number],
                            enemy,
                            active_advs,
                        )

                # logging buffs/debuffs
                turn_logs["enemy"] = enemy.get_log_effect_list()
                for adventurer_number in range(len(active_advs)):
                    turn_logs[f"unit{adventurer_number}"] = active_advs[
                        adventurer_number
                    ].get_log_effect_list()

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
                        temp_adv_effects_list = active_adv.get_specialSkill()
                        temp_adv_skill = interpretSkillAdventurerAttack(
                            temp_adv_effects_list, active_adv, enemy
                        )
                        temp_damage = SADamageFunction(
                            temp_adv_skill,
                            active_adv,
                            enemy,
                            memboost,
                            sa_counter,
                            saRng,
                        )

                        turn_logs["sa"].append(
                            f"{active_adv.name} SA damage for {temp_damage:,}"
                        )

                        interpretSkillAdventurerEffects(
                            temp_adv_effects_list, active_adv, enemy, active_advs
                        )
                        total_damage += temp_damage
                        active_adv.add_damage(temp_damage)

                if sa_counter > 1:
                    temp_damage = CombineSA(active_advs, enemy, character_sa_list)
                    turn_logs["sa"].append(f"Combined SA damage for {temp_damage:,}")
                # RB boss turn
                enemy.turnOrder(turn, active_advs, 0)

                total_damage += enemy.turnOrderCounters(
                    turn,
                    active_advs,
                    active_assists,
                    memboost,
                    counterRng,
                    react_on_st,
                    0,
                    turn_logs,
                )

                # combat skills
                # agi calculation
                # list of (temp_agi,current_speed,temp_adv_skill,active_adv)
                skills_priority_list: list[
                    tuple[
                        float,
                        str,
                        AdventurerSkill | AdventurerCounter | EnemyAttack | None,
                        Adventurer,
                        tuple[str, list],
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
                            current_speed = active_adv.get_combatSkill_agi(current_sf)
                        else:
                            current_speed = "none"

                        adv_is_physical: bool = (
                            active_adv.stats["strength"] >= active_adv.stats["magic"]
                        )
                        # fast skills and agi war
                        if current_sf in [1, 2, 3]:
                            temp_adv_effects_list = active_adv.get_combatSkill(
                                current_sf
                            )
                            temp_adv_skill = interpretSkillAdventurerAttack(
                                temp_adv_effects_list, active_adv, enemy
                            )
                            # buff skills
                            if temp_adv_skill is None:
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

                first_non_fast_skill = 0
                for skill in sorted_skills_priority_list:
                    if skill[1] == "fast":
                        first_non_fast_skill += 1
                    else:
                        break
                # We schedule "normal" speed enemy actions to go
                # right after the last "fast" adventurer skill
                sorted_skills_priority_list.insert(
                    first_non_fast_skill, (0, "", EnemyAttack(), Adventurer(), ("", []))
                )

                for removed_sorted_skill in sorted_skills_priority_list:
                    if isinstance(removed_sorted_skill[2], EnemyAttack):
                        enemy.turnOrder(turn, active_advs, 1)
                        total_damage += enemy.turnOrderCounters(
                            turn,
                            active_advs,
                            active_assists,
                            memboost,
                            counterRng,
                            react_on_st,
                            1,
                            turn_logs,
                        )
                        continue

                    adventurer = removed_sorted_skill[3]

                    if (
                        isinstance(removed_sorted_skill[2], AdventurerSkill)
                        or removed_sorted_skill[2] is None
                    ):
                        cast_skill = cast(
                            AdventurerSkill | None, removed_sorted_skill[2]
                        )
                        temp_damage = DamageFunction(
                            cast_skill,
                            adventurer,
                            enemy,
                            memboost,
                            skillRng,
                        )
                    elif isinstance(removed_sorted_skill[2], AdventurerCounter):
                        # no extra boosts for auto attacks
                        temp_damage = CounterDamageFunction(
                            adventurer,
                            enemy,
                            memboost,
                            counterRng,
                            1,
                        )
                    turn_logs["combat_skills"].append(
                        f"{adventurer.name} skill {adventurer.turnOrder[turn]} damage for {int(temp_damage):,}"
                    )

                    # check if additional count == 0 so you dont attack this turn
                    additional_action = None
                    if adventurer.additionalCount > 0:
                        adventurer.additionalCount -= 1
                        additional_action = adventurer.get_current_additional()
                    interpretSkillAdventurerEffects(
                        removed_sorted_skill[4],
                        adventurer,
                        enemy,
                        active_advs,
                    )
                    total_damage += temp_damage
                    adventurer.add_damage(temp_damage)

                    # additionals here
                    if additional_action:
                        temp_adv_skill = interpretSkillAdventurerAttack(
                            additional_action, adventurer, enemy
                        )
                        # damage
                        temp_damage = DamageFunction(
                            temp_adv_skill,
                            adventurer,
                            enemy,
                            memboost,
                            skillRng,
                        )
                        # effects
                        interpretSkillAdventurerEffects(
                            additional_action,
                            adventurer,
                            enemy,
                            active_advs,
                        )
                        # logging and adding damage
                        aa_name = ""
                        if additional_action[0]:
                            aa_name = f"({additional_action[0]})"
                        turn_logs["combat_skills"].append(
                            f"{adventurer.name} additional {aa_name} damage for {temp_damage:,}"
                        )
                        # damage adding
                        total_damage += temp_damage
                        adventurer.add_damage(temp_damage)

                # end of turn skills
                enemy.turnOrder(turn, active_advs, 2)
                total_damage += enemy.turnOrderCounters(
                    turn,
                    active_advs,
                    active_assists,
                    memboost,
                    counterRng,
                    react_on_st,
                    2,
                    turn_logs,
                )

                # allies tick down status buffs
                for active_adv in active_advs:
                    active_adv.ExtendReduceDebuffs(-1)
                    active_adv.ExtendReduceBuffs(-1, turnCountdown=True)
                # enemy statuses tick down
                enemy.ExtendReduceDebuffs(-1)
                enemy.ExtendReduceBuffs(-1)

                # renew instant effects activations
                for assist in active_assists:
                    assist.current_turn_activations = 0

                # memoria expiry end of turn
                for key in memboost.keys():
                    if memboost[key] and memoria_turns[key][1] == turn + 1:
                        memboost[key] = 0.0

                # sacs
                if turn + 1 < 15 and sac_counter < 2:
                    # twice for two sacs same turn
                    for _ in range(2):
                        for i, active_adv in enumerate(active_advs):
                            # sac
                            if active_adv.turnOrder[turn + 1] == -1 and sac_counter < 2:
                                num_of_sac = len(active_advs) + sac_counter
                                turn_logs["sacs"].append(
                                    f"{active_adv.name} leaving. {unit_list[num_of_sac].name} entering"
                                )

                                active_advs[i] = unit_list[num_of_sac]
                                active_assists[i] = assist_list[num_of_sac]

                                # assist
                                interpretSkillAssistEffects(
                                    assist_list[num_of_sac].skills,
                                    unit_list[num_of_sac],
                                    enemy,
                                    active_advs,
                                )
                                sac_counter += 1
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
