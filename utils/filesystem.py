'''
Created on 24.12.2017

@author: stevo
'''
import os

def GetFileList(path, filter=None):
    filenamelist = os.listdir(path)
    
    if filter:
        ret = list()
        for filename in filenamelist:
            if filename.find(filter) != -1:
                ret.append(filename)
    else:
        ret = filenamelist 
                  
    return ret