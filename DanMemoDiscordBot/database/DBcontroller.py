from typing import Tuple
import mysql.connector
from mysql.connector import MySQLConnection
from mysql.connector.connection import MySQLCursor, MySQLCursorPrepared
import inspect
import os
import json
from urllib.parse import urlparse
from enum import Enum

import database.entities.User
from database.entities.LogsCommand import LogsCommand
from commands.utils import GachaRates, format_row_as_sns, TopCategories



class DatabaseEnvironment(Enum):
    LOCAL = 0
    HEROKU = 1

EDITORS = [175045433662504961, 271030697219588096, 204693066500538368, 226786914294824960, 531944688366649345, 630794201700892702, 171619343946350592, 258258729617719296]


class DBConfig():
    def __init__(self, environment):
        if environment == DatabaseEnvironment.LOCAL:
            self.hostname = "localhost"
            self.username = "root"
            self.password = "danmemo"
            self.port = "3306"
            self.database = "aisbot"
        elif environment == DatabaseEnvironment.HEROKU:
            result = urlparse(os.environ.get("AWS_DATABASE_URL"))
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
        self._connection: MySQLConnection = mysql.connector.connect(
            host = config.hostname,
            user = config.username,
            password = config.password,
            port = config.port,
            database = config.database)
        #print(self.connection)
        self._mycursor: MySQLCursor = self._connection.cursor()
        self._mycursorprepared: MySQLCursorPrepared = self._connection.cursor(prepared=True)
        
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
    
    def characterSearch(self,search):
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
    
    def skillSearch(self,search):
        from commands.cache import Cache
        cache = Cache()
        #units = cache.get_all_assists()
        #units = [unit for unit in units if unit.stars == stars]

        # separate by commas
        searchwords_list = search.split(",")
        ret_dict =dict()
        ret_dict_effect =dict()
        # get rid of spaces
        for index in range(0,len(searchwords_list)):
            searchwords_list[index] = searchwords_list[index].strip()
            # check if they are in the dict readable
            temp = self.human_input_dict.get(searchwords_list[index])
            if(temp != None):
                searchwords_list[index] = temp.strip()
            # if its not whole sentences try single words
            replace_list = []
            for words in searchwords_list[index].split(" "):
                
                print(searchwords_list[index])
                print(words)
                temp = self.human_input_dict.get(words)
                if(temp != None):
                    # (old,new)
                    replace_list.append((words, temp.strip()))
            for (old,new) in replace_list:
                searchwords_list[index] = searchwords_list[index].replace(old,new)

            #searchwords_list[index] = searchwords_list[index].replace(" ","_")
        print(searchwords_list)
        ele_set = {'light', 'wind', 'fire', 'dark', 'ice', 'water', 'earth', 'thunder'}
        ad_skill_effects = cache.get_all_adventurers_skills_effects()
        as_skill_effects = cache.get_all_assists_skills_effects()
        ad_dev_effects = cache.get_all_adventurers_developments()
        ad_dev_skill_effects = cache.get_all_adventurers_developments_skills_effects()
        for words in searchwords_list:
            new_words = words.lower()
            # Target, Attribute(), Modifier(Super, 10%), Type (phys/mag), Element(Wind/Light)
            # row_as_dict = format_row_as_sns(adventurerskilleffectsid = adventurerskilleffectsid, adventurerskillid=adventurerskillid, unit_type=unit_type, duration=duration, element=element, modifier=modifier, type=type, target=target, attribute=attribute, speed=speed, stars=stars, title=title, alias=alias, limited=limited, character=character)
            # row_as_dict = format_row_as_sns(assistskilleffectsid=assistskilleffectsid, assistskillid=assistskillid,unit_type=unit_type, duration=duration, modifier=modifier, target=target, attribute=attribute, stars=stars, title=title, alias=alias, limited=limited, character=character)

            #skillAdeffect_sql= "SELECT DISTINCT ase.AdventurerSkillid FROM danmemo.adventurerskilleffects as ase INNER JOIN danmemo.element as e on e.elementid= ase.eleid INNER JOIN danmemo.modifier as m on m.modifierid = ase.modifierid INNER JOIN danmemo.type as ty on ty.typeid = ase.typeid INNER JOIN danmemo.target as ta on ta.targetid = ase.Targetid INNER JOIN danmemo.attribute as a on a.attributeid = ase.attributeid LEFT JOIN danmemo.speed as s on ase.speedid = s.speedid WHERE m.value LIKE %s or e.name LIKE %s or ta.name=%s or ty.name LIKE %s or a.name LIKE %s or s.name LIKE %s".replace('danmemo',self.database)
            #skillAdElement_sql = "SELECT DISTINCT ase.AdventurerSkillid FROM danmemo.adventurerskilleffects as ase INNER JOIN danmemo.element as e on e.elementid= ase.eleid WHERE e.name = %s".replace('danmemo',self.database)

            #.format
            print(words)
            if(words.lower() in ele_set):
                ad_skill_effects_ret = [skilleffect for skilleffect in ad_skill_effects 
                                        if new_words == skilleffect.element.lower()]
                as_skill_effects_ret = [skilleffect for skilleffect in as_skill_effects 
                                        if new_words == skilleffect.target.lower()
                                        or new_words in skilleffect.attribute.lower()
                                        or new_words in skilleffect.modifier.lower()]
                #self._mycursorprepared.execute(skillAdElement_sql, (words,))
            else:
                #self._mycursorprepared.execute(skillAdeffect_sql, (new_words,new_words,words,new_words,new_words,new_words))
                # we want to iterate through every word
                if(" " in new_words):
                    temp_list = new_words.split(" ")
                    if(len(temp_list) > 0):
                        temp_word = temp_list.pop(0)
                        ad_skill_effects_ret = [skilleffect for skilleffect in ad_skill_effects 
                                                if temp_word in skilleffect.type.lower()
                                                or temp_word == skilleffect.target.lower()
                                                or temp_word in skilleffect.attribute.lower()
                                                or temp_word in skilleffect.speed.lower()
                                                or temp_word in skilleffect.modifier.lower()]
                        as_skill_effects_ret = [skilleffect for skilleffect in as_skill_effects 
                                                if temp_word == skilleffect.target.lower()
                                                or temp_word in skilleffect.attribute.lower()
                                                or temp_word in skilleffect.modifier.lower()]
                        # AND Logic for words
                        for search in temp_list:
                            ad_skill_effects_ret = [skilleffect for skilleffect in ad_skill_effects_ret 
                                                if search in skilleffect.type.lower()
                                                or search == skilleffect.target.lower()
                                                or search in skilleffect.attribute.lower()
                                                or search in skilleffect.speed.lower()
                                                or search in skilleffect.modifier.lower()]
                            as_skill_effects_ret = [skilleffect for skilleffect in as_skill_effects_ret 
                                                if search == skilleffect.target.lower()
                                                or search in skilleffect.attribute.lower()
                                                or search in skilleffect.modifier.lower()]
                    else:
                        # empty
                        ad_skill_effects_ret = []
                        as_skill_effects_ret = []
                        
                else:
                    ad_skill_effects_ret = [skilleffect for skilleffect in ad_skill_effects 
                                            if new_words in skilleffect.type.lower()
                                            or new_words == skilleffect.target.lower()
                                            or new_words in skilleffect.attribute.lower()
                                            or new_words in skilleffect.speed.lower()
                                            or new_words in skilleffect.modifier.lower()]
                    as_skill_effects_ret = [skilleffect for skilleffect in as_skill_effects 
                                            if new_words == skilleffect.target.lower()
                                            or new_words in skilleffect.attribute.lower()
                                            or new_words in skilleffect.modifier.lower()]
            my_set = set()
            # distinct adventurer
            for skilleffect in ad_skill_effects_ret:
                skillid = (skilleffect.adventurerskilleffectsid,"Ad" +str(skilleffect.adventurerskillid))
                if(ret_dict_effect.get(skillid) == None):
                        ret_dict_effect[skillid] = 0
                ret_dict_effect[skillid] = ret_dict_effect.get(skillid)+1
                my_set.add(skilleffect.adventurerskillid)

            for ids in my_set:
                skillid = "Ad" + str(ids)
                if(ret_dict.get(skillid) == None):
                        ret_dict[skillid] = 0
                ret_dict[skillid] = ret_dict.get(skillid)+1
            # assist
            my_set = set()
            # distinct
            for skilleffect in as_skill_effects_ret:
                skillid = (skilleffect.assistskilleffectsid,"As" +str(skilleffect.assistskillid))
                if(ret_dict_effect.get(skillid) == None):
                        ret_dict_effect[skillid] = 0
                ret_dict_effect[skillid] = ret_dict_effect.get(skillid)+1
                my_set.add(skilleffect.assistskillid)

            for ids in my_set:
                skillid = "As" + str(ids)
                if(ret_dict.get(skillid) == None):
                        ret_dict[skillid] = 0
                ret_dict[skillid] = ret_dict.get(skillid)+1


            #skillAveffect_sql='SELECT ad.adventurerdevelopmentid FROM danmemo.adventurerdevelopment as ad LEFT JOIN danmemo.attribute as a on ad.attributeid = a.attributeid WHERE a.name like %s or ad.name like %s'.replace("danmemo",self.database)
            #self._mycursorprepared.execute(skillAveffect_sql,(new_words,new_words))
            av_skill_effects_ret = [skilleffect for skilleffect in ad_dev_effects 
                            if new_words in skilleffect.development.lower()]
            
            av_skill_effects_ret_2 = [skilleffect for skilleffect in ad_dev_skill_effects 
                            if new_words in skilleffect.attribute.lower()]
            print(av_skill_effects_ret)
            my_set = set()
           # distinct
           #  adventurerdevelopmentid=adventurerdevelopmentid,unit_type=unit_type, development=development, modifier=modifier, attribute=attribute, stars=stars, title=title, alias=alias, limited=limited, character=character)

            for skilleffect in av_skill_effects_ret:
                skillid = (skilleffect.adventurerdevelopmentid,"Av" +str(skilleffect.adventurerdevelopmentid))
                if(ret_dict_effect.get(skillid) == None):
                        ret_dict_effect[skillid] = 0
                ret_dict_effect[skillid] = ret_dict_effect.get(skillid)+1
                my_set.add(skilleffect.adventurerdevelopmentid)
            

            for skilleffect in av_skill_effects_ret_2:
                skillid = (skilleffect.adventurerdevelopmentid,"Av" +str(skilleffect.adventurerdevelopmentid))
                if(ret_dict_effect.get(skillid) == None):
                        ret_dict_effect[skillid] = 0
                ret_dict_effect[skillid] = ret_dict_effect.get(skillid)+1
                my_set.add(skilleffect.adventurerdevelopmentid)

            for ids in my_set:
                skillid = "Av" + str(ids)
                if(ret_dict.get(skillid) == None):
                        ret_dict[skillid] = 0
                ret_dict[skillid] = ret_dict.get(skillid)+1

        # get all the skills with the highest freq
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
        # now sort by skilleffect id freq
        dictlist = [(k,v) for k,v in ret_dict_effect.items()]
        dictlist =  [skilleffect for skilleffect in dictlist 
                        if (skilleffect[0])[1] in ret_list]
        #sort list
        # take second element for sort
        def takeSecond(elem):
            return elem[1]
        dictlist.sort(key=takeSecond,reverse=True)
        # final loop to get rid of skill duplicates
        ret_list = []
        dup_set = set()
        for sortedValues in dictlist:
            curr_id = (sortedValues[0])[1]
            if(not(curr_id in dup_set)):
                ret_list.append(curr_id)
                dup_set.add(curr_id)
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
        reg_skill=[]
        instant_skill=[]
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
            skillname, ret, skilltype = self.assembleAssistSkill(skillid)
            if(skilltype == "regular"):
                reg_skill.append((skillname,ret))
            elif(skilltype == "instant_effect"):
                instant_skill.append((skillname,ret))
        
        # ++ instant_skill goes with ++ reg_skill and + instant_skill goes with + reg_skill
        for in_skill_name, in_skill_ret in instant_skill:
            if("++" in in_skill_name):
                for reg_skill_name, reg_skill_ret in reg_skill:
                    if("++" in reg_skill_name):
                        skill.append((reg_skill_name, reg_skill_ret + "\nInstant Effect:\n{}".format(in_skill_ret)))
            elif("+" in in_skill_name):
                for reg_skill_name, reg_skill_ret in reg_skill:
                    if(not("++" in reg_skill_name)):
                        skill.append((reg_skill_name, reg_skill_ret + "\nInstant Effect:\n{}".format(in_skill_ret)))
        if(len(instant_skill) != 2):
            skill = reg_skill

        return (title_name, title, skill ,stats_dict)

    def assembleAssistSkill(self, skillid) -> Tuple[str, str, str]:
        ret =""
        skillname = ""
        skilltype = ""
        skill_sql="SELECT skillname, skilltype FROM danmemo.assistskill where assistskillid={}".replace("danmemo",self.database).format(skillid)
        effects_sql="SELECT t.name,m.value,a.name,e.duration, e.maxActivations, ele.name, ty.name\
            FROM {}.assistskilleffects as e\
            LEFT JOIN {}.element AS ele on ele.elementid = e.elementid\
            INNER JOIN {}.modifier as m on m.modifierid = e.modifierid\
            LEFT JOIN {}.type AS ty on ty.typeid = e.typeid\
            INNER JOIN {}.target as t on t.targetid = e.Targetid\
            INNER JOIN {}.attribute as a on a.attributeid = e.attributeid\
            where assistskillid={}".format(*((self.database.lower(),)*6),skillid)
        self._mycursor.execute(skill_sql)
        # separate skill type from skill names :thinking: should be instant_effect and also regular
        for row in self._mycursor:
            # skilltype : skillname
            skillname=skillname +"[{}]:\n".format(row[0].strip())
            skilltype = skilltype + "{}".format(row[1].strip())
        self._mycursor.execute(effects_sql)
        for row in self._mycursor:
            temp_target = row[0]
            temp_modifier=row[1]
            temp_attribute=row[2]
            temp_duration = row[3]
            temp_max_activations = row[4]
            temp_element = row[5]
            temp_type = row[6]

            if(temp_attribute.lower()=="all_damage_resist" or temp_attribute.lower()=="single_damage_resist"):
                temp_modifier = int(temp_modifier)*-1
                if(temp_modifier > 0):
                    temp_modifier = "+"+str(temp_modifier)
                else:
                    temp_modifier =str(temp_modifier)
            if(temp_type == None or temp_type.strip() == "None"):
                temp_type = ""
            if(temp_element == None or temp_element.strip() == "None"):
                temp_element = ""
            else:
                temp_element = temp_element.capitalize()
            
            if(temp_attribute == None or temp_attribute.lower() == "none"):
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
            # element 

            if(temp_modifier[1:].isnumeric() and temp_modifier[0]!='x'):
                temp_modifier= temp_modifier+"%"


            if(temp_duration != None and temp_duration.strip() != "None"):
                ret=ret + "[{}] {} {} {} {} /{} turn(s) \n".format(temp_target,temp_modifier,temp_element,temp_type,temp_attribute,temp_duration)
            else:
                ret=ret + "[{}] {} {} {} {} \n".format(temp_target,temp_modifier,temp_element,temp_type,temp_attribute)
            if(temp_max_activations !="None" and temp_max_activations!=None):
                ret=ret + "**{} per turn**".format(temp_max_activations)    
        return (skillname, ret, skilltype)

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
            else:
                temp_element = temp_element.capitalize()
            if(temp_speed== None or temp_speed.strip() == "None"):
                temp_speed = ""
            if(temp_attribute == None or temp_attribute.strip() == "None"):
                temp_attribute = ""
                
            if(temp_attribute.lower()=="all_damage_resist" or temp_attribute.lower()=="single_damage_resist"):
                temp_modifier = int(temp_modifier)*-1
                if(temp_modifier > 0):
                    temp_modifier = "+"+str(temp_modifier)
                else:
                    temp_modifier = str(temp_modifier)
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
    
    def assembleAdventurerDevelopment(self, adventurerDevelopmentid) -> Tuple[str, str, str, str, int]:
        self._mycursor.execute("SELECT ad.name,adv.title,c.name,adv.adventurerid FROM danmemo.adventurerdevelopment as ad LEFT JOIN danmemo.adventurer as adv on adv.adventurerid = ad.adventurerid LEFT JOIN danmemo.character as c on adv.characterid= c.characterid WHERE ad.adventurerdevelopmentid = {}".replace("danmemo", self.database).format(adventurerDevelopmentid))
        effects_sql = "SELECT ta.name AS target, m.value AS modifier,  a.name AS attribute, adse.duration, ty.name AS type, e.name AS element, s.name AS speed\
                            FROM {}.adventurerdevelopmentskilleffects AS adse\
                            INNER JOIN {}.element AS e on e.elementid = adse.eleid\
                            INNER JOIN {}.modifier AS m on m.modifierid = adse.modifierid\
                            INNER JOIN {}.type AS ty on ty.typeid = adse.typeid\
                            INNER JOIN {}.target AS ta on ta.targetid = adse.Targetid\
                            INNER JOIN {}.attribute AS a on a.attributeid = adse.attributeid\
                            LEFT JOIN {}.speed AS s on adse.speedid = s.speedid\
                            WHERE adse.adventurerdevelopmentid={}"\
                            .format(*((self.database.lower(),)*7),adventurerDevelopmentid)
        
        for row in self._mycursor:
            skillname = row[0].strip()
            #adventurername = row[3] + " " + row[4]
            adtitle = row[1]
            adname=row[2]
            adid=row[3]
        
        self._mycursor.execute(effects_sql)
        ret = ""
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
            else:
                temp_element = temp_element.capitalize()
            if(temp_speed== None or temp_speed.strip() == "None"):
                temp_speed = ""
            if(temp_attribute == None or temp_attribute.strip() == "None"):
                temp_attribute = ""
                
            if(temp_attribute.lower()=="all_damage_resist" or temp_attribute.lower()=="single_damage_resist"):
                temp_modifier = int(temp_modifier)*-1
                if(temp_modifier > 0):
                    temp_modifier = "+"+str(temp_modifier)
                else:
                    temp_modifier = str(temp_modifier)
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
                if(temp_target != None and temp_target.strip() != "None"):
                    ret=ret + "[{}] {} {} {} {} {} /{} turn(s) \n".format(temp_target,temp_speed,temp_modifier,temp_element,temp_type,temp_attribute,row[3])
                else:
                    ret=ret + "{} {} {} {} {} /{} turn(s) \n".format(temp_speed,temp_modifier,temp_element,temp_type,temp_attribute,row[3])
            else:
                if(temp_target != None and temp_target.strip() != "None"):
                    ret=ret + "[{}] {} {} {} {} {} \n".format(temp_target,temp_speed,temp_modifier,temp_element,temp_type,temp_attribute)
                else:
                    ret=ret + "{} {} {} {} {} \n".format(temp_speed,temp_modifier,temp_element,temp_type,temp_attribute)
        
        return (skillname, ret, adtitle, adname, adid)
        
    def assembleAdventurerDevelopmentFromAdId(self, adventurerid):
        self._mycursor.execute("SELECT ad.name, ad.adventurerdevelopmentid FROM danmemo.adventurerdevelopment as ad LEFT JOIN danmemo.adventurer as adv on adv.adventurerid = ad.adventurerid LEFT JOIN danmemo.character as c on adv.characterid= c.characterid WHERE adv.adventurerid = {}".replace("danmemo", self.database).format(adventurerid))
        

        skillname_list = []
        adventurerdevelopmentid_list = []

        for row in self._mycursor:
            # skilltype : skillname
            skillname_list.append(row[0])
            adventurerdevelopmentid_list.append(row[1])
        
        ret_list = []
        for adventurerdevelopmentid in range(0,len(adventurerdevelopmentid_list)):
            effects_sql = "SELECT ta.name AS target, m.value AS modifier,  a.name AS attribute, adse.duration, ty.name AS type, e.name AS element, s.name AS speed\
                            FROM {}.adventurerdevelopmentskilleffects AS adse\
                            INNER JOIN {}.element AS e on e.elementid = adse.eleid\
                            INNER JOIN {}.modifier AS m on m.modifierid = adse.modifierid\
                            INNER JOIN {}.type AS ty on ty.typeid = adse.typeid\
                            INNER JOIN {}.target AS ta on ta.targetid = adse.Targetid\
                            INNER JOIN {}.attribute AS a on a.attributeid = adse.attributeid\
                            LEFT JOIN {}.speed AS s on adse.speedid = s.speedid\
                            WHERE adse.adventurerdevelopmentid={}"\
                            .format(*((self.database.lower(),)*7),adventurerdevelopmentid_list[adventurerdevelopmentid])
            self._mycursor.execute(effects_sql)
            ret = ""
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
                else:
                    temp_element = temp_element.capitalize()
                if(temp_speed== None or temp_speed.strip() == "None"):
                    temp_speed = ""
                if(temp_attribute == None or temp_attribute.strip() == "None"):
                    temp_attribute = ""
                    
                if(temp_attribute.lower()=="all_damage_resist" or temp_attribute.lower()=="single_damage_resist"):
                    temp_modifier = int(temp_modifier)*-1
                    if(temp_modifier > 0):
                        temp_modifier = "+"+str(temp_modifier)
                    else:
                        temp_modifier = str(temp_modifier)
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
                    if(temp_target != None and temp_target.strip() != "None"):
                        ret=ret + "[{}] {} {} {} {} {} /{} turn(s) \n".format(temp_target,temp_speed,temp_modifier,temp_element,temp_type,temp_attribute,row[3])
                    else:
                        ret=ret + "{} {} {} {} {} /{} turn(s) \n".format(temp_speed,temp_modifier,temp_element,temp_type,temp_attribute,row[3])
                else:
                    if(temp_target != None and temp_target.strip() != "None"):
                        ret=ret + "[{}] {} {} {} {} {} \n".format(temp_target,temp_speed,temp_modifier,temp_element,temp_type,temp_attribute)
                    else:
                        ret=ret + "{} {} {} {} {} \n".format(temp_speed,temp_modifier,temp_element,temp_type,temp_attribute)
            ret_list.append([skillname_list[adventurerdevelopmentid],ret])
            
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

    def getAdventurerIdFromSkill(self, skillid: int) -> int:
            adventurer_base_sql = "SELECT adventurerid from danmemo.adventurerskill where adventurerskillid={}".replace("danmemo",self.database).format(skillid)
            self._mycursor.execute(adventurer_base_sql)
            for row in self._mycursor:
                    return row[0]
    
    def getAssistIdFromSkill(self, skillid: int) -> int:
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

    def get_user(self, discord_id, discord_unique_id):
        sql = "SELECT user_id, discord_id, crepes, last_bento_date, units, units_summary, gacha_mode, discord_unique_id, units_distinct_number, units_score FROM {}.user user WHERE user.discord_id = %s or user.discord_unique_id = %s"\
            .format(self.database)
        print(sql)
        parameters = (discord_id,discord_unique_id)

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

            if row[5] is None:
                units_summary = None
            else:
                units_summary = json.loads(row[5])

            gacha_mode = row[6]
            discord_unique_id = row[7]
            units_distinct_number = row[8]
            units_score = row[9]

            user = database.entities.User.User(user_id, discordid, crepes, last_bento_date, units, units_summary, gacha_mode, discord_unique_id, units_distinct_number, units_score)

            return user

    def get_top_users(self, category):
        if category == TopCategories.GOURMETS:
            column = "crepes"
        else:
            column = "units_score"

        sql = "SELECT user_id, discord_id, crepes, last_bento_date, units, units_summary, gacha_mode, discord_unique_id, units_distinct_number, units_score FROM {}.user user WHERE user.{} > 0 ORDER BY user.{} DESC"\
            .format(self.database, column, column)
        print(sql)

        self._mycursor.execute(sql)
        users = []
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

            if row[5] is None:
                units_summary = None
            else:
                units_summary = json.loads(row[5])

            gacha_mode = row[6]
            discord_unique_id = row[7]
            units_distinct_number = row[8]
            units_score = row[9]

            user = database.entities.User.User(user_id, discordid, crepes, last_bento_date, units, units_summary, gacha_mode, discord_unique_id, units_distinct_number, units_score)
            users.append(user)
        return users

    @staticmethod
    def remove_quotes(string):
        if string is not None:
            return string[1:-1]
        return string

    def update_user(self, user, date, command):
        if user.user_id is None:
            sql = "INSERT INTO {}.user (discord_id, crepes, last_bento_date, units_summary, gacha_mode, discord_unique_id, units_distinct_number, units_score) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)".format(self.database)
            parameters = (user.discord_id, user.crepes, user.last_bento_date, json.dumps(user.units_summary), user.gacha_mode, user.discord_unique_id, user.units_distinct_number, user.units_score)
        else:
            sql = "UPDATE {}.user SET discord_id = %s, crepes = %s, last_bento_date = %s, units_summary = %s, gacha_mode = %s, discord_unique_id = %s, units_distinct_number = %s, units_score = %s" \
                  " WHERE user_id = %s".format(self.database)
            parameters = (user.discord_id, user.crepes, user.last_bento_date, json.dumps(user.units_summary), user.gacha_mode, user.discord_unique_id, user.units_distinct_number, user.units_score, user.user_id)

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

    # def get_all_adventurers_skills(self):
    #     sql = "SELECT ase.duration, e.name AS element, m.value AS modifier, ty.name AS type, ta.name AS target, a.name AS attribute, s.name AS speed, ad.stars, ad.title, c.name\
    #     FROM {}.adventurerskilleffects AS ase\
    #     INNER JOIN {}.element AS e on e.elementid = ase.eleid\
    #     INNER JOIN {}.modifier AS m on m.modifierid = ase.modifierid\
    #     INNER JOIN {}.type AS ty on ty.typeid = ase.typeid\
    #     INNER JOIN {}.target AS ta on ta.targetid = ase.Targetid\
    #     INNER JOIN {}.attribute AS a on a.attributeid = ase.attributeid\
    #     LEFT JOIN {}.speed AS s on ase.speedid = s.speedid\
    #     INNER JOIN {}.adventurerskill AS ads on ads.adventurerskillid = ase.adventurerskillid\
    #     INNER JOIN {}.adventurer AS ad on ad.adventurerid = ads.adventurerid\
    #     INNER JOIN {}.character AS c on c.characterid = ad.characterid"\
    #     .format(*((self.database.lower(),)*10))

    #     print(sql)

    #     self._mycursor.execute(sql)

    #     res = []
    #     unit_type = "adventurer"
    #     for row in self._mycursor:
    #         unit_id, character_id, alias, unit_label, stars, is_limited, character_name, is_collab = row
    #         row_as_dict = format_row_as_sns(unit_type=unit_type, unit_id=unit_id, character_id=character_id, alias=alias, unit_label=unit_label, stars=stars, is_limited=is_limited, character_name=character_name, is_collab=is_collab)
    #         res.append(row_as_dict)
    #     return res

    # def get_all_adventurers_developments(self):
    #     sql = "SELECT addev.name as development, m.value as modifier, a.name as attribute, ad.stars, ad.title, ad.alias, ad.limited, c.name\
    #     FROM {}.adventurerdevelopment as addev\
    #     INNER JOIN {}.modifier as m on m.modifierid = addev.modifierid\
    #     INNER JOIN {}.attribute as a on a.attributeid = addev.attributeid\
    #     INNER JOIN {}.adventurer as ad on ad.adventurerid = addev.adventurerid\
    #     INNER JOIN {}.character as c on c.characterid = ad.characterid"\
    #     .format(*((self.database.lower(),)*5))

    #     self._mycursor.execute(sql)

    #     res = []
    #     unit_type = "adventurer"
    #     for row in self._mycursor:
    #         development, modifier, attribute, stars, title, alias, limited, character = row
    #         row_as_dict = format_row_as_sns(unit_type=unit_type, development=development, modifier=modifier, attribute=attribute, stars=stars, title=title, alias=alias, limited=limited, character=character)
    #         res.append(row_as_dict)
    #     return res

    # def get_all_adventurers_skills(self):
    #     sql = "SELECT ase.duration, e.name AS element, m.value AS modifier, ty.name AS type, ta.name AS target, a.name AS attribute, s.name AS speed, ad.stars, ad.title, ad.alias, ad.limited, c.name\
    #     FROM {}.adventurerskilleffects AS ase\
    #     INNER JOIN {}.element AS e on e.elementid = ase.eleid\
    #     INNER JOIN {}.modifier AS m on m.modifierid = ase.modifierid\
    #     INNER JOIN {}.type AS ty on ty.typeid = ase.typeid\
    #     INNER JOIN {}.target AS ta on ta.targetid = ase.Targetid\
    #     INNER JOIN {}.attribute AS a on a.attributeid = ase.attributeid\
    #     LEFT JOIN {}.speed AS s on ase.speedid = s.speedid\
    #     INNER JOIN {}.adventurerskill AS ads on ads.adventurerskillid = ase.adventurerskillid\
    #     INNER JOIN {}.adventurer AS ad on ad.adventurerid = ads.adventurerid\
    #     INNER JOIN {}.character AS c on c.characterid = ad.characterid"\
    #     .format(*((self.database.lower(),)*10))

    #     self._mycursor.execute(sql)

    #     res = []
    #     unit_type = "adventurer"
    #     for row in self._mycursor:
    #         duration, element, modifier, type, target, attribute, speed, stars, title, alias, limited, character = row
    #         row_as_dict = format_row_as_sns(unit_type=unit_type, duration=duration, element=element, modifier=modifier, type=type, target=target, attribute=attribute, speed=speed, stars=stars, title=title, alias=alias, limited=limited, character=character)
    #         res.append(row_as_dict)
    #     return res

    # def get_all_assists_skills(self):
    #     sql = "SELECT ase.duration, m.value as modifier, ta.name as target, a.name as attribute, assist.stars, assist.title, assist.alias, assist.limited, c.name\
    #     FROM {}.assistskilleffects as ase\
    #     INNER JOIN {}.modifier as m on m.modifierid = ase.modifierid\
    #     INNER JOIN {}.target as ta on ta.targetid = ase.Targetid\
    #     INNER JOIN {}.attribute as a on a.attributeid = ase.attributeid\
    #     INNER JOIN {}.assistskill as ass on ass.assistskillid = ase.assistskillid\
    #     INNER JOIN {}.assist as assist on assist.assistid = ass.assistid\
    #     INNER JOIN {}.character as c on c.characterid = assist.characterid"\
    #     .format(*((self.database.lower(),)*7))

    #     self._mycursor.execute(sql)

    #     res = []
    #     unit_type = "assist"
    #     for row in self._mycursor:
    #         duration, modifier, target, attribute, stars, title, alias, limited, character = row
    #         row_as_dict = format_row_as_sns(unit_type=unit_type, duration=duration, modifier=modifier, target=target, attribute=attribute, stars=stars, title=title, alias=alias, limited=limited, character=character)
    #         res.append(row_as_dict)
    #     return res


    # def get_all_adventurers_developments(self):
    #     sql = "SELECT addev.name as development, m.value as modifier, a.name as attribute, ad.stars, ad.title, ad.alias, ad.limited, c.name\
    #     FROM {}.adventurerdevelopment as addev\
    #     INNER JOIN {}.modifier as m on m.modifierid = addev.modifierid\
    #     INNER JOIN {}.attribute as a on a.attributeid = addev.attributeid\
    #     INNER JOIN {}.adventurer as ad on ad.adventurerid = addev.adventurerid\
    #     INNER JOIN {}.character as c on c.characterid = ad.characterid"\
    #     .format(*((self.database.lower(),)*5))

    #     self._mycursor.execute(sql)

    #     res = []
    #     unit_type = "adventurer"
    #     for row in self._mycursor:
    #         development, modifier, attribute, stars, title, alias, limited, character = row
    #         row_as_dict = format_row_as_sns(unit_type=unit_type, development=development, modifier=modifier, attribute=attribute, stars=stars, title=title, alias=alias, limited=limited, character=character)
    #         res.append(row_as_dict)
    #     return res
    
    def get_all_adventurers_developments_skills(self):
        sql = "SELECT addev.adventurerdevelopmentid,addev.name as development, ad.stars, ad.title, ad.alias, ad.limited, c.name, addev.adventurerid\
        FROM {}.adventurerdevelopment as addev\
        INNER JOIN {}.adventurer as ad on ad.adventurerid = addev.adventurerid\
        INNER JOIN {}.character as c on c.characterid = ad.characterid"\
        .format(*((self.database.lower(),)*3))

        self._mycursor.execute(sql)

        res = []
        unit_type = "adventurer"
        for row in self._mycursor:
            adventurerdevelopmentid, development, stars, title, alias, limited, character,adventurerid = row
            row_as_dict = format_row_as_sns(adventurerdevelopmentid=adventurerdevelopmentid,unit_type=unit_type, development=development, stars=stars, title=title, alias=alias, limited=limited, character=character, adventurerid=adventurerid)
            res.append(row_as_dict)
        return res

    def get_all_adventurers_developments_skills_effects(self):
        sql = "SELECT adse.adventurerdevelopmentskilleffectsid, adds.adventurerdevelopmentid, adse.duration, e.name AS element, m.value AS modifier, ty.name AS type, ta.name AS target, a.name AS attribute, s.name AS speed, ad.stars, ad.title, ad.alias, ad.limited, c.name\
        FROM {}.adventurerdevelopmentskilleffects AS adse\
        INNER JOIN {}.element AS e on e.elementid = adse.eleid\
        INNER JOIN {}.modifier AS m on m.modifierid = adse.modifierid\
        INNER JOIN {}.type AS ty on ty.typeid = adse.typeid\
        INNER JOIN {}.target AS ta on ta.targetid = adse.Targetid\
        INNER JOIN {}.attribute AS a on a.attributeid = adse.attributeid\
        LEFT JOIN {}.speed AS s on adse.speedid = s.speedid\
        INNER JOIN {}.adventurerdevelopment AS adds on adds.adventurerdevelopmentid = adse.adventurerdevelopmentid\
        INNER JOIN {}.adventurer AS ad on ad.adventurerid = adds.adventurerid\
        INNER JOIN {}.character AS c on c.characterid = ad.characterid"\
        .format(*((self.database.lower(),)*10))

        self._mycursor.execute(sql)

        res = []
        unit_type = "adventurer"
        for row in self._mycursor:
            adventurerdevelopmentskilleffectsid, adventurerdevelopmentid, duration, element, modifier, type, target, attribute, speed, stars, title, alias, limited, character = row
            row_as_dict = format_row_as_sns(adventurerdevelopmentskilleffectsid = adventurerdevelopmentskilleffectsid, adventurerdevelopmentid=adventurerdevelopmentid, unit_type=unit_type, duration=duration, element=element, modifier=modifier, type=type, target=target, attribute=attribute, speed=speed, stars=stars, title=title, alias=alias, limited=limited, character=character)
            res.append(row_as_dict)
        return res



    def get_all_adventurers_skills(self):
        sql = "SELECT adventurerskillid, adventurerid, skillname, skilltype\
        FROM {}.adventurerskill"\
        .format(self.database.lower())
        self._mycursor.execute(sql)
        res = []
        for row in self._mycursor:
            adventurerskillid, adventurerid, skillname, skilltype= row
            row_as_dict = format_row_as_sns(adventurerskillid= adventurerskillid, adventurerid= adventurerid, skillname=skillname, skilltype=skilltype)
            res.append(row_as_dict)
        return res

    def get_all_adventurers_skills_effects(self):
        sql = "SELECT ase.AdventurerSkillEffectsid, ase.AdventurerSkillid, ase.duration, e.name AS element, m.value AS modifier, ty.name AS type, ta.name AS target, a.name AS attribute, s.name AS speed, ad.stars, ad.title, ad.alias, ad.limited, c.name\
        FROM {}.adventurerskilleffects AS ase\
        INNER JOIN {}.element AS e on e.elementid = ase.eleid\
        INNER JOIN {}.modifier AS m on m.modifierid = ase.modifierid\
        INNER JOIN {}.type AS ty on ty.typeid = ase.typeid\
        INNER JOIN {}.target AS ta on ta.targetid = ase.Targetid\
        INNER JOIN {}.attribute AS a on a.attributeid = ase.attributeid\
        LEFT JOIN {}.speed AS s on ase.speedid = s.speedid\
        INNER JOIN {}.adventurerskill AS ads on ads.adventurerskillid = ase.adventurerskillid\
        INNER JOIN {}.adventurer AS ad on ad.adventurerid = ads.adventurerid\
        INNER JOIN {}.character AS c on c.characterid = ad.characterid"\
        .format(*((self.database.lower(),)*10))

        self._mycursor.execute(sql)

        res = []
        unit_type = "adventurer"
        for row in self._mycursor:
            adventurerskilleffectsid, adventurerskillid, duration, element, modifier, type, target, attribute, speed, stars, title, alias, limited, character = row
            row_as_dict = format_row_as_sns(adventurerskilleffectsid = adventurerskilleffectsid, adventurerskillid=adventurerskillid, unit_type=unit_type, duration=duration, element=element, modifier=modifier, type=type, target=target, attribute=attribute, speed=speed, stars=stars, title=title, alias=alias, limited=limited, character=character)
            res.append(row_as_dict)
        return res

    def get_all_assists_skills(self):
        sql = "SELECT assistskillid, assistid, skillname, skilltype\
        FROM {}.assistskill"\
        .format(self.database.lower())
        self._mycursor.execute(sql)
        res = []
        for row in self._mycursor:
            assistsskillid, assistsid, skillname,skilltype= row
            row_as_dict = format_row_as_sns(assistsskillid= assistsskillid, assistsid= assistsid, skillname=skillname,skilltype=skilltype)
            res.append(row_as_dict)
        return res

    def get_all_assists_skills_effects(self):
        sql = "SELECT ase.assistskilleffectsid, ase.assistskillid, ase.duration, m.value as modifier, ta.name as target, a.name as attribute, assist.stars, assist.title, assist.alias, assist.limited, c.name, ase.maxActivations, e.name AS element, ty.name AS type\
        FROM {}.assistskilleffects as ase\
        LEFT JOIN {}.element AS e on e.elementid = ase.elementid\
        INNER JOIN {}.modifier as m on m.modifierid = ase.modifierid\
        LEFT JOIN {}.type AS ty on ty.typeid = ase.typeid\
        INNER JOIN {}.target as ta on ta.targetid = ase.Targetid\
        INNER JOIN {}.attribute as a on a.attributeid = ase.attributeid\
        INNER JOIN {}.assistskill as ass on ass.assistskillid = ase.assistskillid\
        INNER JOIN {}.assist as assist on assist.assistid = ass.assistid\
        INNER JOIN {}.character as c on c.characterid = assist.characterid"\
        .format(*((self.database.lower(),)*9))

        self._mycursor.execute(sql)

        res = []
        unit_type = "assist"
        for row in self._mycursor:
            assistskilleffectsid, assistskillid,duration, modifier, target, attribute, stars, title, alias, limited, character,maxActivcations, element,type = row
            row_as_dict = format_row_as_sns(assistskilleffectsid=assistskilleffectsid, assistskillid=assistskillid,unit_type=unit_type, duration=duration, modifier=modifier, target=target, attribute=attribute, stars=stars, title=title, alias=alias, limited=limited, character=character,maxActivcations=maxActivcations,element=element,type=type)
            res.append(row_as_dict)
        return res
    # attribute4 id 374 = sa_gauge_charge
    def get_all_assist_sa_gauge_charge(self):
        sql = "SELECT askill.skillname,assist.title,chara.name,ta.name, mo.value FROM\
                {}.assistskilleffects as askille\
                LEFT JOIN {}.assistskill as askill on askille.assistskillid = askill.assistskillid\
                LEFT JOIN {}.assist as assist on assist.assistid = askill.assistid\
                LEFT JOIN {}.character as chara on chara.characterid = assist.characterid\
                LEFT JOIN {}.target as ta on ta.targetid = askille.targetid\
                LEFT JOIN {}.modifier as mo on mo.modifierid = askille.modifierid\
                where attributeid = 374;".format(*((self.database.lower(),)*6))

        self._mycursor.execute(sql)

        res = []
        for row in self._mycursor:
            skillname, title, name, target, modifier= row
            row_as_dict = format_row_as_sns(skillname=skillname,title=title,name=name,modifier=modifier,target=target)
            res.append(row_as_dict)
        return res

# attribute4 id 374 = sa_gauge_charge
    def get_all_adventurer_sa_gauge_charge(self):
        sql = "SELECT askill.skillname,adventurer.title,chara.name,ta.name, mo.value, askill.skilltype FROM\
                {}.adventurerskilleffects as askille\
                LEFT JOIN {}.adventurerskill as askill on askille.adventurerskillid = askill.adventurerskillid\
                LEFT JOIN {}.adventurer as adventurer on adventurer.adventurerid = askill.adventurerid\
                LEFT JOIN {}.character as chara on chara.characterid = adventurer.characterid\
                LEFT JOIN {}.target as ta on ta.targetid = askille.targetid\
                LEFT JOIN {}.modifier as mo on mo.modifierid = askille.modifierid\
                where attributeid = 374;".format(*((self.database.lower(),)*6))

        self._mycursor.execute(sql)

        res = []
        for row in self._mycursor:
            skillname, title,name, target, modifier, skilltype= row
            row_ad_dict = format_row_as_sns(skillname=skillname,title=title,name=name,target=target,modifier=modifier,skilltype=skilltype)
            res.append(row_ad_dict)
        return res

    def get_all_adventurer_stats(self):
        sql = "SELECT adventurerstatsid, adventurerid, advstats.attributeid, attri.name, value FROM {}.adventurerstats as advstats\
                LEFT JOIN {}.attribute as attri on attri.attributeid=advstats.attributeid;".format(*((self.database.lower(),)*2))

        self._mycursor.execute(sql)

        res = []
        for row in self._mycursor:
            adventurerstatsid, adventurerid,attributeid, attriname, value= row
            row_ad_dict = format_row_as_sns(adventurerstatsid=adventurerstatsid,adventurerid=adventurerid,attributeid=attributeid,attriname=attriname,value=value)
            res.append(row_ad_dict)
        return res

    def get_all_assist_stats(self):
        sql = "SELECT assiststatsid, assistid, asstats.attributeid, attri.name, value FROM {}.assiststats as asstats\
                LEFT JOIN {}.attribute as attri on attri.attributeid=asstats.attributeid".format(*((self.database.lower(),)*2))

        self._mycursor.execute(sql)

        res = []
        for row in self._mycursor:
            assiststatsid, assistid,attributeid, attriname, value= row
            row_ad_dict = format_row_as_sns(assiststatsid=assiststatsid,assistid=assistid,attributeid=attributeid,attriname=attriname,value=value)
            res.append(row_ad_dict)
        return res

if __name__ == "__main__":
    db_config = DBConfig(DatabaseEnvironment.LOCAL)
    db = DBcontroller(db_config)
    skilleffects_id_list = db.dispatchSearch("millionaire anonymous 1")