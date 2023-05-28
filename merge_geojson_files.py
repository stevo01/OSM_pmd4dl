'''
Created on 21.12.2017

@author: stevo
'''

import geojson
from utils.filesystem import GetFileList
from optparse import OptionParser
from geojson.feature import FeatureCollection


class JsonFileInfoList(object):

    class JsonFileInfo():

        def __init__(self, filename):
            # check extension
            if(filename[-8:] != '.geojson'):
                assert(0)

            self.filename = filename
            self.mapname = filename[:-22]

    def __init__(self):
        # check extension
        self.jsonfilelist = list()

    def append(self, value1):
        self.jsonfilelist.append(value1)
        return

    def GetFilenameList(self):
        retv = list()
        for entry in self.jsonfilelist:
            filename = entry
            print(filename)
            retv.append(filename)
        return retv


def GetJsonFiles(InDir):
    jsonfileinfolist = JsonFileInfoList()
    jsonfilenamelist = GetFileList(InDir, '.geojson')

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
    atlas = list()

    parser.add_option("-d", "--InDir", type="string", help="Input Directory", dest="InDir", default="./sample/geojson/dl/")
    parser.add_option("-o", "--OutFile", type="string", help="Output Filename", dest="OutFile", default="./sample/overview.geojson")
    options, arguments = parser.parse_args()

    # get all json files from given directory
    filenamelist = GetJsonFiles(options.InDir)

    print (filenamelist)

    # for entry in filenamelist:
    #    print(entry)

    # create list for huell
    feature_list = list()


    print("merge_geojson_files started")
    print("input file directory {}".format(options.InDir))
    print("output file name     {}".format(options.OutFile))

    # loop over all files and merge
    for filename in filenamelist:

        with open(options.InDir + filename) as f:
            content = f.read()
            gj_data = geojson.loads(content)
            
            gj_data.properties["date"]="2023-04-01T12:00:00Z"    

            feature_list.append(gj_data)

    jsonres = FeatureCollection(feature_list)

    if jsonres.is_valid is not True:
        print(jsonres.errors())

    # print created geojson object to console
    # print(geojson.dumps(jsonres, indent=4, sort_keys=True))

    # print created geojson object to output file
    with open(options.OutFile, 'w') as f:
        f.write(geojson.dumps(jsonres, indent=4, sort_keys=True))

    print("exit merge_geojson_files")
