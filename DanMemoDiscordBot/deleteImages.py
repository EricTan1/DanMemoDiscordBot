import json
import os
path = 'lottery/'
import sys

for folders in os.listdir(path):
    for filename in os.listdir(path+"/"+folders):
        if(not("hex.png" in filename or "texture.png" in filename)):
            os.remove(path+"/"+folders+"/"+filename)