from database.entities.Adventurer import (
    Adventurer,
    AdventurerDevelopment,
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


class AdventureC:
    def __init__(self, title, name, types, stars, limited, ascended, stats, skills):
        self._title = title
        self._name = name
        self._type = types
        self._stars = stars
        self._limited = limited
        self.ascended = ascended
        self.stats = stats
        self.skills = skills


class AssistC:
    def __init__(self, title, name, stars, limited, stats, skills):
        self._title = title
        self._name = name
        self._stars = stars
        self._limited = limited
        self.stats = stats
        self.skills = skills


class InsertCharacter:
    def __init__(self, database):
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
        # stats
        for attributeKeys in adventureComplete.stats:
            attributeid = self.getBaseConstants(Attribute(None, attributeKeys), False)
            db.insertData(
                AdventurerStats(
                    None,
                    adventurerid,
                    attributeid,
                    str(adventureComplete.stats.get(attributeKeys)),
                )
            )
        # skills
        for skillsKeys in adventureComplete.skills:
            skillsList = adventureComplete.skills.get(skillsKeys)
            if skillsKeys == "special":
                adventurerskillid = db.insertData(
                    AdventurerSkill(
                        None, adventurerid, skillsList.get("name"), skillsKeys
                    )
                )
                self.insertAdventurerSkillEffects(
                    adventurerskillid, skillsList.get("effects")
                )
            elif skillsKeys == "combat":
                for skills in skillsList:
                    adventurerskillid = db.insertData(
                        AdventurerSkill(
                            None, adventurerid, skills.get("name"), skillsKeys
                        )
                    )
                    self.insertAdventurerSkillEffects(
                        adventurerskillid, skills.get("effects")
                    )
            # development
            else:
                for skills in skillsList:
                    for effects in skills.get("effects"):
                        temp_attribute = effects.get("attribute")
                        temp_modifier = effects.get("modifier")
                        if temp_modifier == None:
                            temp_modifier = ""
                        if (
                            len(temp_modifier) > 0
                            and temp_modifier[len(temp_modifier) - 1] == "%"
                        ):
                            temp_modifier = temp_modifier[: len(temp_modifier) - 1]
                        attributeid = self.getBaseConstants(
                            Attribute(None, temp_attribute), False
                        )
                        modifierid = self.getBaseConstants(
                            Modifier(None, temp_modifier), True
                        )
                        # AdventurerDevelopment
                        db.insertData(
                            AdventurerDevelopment(
                                None,
                                adventurerid,
                                skills.get("name"),
                                attributeid,
                                modifierid,
                            )
                        )

    def insertAdventurerSkillEffects(self, adventurerskillid, skilleffectList):
        # AdventurerSkillEffects SET UP
        for effects in skilleffectList:
            # Type+Element
            temp_type = effects.get("type")
            if temp_type == None:
                temp_type = ""
            temp_element = effects.get("element")
            if temp_element == None:
                temp_element = ""
                # temp_index = temp_value.find("_")
                # temp_element = temp_value[0:temp_index]
                # temp_ad_ele = temp_element
                # temp_type = temp_value[temp_index+1:]
            # else:
            # temp_type = ""
            # temp_element=""
            # Element
            eleid = self.getBaseConstants(Element(None, temp_element), False)
            # Type for skills
            typeid = self.getBaseConstants(Type(None, temp_type), False)
            temp_target = effects.get("target")
            temp_attribute = effects.get("attribute")
            temp_speed = effects.get("speed")
            temp_modifier = effects.get("modifier")
            if temp_modifier == None:
                temp_modifier = ""
            if len(temp_modifier) > 0 and temp_modifier[len(temp_modifier) - 1] == "%":
                temp_modifier = temp_modifier[: len(temp_modifier) - 1]
            targetid = self.getBaseConstants(Target(None, temp_target), False)
            attributeid = self.getBaseConstants(Attribute(None, temp_attribute), False)
            speedid = self.getBaseConstants(Speed(None, temp_speed), False)
            modifierid = self.getBaseConstants(Modifier(None, temp_modifier), True)
            # inserting effects
            db.insertData(
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

    def insertAssist(self, assistComplete: AssistC):
        characterid = self.getInsertCharacterID(assistComplete._name, False)
        assistid = self.getInsertAssistID(
            characterid,
            assistComplete._limited,
            assistComplete._stars,
            assistComplete._title,
        )
        # stats
        for attributeKeys in assistComplete.stats:
            attributeid = self.getBaseConstants(Attribute(None, attributeKeys), False)
            db.insertData(
                AssistStats(
                    None,
                    assistid,
                    attributeid,
                    str(assistComplete.stats.get(attributeKeys)),
                )
            )
        # skills
        for skills in assistComplete.skills:
            assistskillid = db.insertData(
                AssistSkill(None, assistid, skills.get("name"))
            )
            self.insertAssistSkillEffects(assistskillid, skills.get("effects"))

    def insertAssistSkillEffects(self, assistskillid, skilleffectList):
        # assistskilleffects SET UP
        for effects in skilleffectList:
            # Type for skills
            # typeid=self.getBaseConstants(Type(None, temp_type), False)
            temp_target = effects.get("target")
            temp_attribute = effects.get("attribute")
            temp_modifier = effects.get("modifier")
            if len(temp_modifier) > 0 and temp_modifier[len(temp_modifier) - 1] == "%":
                temp_modifier = temp_modifier[: len(temp_modifier) - 1]
            targetid = self.getBaseConstants(Target(None, temp_target), False)
            attributeid = self.getBaseConstants(Attribute(None, temp_attribute), False)
            modifierid = self.getBaseConstants(Modifier(None, temp_modifier), True)
            # inserting effects
            db.insertData(
                AssistSkillEffects(
                    None,
                    assistskillid,
                    targetid,
                    attributeid,
                    modifierid,
                    effects.get("duration"),
                )
            )

    def getBaseConstants(self, baseConstant, isMod):
        ret = -1
        # modifier has value instead of name (b/c made more sense but now im getting punished for it lol)
        if isMod:
            ret_list = db.getDataColumn(
                str(type(baseConstant).__name__).lower(), "value", baseConstant.value
            )
        else:
            ret_list = db.getDataColumn(
                str(type(baseConstant).__name__).lower(), "name", baseConstant.name
            )
        # check if character in, if it is then get id else insert
        if len(ret_list) == 0:
            ret = db.insertData(baseConstant)
        else:
            # id is always first column
            ret = (ret_list[0])[0]
        return ret

    def getInsertCharacterID(self, name, iscollab):
        ret = -1
        ret_list = db.getDataColumn("character", "name", name)
        # check if character in, if it is then get id else insert
        if len(ret_list) == 0:
            ret = db.insertData(Character(None, name, iscollab))
        else:
            # id is always first column
            ret = (ret_list[0])[0]
        return ret

    def getInsertAdventurerID(self, characterid, typeid, limited, stars, title):
        ret = -1
        ret_list = db.getDataColumn("adventurer", "title", title)
        # check if character in, if it is then get id else insert
        if len(ret_list) == 0:
            ret = db.insertData(
                Adventurer(
                    None, characterid, typeid, title, limited, False, stars, None, None
                )
            )
        else:
            # id is always first column
            ret = (ret_list[0])[0]
        return ret

    def getInsertAssistID(self, characterid, limited, stars, title):
        ret = -1
        ret_list = db.getDataColumn("assist", "title", title)
        # check if character in, if it is then get id else insert
        if len(ret_list) == 0:
            ret = db.insertData(
                Assist(None, characterid, title, limited, stars, None, None)
            )
        else:
            # id is always first column
            ret = (ret_list[0])[0]
        return ret


if __name__ == "__main__":
    pass
    # db = DBcontroller("us-cdbr-iron-east-04.cleardb.net","bdcaa58f136231","c268bc42","3306","heroku_0fe8a18d3b21642")
    # ic = InsertCharacter(db)
    # mod_list = db.getDataColumnList("modifier", "value")
    # type_list =db.getDataColumnList("type", "name")
    # ele_list = db.getDataColumnList("element", "name")
    # speed_list = ["fast","slow"]
    # attribute_list =db.getDataColumnList("attribute", "name")
    # print(attribute_list)
    # path = '../../database/update/'
    # with open('Database/terms/human_input.json', 'r') as f:
    # human_input_dict = json.load(f)
    # for filename in os.listdir(path):
    # with open(path + '/' + filename, 'r', encoding="utf8") as f:
    ##as_dict = json.load(f)
    ##if(as_dict.get("limited")== None):
    ##as_dict["limited"]=False
    ##temp_as = AssistC(as_dict.get("title"), as_dict.get("name"), as_dict.get("stars"), as_dict.get("limited"), as_dict.get("stats"), as_dict.get("skills"))
    ##print(as_dict.get("stats"))
    ##ic.insertAssist(temp_as)
    # line = f.readline()
    ##Adv
    #
