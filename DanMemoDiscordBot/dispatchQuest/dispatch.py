from database.DBcontroller import DBcontroller
import os
class Dispatch():
    def __init__(self, dispatchid, typename:str, stage, name:str,char1id:str, char2id:str,
                 char3id:str, char4id:str):
        ''' (Adventurer, int, int, int, bool, bool, int, str or None, str or
             None) -> Adventurer
             stars : the base stars of a unit (1/2/3/4)
             limited : is the unit time-limited?
             ascended : does the unit have hero ascension?
        '''
        self.dispatchid = dispatchid
        self.typename = str(typename)
        self.stage = stage
        self.name = str(name)
        self.char1id = str(char1id)
        self.char2id = str(char2id)
        self.char3id = str(char3id)
        self.char4id = str(char4id)
#connection = mysql.connector.connect(
    #host="localhost",
    #user="root",
    #password="danmemo", port=3306, database="danmemo")
db = DBcontroller("localhost", "root", "danmemo", "3306", "danmemo")
dispatch_dict = dict()

with open('dispatchQuest/dispatch.txt', 'r') as f:
    line = f.readline()
    while(line):
        
        stage=None
        split_list = line.split(" - ")
        split_list2 = split_list[1].split(":")
        
        #print(split_list)
        temp = split_list[0]
        if("(" in temp):
            typename = temp[:temp.find('(')]
            stage = temp[temp.find('('):]
        else:
            typename = temp
        char_list = split_list2[1].split(",")
        path ="lottery"
        for x in range(0,len(char_list)):
            char_list[x] = char_list[x].strip()
            for filename in os.listdir(path):
                if(char_list[x] in filename):
                    dispatch_dict[char_list[x]]=filename
                    break
        #print(char_list)
        #print(typename)
        #print(stage)
        #print(split_list2[0]
        
            
        #db.insertData(Dispatch(None,typename,stage,split_list2[0],char_list[0],char_list[1],char_list[2],char_list[3]))
        line = f.readline()
print(dispatch_dict)