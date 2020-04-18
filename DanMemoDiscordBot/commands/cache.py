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

        db = DBcontroller(dbConfig)

        self.data["adventurers"] = db.get_all_adventurers()
        self.data["assists"] = db.get_all_assists()

        db.closeconnection()

    def get_all_adventurers(self):
        return self.data["adventurers"]

    def get_all_assists(self):
        return self.data["assists"]

