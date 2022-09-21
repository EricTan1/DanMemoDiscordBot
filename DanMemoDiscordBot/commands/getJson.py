import json
import os
import zipfile
from typing import List

import interactions
from interactions.ext.files import CommandContext

from commands.cache import Cache
from database.DBcontroller import EDITORS


async def run(ctx: CommandContext):
    if ctx.author.id in EDITORS:
        # to tell Discord this command may take longer than the default 3s timeout
        await ctx.defer()

        cache = Cache()
        # SELECT a.adventurerid, a.characterid, a.typeid, a.alias, a.title, a.stars, a.limited, a.ascended,c.name, c.iscollab, t.name
        # unit_id, character_id, type_id, alias, unit_label, stars, is_limited, is_ascended, character_name, is_collab, type_name
        ad_list = cache.get_all_adventurers()
        # SELECT adventurerskillid, adventurerid, skillname, skilltype
        ad_skill = cache.get_all_adventurers_skills()
        # SELECT ase.AdventurerSkillEffectsid, ase.AdventurerSkillid, ase.duration, e.name AS element, m.value AS modifier, ty.name AS type, ta.name AS target, a.name AS attribute, s.name AS speed, ad.stars, ad.title, ad.alias, ad.limited, c.name
        ad_skill_effects = cache.get_all_adventurers_skills_effects()
        # SELECT addev.adventurerdevelopmentid,addev.name as development, m.value as modifier, a.name as attribute, ad.stars, ad.title, ad.alias, ad.limited, c.name
        ad_dev_skills = cache.get_all_adventurers_developments()
        # SELECT addev.adventurerdevelopmentid,addev.name as development, m.value as modifier, a.name as attribute, ad.stars, ad.title, ad.alias, ad.limited, c.name, addev.adventurerid
        ad_dev_skill_effects = cache.get_all_adventurers_developments_skills_effects()
        # SELECT adventurerstatsid, adventurerid, advstats.attributeid, attri.name, value
        adv_stats = cache.get_all_adventurers_stats()

        # ad_skill_effects_ret = [skilleffect for skilleffect in ad_skill_effects if temp_word in skilleffect.type.lower()]
        # loop through all adventurers
        for current_adv in ad_list:
            current_adv_json = dict()
            # title
            current_adv_json["title"] = current_adv.unit_label
            # name
            current_adv_json["name"] = current_adv.character_name
            # type
            current_adv_json["type"] = current_adv.type_name
            # stars
            current_adv_json["stars"] = current_adv.stars
            # limited
            current_adv_json["limited"] = bool(current_adv.is_limited)

            # stats
            current_adv_json["stats"] = dict()
            ad_stats_temp = [
                stats
                for stats in adv_stats
                if current_adv.unit_id == stats.adventurerid
            ]
            for curr_stats in ad_stats_temp:
                current_adv_json["stats"][curr_stats.attriname] = eval(curr_stats.value)

            # skills
            ad_skills_temp = [
                skills
                for skills in ad_skill
                if current_adv.unit_id == skills.adventurerid
            ]
            current_adv_json["skills"] = dict()
            current_adv_json["skills"]["special"] = dict()
            current_adv_json["skills"]["combat"] = []
            current_adv_json["skills"]["additionals"] = []

            for curr_skills in ad_skills_temp:
                ad_skills_effect_temp = [
                    skills
                    for skills in ad_skill_effects
                    if curr_skills.adventurerskillid == skills.adventurerskillid
                ]
                curr_effects_list = set_skill_effects(
                    ad_skills_effect_temp,
                    is_assist=False,
                )

                # special
                if curr_skills.skilltype == "special":
                    current_adv_json["skills"]["special"][
                        "name"
                    ] = curr_skills.skillname
                    current_adv_json["skills"]["special"]["effects"] = curr_effects_list
                # combat
                elif curr_skills.skilltype == "combat":
                    curr_combat_effect = dict()
                    curr_combat_effect["name"] = curr_skills.skillname
                    curr_combat_effect["effects"] = curr_effects_list
                    current_adv_json["skills"]["combat"].append(curr_combat_effect)
                elif curr_skills.skilltype == "additionals":
                    curr_combat_effect = dict()
                    curr_combat_effect["name"] = curr_skills.skillname
                    curr_combat_effect["effects"] = curr_effects_list
                    current_adv_json["skills"]["additionals"].append(curr_combat_effect)
            # development
            current_adv_json["skills"]["development"] = []
            ad_dev_effects_temp = [
                dev for dev in ad_dev_skills if current_adv.unit_id == dev.adventurerid
            ]
            # 1 unit

            for curr_adv_dev in ad_dev_effects_temp:
                ad_dev_skills_effect_temp = [
                    skills
                    for skills in ad_dev_skill_effects
                    if curr_adv_dev.adventurerdevelopmentid
                    == skills.adventurerdevelopmentid
                ]
                curr_effects_list = set_skill_effects(
                    ad_dev_skills_effect_temp, is_assist=False
                )
                curr_adv_dev_dict = dict()
                curr_adv_dev_dict["name"] = curr_adv_dev.development
                curr_adv_dev_dict["effects"] = curr_effects_list
                current_adv_json["skills"]["development"].append(curr_adv_dev_dict)

            with open(
                f"./testJsonAdv/{current_adv.unit_label} - {current_adv.character_name}.json",
                "w",
            ) as fp:
                json.dump(current_adv_json, fp, indent=4)

        # loop through all assists
        # unit_id, character_id, alias, unit_label, stars, is_limited, character_name, is_collab = row
        as_list = cache.get_all_assists()
        # assistsskillid, assistsid, skillname= row
        as_skill = cache.get_all_assists_skills()
        # assistskilleffectsid, assistskillid,duration, modifier, target, attribute, stars, title, alias, limited, character = row
        as_skill_effects = cache.get_all_assists_skills_effects()
        # assiststatsid, assistid,attributeid, attriname, value= row
        as_stats = cache.get_all_assists_stats()

        for current_as in as_list:
            current_as_json = dict()
            # title
            current_as_json["title"] = current_as.unit_label
            # name
            current_as_json["name"] = current_as.character_name
            # stars
            current_as_json["stars"] = current_as.stars
            # limited
            current_as_json["limited"] = bool(current_as.is_limited)

            # stats
            current_as_json["stats"] = dict()
            ad_stats_temp = [
                stats for stats in as_stats if current_as.unit_id == stats.assistid
            ]
            for curr_stats in ad_stats_temp:
                current_as_json["stats"][curr_stats.attriname] = eval(curr_stats.value)

            # skills
            as_skills_temp = [
                skills for skills in as_skill if current_as.unit_id == skills.assistsid
            ]
            current_as_json["skills"] = dict()
            current_as_json["skills"]["regular"] = []
            current_as_json["skills"]["instant_effect"] = []

            for curr_skills in as_skills_temp:
                as_skills_effect_temp = [
                    skills
                    for skills in as_skill_effects
                    if curr_skills.assistsskillid == skills.assistskillid
                ]
                curr_effects_list = set_skill_effects(
                    as_skills_effect_temp, is_assist=True
                )

                if curr_skills.skilltype == "regular":
                    curr_combat_effect = dict()
                    curr_combat_effect["name"] = curr_skills.skillname
                    curr_combat_effect["effects"] = curr_effects_list
                    current_as_json["skills"]["regular"].append(curr_combat_effect)
                # instant_effect
                elif curr_skills.skilltype == "instant_effect":
                    curr_combat_effect = dict()
                    curr_combat_effect["name"] = curr_skills.skillname
                    curr_combat_effect["effects"] = curr_effects_list
                    current_as_json["skills"]["instant_effect"].append(
                        curr_combat_effect
                    )

            with open(
                f"./testJsonAs/{current_as.unit_label} - {current_as.character_name}.json",
                "w",
            ) as fp:
                json.dump(current_as_json, fp, indent=4)

        # ZIP THE FILES TO ATTACH FOR DISCORD
        zipf = zipfile.ZipFile("AdventurerJson.zip", "w", zipfile.ZIP_DEFLATED)
        zipdir("testJsonAdv/", zipf)
        zipf.close()

        zipf2 = zipfile.ZipFile("AssistJson.zip", "w", zipfile.ZIP_DEFLATED)
        zipdir("testJsonAs/", zipf2)
        zipf2.close()

        await ctx.send(
            "Here's the current database in JSON format",
            files=[
                interactions.File("./AdventurerJson.zip"),
                interactions.File("./AssistJson.zip"),
            ],
        )


def set_skill_effects(effects: list, is_assist: bool) -> List[dict]:
    curr_effects_list = []

    for curr_effects in effects:
        curr_effects_dict = dict()
        # duration, element, modifier, type, target, attribute, optional speed
        if curr_effects.duration:
            curr_effects_dict["duration"] = curr_effects.duration

        if curr_effects.modifier:
            curr_effects_dict["modifier"] = curr_effects.modifier

        if curr_effects.target and curr_effects.target.strip().lower() != "none":
            curr_effects_dict["target"] = curr_effects.target

        if curr_effects.attribute:
            curr_effects_dict["attribute"] = curr_effects.attribute

        if curr_effects.element:
            curr_effects_dict["element"] = curr_effects.element

        if curr_effects.type:
            curr_effects_dict["type"] = curr_effects.type

        if is_assist and curr_effects.maxActivations:
            curr_effects_dict["max_activations"] = curr_effects.maxActivations

        if (
            not is_assist
            and curr_effects.speed
            and curr_effects.speed.strip().lower() != "none"
        ):
            curr_effects_dict["speed"] = curr_effects.speed

        curr_effects_list.append(curr_effects_dict)

    return curr_effects_list


def zipdir(path: str, ziph: zipfile.ZipFile):
    # ziph is zipfile handle
    for root, dirs, files in os.walk(path):
        for file in files:
            ziph.write(
                os.path.join(root, file),
                os.path.relpath(os.path.join(root, file), os.path.join(path, "..")),
            )
