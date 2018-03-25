'''
Created on 21.12.2017

@author: stevo
'''

import geojson
from utils.osmchart import osmchart_atlas
from utils.filesystem import GetFileList
from optparse import OptionParser
from geojson.feature import Feature, FeatureCollection
from geojson.geometry import Polygon
from utils.pyFTP import ftpAccess


class JsonFileInfoList(object):
    
    class JsonFileInfo():
        def __init__(self, filename):
            # check extension
            if(filename[-5:] != '.json'):
                assert(0)
            
            self.filename=filename
            self.mapname = filename[:-19]
            self.timestamp = filename[-18:-5]
            
            print("{}-{}".format(self.mapname,self.timestamp))
    
    def __init__(self):
        # check extension
        self.jsonfilelist = list()  
    
    def SearchMapEntry(self, name):
        retv=None
        idx=0
        for entry in self.jsonfilelist:
            if entry.mapname == name:
                retv=idx
                break
            idx = idx + 1
        return retv
    
    def append(self, value1): 
        
        value = JsonFileInfoList.JsonFileInfo(value1)
        
        # check if entry for map exists
        idx = self.SearchMapEntry(value.mapname) 
        if  idx == None:
            self.jsonfilelist.append(value)
        else:
            print("JsonFileInfoList: update Entry, {}, {}".format(self.jsonfilelist[idx].timestamp, value.timestamp))
            if(self.jsonfilelist[idx].timestamp < value.timestamp):
                # update timestamp
                self.jsonfilelist[idx].timestamp = value.timestamp
            else:
                pass
        return    
            
    def GetFilenameList(self):
        retv = list()
        for entry in self.jsonfilelist:
            retv.append("{}-{}.json".format(entry.mapname,entry.timestamp))
        return retv
    

def GetJsonFiles(InDir):
    jsonfileinfolist=JsonFileInfoList()
    jsonfilenamelist = GetFileList(InDir,'.json')
       
    # search file with newest timestamp in filename
    for entry in jsonfilenamelist:
        jsonfileinfolist.append(entry)
    
    return jsonfileinfolist.GetFilenameList()


# brief: prepare meta data for download layer
# 
# purpose:
# 
# this script read meta data for several chart bundles and "merge" it into an "single file"
# command line parameter description:
#    -i: points to input directory, the application will search for *.json input files here
#        the script expects a geojson file (see sample directory for example of the fomat)
#    -o: output file with collection of bundles for download layer
#    -f: 
# usage: python: pmd4dl -i ./sample/    
if __name__ == '__main__':
    
    parser = OptionParser()
    usage = "usage: %prog [options] arg1 arg2"
    atlas=list()
    
    parser.add_option("-d",     "--InDir",       type="string", help="Input Directory",  dest="InDir"  ,  default="./sample/")
    parser.add_option("-o",     "--OutFile",     type="string", help="Output Filename",  dest="OutFile",  default="./sample/dl.geojson")
    parser.add_option("-f",     "--factor",      type="float" , help="filter value",     dest="factor" ,  default=2)
    parser.add_option("-u",     "--url",         type="string", help="url"         ,     dest="url"    ,  default="ftp://ftp5.gwdg.de/pub/misc/openstreetmap/openseamap/charts/kap/")
    parser.add_option("-a",     "--address",  type="string", help="server address"                 ,     dest="address" ,  default="ftp5.gwdg.de")
    parser.add_option("-i",     "--dir",      type="string", help="json file directory on server"  ,     dest="InPath"  ,  default="/pub/misc/openstreetmap/openseamap/charts/history/kap")
 
    options, arguments = parser.parse_args()
    
    # get all json files from given directory
    filenamelist = GetJsonFiles(options.InDir)
    
    #for entry in filenamelist:
    #    print(entry)
    
    # create list for huell
    feature_list = list()
        
    print("pmd4dl started")
    print("input file directory {}".format(options.InDir))
    print("output file name     {}".format(options.OutFile))
    print("download url         {}".format(options.url))
    print("facor                {}".format(options.factor))
    
    ftphandler = ftpAccess(options.address)
    ftpfilenamelist =  ftphandler.GetFileListFtp(options.InPath) 
 
    # loop over all files
    for filename in filenamelist:
        
        # create atlas object from given geo json file with atlas meta data
        a=osmchart_atlas(options.InDir+filename)    
        
        if(len(a.chartlist)):
            # calculate "convex hull" over all coordinates
            huell = a.CalcHull(level=options.factor)
            
            kap_file_url = options.url + filename[:-4]+'7z' 
            
            # create Polygon Object and take over properties 
            
            # note: some properties are missing in the current version of meta files  
            # see http://wiki.openseamap.org/wiki/OpenSeaMap-dev:De:Chart_Download_Layer#Dateiformat:_GeoJSON for details
            kapfileworkaround = True # should be set to None if meta files include all required properties 
                    
            if kapfileworkaround == None:
                jsonres = Feature(geometry=Polygon([huell],properties=a.properties))
            else:
                
                try:
                    name=a.properties['name:en']
                except:
                    pass
                
                try:
                    name=a.properties['name']
                except:
                    pass
                
                try:
                    format=a.properties['format']
                except:
                    format="KAP"
                    
                try:
                    app=a.properties['app']
                except:
                    app="opencpn"
                    
                try:
                    size="unknown"
                    for entry in ftpfilenamelist:
                        name = filename[:-4]+"7z"
                        if entry[0]==name:
                            size = entry[1]
                            break
                    pass
                except:
                    pass
                 
                jsonres = Feature(geometry=Polygon([huell]), properties={ 
                                                      "name:en": name,
                                                      "format": format, 
                                                      "app": app,
                                                      "app:url": 'https://opencpn.org/',
                                                      "url": kap_file_url, 
                                                      "date": a.properties['date'], 
                                                      "filesize": size,
                                                      })
            
            #all created polygon object to list with all hull polygons
            feature_list.append(jsonres)
            
            # just a self check
            if jsonres.is_valid != True:
                print(jsonres.errors())
            
            # print debug message
            print("add buendle - name: {}, date: {}, format: {}".format(name,a.properties['date'],format))        
       
    # create FeatureCollection with all created polygons
    jsonres = FeatureCollection(feature_list)
    
    if jsonres.is_valid != True:
        print(jsonres.errors())
    
    
    # print created geojson object to console
    # print(geojson.dumps(jsonres, indent=4, sort_keys=True))   
    
    # print created geojson object to output file
    with open(options.OutFile, 'w') as f:
        f.write(geojson.dumps(jsonres, indent=4, sort_keys=True))
            
