'''
Created on 24.12.2017

@author: stevo
'''
import os
from ftplib import FTP_TLS
import sys


filenamelist = list()

def addline(text):
        temp = text.split(' ')
        filename=temp[-1:][0]
        filenamelist.append(filename)
        
def addline1(text):
    print(text)
        
    
class ftpAccess():

    def __init__(self, url):
        self.ftp = FTP_TLS(url)
        self.ftp.login("anonymous","anonymous",secure=False)           # login anonymously before securing control channel
        
    def GetFtpFile(self, InPath, filename, downloaddir ):
        
        outfile=downloaddir+filename
        
        self.ftp.cwd(InPath)
       
        self.ftp.retrbinary("RETR " + filename ,open(outfile, 'wb').write)
            
        
    def GetFileListFtp(self, pathname):
        self.ftp.cwd(pathname)
        ret=list()
        out = self.ftp.retrlines('LIST',addline) # list directory content securely
       
        # search json files        temp = entry.split(' ')
        for filename in filenamelist:
            try:
                a = self.ftp.size(filename)
                print("{} - {}".format(filename, a))
                ret.append([filename,a])
            except:
                print("{} - xxx".format(filename))
                pass
            
        return ret