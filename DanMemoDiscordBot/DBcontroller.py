import mysql.connector
import inspect
from collections import namedtuple
import os
import sys
import json
sys.path.append('Entities/')

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
    with open('Database/terms/human_readable.json', 'r') as f:
      self.human_readable_dict = json.load(f)
    with open('Database/terms/human_input.json', 'r') as f:
      self.human_input_dict = json.load(f)

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
    return self._mycursor.lastrowid
    
    
  
  def updateData(self, entity):
    ''' (DBcontroller, Entity, str, ?) -> bool
    returns whether or not it is a successful update
    '''
    pass
  
  def getAdventurerName(self, adventurerid):
    sql="SELECT a.title, c.name FROM danmemo.character as c, danmemo.adventurer as a WHERE a.adventurerid={} and c.characterid = a.characterid".format(adventurerid)
    self._mycursor.execute(sql)
    for row in self._mycursor: 
      ret = "{} {}".format(row[0],row[1])
      print(row)
    return ret

  def getDataColumn(self, entityname, column, value):
    ''' (DBcontroller, Entity, str, ?) -> List of Entity
    returns the entity list based on the columns
    '''
    sql = 'SELECT * FROM {}.{} WHERE {}=%s'.format(self.database.lower(),
                                                   entityname.lower(),
                                                   column.lower())
    
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
      # adventurerid
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
    

  def skillSearch(self,search, filter_dict):
    # separate by commas
    searchwords_list = search.split(",")
    ret_dict =dict()
    # get rid of spaces
    for index in range(0,len(searchwords_list)):
      searchwords_list[index] = searchwords_list[index].strip()
      # check if they are in the dict readable
      temp = self.human_input_dict.get(searchwords_list[index])
      if(temp != None):
        searchwords_list[index] = temp
      searchwords_list[index] = searchwords_list[index].replace(" ","_")
    print(searchwords_list)
    for words in searchwords_list:
      # Target, Attribute(), Modifier(Super, 10%), Type (phys/mag), Element(Wind/Light)
      skilleffect_sql= "SELECT ase.AdventurerSkillEffectsid FROM danmemo.adventurerskilleffects as ase INNER JOIN danmemo.element as e on e.elementid= ase.eleid INNER JOIN danmemo.modifier as m on m.modifierid = ase.modifierid INNER JOIN danmemo.type as ty on ty.typeid = ase.typeid INNER JOIN danmemo.target as ta on ta.targetid = ase.Targetid INNER JOIN danmemo.attribute as a on a.attributeid = ase.attributeid LEFT JOIN danmemo.speed as s on ase.speedid = s.speedid WHERE m.value LIKE '%{}%' or e.name LIKE '%{}%' or ta.name LIKE '%{}%' or ty.name LIKE '%{}%' or a.name LIKE '%{}%' or s.name LIKE '%{}%'".format(words,words,words,words,words,words)
      self._mycursor.execute(skilleffect_sql)
      for row in self._mycursor:
        skillid = row[0]
        if(ret_dict.get(skillid) == None):
            ret_dict[skillid] = 0
        ret_dict[skillid] = ret_dict.get(skillid)+1
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

      
  def assembleAdventurer(self, adventurerid):
    ret=""
    adventurer_base_sql = "SELECT title, c.name, limited, ascended,stars FROM danmemo.adventurer as a, danmemo.character as c where c.characterid=a.characterid and a.adventurerid={}".format(adventurerid)
    skill_id_sql = "SELECT adventurerskillid FROM danmemo.adventurerskill where adventurerid = {}".format(adventurerid)
    dev_id_sql = "SELECT * FROM danmemo.adventurerdevelopment where adventurerid = {}".format(adventurerid)
    # base adventurer assemble
    self._mycursor.execute(adventurer_base_sql)
    # free up the list cursor
    for row in self._mycursor:
      # TITLE CHARACTERNAME STARS
      # CHECK IF TIME LIMITED
      ret = ret + "{} {}".format(row[0],row[1])
      if(bool(row[2])):
        ret = ret + " [Limited-Time] "
      for x in range(0,row[4]):
        ret = ret + ":star:"
      ret = ret + "\n"
    # stats
    
    # adventurer skill assemble
    skillid_list = []
    self._mycursor.execute(skill_id_sql)
    # free up the list cursor
    for row in self._mycursor:  
      skillid_list.append(row[0])
    for skillid in skillid_list:
      ret = ret + self.assembleAdventurerSkill(skillid)
    # assemble adventure development
    return ret

  def assembleAssist(self, assistid):
    # stats (based on LB? idk somehow dynamically change stats here maybe send?)
    # adventurer skill assemble
    # SA/Combat
    # Skill Effects
    # assemble adventure development
    pass

  def assembleAdventurerSkill(self, skillid):
    ret =""
    skill_sql="SELECT skilltype, skillname FROM danmemo.adventurerskill where adventurerskillid={}".format(skillid)
    effects_sql="SELECT  t.name,m.value,a.name,e.duration,ty.name,ele.name,s.name FROM danmemo.adventurerskilleffects as e,danmemo.target as t,danmemo.modifier as m,danmemo.attribute as a, danmemo.type as ty, danmemo.element as ele, danmemo.speed as s where adventurerskillid={} and m.modifierid=e.modifierid and e.targetid = t.targetid and a.attributeid = e.attributeid and e.eleid=ele.elementid and ty.typeid=e.typeid and s.speedid = e.speedid".format(skillid)
    self._mycursor.execute(skill_sql)
    for row in self._mycursor:
      # skilltype : skillname
      ret=ret + "{}: {} \n".format(row[0],row[1])
    self._mycursor.execute(effects_sql)
    for row in self._mycursor:
      temp_target = row[0]
      temp_modifier=row[1]
      temp_attribute=row[2]
      temp_duration = row[3]
      temp_type = row[4]
      temp_element = row[5]
      temp_speed = row[6]
      if(temp_type == None):
        temp_type = ""
      if(temp_element == None):
        temp_element = ""      
      if(temp_speed== None):
        temp_speed = ""
      # [TARGET] Modifier Attribute /duration
      if(self.human_readable_dict.get(temp_target)!= None):
        temp_target=self.human_readable_dict.get(temp_target)
      if(self.human_readable_dict.get(temp_modifier)!= None):
        temp_modifier=self.human_readable_dict.get(temp_modifier)
      if(self.human_readable_dict.get(temp_attribute)!= None):
        temp_attribute=self.human_readable_dict.get(temp_attribute)
      
      if(self.human_readable_dict.get(temp_type)!= None):
        temp_type=self.human_readable_dict.get(temp_type)
      if(self.human_readable_dict.get(temp_element)!= None):
        temp_element=self.human_readable_dict.get(temp_element)
      if(self.human_readable_dict.get(temp_speed)!= None):
        temp_speed=self.human_readable_dict.get(temp_speed)      
      if(temp_modifier[1:].isnumeric()):
        temp_modifier= temp_modifier+"%"

      if(temp_duration != "None"):
        ret=ret + "[{}] {} {} {} {} {} /{} turn(s) \n".format(temp_target,temp_speed,temp_modifier,temp_element,temp_type,temp_attribute,row[3])
      else:
        ret=ret + "[{}] {} {} {} {} {} \n".format(temp_target,temp_speed,temp_modifier,temp_element,temp_type,temp_attribute)        
    return ret + "\n"
  
  def getSkillIdFromEffect(self, adventurerskilleffectsid):
    self._mycursor.execute("SELECT AdventurerSkillid FROM danmemo.adventurerskilleffects WHERE AdventurerSkillEffectsid={}".format(adventurerskilleffectsid))
    for row in self._mycursor:
      return row[0]

  def getAdventurerIdFromSkill(self, skillid):
      adventurer_base_sql = "SELECT adventurerid from danmemo.adventurerskill where adventurerskillid={}".format(skillid)
      self._mycursor.execute(adventurer_base_sql)
      for row in self._mycursor:
          return row[0]
  
  def assembleAdventurerCharacterData(self, adventurerid):
    ret = ""
    adventurer_base_sql = "SELECT title, c.name, limited, ascended,stars FROM danmemo.adventurer as a, danmemo.character as c where c.characterid=a.characterid and a.adventurerid={}".format(adventurerid)
    self._mycursor.execute(adventurer_base_sql)
    for row in self._mycursor:
      # TITLE CHARACTERNAME STARS
      # CHECK IF TIME LIMITED
      ret = ret + "{} {}".format(row[0],row[1])
      if(bool(row[2])):
        ret = ret + " [Limited-Time] "
      for x in range(0,row[4]):
        ret = ret + ":star:"
      ret = ret + "\n"
    return ret
    
if __name__ == "__main__":
  db = DBcontroller("localhost","root","danmemo","3306","danmemo")
  skilleffects_id_list = db.skillSearch("light, phyres, low",{})
  # getting rid of duplicates for adventurerskill
  my_set = set()
  message =""
  for skilleffectsid in skilleffects_id_list:
    skillid = db.getSkillIdFromEffect(skilleffectsid)
    my_set.add(skillid)
  for adventurerskillid in my_set:
    adventurerid = db.getAdventurerIdFromSkill(adventurerskillid)
    message =message +  db.assembleAdventurerCharacterData(adventurerid)    
    message = message + db.assembleAdventurerSkill(adventurerskillid)

  print(message)

  