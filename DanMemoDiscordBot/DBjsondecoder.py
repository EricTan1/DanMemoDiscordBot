import json
import os
path = '../Database/adventurers/'

class Adventurer:
    def __init__(self, title, name, types, stars, limited, ascended, stats, sa, c_skills, development):
        self._title = title
        self._name = name
        self._type = types
        self._stars = stars
        self._limited = limited
        self.ascended = ascended
        self.stats = stats
        self.sa = sa
        self.skills = c_skills
        self.development = development



ad_list = []
for filename in os.listdir(path):
    with open(path + '/' + filename, 'r') as f:
        ad_dict = json.load(f)
        ad_list.append(Adventurer(ad_dict.get("title"), ad_dict.get("name"), ad_dict.get("type"), ad_dict.get("stars"), ad_dict.get("limited"), False, ad_dict.get("stats"), ad_dict.get("skills").get("special"), ad_dict.get("skills").get("combat"), ad_dict.get("skills").get("development")))
        # print(ad_dict)

print(ad_list[0]._name)