import json
import os
import sys

wanted = ["all_rectangle.png","hex.png","texture.png","white.png"]

path = "units/"
for folders in os.listdir(path):
    for filename in os.listdir(path+"/"+folders):
        if filename not in wanted:
        	file = path+"/"+folders+"/"+filename
        	print("Deleting "+file)
        	os.remove(path+"/"+folders+"/"+filename)