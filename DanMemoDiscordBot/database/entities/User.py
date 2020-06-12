import json
import datetime

import database.DBcontroller 
from database.entities.BaseConstants import Base
from commands.utils import dict_to_sns, sns_to_dict


class User():
    '''
    This class is an object that represents the User table in the DB
    '''
    def __init__(self, user_id, discord_id: str, crepes=None, last_bento_date=None, units=None, gacha_mode=0):
        ''' (self, int, str, str) -> User
        userid: the inner id of the user
        discord_id: the id of the user in discord
        '''
        self.user_id = user_id
        self.discord_id = discord_id
        self.crepes = crepes
        self.last_bento_date = last_bento_date
        self.units = units
        self.gacha_mode = gacha_mode

    def __str__(self):
        return str(self.__dict__)

    '''def dumpData(self):
        return "'"+json.dumps(self.data)+"'"
    
    def undumpData(dataJson):
        print(dataJson)
        return json.loads(dataJson)'''

    @staticmethod
    def get_user(db_config, author):
        discord_id = author

        db = database.DBcontroller.DBcontroller(db_config)
        user = db.get_user(discord_id)
        db.closeconnection()

        if user is None:
            user = User(None, discord_id)

        print(user)

        return user

    def update_user(self, db_config, date, message_content):
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

    @staticmethod
    def get_unit_key(unit):
        return "["+unit.unit_label+"] "+unit.character_name


