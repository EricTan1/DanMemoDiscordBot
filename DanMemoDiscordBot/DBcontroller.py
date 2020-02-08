import mysql.connector
import inspect
from collections import namedtuple
import os
import sys
sys.path.append('../Entities/')

from Adventurer import Adventurer,AdventurerSkill,AdventurerSkillEffects,AdventurerDevelopment, AdventurerStats
from BaseConstants import Element, Target, Type, Attribute,Modifier

class DBcontroller:

  def __init__(self, host, user, password, port, database):
    ''' (DBcontroller, str, str ,str, int ,str) -> DBcontroller
    '''
    print("created connection")
    self.database = database
    self._connection = mysql.connector.connect(
        host=host,
        user=user,
        password=password, port=port, database=database)
    #print(self.connection)
    self._mycursor = self._connection.cursor()

  def closeconnection(self):
    ''' (DBcontroller) -> None
    Closes the DB connection
    '''
    self._connection.close()

  def insertData(self, entity):
    ''' (DBcontroller, Entity) -> bool
    returns whether or not it is a successful insert
    '''
    # get all the attributes of the members and their corresponding values
    attributes =inspect.getmembers(entity, lambda a:not(inspect.isroutine(a)))
    attributes =[a for a in attributes if not(a[0].startswith('__') and a[0].endswith('__'))]
    
    attribute_list = []
    value_list = []
    valueprep_list=[]
    
    for attributetuple in attributes:
      (attributename, attributevalue) = attributetuple
      attribute_list.append(attributename)
      valueprep_list.append('%s')
      value_list.append(attributevalue)
    
    attribute_list= str(tuple(attribute_list)).replace("'","")
    valueprep_list= str(tuple(valueprep_list)).replace("'","")
    
    
    sql="INSERT INTO {}.{} {} VALUES {}".format(self.database,str(type(entity).__name__).lower(),
                                             attribute_list.lower(),valueprep_list.lower())
    values = tuple(value_list)
    print(sql + "\n")
    print(str(values)+ "\n")
    self._mycursor.execute(sql,values)
    self._connection.commit()
    print(self._mycursor.rowcount, "record inserted.")
    
    
  
  def updateData(self, entity):
    ''' (DBcontroller, Entity, str, ?) -> bool
    returns whether or not it is a successful update
    '''
    pass  

  def getDataColumn(self, entityname, column, value):
    ''' (DBcontroller, Entity, str, ?) -> List of Entity
    returns the entity list based on the columns
    '''
    sql = 'SELECT * FROM {}.{} WHERE {}=%s'.format(self.database.lower(),
                                                   entityname.lower(),
                                                   column.lower())
    print(sql)
    
    self._mycursor.execute(sql,(value,))
    ret_list =[]
    for row in self._mycursor: 
      ret_list.append(row)
    print(ret_list)
    return ret_list
  
  def characterSearch(self,search, filter_dict):
    print("searching")
    ret_dict =dict()
    
    # Search by title first
    words_list = search.split(" ")
    for words in words_list:
      characterTitleSql= "SELECT adventurerid from danmemo.adventurer as a, danmemo.character as c where (c.name like'%{}%' or a.title like '%{}%') and c.characterid = a.characterid".format(words,words)
      self._mycursor.execute(characterTitleSql)
      for row in self._mycursor:
        ad_id = row[0]
        if(ret_dict.get(ad_id) == None):
          ret_dict[ad_id] = 0
        ret_dict[ad_id] = ret_dict.get(ad_id)+1
    ret_list=[]
    highest= None
    for keys in ret_dict:
      if(highest==None):
        highest = ret_dict.get(keys)
        ret_list.append(keys)
      elif(highest < ret_dict.get(keys)):
        highest = ret_dict.get(keys)
        ret_list = [keys]
      elif(highest == ret_dict.get(keys)):
        ret_list.append(keys)
    return ret_list
      
        #ret_dict[]
    # if we can find a title and exactly 1 result then return it
    
    
    # if multiple results then have priority?
    
    # break down the search?
    

  def skillSearch(self,search, filter_dict):
    character_sql= "SELECT adventurerid, title from danmemo.adventurer as a, danmemo.character as c where c.name like'%ais%' and c.characterid = a.characterid"
    self._mycursor.execute(character_sql)
    for row in self._mycursor:  
      print(row)


if __name__ == "__main__":
  db = DBcontroller("localhost","root","danmemo","3306","danmemo")
  print(db.characterSearch("devil ais wallenstein",{}))
  