import json
import os
import sys

path = "units/"
#for folders in os.listdir(path):
    #os.rename()
with open("units_map.txt") as fp:
    line = fp.readline()
    while line:
        gac_id, fullname, label, character = line.split(";")
        character = character.strip()

        old_folder_name = path+"gac_"+gac_id
        new_folder_name = path+character+" ["+label+"]"

        try:
            print("From '"+old_folder_name+"' to '"+new_folder_name+"'")
            os.rename(old_folder_name, new_folder_name)
        except Exception as e:
            #print("Could not find folder '"+old_folder_name+"' to rename it to '"+new_folder_name+"'")
            #print("Error: "+str(e))
            pass
        line = fp.readline()

'''
Could not find folder: 'units/gac_1011004005' to rename it to 'Yamato Mikoto [Azure Blade]'
Could not find folder: 'units/gac_1011012003' to rename it to 'Bete Loga [Ulfheoinn]'
Could not find folder: 'units/gac_1012033003' to rename it to 'Ganesha [Masked Lord]'
Could not find folder: 'units/gac_1012040001' to rename it to 'Takemikazuchi [Far East God]'
Could not find folder: 'units/gac_1012044004' to rename it to 'Dionysus [Splendid Nobleman]'
Could not find folder: 'units/gac_1012046002' to rename it to 'Goibniu [Godly Swordsmith]'

Left over folders:
gac_1011002005 => Bell Cranel [Adventurer]
gac_1011012003
'''