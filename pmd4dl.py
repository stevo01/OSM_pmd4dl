'''
Created on 21.12.2017

@author: stevo
'''

import geojson
from utils.osmchart import osmchart_atlas
from utils.filesystem import GetFileList
from geojson.geometry import Polygon, GeometryCollection
from optparse import OptionParser


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
    
    #parser.add_option("-d",     "--DownloadPath", type="string", help="download path",                       dest="DownloadPath", default="./download")
    parser.add_option("-i",     "--InDir",       type="string", help="Input Directory",  dest="InDir"  ,  default="./sample/")
    parser.add_option("-o",     "--OutFile",     type="string", help="Output Filename",  dest="OutFile",  default="./sample/dl.geojson")
    parser.add_option("-f",     "--factor",      type="float", help="filter value",      dest="factor" ,  default=2)
    
    options, arguments = parser.parse_args()
    
    # get all json files from given directory
    filenamelist = GetFileList(options.InDir,'.json')
    
    # create list for huell
    huell_list = list()
    
    print("pmd4dl started")
    print("input file directory {}".format(options.InDir))
    print("output file name     {}".format(options.OutFile))
    print("facor                {}".format(options.factor))
    
    # loop over all files
    for filename in filenamelist:
        
        # create atlas object from given geo json file with atlas meta data
        a=osmchart_atlas(options.InDir+filename)    
        
        # calculate "convex hull" over all coordinates
        huell = a.CalcHull(level=options.factor)
        
        # create Polygon Object and take over properties 
        jsonres = Polygon([huell],properties={"kind": a.properties['kind'], 
                                              "name:en": a.properties['name:en'],
                                              "format": a.properties['format'], 
                                              "app": a.properties['app'], 
                                              "date": a.properties['date'], })

        #all created polygon object to list with all hull polygons
        huell_list.append(jsonres)
        
        # just a self check
        if jsonres.is_valid != True:
            print(jsonres.errors())
        
        # print debug message
        print("add buendle - name: {}, date: {}, format: {}".format(a.properties['name:en'],a.properties['date'],a.properties['format']))        
   
    # create GeometryCollection with all created polygons
    jsonres = GeometryCollection(huell_list)
    
    if jsonres.is_valid != True:
        print(jsonres.errors())
    
    
    # print created geojson object to console
    # print(geojson.dumps(jsonres, indent=4, sort_keys=True))   
    
    # print created geojson object to output file
    with open(options.OutFile, 'w') as f:
        f.write(geojson.dumps(jsonres, indent=4, sort_keys=True))
            
