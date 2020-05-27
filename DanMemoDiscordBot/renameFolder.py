import json
import os
path = 'lottery/'
import sys
""" DATAMINE IMAGE SETTING UP FILE. Reduces space of images and renames folders to corresponding units.
"""
#for folders in os.listdir(path):
    #os.rename()
with open('message.txt') as fp:
    line = fp.readline()
    while line:
        temp = line.split(";")
        print(temp)
        print(temp[2].strip() +" "+ temp[3].strip())
        print(temp[0])
        try:
            os.rename(path+"gac_"+temp[0],path+temp[2].strip() +" "+ temp[3].strip())
        except:
            pass
        line = fp.readline()
