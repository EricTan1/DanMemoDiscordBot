from database.DBcontroller import DBcontroller

def singleton(cls, *args, **kw):
    instances = {}
    def _singleton(*args, **kw):
       if cls not in instances:
            instances[cls] = cls(*args, **kw)
       return instances[cls]
    return _singleton

@singleton
class Cache(object):
    def __init__(self, dbConfig=None):
        self.data = {}
        self.refreshcache(dbConfig)
      

    def get_all_adventurers(self):
        return self.data["adventurers"]

    def get_all_adventurers_developments(self):
        return self.data["adventurers_developments"]
    
    def get_all_adventurers_skills(self):
        return self.data["adventurers_skills"]
    
    def get_all_adventurers_skills_effects(self):
        return self.data["adventurers_skills_effects"]
        
    def get_all_assists(self):
        return self.data["assists"]

    def get_all_assists_skills(self):
        return self.data["assists_skills"]

    def get_all_assists_skills_effects(self):
        return self.data["assists_skills_effects"]

    def get_assist_sa_gauge(self):
        return self.data["assist_sa_gauge"]

    def get_adventurer_sa_gauge(self):
        return self.data["adventurer_sa_gauge"]
    
    def get_all_adventurers_stats(self):
        return self.data["adventurer_stats"]

    def get_all_assists_stats(self):
        return self.data["assist_stats"]
    
    def refreshcache(self, dbConfig):
        db = DBcontroller(dbConfig)
        #SELECT a.adventurerid, a.characterid, a.typeid, a.alias, a.title, a.stars, a.limited, a.ascended,c.name, c.iscollab
        self.data["adventurers"] = db.get_all_adventurers()
        self.data["assists"] = db.get_all_assists()
        #SELECT addev.adventurerdevelopmentid,addev.name as development, m.value as modifier, a.name as attribute, ad.stars, ad.title, ad.alias, ad.limited, c.name
        self.data["adventurers_developments"] = db.get_all_adventurers_developments()
        #SELECT adventurerskillid, adventurerid, skillname, skilltype
        self.data["adventurers_skills"] = db.get_all_adventurers_skills()
        self.data["assists_skills"] = db.get_all_assists_skills()
        #SELECT ase.AdventurerSkillEffectsid, ase.AdventurerSkillid, ase.duration, e.name AS element, m.value AS modifier, ty.name AS type, ta.name AS target, a.name AS attribute, s.name AS speed, ad.stars, ad.title, ad.alias, ad.limited, c.name
        self.data["adventurers_skills_effects"] = db.get_all_adventurers_skills_effects()
        self.data["assists_skills_effects"] = db.get_all_assists_skills_effects()
        self.data["assist_sa_gauge"] = db.get_all_assist_sa_gauge_charge()
        self.data["adventurer_sa_gauge"] = db.get_all_adventurer_sa_gauge_charge()
        self.data["adventurer_stats"] = db.get_all_adventurer_stats()
        self.data["assist_stats"] = db.get_all_assist_stats()
        db.closeconnection()
