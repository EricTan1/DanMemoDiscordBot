import json
import datetime

import database.DBcontroller 
from database.entities.BaseConstants import Base

class User():
    '''
    This class is an object that represents the User table in the DB
    '''
    def __init__(self, user_id, discord_id:str, data:str):
        ''' (self, int, str, str) -> User
        userid: the inner id of the user
        discord_id: the id of the user in discord
        data: all data of the user as json
        '''
        self.user_id = user_id
        self.discord_id = discord_id
        if data is None:
            self.data = {}
        else:
            self.data = data

    def __str__(self):
        return str(self.__dict__)

    def dumpData(self):
        return "'"+json.dumps(self.data)+"'"
    def undumpData(dataJson):
        print(dataJson)
        return json.loads(dataJson)

    def get_user(dbConfig, author):
        discord_id = "'"+str(author)+"'"

        db = database.DBcontroller.DBcontroller(dbConfig)
        user = db.getUser(discord_id)
        db.closeconnection()

        if user is None:
            user = User(None, discord_id, None)

        print(user)

        return user

    def updateUser(self, dbConfig):
        db = database.DBcontroller.DBcontroller(dbConfig)
        db.updateUser(self)
        db.closeconnection()

    def get_last_bento_date(self):
        key = "last_bento_date"
        date = self.data.get(key,None)
        if date != None:
            date = datetime.datetime.strptime(date, "%Y-%m-%d %H:%M:%S.%f")
        return date
    def set_last_bento_date(self,value):
        self.data["last_bento_date"] = str(value)

    def get_crepes_number(self):
        key = "crepes_number"
        return self.data.get(key,None)
    def set_crepes_number(self,value):
        self.data["crepes_number"] = value