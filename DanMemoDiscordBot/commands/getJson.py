import json
import os
import zipfile

import sys
from database.DBcontroller import DBcontroller
from database.DBcontroller import DatabaseEnvironment, DBConfig

from commands.cache import Cache

from datetime import datetime
import discord



async def run(client, ctx):
    if(ctx.message.author.id == 175045433662504961 or ctx.message.author.id == 271030697219588096 or ctx.message.author.id == 204693066500538368 or
    ctx.message.author.id == 226786914294824960 or ctx.message.author.id == 531944688366649345 or ctx.message.author.id == 630794201700892702 or ctx.message.author.id ==171619343946350592):
        cache = Cache()
        #SELECT a.adventurerid, a.characterid, a.typeid, a.alias, a.title, a.stars, a.limited, a.ascended,c.name, c.iscollab, t.name
        # unit_id, character_id, type_id, alias, unit_label, stars, is_limited, is_ascended, character_name, is_collab, type_name
        ad_list = cache.get_all_adventurers()
        #SELECT adventurerskillid, adventurerid, skillname, skilltype
        ad_skill = cache.get_all_adventurers_skills()
        #SELECT ase.AdventurerSkillEffectsid, ase.AdventurerSkillid, ase.duration, e.name AS element, m.value AS modifier, ty.name AS type, ta.name AS target, a.name AS attribute, s.name AS speed, ad.stars, ad.title, ad.alias, ad.limited, c.name
        ad_skill_effects=cache.get_all_adventurers_skills_effects()
        #SELECT addev.adventurerdevelopmentid,addev.name as development, m.value as modifier, a.name as attribute, ad.stars, ad.title, ad.alias, ad.limited, c.name
        ad_dev_effects = cache.get_all_adventurers_developments()
        #SELECT adventurerstatsid, adventurerid, advstats.attributeid, attri.name, value
        adv_stats = cache.get_all_adventurers_stats()

        #ad_skill_effects_ret = [skilleffect for skilleffect in ad_skill_effects if temp_word in skilleffect.type.lower()]
        # loop through all adventurers
        for current_adv in ad_list:
            current_adv_json = dict()
            #title
            current_adv_json["title"]=current_adv.unit_label
            #name
            current_adv_json["name"]=current_adv.character_name
            #type
            current_adv_json["type"]=current_adv.type_name
            #stars
            current_adv_json["stars"]=current_adv.stars
            #limited
            current_adv_json["limited"]=bool(current_adv.is_limited)

            #stats
            current_adv_json["stats"] = dict()
            ad_stats_temp = [stats for stats in adv_stats if current_adv.unit_id == stats.adventurerid]
            for curr_stats in ad_stats_temp:
                current_adv_json.get("stats")[curr_stats.attriname] = eval(curr_stats.value)

            #skills
            ad_skills_temp = [skills for skills in ad_skill if current_adv.unit_id == skills.adventurerid]
            current_adv_json["skills"] = dict()
            current_adv_json.get("skills")["special"] = dict()
            current_adv_json.get("skills")["combat"] = []
            current_adv_json.get("skills")["additonals"] = dict()

            for curr_skills in ad_skills_temp:
                ad_skills_effect_temp = [skills for skills in ad_skill_effects if curr_skills.adventurerskillid == skills.adventurerskillid]
                curr_effects_list = []

                for curr_effects in ad_skills_effect_temp:
                    curr_effects_dict = dict()
                    #duration, element, modifier, type, target, attribute, speed
                    if(curr_effects.duration != "" and curr_effects.duration != None):
                        curr_effects_dict["duration"] = curr_effects.duration

                    if(curr_effects.element != "" and curr_effects.element != None):
                        curr_effects_dict["element"] = curr_effects.element

                    if(curr_effects.modifier != "" and curr_effects.modifier != None):
                        curr_effects_dict["modifier"] = curr_effects.modifier

                    if(curr_effects.type != "" and curr_effects.type != None):
                        curr_effects_dict["type"] = curr_effects.type

                    if(curr_effects.target != "" and curr_effects.target != None):
                        curr_effects_dict["target"] = curr_effects.target

                    if(curr_effects.attribute != "" and curr_effects.attribute != None):
                        curr_effects_dict["attribute"] = curr_effects.attribute

                    if(curr_effects.speed != "" and curr_effects.speed != None):
                        curr_effects_dict["speed"] = curr_effects.speed
                    curr_effects_list.append(curr_effects_dict)

                #special
                if(curr_skills.skilltype =="special"):
                    current_adv_json.get("skills").get("special")["name"]=curr_skills.skillname
                    current_adv_json.get("skills").get("special")["effects"]=curr_effects_list
                #combat
                elif(curr_skills.skilltype =="combat"):
                    curr_combat_effect = dict()
                    curr_combat_effect["name"]=curr_skills.skillname
                    curr_combat_effect["effects"]=curr_effects_list
                    current_adv_json.get("skills").get("combat").append(curr_combat_effect)
                else:
                    current_adv_json.get("skills").get("additonals")["name"]=curr_skills.skillname
                    current_adv_json.get("skills").get("additonals")["effects"]=curr_effects_list
            #development
            current_adv_json.get("skills")["development"] = []
            ad_dev_effects_temp = [dev for dev in ad_dev_effects if current_adv.unit_id == dev.adventurerid]

            for curr_adv_dev in ad_dev_effects_temp:
                curr_adv_dev_dict = dict()
                curr_adv_dev_dict["name"] = curr_adv_dev.development
                curr_adv_dev_dict["effects"]=[{"attribute":curr_adv_dev.attribute,"modifier":curr_adv_dev.modifier}]
                current_adv_json.get("skills").get("development").append(curr_adv_dev_dict)

            with open('./testJsonAdv/{} - {}.json'.format(current_adv.unit_label, current_adv.character_name), 'w') as fp:
                json.dump(current_adv_json, fp,indent=4)

        # loop through all assists
        #unit_id, character_id, alias, unit_label, stars, is_limited, character_name, is_collab = row
        as_list = cache.get_all_assists()
        #assistsskillid, assistsid, skillname= row
        as_skill = cache.get_all_assists_skills()
        #assistskilleffectsid, assistskillid,duration, modifier, target, attribute, stars, title, alias, limited, character = row
        as_skill_effects=cache.get_all_assists_skills_effects()
        #assiststatsid, assistid,attributeid, attriname, value= row
        as_stats = cache.get_all_assists_stats()





        for current_as in as_list:
            current_as_json = dict()
            #title
            current_as_json["title"]=current_as.unit_label
            #name
            current_as_json["name"]=current_as.character_name
            #stars
            current_as_json["stars"]=current_as.stars
            #limited
            current_as_json["limited"]=bool(current_as.is_limited)

            #stats
            current_as_json["stats"] = dict()
            ad_stats_temp = [stats for stats in as_stats if current_as.unit_id == stats.assistid]
            for curr_stats in ad_stats_temp:
                current_as_json.get("stats")[curr_stats.attriname] = eval(curr_stats.value)

            #skills
            as_skills_temp = [skills for skills in as_skill if current_as.unit_id == skills.assistsid]
            current_as_json["skills"] = []

            for curr_skills in as_skills_temp:
                as_skills_effect_temp = [skills for skills in as_skill_effects if curr_skills.assistsskillid == skills.assistskillid]
                curr_effects_list = []

                for curr_effects in as_skills_effect_temp:
                    curr_effects_dict = dict()
                    #duration, element, modifier, type, target, attribute, speed
                    if(curr_effects.duration != "" and curr_effects.duration != None):
                        curr_effects_dict["duration"] = curr_effects.duration

                    if(curr_effects.modifier != "" and curr_effects.modifier != None):
                        curr_effects_dict["modifier"] = curr_effects.modifier

                    if(curr_effects.target != "" and curr_effects.target != None):
                        curr_effects_dict["target"] = curr_effects.target

                    if(curr_effects.attribute != "" and curr_effects.attribute != None):
                        curr_effects_dict["attribute"] = curr_effects.attribute
                    curr_effects_list.append(curr_effects_dict)

                curr_combat_effect = dict()
                curr_combat_effect["name"]=curr_skills.skillname
                curr_combat_effect["effects"]=curr_effects_list
                current_as_json.get("skills").append(curr_combat_effect)
            with open('./testJsonAs/{} - {}.json'.format(current_as.unit_label, current_as.character_name), 'w') as fp:
                json.dump(current_as_json, fp,indent=4)
        
        # ZIP THE FILES TO ATTACH FOR DISCORD
        zipf = zipfile.ZipFile('AdventurerJson.zip', 'w', zipfile.ZIP_DEFLATED)
        zipdir('testJsonAdv/', zipf)
        zipf.close()

        zipf2 = zipfile.ZipFile('AssistJson.zip', 'w', zipfile.ZIP_DEFLATED)
        zipdir('testJsonAs/', zipf2)
        zipf2.close()

        await ctx.send("Here is the current database in JSON format", files=[discord.File("./AdventurerJson.zip"),discord.File("./AssistJson.zip")])
        

def zipdir(path, ziph):
    # ziph is zipfile handle
    for root, dirs, files in os.walk(path):
        for file in files:
            ziph.write(os.path.join(root, file), 
                       os.path.relpath(os.path.join(root, file), 
                                       os.path.join(path, '..')))