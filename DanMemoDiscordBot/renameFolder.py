import json
import os
path = 'lottery/'
import sys

#for folders in os.listdir(path):
    #os.rename()
with open('message.txt') as fp:
    line = fp.readline()
    while line:
        temp = line.split(";")
        print(temp[2].strip() +" "+ temp[3].strip())
        print(temp[0])
        try:
            os.rename(path+"gac_"+temp[0],path+temp[2].strip() +" "+ temp[3].strip())
        except:
            pass
        line = fp.readline()
