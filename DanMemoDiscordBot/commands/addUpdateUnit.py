import json
import os
from io import BytesIO
from typing import Any

from aiohttp import ClientSession
from interactions import Attachment, File, SlashContext

from database.DBcontroller import EDITORS, DatabaseEnvironment, DBConfig, DBcontroller
from database.entities.Adventurer import (
    Adventurer,
    AdventurerDevelopment,
    AdventurerDevelopmentSkillEffects,
    AdventurerSkill,
    AdventurerSkillEffects,
    AdventurerStats,
)
from database.entities.Assist import (
    Assist,
    AssistSkill,
    AssistSkillEffects,
    AssistStats,
)
from database.entities.BaseConstants import (
    Attribute,
    Element,
    Modifier,
    Speed,
    Target,
    Type,
)
from database.entities.Character import Character

""" DB SETTING UP FILE json -> sql
"""


class AdventureC:
    def __init__(
        self,
        title: str,
        name: str,
        types: str,
        stars: int,
        limited: int,
        ascended: bool,
        stats: dict,
        skills: dict,
    ):
        self._title = title
        self._name = name
        self._type = types
        self._stars = stars
        self._limited = limited
        self.ascended = ascended
        self.stats = stats
        self.skills = skills


class AssistC:
    def __init__(
        self,
        title: str,
        name: str,
        stars: int,
        limited: int,
        stats: dict,
        skills: dict,
    ):
        self._title = title
        self._name = name
        self._stars = stars
        self._limited = limited
        self.stats = stats
        self.skills = skills


STATLIST = {
    "hp",
    "mp",
    "physical_attack",
    "magic_attack",
    "defense",
    "strength",
    "endurance",
    "dexterity",
    "agility",
    "magic",
}


class InsertCharacter:
    def __init__(self, database: DBcontroller):
        self._db = database

    def insertAdventurer(self, adventureComplete: AdventureC):
        characterid = self.getInsertCharacterID(adventureComplete._name, False)
        typeid = self.getBaseConstants(Type(None, adventureComplete._type), False)
        adventurerid = self.getInsertAdventurerID(
            characterid,
            typeid,
            adventureComplete._limited,
            adventureComplete._stars,
            adventureComplete._title,
        )
        temp_list = set()
        for attributeKeys in adventureComplete.stats:
            temp_list.add(attributeKeys.lower())
            attributeid = self.getBaseConstants(Attribute(None, attributeKeys), False)
            self._db.insertData(
                AdventurerStats(
                    None,
                    adventurerid,
                    attributeid,
                    str(adventureComplete.stats.get(attributeKeys)),
                )
            )
        if STATLIST != temp_list:
            print(
                "HEY STAT NAMED WRONG >:( FOR : "
                + adventureComplete._title
                + " "
                + adventureComplete._name
            )
            raise Exception("spam", "eggs")
        # skills
        for skillsKeys in adventureComplete.skills:
            skillsList = adventureComplete.skills[skillsKeys]
            if skillsKeys == "special":
                adventurerskillid = self._db.insertData(
                    AdventurerSkill(
                        None, adventurerid, skillsList.get("name"), skillsKeys
                    )
                )
                self.insertAdventurerSkillEffects(
                    adventurerskillid, skillsList["effects"]
                )
            elif skillsKeys == "combat":
                for skills in skillsList:
                    adventurerskillid = self._db.insertData(
                        AdventurerSkill(
                            None, adventurerid, skills.get("name"), skillsKeys
                        )
                    )
                    self.insertAdventurerSkillEffects(
                        adventurerskillid, skills["effects"]
                    )
            elif skillsKeys == "additionals":
                for skills in skillsList:
                    adventurerskillid = self._db.insertData(
                        AdventurerSkill(
                            None, adventurerid, skills.get("name"), skillsKeys
                        )
                    )
                    self.insertAdventurerSkillEffects(
                        adventurerskillid, skills["effects"]
                    )
            # development
            else:
                for skills in skillsList:
                    adventurerdevelopmentid = self._db.insertData(
                        AdventurerDevelopment(None, adventurerid, skills.get("name"))
                    )
                    self.insertAdventurerDevelopmentSkillEffects(
                        adventurerdevelopmentid, skills["effects"]
                    )

                    # self._db.insertData(AdventurerDevelopmentSkillEffects(None, adventurerdevelopmentid, skills.get("name"), attributeid, modifierid))

    def insertAdventurerSkillEffects(self, adventurerskillid, skilleffectList: list):
        ele_list = ["light", "wind", "fire", "dark", "ice", "water", "earth", "thunder"]
        # AdventurerSkillEffects SET UP
        for effects in skilleffectList:
            # Type+Element
            temp_type = effects.get("type")
            if temp_type is None:
                temp_type = ""
            temp_element = effects.get("element")
            if temp_element is None:
                temp_element = ""
            if temp_type.split("_")[0] in ele_list:
                temp_split = temp_type.split("_")
                temp_element = temp_split[0]
                if temp_type is not None and len(temp_split) == 3:
                    temp_type = temp_split[1] + "_" + temp_split[2]
            # Element
            eleid = self.getBaseConstants(Element(None, temp_element), False)
            # Type for skills
            typeid = self.getBaseConstants(Type(None, temp_type), False)
            temp_target = effects.get("target")
            temp_attribute = effects.get("attribute")
            temp_speed = effects.get("speed")
            temp_modifier = effects.get("modifier")
            if temp_modifier is None:
                temp_modifier = ""
            if len(temp_modifier) > 0 and temp_modifier[len(temp_modifier) - 1] == "%":
                temp_modifier = temp_modifier[: len(temp_modifier) - 1]
            targetid = self.getBaseConstants(Target(None, temp_target), False)
            attributeid = self.getBaseConstants(Attribute(None, temp_attribute), False)
            speedid = self.getBaseConstants(Speed(None, temp_speed), False)
            modifierid = self.getBaseConstants(Modifier(None, temp_modifier), True)
            # inserting effects
            self._db.insertData(
                AdventurerSkillEffects(
                    None,
                    adventurerskillid,
                    targetid,
                    attributeid,
                    modifierid,
                    effects.get("duration"),
                    typeid,
                    eleid,
                    speedid,
                )
            )

    def insertAdventurerDevelopmentSkillEffects(
        self, adventurerdevelopmentid, skilleffectList: list
    ):
        ele_list = ["light", "wind", "fire", "dark", "ice", "water", "earth", "thunder"]
        # AdventurerSkillEffects SET UP
        for effects in skilleffectList:
            # Type+Element
            temp_type = effects.get("type")
            if temp_type is None:
                temp_type = ""
            temp_element = effects.get("element")
            if temp_element is None:
                temp_element = ""
            if temp_type.split("_")[0] in ele_list:
                temp_split = temp_type.split("_")
                temp_element = temp_split[0]
                if temp_type is not None and len(temp_split) == 3:
                    temp_type = temp_split[1] + "_" + temp_split[2]
            # Element
            eleid = self.getBaseConstants(Element(None, temp_element), False)
            # Type for skills
            typeid = self.getBaseConstants(Type(None, temp_type), False)
            temp_target = effects.get("target")
            temp_attribute = effects.get("attribute")
            temp_speed = effects.get("speed")
            temp_modifier = effects.get("modifier")
            if temp_modifier is None:
                temp_modifier = ""
            if len(temp_modifier) > 0 and temp_modifier[len(temp_modifier) - 1] == "%":
                temp_modifier = temp_modifier[: len(temp_modifier) - 1]
            targetid = self.getBaseConstants(Target(None, temp_target), False)
            attributeid = self.getBaseConstants(Attribute(None, temp_attribute), False)
            speedid = self.getBaseConstants(Speed(None, temp_speed), False)
            modifierid = self.getBaseConstants(Modifier(None, temp_modifier), True)
            # inserting effects
            self._db.insertData(
                AdventurerDevelopmentSkillEffects(
                    None,
                    adventurerdevelopmentid,
                    targetid,
                    attributeid,
                    modifierid,
                    effects.get("duration"),
                    typeid,
                    eleid,
                    speedid,
                )
            )

    def insertAssist(self, assistComplete: AssistC):
        characterid = self.getInsertCharacterID(assistComplete._name, False)
        assistid = self.getInsertAssistID(
            characterid,
            int(assistComplete._limited),
            assistComplete._stars,
            assistComplete._title,
        )
        temp_list = set()
        for attributeKeys in assistComplete.stats:
            temp_list.add(attributeKeys.lower())
            attributeid = self.getBaseConstants(Attribute(None, attributeKeys), False)
            self._db.insertData(
                AssistStats(
                    None,
                    assistid,
                    attributeid,
                    str(assistComplete.stats.get(attributeKeys)),
                )
            )
        if STATLIST != temp_list:
            print(
                "HEY STAT NAMED WRONG >:( FOR : "
                + assistComplete._title
                + " "
                + assistComplete._name
            )
            raise Exception("spam", "eggs")
        # skills
        for skills_keys in assistComplete.skills:
            for skills_list in assistComplete.skills[skills_keys]:
                assistskillid = self._db.insertData(
                    AssistSkill(None, assistid, skills_list.get("name"), skills_keys)
                )
                self.insertAssistSkillEffects(assistskillid, skills_list["effects"])

    def insertAssistSkillEffects(self, assistskillid, skilleffectList: list):
        # assistskilleffects SET UP
        for effects in skilleffectList:
            temp_target = effects.get("target")
            temp_attribute = effects.get("attribute")
            temp_modifier = effects.get("modifier")
            temp_element = effects.get("element")
            temp_type = effects.get("type")
            if temp_modifier is None:
                temp_modifier = ""
            if len(temp_modifier) > 0 and temp_modifier[len(temp_modifier) - 1] == "%":
                temp_modifier = temp_modifier[: len(temp_modifier) - 1]
            targetid = self.getBaseConstants(Target(None, temp_target), False)
            attributeid = self.getBaseConstants(Attribute(None, temp_attribute), False)
            modifierid = self.getBaseConstants(Modifier(None, temp_modifier), True)
            if temp_element is None:
                temp_element = ""
            if temp_type is None:
                temp_type = ""

            eleid = self.getBaseConstants(Element(None, temp_element), False)
            typeid = self.getBaseConstants(Type(None, temp_type), False)

            # inserting effects
            self._db.insertData(
                AssistSkillEffects(
                    None,
                    assistskillid,
                    targetid,
                    attributeid,
                    modifierid,
                    effects.get("duration"),
                    effects.get("max_activations"),
                    eleid,
                    typeid,
                )
            )

    def getBaseConstants(self, baseConstant, isMod: bool) -> int:
        ret = -1
        # modifier has value instead of name (b/c made more sense but now im getting punished for it lol)
        if isMod:
            ret_list = self._db.getDataColumn(
                str(type(baseConstant).__name__).lower(), "value", baseConstant.value
            )
        else:
            ret_list = self._db.getDataColumn(
                str(type(baseConstant).__name__).lower(), "name", baseConstant.name
            )
        # check if character in, if it is then get id else insert
        if len(ret_list) == 0:
            ret = self._db.insertData(baseConstant)
        else:
            # id is always first column
            ret = (ret_list[0])[0]
        return ret

    def getInsertCharacterID(self, name: str, iscollab: bool) -> int:
        ret = -1
        ret_list = self._db.getDataColumn("character", "name", name)
        # check if character in, if it is then get id else insert
        if len(ret_list) == 0:
            ret = self._db.insertData(Character(None, name, iscollab))
        else:
            # id is always first column
            ret = (ret_list[0])[0]
        return ret

    def getInsertAdventurerID(
        self, characterid: int, typeid: int, limited: int, stars: int, title: str
    ) -> int:
        ret = -1
        ret_list = self._db.getDataColumn("adventurer", "title", title)
        # check if character in, if it is then get id else insert
        if len(ret_list) == 0:
            ret = self._db.insertData(
                Adventurer(
                    None, characterid, typeid, title, limited, False, stars, None
                )
            )
        else:
            # id is always first column
            ret = (ret_list[0])[0]
            # delete so we can insert the chara again
            if self._db.deleteById("adventurer", "adventurerid", ret):
                ret = self._db.insertData(
                    Adventurer(
                        None, characterid, typeid, title, limited, False, stars, None
                    )
                )
        return ret

    def getInsertAssistID(
        self, characterid: int, limited: int, stars: int, title: str
    ) -> int:
        ret = -1
        ret_list = self._db.getDataColumn("assist", "title", title)
        # check if character in, if it is then get id else insert
        if len(ret_list) == 0:
            ret = self._db.insertData(
                Assist(None, characterid, title, limited, stars, None)
            )
        else:
            # id is always first column
            ret = (ret_list[0])[0]
            # delete so we can insert the chara again
            if self._db.deleteById("assist", "assistid", ret):
                ret = self._db.insertData(
                    Assist(None, characterid, title, limited, stars, None)
                )
        return ret


if __name__ == "__main__":
    path = "../../DB/missingad"
    db = DBcontroller(DBConfig(DatabaseEnvironment.LOCAL))
    ic = InsertCharacter(db)
    for filename in os.listdir(path):
        with open(path + "/" + filename, "r", encoding="utf8") as f:
            if filename != "desktop.ini":
                print(filename)
                as_dict = json.load(f)
                if as_dict.get("limited") is None:
                    as_dict["limited"] = False

                temp_ad = AdventureC(
                    as_dict.get("title"),
                    as_dict.get("name"),
                    as_dict.get("type"),
                    as_dict.get("stars"),
                    as_dict.get("limited"),
                    True,
                    as_dict.get("stats"),
                    as_dict.get("skills"),
                )
                ic.insertAdventurer(temp_ad)


async def run(
    dbConfig: DBConfig,
    ctx: SlashContext,
    unit_file: Attachment,
):
    # permission checking
    if int(ctx.author.id) in EDITORS:
        ic = InsertCharacter(DBcontroller(dbConfig))

        try:
            async with ClientSession() as session:
                async with session.get(unit_file.url) as resp:
                    my_json = await resp.text()
            as_dict: dict[str, Any] = json.loads(my_json)

            if "type" in as_dict.keys():
                sub_command = "adventurer"
            else:
                sub_command = "assist"

            validateStructure(as_dict, sub_command)

            if as_dict.get("limited") is None:
                as_dict["limited"] = 0
            if sub_command == "assist":
                temp_as = AssistC(
                    as_dict.get("title"),
                    as_dict.get("name"),
                    as_dict.get("stars"),
                    as_dict.get("limited"),
                    as_dict.get("stats"),
                    as_dict.get("skills"),
                )
                ic.insertAssist(temp_as)
            elif sub_command == "adventurer":
                temp_ad = AdventureC(
                    as_dict.get("title"),
                    as_dict.get("name"),
                    as_dict.get("type"),
                    as_dict.get("stars"),
                    as_dict.get("limited"),
                    True,
                    as_dict.get("stats"),
                    as_dict.get("skills"),
                )
                ic.insertAdventurer(temp_ad)
            else:
                return await ctx.send("Error reading command")
        except:
            return await ctx.send("Error in reading json")

        title = f"{as_dict['title']} - {as_dict['name']}.json"
        await ctx.send(
            "Character has been added",
            files=File(BytesIO(my_json.encode()), file_name=title),
        )


# Basic validation for the unit json's structure.
# TODO: use TypedDict, or better Pydantic, for full validation
def validateStructure(unitDict: dict[str, Any], unitType: str):
    assert (
        set(["title", "name", "stars", "limited", "stats", "skills"]) <= unitDict.keys()
    )
    assert set(STATLIST) == unitDict["stats"].keys()

    if unitType == "adventurer":
        assert "type" in unitDict.keys()
        assert (
            set(["special", "combat", "additionals", "development"])
            == unitDict["skills"].keys()
        )
    elif unitType == "assist":
        assert set(["regular", "instant_effect"]) == unitDict["skills"].keys()
    else:
        raise
