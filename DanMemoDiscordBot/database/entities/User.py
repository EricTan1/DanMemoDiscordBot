import database.DBcontroller
from commands.utils import sns_to_dict

class User():
    '''
    This class is an object that represents the User table in the DB
    '''
    def __init__(self, user_id, discord_id: str, crepes=None, last_bento_date=None, units=None, units_summary=None, gacha_mode=0, discord_unique_id=None, units_distinct_number=0, units_score=0):
        ''' (self, int, str, str) -> User
        userid: the inner id of the user
        discord_id: the id of the user in discord
        '''
        self.user_id = user_id
        self.discord_id = discord_id
        self.crepes = crepes
        self.last_bento_date = last_bento_date
        self.units = units
        self.units_summary = units_summary
        self.gacha_mode = gacha_mode
        self.discord_unique_id = discord_unique_id
        self.units_distinct_number = units_distinct_number
        self.units_score = units_score

    def __str__(self):
        return str(self.__dict__)

    '''def dumpData(self):
        return "'"+json.dumps(self.data)+"'"
    
    def undumpData(dataJson):
        print(dataJson)
        return json.loads(dataJson)'''

    @staticmethod
    def get_user(db_config, discord_id: str, discord_unique_id: str) -> "User":
        db = database.DBcontroller.DBcontroller(db_config)
        user = db.get_user(discord_id,discord_unique_id)
        db.closeconnection()

        if user is None:
            user = User(None, discord_id, discord_unique_id=discord_unique_id)
        if user.discord_unique_id is None:
            user.discord_unique_id = discord_unique_id

        if user.units_summary is not None:
            user.load_units()

        print("Retrieved user:",user)

        return user

    def update_user(self, db_config, date, message_content):
        self.update_units_summary()

        db = database.DBcontroller.DBcontroller(db_config)
        db.update_user(self, date, message_content)
        db.closeconnection()

    def add_units(self,new_units):
        if self.units is None:
            self.units = {}

        for unit in new_units:
            key = User.get_unit_key(unit)

            if not key in self.units:
                self.units[key] = sns_to_dict(unit)
                self.units[key]["number"] = 0

            self.units[key]["number"] = self.units[key]["number"] + 1

    def update_stats(self):
        self.units_distinct_number = len(self.units)

        units_score = 0
        for key in self.units:
            units_score += min(self.units[key]["number"],6)
        self.units_score = units_score

    def update_units_summary(self):
        if self.units is None:
            return
        self.units_summary = {}
        for key in self.units:
            self.units_summary[key] = self.units[key]["number"]

    def load_units(self):
        from commands.cache import Cache

        cache = Cache()
        adventurers = cache.get_all_adventurers()
        assists = cache.get_all_assists()
        units = adventurers + assists

        self.units = {}
        for unit in units:
            key = User.get_unit_key(unit)
            if key in self.units_summary:
                self.units[key] = sns_to_dict(unit)
                self.units[key]["number"] = self.units_summary[key]

    @staticmethod
    def get_unit_key(unit):
        return "["+unit.unit_label+"] "+unit.character_name
