import mysql.connector
import inspect
import os
import json
from urllib.parse import urlparse
from enum import Enum
import datetime

from database.entities.Adventurer import Adventurer, AdventurerSkill, AdventurerSkillEffects, AdventurerDevelopment, AdventurerStats
from database.entities.BaseConstants import Element, Target, Type, Attribute, Modifier
import database.entities.User
from database.entities.LogsCommand import LogsCommand
from commands.utils import GachaRates, format_row_as_sns


class DatabaseEnvironment(Enum):
    LOCAL = 0
    HEROKU = 1


class DBConfig():
    def __init__(self, environment):
        if environment == DatabaseEnvironment.LOCAL:
            self.hostname = "localhost"
            self.username = "root"
            self.password = "danmemo"
            self.port = "3306"
            self.database = "danmemo"
        elif environment == DatabaseEnvironment.HEROKU:
            result = urlparse(os.environ.get("CLEARDB_DATABASE_URL"))
            self.hostname = result.hostname
            self.username = result.username
            self.password = result.password
            self.port = "3306"
            self.database = result.path[1:]
        else:
            raise Exception("Unknown database environment:",environment)


class DBcontroller:
    def __init__(self, config):
        ''' (DBcontroller, DBConfig) -> DBcontroller
        '''
        print("Created connection")
        self.database = config.database
        self._connection = mysql.connector.connect(
            host = config.hostname,
            user = config.username,
            password = config.password,
            port = config.port,
            database = config.database)
        #print(self.connection)
        self._mycursor = self._connection.cursor()
        self._mycursorprepared = self._connection.cursor(prepared=True)        
        
        with open('database/terms/human_readable.json', 'r') as f:
            self.human_readable_dict = json.load(f)
        with open('database/terms/human_input.json', 'r') as f:
            self.human_input_dict = json.load(f)
        with open('database/terms/human_input_character.json', 'r') as f:
            self.human_input_character_dict = json.load(f)

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
        print(adventurerid)        
        sql="SELECT a.title, c.name FROM danmemo.character as c, danmemo.adventurer as a WHERE a.adventurerid={} and c.characterid = a.characterid".replace("danmemo",self.database).format(adventurerid)
        self._mycursor.execute(sql)
        for row in self._mycursor: 
            ret = "[{}] {}".format(row[0],row[1])
            print(row)
        return ret

    def getAssistName(self, assistid):
        sql="SELECT a.title, c.name FROM danmemo.character as c, danmemo.assist as a WHERE a.assistid={} and c.characterid = a.characterid".replace("danmemo",self.database).format(assistid)
        self._mycursor.execute(sql)
        for row in self._mycursor: 
            ret = "[{}] {}".format(row[0],row[1])
            print(row)
        return ret
    def deleteById(self, entityname, column, value):
        ''' (DBcontroller, Entity, str, ?) -> List of Entity
        returns the entity list based on the columns
        '''
        sql = 'DELETE FROM {}.{} WHERE {}=%s'.format(self.database.lower(),
                                                                                                     entityname.lower(),
                                                                                                     column.lower())
        
        self._mycursor.execute(sql,(value,))
        self._connection.commit()
        print("exists and deleting")
        return True

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
        return ret_list
    
    def getDataColumnList(self, entityname, column):
        ''' (DBcontroller, Entity, str, ?) -> List of Entity
        returns the entity list based on the columns
        '''
        sql = 'SELECT {} FROM {}.{} '.format(column,self.database.lower(),
                                                                                                     entityname.lower())
        
        self._mycursor.execute(sql)
        ret_list =[]
        for row in self._mycursor: 
            ret_list.append(row[0])
        return ret_list    
    
    def characterSearch(self,search, filter_dict):
        print("searching")
        ret_dict =dict()
        for words in self.human_input_character_dict:
            if(" "+ words+ " " in search):
                search = search.replace(" "+ words+ " "," "+self.human_input_character_dict.get(words)+" ")
        search = search.strip()
        # Search by title first
        words_list = search.split(" ")
        for words in words_list:
            # adventurerid
            words = "%{}%".format(words)
            characterAdTitleSql= 'SELECT adventurerid, a.title, c.name from danmemo.adventurer as a, danmemo.character as c where (c.name like %s or a.title like %s or a.alias like %s) and c.characterid = a.characterid'.replace("danmemo",self.database)
            # .format(words,words,words)
            self._mycursorprepared.execute(characterAdTitleSql,(words,words,words))
            for row in self._mycursorprepared:
                ad_id = "Ad"+str(row[0])
                if(ret_dict.get(ad_id) == None):
                    ret_dict[ad_id] = [0,row[1],row[2]]
                ret_dict[ad_id] = [ret_dict.get(ad_id)[0]+1,row[1],row[2]]
            # ASSIST
            characterAsTitleSql= 'SELECT assistid, a.title, c.name from danmemo.assist as a, danmemo.character as c where (c.name like %s or a.title like %s or a.alias like %s) and c.characterid = a.characterid'.replace("danmemo",self.database)
            #.format(words,words,words)
            self._mycursorprepared.execute(characterAsTitleSql,(words,words,words))
            for row in self._mycursorprepared:
                as_id = "As"+str(row[0])
                if(ret_dict.get(as_id) == None):
                    ret_dict[as_id] = [0,row[1],row[2]]
                ret_dict[as_id] = [ret_dict.get(as_id)[0]+1,row[1],row[2]]

        ret_list=[]
        highest= None
        for keys in ret_dict:
            if(highest==None):
                highest = ret_dict.get(keys)[0]
                ret_list.append(ret_dict.get(keys)+[keys])
            elif(highest < ret_dict.get(keys)[0]):
                highest = ret_dict.get(keys)[0]
                ret_list = [ret_dict.get(keys)+[keys]]
            elif(highest == ret_dict.get(keys)[0]):
                ret_list.append(ret_dict.get(keys)+[keys])
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
        ele_set = {'light', 'wind', 'fire', 'dark', 'ice', 'water', 'earth', 'thunder'}
        for words in searchwords_list:
            new_words = "%{}%".format(words)
            # Target, Attribute(), Modifier(Super, 10%), Type (phys/mag), Element(Wind/Light)
            skillAdeffect_sql= "SELECT DISTINCT ase.AdventurerSkillid FROM danmemo.adventurerskilleffects as ase INNER JOIN danmemo.element as e on e.elementid= ase.eleid INNER JOIN danmemo.modifier as m on m.modifierid = ase.modifierid INNER JOIN danmemo.type as ty on ty.typeid = ase.typeid INNER JOIN danmemo.target as ta on ta.targetid = ase.Targetid INNER JOIN danmemo.attribute as a on a.attributeid = ase.attributeid LEFT JOIN danmemo.speed as s on ase.speedid = s.speedid WHERE m.value LIKE %s or e.name LIKE %s or ta.name=%s or ty.name LIKE %s or a.name LIKE %s or s.name LIKE %s".replace('danmemo',self.database)
            skillAdElement_sql = "SELECT DISTINCT ase.AdventurerSkillid FROM danmemo.adventurerskilleffects as ase INNER JOIN danmemo.element as e on e.elementid= ase.eleid WHERE e.name = %s".replace('danmemo',self.database)

            #.format
            print(words)
            if(words.lower() in ele_set):
                self._mycursorprepared.execute(skillAdElement_sql, (words,))
            else:
                self._mycursorprepared.execute(skillAdeffect_sql, (new_words,new_words,words,new_words,new_words,new_words))
            for row in self._mycursorprepared:
                skillid = "Ad" + str(row[0])
                print(skillid)
                if(ret_dict.get(skillid) == None):
                        ret_dict[skillid] = 0
                ret_dict[skillid] = ret_dict.get(skillid)+1
            skillAseffect_sql= "SELECT DISTINCT ase.assistskillid FROM danmemo.assistskilleffects as ase INNER JOIN danmemo.modifier as m on m.modifierid = ase.modifierid INNER JOIN danmemo.target as ta on ta.targetid = ase.Targetid INNER JOIN danmemo.attribute as a on a.attributeid = ase.attributeid WHERE m.value LIKE %s or ta.name LIKE %s or a.name LIKE %s".replace('danmemo',self.database)
            self._mycursorprepared.execute(skillAseffect_sql,(new_words,new_words,new_words))            
            for row in self._mycursorprepared:
                skillid = "As" + str(row[0])
                if(ret_dict.get(skillid) == None):
                        ret_dict[skillid] = 0
                ret_dict[skillid] = ret_dict.get(skillid)+1
            skillAveffect_sql='SELECT ad.adventurerdevelopmentid FROM danmemo.adventurerdevelopment as ad LEFT JOIN danmemo.attribute as a on ad.attributeid = a.attributeid WHERE a.name like %s or ad.name like %s'.replace("danmemo",self.database)
            self._mycursorprepared.execute(skillAveffect_sql,(new_words,new_words))
            for row in self._mycursorprepared:
                skillid = "Av" + str(row[0])
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
        print(ret_list)
        return ret_list

    def assembleAdventurer(self, adventurerid):
        title=""
        title_name = ""
        skill=[]
        adventurer_base_sql = "SELECT title, c.name, limited, ascended,stars,t.name FROM danmemo.adventurer as a, danmemo.character as c, danmemo.type as t where c.characterid=a.characterid and t.typeid = a.typeid and a.adventurerid={}".replace("danmemo",self.database).format(adventurerid)
        skill_id_sql = "SELECT adventurerskillid FROM danmemo.adventurerskill where adventurerid = {}".replace("danmemo",self.database).format(adventurerid)
        dev_id_sql = "SELECT * FROM danmemo.adventurerdevelopment where adventurerid = {}".replace("danmemo",self.database).format(adventurerid)
        # base adventurer assemble
        self._mycursor.execute(adventurer_base_sql)
        # free up the list cursor
        for row in self._mycursor:
            # TITLE CHARACTERNAME STARS
            # CHECK IF TIME LIMITED
            title = title + "[{}] {}\n".format(row[0],row[1])
            title_name = title_name + "{} {}".format(row[0],row[1])
            if(bool(row[2])):
                title = title + "[Limited-Time] "
            for x in range(0,row[4]):
                title = title + ":star:"
            ascended = row[3]
            unit_type = row[5]
        # stats
        stats_dict = self.assembleAdventurerStats(adventurerid)
        
        # adventurer skill assemble
        skillid_list = []
        self._mycursor.execute(skill_id_sql)
        # free up the list cursor
        for row in self._mycursor:    
            skillid_list.append(row[0])
        for skillid in skillid_list:
            skill.append(self.assembleAdventurerSkill(skillid))
        # assemble adventure development
        dev_ret = self.assembleAdventurerDevelopmentFromAdId(adventurerid)
        return (title_name, title, skill, stats_dict,dev_ret, ascended, unit_type)

    def assembleAssist(self, assistid):
        title = ""
        title_name = ""        
        skill=[]        
        assist_base_sql = "SELECT title, c.name, limited,stars FROM danmemo.assist as a, danmemo.character as c where c.characterid=a.characterid and a.assistid={}".replace("danmemo",self.database).format(assistid)
        skill_id_sql = "SELECT assistskillid FROM danmemo.assistskill where assistid = {}".replace("danmemo",self.database).format(assistid)
        # base assist assemble
        self._mycursor.execute(assist_base_sql)
        # free up the list cursor
        for row in self._mycursor:
            # TITLE CHARACTERNAME STARS
            # CHECK IF TIME LIMITED
            title = title + "[{}] {}\n".format(row[0],row[1])
            title_name = title_name + "{} {}".format(row[0],row[1])            
            if(bool(row[2])):
                title = title + "[Limited-Time] "
            for x in range(0,row[3]):
                title = title + ":star:"
        # stats (based on LB? idk somehow dynamically change stats here maybe send?)
        stats_dict = self.assembleAssistStats(assistid)
        # assist skill assemble (MLB skill VS non MLB (dyamically later?))
        # Skill Effects
        skillid_list = []
        self._mycursor.execute(skill_id_sql)
        # free up the list cursor
        for row in self._mycursor:    
            skillid_list.append(row[0])
        for skillid in skillid_list:
            skill.append(self.assembleAssistSkill(skillid))
        return (title_name, title, skill ,stats_dict)

    def assembleAssistSkill(self, skillid):
        ret =""
        skillname = ""
        skill_sql="SELECT skillname FROM danmemo.assistskill where assistskillid={}".replace("danmemo",self.database).format(skillid)
        effects_sql="SELECT t.name,m.value,a.name,e.duration FROM danmemo.assistskilleffects as e,danmemo.target as t,danmemo.modifier as m,danmemo.attribute as a where assistskillid={} and m.modifierid=e.modifierid and e.targetid = t.targetid and a.attributeid = e.attributeid".replace("danmemo",self.database).format(skillid)
        self._mycursor.execute(skill_sql)
        for row in self._mycursor:
            # skilltype : skillname
            skillname=skillname + "[{}]:\n".format(row[0].strip())
        self._mycursor.execute(effects_sql)
        for row in self._mycursor:
            temp_target = row[0]
            temp_modifier=row[1]
            temp_attribute=row[2]
            temp_duration = row[3]
    
            # [TARGET] Modifier Attribute /duration
            if(self.human_readable_dict.get(temp_target)!= None):
                temp_target=self.human_readable_dict.get(temp_target)
            if(self.human_readable_dict.get(temp_modifier)!= None):
                temp_modifier=self.human_readable_dict.get(temp_modifier)
            if(self.human_readable_dict.get(temp_attribute)!= None):
                temp_attribute=self.human_readable_dict.get(temp_attribute)
            if(temp_modifier[1:].isnumeric() and temp_modifier[0]!='x'):
                temp_modifier= temp_modifier+"%"

            if(temp_duration != None and temp_duration.strip() != "None"):
                ret=ret + "[{}] {} {} /{} turn(s) \n".format(temp_target,temp_modifier,temp_attribute,temp_duration)
            else:
                ret=ret + "[{}] {} {} \n".format(temp_target,temp_modifier,temp_attribute)                
        return (skillname,ret)

    def assembleAdventurerSkill(self, skillid):
        ret = ""
        skillname = ""        
        skill_sql = "SELECT skilltype, skillname FROM danmemo.adventurerskill where adventurerskillid={}".replace("danmemo",self.database).format(skillid)
        effects_sql = "SELECT t.name,m.value,a.name,e.duration,ty.name,ele.name,s.name FROM (danmemo.adventurerskilleffects as e,danmemo.target as t,danmemo.modifier as m,danmemo.attribute as a, danmemo.type as ty, danmemo.element as ele) LEFT JOIN danmemo.speed as s ON s.speedid = e.speedid where adventurerskillid={} and m.modifierid=e.modifierid and e.targetid = t.targetid and a.attributeid = e.attributeid and e.eleid=ele.elementid and ty.typeid=e.typeid".replace("danmemo",self.database).format(skillid)
        print(effects_sql)
        self._mycursor.execute(skill_sql)
        for row in self._mycursor:
            # skilltype : skillname
            skillname=skillname + "{}: {} \n".format(row[0].capitalize(),row[1])
        self._mycursor.execute(effects_sql)
        for row in self._mycursor:
            temp_target = row[0]
            temp_modifier=row[1]
            temp_attribute=row[2]
            temp_duration = row[3]
            temp_type = row[4]
            temp_element = row[5]
            temp_speed = row[6]
            if(temp_type == None or temp_type.strip() == "None"):
                temp_type = ""
            if(temp_element == None or temp_element.strip() == "None"):
                temp_element = ""            
            if(temp_speed== None or temp_speed.strip() == "None"):
                temp_speed = ""
            if(temp_attribute == None or temp_attribute.strip() == "None"):
                temp_attribute = ""
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
            if(temp_modifier[1:].isnumeric() and temp_modifier[0]!='x'):
                temp_modifier= temp_modifier+"%"

            if(temp_duration != None and temp_duration.strip() != "None"):
                ret=ret + "[{}] {} {} {} {} {} /{} turn(s) \n".format(temp_target,temp_speed,temp_modifier,temp_element,temp_type,temp_attribute,row[3])
            else:
                print(temp_type)
                ret=ret + "[{}] {} {} {} {} {} \n".format(temp_target,temp_speed,temp_modifier,temp_element,temp_type,temp_attribute)                
        return (skillname,ret)
    
    def assembleAdventurerDevelopment(self, adventurerDevelopmentid):
        self._mycursor.execute("SELECT ad.name,a.name,m.value,adv.title,c.name,adv.adventurerid FROM danmemo.adventurerdevelopment as ad LEFT JOIN danmemo.adventurer as adv on adv.adventurerid = ad.adventurerid LEFT JOIN danmemo.attribute as a on ad.attributeid = a.attributeid LEFT JOIN danmemo.modifier as m on ad.modifierid = m.modifierid LEFT JOIN danmemo.character as c on adv.characterid= c.characterid WHERE ad.adventurerdevelopmentid = {}".replace("danmemo", self.database).format(adventurerDevelopmentid))
        for row in self._mycursor:
            skillname = row[0].strip()
            temp_attribute = row[1]
            temp_modifier = row[2]            
            if(self.human_readable_dict.get(temp_modifier)!= None):
                temp_modifier=self.human_readable_dict.get(temp_modifier)
            if(self.human_readable_dict.get(temp_attribute)!= None):
                temp_attribute=self.human_readable_dict.get(temp_attribute)
            if(temp_modifier[1:].isnumeric() and temp_modifier[0]!='x'):
                temp_modifier= temp_modifier+"%"
            skilleffect = "{} {}".format(temp_attribute,temp_modifier)
            #adventurername = row[3] + " " + row[4]
            adtitle = row[3]
            adname=row[4]
            adid=row[5]
            return (skillname,skilleffect,adtitle, adname, adid)
        
    def assembleAdventurerDevelopmentFromAdId(self, adventurerid):
        self._mycursor.execute("SELECT ad.name,a.name,m.value FROM danmemo.adventurerdevelopment as ad LEFT JOIN danmemo.adventurer as adv on adv.adventurerid = ad.adventurerid LEFT JOIN danmemo.attribute as a on ad.attributeid = a.attributeid LEFT JOIN danmemo.modifier as m on ad.modifierid = m.modifierid LEFT JOIN danmemo.character as c on adv.characterid= c.characterid WHERE adv.adventurerid = {}".replace("danmemo", self.database).format(adventurerid))
        ret_list = []
        for row in self._mycursor:
            skillname = row[0].strip()
            temp_attribute = row[1]
            temp_modifier = row[2]            
            if(self.human_readable_dict.get(temp_modifier)!= None):
                temp_modifier=self.human_readable_dict.get(temp_modifier)
            if(self.human_readable_dict.get(temp_attribute)!= None):
                temp_attribute=self.human_readable_dict.get(temp_attribute)
            if(temp_modifier[1:].isnumeric() and temp_modifier[0]!='x'):
                temp_modifier= temp_modifier+"%"
            skilleffect = "{} {}".format(temp_attribute,temp_modifier)
            ret_list.append([skillname,skilleffect])
            
        return ret_list
    
    def assembleAdventurerStats(self, adventurerid):
        ret_dict = dict()
        self._mycursor.execute("SELECT a.name,stats.value FROM danmemo.adventurerstats as stats LEFT JOIN danmemo.attribute as a ON stats.attributeid = a.attributeid where stats.adventurerid = {};".replace("danmemo", self.database).format(adventurerid))
        for row in self._mycursor:
            ret_dict[row[0]]=row[1].strip('][').split(', ') 
        return ret_dict

    def getAdSkillIdFromEffect(self, adventurerskilleffectsid):
        self._mycursor.execute("SELECT AdventurerSkillid FROM danmemo.adventurerskilleffects WHERE AdventurerSkillEffectsid={}".replace("danmemo",self.database).format(adventurerskilleffectsid))
        for row in self._mycursor:
            return row[0]
    
    def getAsSkillIdFromEffect(self, assistskilleffectsid):
        self._mycursor.execute("SELECT assistSkillid FROM danmemo.assistskilleffects WHERE assistSkillEffectsid={}".replace("danmemo",self.database).format(assistskilleffectsid))
        for row in self._mycursor:
            return row[0]    

    def getAdventurerIdFromSkill(self, skillid):
            adventurer_base_sql = "SELECT adventurerid from danmemo.adventurerskill where adventurerskillid={}".replace("danmemo",self.database).format(skillid)
            self._mycursor.execute(adventurer_base_sql)
            for row in self._mycursor:
                    return row[0]
    
    def getAssistIdFromSkill(self, skillid):
            assist_base_sql = "SELECT assistid from danmemo.assistskill where assistskillid={}".replace("danmemo",self.database).format(skillid)
            self._mycursor.execute(assist_base_sql)
            for row in self._mycursor:
                    return row[0]    
    
    def assembleAssistStats(self, assistid):
        ret_dict = dict()
        self._mycursor.execute("SELECT a.name,stats.value FROM danmemo.assiststats as stats LEFT JOIN danmemo.attribute as a ON stats.attributeid = a.attributeid where stats.assistid = {};".replace("danmemo", self.database).format(assistid))
        for row in self._mycursor:
            ret_dict[row[0]]=row[1].strip('][').split(', ') 
        return ret_dict
    
    def assembleAdventurerCharacterData(self, adventurerid):
        ret = ""
        adventurer_base_sql = "SELECT title, c.name, limited, ascended,stars FROM danmemo.adventurer as a, danmemo.character as c where c.characterid=a.characterid and a.adventurerid={}".replace("danmemo",self.database).format(adventurerid)
        self._mycursor.execute(adventurer_base_sql)
        for row in self._mycursor:
            # TITLE CHARACTERNAME STARS
            # CHECK IF TIME LIMITED
            ret = ret + "{} {}".format(row[0],row[1])
            if(bool(row[2])):
                ret = ret + "\n[Limited-Time] "
            for x in range(0,row[4]):
                ret = ret + ":star:"
            ret = ret + "\n"
        return ret
    
    def assembleAdventurerCharacterName(self, adventurerid):
        adventurer_base_sql = "SELECT title, c.name, limited, ascended,stars FROM danmemo.adventurer as a, danmemo.character as c where c.characterid=a.characterid and a.adventurerid={}".replace("danmemo",self.database).format(adventurerid)
        self._mycursor.execute(adventurer_base_sql)
        for row in self._mycursor:
            # TITLE CHARACTERNAME STARS
            # CHECK IF TIME LIMITED
            return (row[0],row[1])
        
    def assembleAssistCharacterName(self, assistid):
        ret = ""
        assist_base_sql = "SELECT title, c.name, limited,stars FROM danmemo.assist as a, danmemo.character as c where c.characterid=a.characterid and a.assistid={}".replace("danmemo",self.database).format(assistid)
        skill_id_sql = "SELECT assistskillid FROM danmemo.assistskill where assistid = {}".replace("danmemo",self.database).format(assistid)
        # base assist assemble
        self._mycursor.execute(assist_base_sql)
        # free up the list cursor
        for row in self._mycursor:
            # TITLE CHARACTERNAME STARS
            # CHECK IF TIME LIMITED
            # title name
            return (row[0],row[1])
        
    def dispatchSearch(self, search):
        search = search.split(" ")
        ret_dict = dict()
        for words in search:
            words = "%{}%".format(words)
            sql='SELECT dispatchid,typename,stage,name,char1id,char2id,char3id,char4id FROM danmemo.dispatch where typename like %s or stage like %s or name like %s;'.replace("danmemo",self.database)
            self._mycursorprepared.execute(sql,(words,words,words))
            for row in self._mycursorprepared: 
                d_id = row[0]
                #print("{} {} {} {} {} {} {}".format(row[1],row[2],row[3],row[4],row[5],row[6],row[7]))
                if(ret_dict.get(d_id) == None):
                    ret_dict[d_id] = [0,row[1],row[2],row[3],row[4],row[5],row[6],row[7]]
                ret_dict[d_id] = [ret_dict.get(d_id)[0]+1,row[1],row[2],row[3],row[4],row[5],row[6],row[7]]
        ret_list=[]
        highest= None
        for keys in ret_dict:
            if(highest==None):
                highest = (ret_dict.get(keys))[0]
                ret_list.append(ret_dict.get(keys))
            elif(highest < (ret_dict.get(keys))[0]):
                highest = (ret_dict.get(keys))[0]
                ret_list = [ret_dict.get(keys)]
            elif(highest == (ret_dict.get(keys))[0]):
                ret_list.append(ret_dict.get(keys))
        print(ret_list)
        return ret_list
                
    def assembleAssistCharacterData(self, assistid):
        ret = ""
        assist_base_sql = "SELECT title, c.name, limited,stars FROM danmemo.assist as a, danmemo.character as c where c.characterid=a.characterid and a.assistid={}".replace("danmemo",self.database).format(assistid)
        skill_id_sql = "SELECT assistskillid FROM danmemo.assistskill where assistid = {}".replace("danmemo",self.database).format(assistid)
        # base assist assemble
        self._mycursor.execute(assist_base_sql)
        # free up the list cursor
        for row in self._mycursor:
            # TITLE CHARACTERNAME STARS
            # CHECK IF TIME LIMITED
            ret = ret + "[{}] {}\n".format(row[0],row[1])
            if(bool(row[2])):
                ret = ret + " [Limited-Time] "
            for x in range(0,row[3]):
                ret = ret + ":star:"
            ret = ret + "\n"
        return ret
    
    def getRandomUnit(self, gacha_category):
        if gacha_category == GachaRates.ADVENTURER_2_STARS.name:
            stars = 2
            table = "adventurer"
        elif gacha_category == GachaRates.ADVENTURER_3_STARS.name:
            stars = 3
            table = "adventurer"
        elif gacha_category == GachaRates.ADVENTURER_4_STARS.name:
            stars = 4
            table = "adventurer"
        elif gacha_category == GachaRates.ASSIST_2_STARS.name:
            stars = 2
            table = "assist"
        elif gacha_category == GachaRates.ASSIST_3_STARS.name:
            stars = 3
            table = "assist"
        elif gacha_category == GachaRates.ASSIST_4_STARS.name:
            stars = 4
            table = "assist"
        else:
            raise Exception("Unknown gacha category:",gacha_category)

        unit_id = table + "id"

        sql = "SELECT {} FROM {}.{} WHERE stars = {} ORDER BY RAND() LIMIT 1".format(unit_id,
                                                                                    self.database,
                                                                                    table,
                                                                                    stars)
        sql = "SELECT {}, stars, title, name FROM {}.{} as a \
                INNER JOIN {}.character as c ON c.characterid = a.characterid \
                WHERE {} IN (SELECT {} FROM ({}) t);".format(unit_id, self.database, table,
                                                            self.database,
                                                            unit_id, unit_id, sql)
        self._mycursor.execute(sql)
        for row in self._mycursor:
            unit_type, stars, unit_id, title, name = table, row[1], row[0], row[2], row[3]
            print(unit_type, stars, unit_id, title, name)
            return unit_type, stars, unit_id, title, name

    def get_user(self, discord_id):
        sql = "SELECT user_id, discord_id, crepes, last_bento_date, units FROM {}.user user WHERE user.discord_id = %s"\
            .format(self.database)
        print(sql)
        parameters = (discord_id,)

        self._mycursor.execute(sql,parameters)
        for row in self._mycursor:
            user_id = row[0]
            discordid = row[1]
            #data = database.entities.User.User.undumpData(self.remove_quotes(row[2]))
            crepes = row[2]
            last_bento_date = row[3]

            if row[4] is None:
                units = None
            else:
                units = json.loads(row[4])

            user = database.entities.User.User(user_id, discordid, crepes, last_bento_date, units)

            return user

    @staticmethod
    def remove_quotes(string):
        if string is not None:
            return string[1:-1]
        return string

    def update_user(self, user, date, command):
        if user.user_id is None:
            sql = "INSERT INTO {}.user (discord_id, crepes, last_bento_date, units) VALUES (%s,%s,%s,%s)".format(self.database)
            parameters = (user.discord_id, user.crepes, user.last_bento_date, json.dumps(user.units))
        else:
            sql = "UPDATE {}.user SET discord_id = %s, crepes = %s, last_bento_date = %s, units = %s" \
                  " WHERE user_id = %s".format(self.database)
            parameters = (user.discord_id, user.crepes, user.last_bento_date, json.dumps(user.units), user.user_id)

        log = LogsCommand(user.discord_id, date, command, sql, parameters)
        print(log)

        self._mycursor.execute(sql, parameters)
        self._connection.commit()
        print(self._mycursor.rowcount, "record inserted.")

        self.log_command(log)

        return self._mycursor.lastrowid

    def log_command(self, log_command):
        sql = "INSERT INTO {}.logs_command (discord_id, date, command, query, parameters) VALUES (%s,%s,%s,%s,%s)"\
            .format(self.database)
        parameters = (log_command.discord_id, log_command.date, log_command.command, log_command.query,
                      str(log_command.parameters))

        print(sql)
        print(parameters)

        self._mycursor.execute(sql, parameters)
        self._connection.commit()
        print(self._mycursor.rowcount, "record inserted.")
        return self._mycursor.lastrowid

    def get_all_adventurers(self):
        sql = "SELECT a.adventurerid, a.characterid, a.typeid, a.alias, a.title, a.stars, a.limited, a.ascended, \
              c.name, c.iscollab,\
              t.name\
              FROM {}.adventurer AS a,\
              {}.character AS c,\
              {}.type AS t\
              WHERE c.characterid = a.characterid AND t.typeid = a.typeid".format(self.database.lower(),self.database.lower(),self.database.lower())

        self._mycursor.execute(sql)

        res = []
        unit_type = "adventurer"
        for row in self._mycursor:
            unit_id, character_id, type_id, alias, unit_label, stars, is_limited, is_ascended, character_name, is_collab, type_name = row
            row_as_dict = format_row_as_sns(unit_type=unit_type, unit_id=unit_id, character_id=character_id, type_id=type_id, alias=alias, unit_label=unit_label, stars=stars, is_limited=is_limited, is_ascended=is_ascended, character_name=character_name, is_collab=is_collab, type_name=type_name)
            res.append(row_as_dict)
        return res

    def get_all_assists(self):
        sql = "SELECT a.assistid, a.characterid, a.alias, a.title, a.stars, a.limited, c.name, c.iscollab\
              FROM {}.assist AS a, {}.character AS c\
              WHERE c.characterid = a.characterid".format(self.database.lower(),self.database.lower())

        self._mycursor.execute(sql)

        res = []
        unit_type = "assist"
        for row in self._mycursor:
            unit_id, character_id, alias, unit_label, stars, is_limited, character_name, is_collab = row
            row_as_dict = format_row_as_sns(unit_type=unit_type, unit_id=unit_id, character_id=character_id, alias=alias, unit_label=unit_label, stars=stars, is_limited=is_limited, character_name=character_name, is_collab=is_collab)
            res.append(row_as_dict)
        return res


if __name__ == "__main__":
    db_config = DBConfig(DatabaseEnvironment.LOCAL)
    db = DBcontroller(db_config)
    skilleffects_id_list = db.dispatchSearch("millionaire anonymous 1")