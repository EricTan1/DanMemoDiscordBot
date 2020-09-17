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
    
    def refreshcache(self, dbConfig):
        db = DBcontroller(dbConfig)
        self.data["adventurers"] = db.get_all_adventurers()
        self.data["assists"] = db.get_all_assists()
        self.data["adventurers_developments"] = db.get_all_adventurers_developments()
        self.data["adventurers_skills"] = db.get_all_adventurers_skills()
        self.data["assists_skills"] = db.get_all_assists_skills()
        self.data["adventurers_skills_effects"] = db.get_all_adventurers_skills_effects()
        self.data["assists_skills_effects"] = db.get_all_assists_skills_effects()
        self.data["assist_sa_gauge"] = db.get_all_assist_sa_gauge_charge()
        self.data["adventurer_sa_gauge"] = db.get_all_adventurer_sa_gauge_charge()
        db.closeconnection()
