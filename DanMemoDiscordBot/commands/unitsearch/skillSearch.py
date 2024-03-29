from interactions import Embed

from database.DBcontroller import DBcontroller


def get_page_list(my_list: list, db: DBcontroller) -> tuple[list, int]:
    rotating_list = []
    count = 0
    temp_list: list[tuple[tuple[str, str, str], list[tuple[str, str]]]] = []
    dup_dict_ad: dict[int, tuple[int, int]] = dict()
    dup_dict_as: dict[int, tuple[int, int]] = dict()
    rotating_list.append(temp_list)
    total_results = len(my_list)
    for skillid in my_list:
        if "Ad" in skillid:
            adventurerid = db.getAdventurerIdFromSkill(skillid[2:])
            if adventurerid in dup_dict_ad:
                count -= 1
                total_results -= 1
                skillinfo = db.assembleAdventurerSkill(skillid[2:])
                (pos1, pos2) = dup_dict_ad[adventurerid]
                skill = (f"*{skillinfo[0].strip()}*", skillinfo[1])
                rotating_list[pos1][pos2][1].append(skill)
            else:
                skillinfo = db.assembleAdventurerSkill(skillid[2:])
                names = db.assembleAdventurerCharacterName(adventurerid)
                # [TITLE, NAME, FILTERS, SKILL INFO]
                temp_list.append(
                    (
                        (names[0], names[1], "adventurer"),
                        [(f"*{skillinfo[0].strip()}*", skillinfo[1])],
                    )
                )
                dup_dict_ad[adventurerid] = (len(rotating_list) - 1, len(temp_list) - 1)
        elif "As" in skillid:
            assistid = db.getAssistIdFromSkill(skillid[2:])
            if assistid in dup_dict_as:
                count -= 1
                total_results -= 1
                skillinfo = db.assembleAssistSkill(skillid[2:])
                (pos1, pos2) = dup_dict_as[assistid]
                skill = (f"*{skillinfo[0].strip()}*", skillinfo[1])
                rotating_list[pos1][pos2][1].append(skill)
            else:
                skillinfo = db.assembleAssistSkill(skillid[2:])
                names = db.assembleAssistCharacterName(assistid)
                temp_list.append(
                    (
                        (names[0], names[1], "assist"),
                        [(f"*{skillinfo[0].strip()}*", skillinfo[1])],
                    )
                )
                dup_dict_as[assistid] = (len(rotating_list) - 1, len(temp_list) - 1)
        else:
            skillinfo = db.assembleAdventurerDevelopment(skillid[2:])
            adventurerid = skillinfo[4]
            if adventurerid in dup_dict_ad:
                count -= 1
                total_results -= 1
                (pos1, pos2) = dup_dict_ad[adventurerid]
                skill = (skillinfo[0].strip(), skillinfo[1])
                rotating_list[pos1][pos2][1].append(skill)
            else:
                names = db.assembleAdventurerCharacterName(adventurerid)
                temp_list.append(
                    (
                        (names[0], names[1], "adventurer"),
                        [(f"*{skillinfo[0].strip()}*", skillinfo[1])],
                    )
                )
        count = count + 1
        if count == 5:
            temp_list = []
            rotating_list.append(temp_list)
            count = 0

    # remove last empty list
    if len(rotating_list[len(rotating_list) - 1]) == 0:
        rotating_list.pop(len(rotating_list) - 1)

    return rotating_list, total_results


def get_unit_image_path(unit: tuple[tuple, list]) -> str:
    return "./images/units/" + unit[0][1] + " [" + unit[0][0] + "]/"


def filterAddRemove(
    page_list: list[list], current_filter: str, name: str, total_results: int
) -> tuple[list[list], str, int]:
    if name == current_filter:
        current_filter = "none"
        return page_list, current_filter, total_results
    # else
    current_filter = name
    current_page_list = []
    temp_page: list[list] = []
    current_page_list.append(temp_page)
    count = 0
    for pages in page_list:
        for skills in pages:
            is_filtered = True
            if not (current_filter == skills[0][2]):
                is_filtered = False
            if is_filtered:
                temp_page.append(skills)
                count += 1
            if len(temp_page) == 5:
                temp_page = []
                current_page_list.append(temp_page)
    # remove last empty list
    if len(current_page_list[len(current_page_list) - 1]) == 0:
        current_page_list.pop(len(current_page_list) - 1)
    return (current_page_list, current_filter, count)


def clearSetField(temp_embed: Embed, data: list[list]) -> Embed:
    temp_embed.fields = []
    for skills in data:
        title = f"__[{skills[0][0]}] {skills[0][1]}__\n"
        for skill in skills[1]:
            title = title + skill[0]
            temp_embed.add_field(value=skill[1], name=title)
            title = ""
    return temp_embed
