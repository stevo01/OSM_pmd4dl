'''
Created on 24.03.2018

@author: stevo
'''
from utils.pyFTP import ftpAccess
from optparse import OptionParser

if __name__ == '__main__':

    parser = OptionParser()
    usage = "usage: %prog [options] arg1 arg2"
    atlas = list()

    parser.add_option("-a", "--address", type="string", help="server address", dest="address", default="ftp5.gwdg.de")
    parser.add_option("-i", "--dir", type="string", help="json file directory on server", dest="InPath", default="/pub/misc/openstreetmap/openseamap/charts/kap")
    parser.add_option("-o", "--filedir", type="string", help="url", dest="OutPath", default="sample/kap/")

    options, arguments = parser.parse_args()
    ftphandler = ftpAccess(options.address)
    ftpfilenamelist = ftphandler.GetFileListFtp(options.InPath)
    jsonfilelist = list()

    # loop over all files
    for file in ftpfilenamelist:
        filename = file[0]
        # search JsonFiles
        if (filename[-5:].find('.json') != -1):
            print("download file {}".format(filename))
            jsonfilelist.append(filename)
            jsondata = ftphandler.GetFtpFile(options.InPath, filename, options.OutPath)
