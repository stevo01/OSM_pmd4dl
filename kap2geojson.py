'''
Created on 28.08.2018

@author: stevo
'''
from optparse import OptionParser
from UnitTests.osmchart import HandleDate
import os
from utils.mobac import ExtractMapsFromAtlas
from utils.convex_huell import convexhull
import geojson
from geojson.feature import Feature
from geojson.geometry import Polygon

# this script generates a geojson file for open sea map download layer

# smaple geo json file:
# https://wiki.openseamap.org/wiki/OpenSeaMap-dev:De:Chart_Download_Layer

if __name__ == '__main__':

    parser = OptionParser()
    usage = "usage: %creator [options] arg1 arg2"
    atlas = list()

    parser.add_option("-u", "--url", type="string", help="server address", dest="url", default="https://ftp5.gwdg.de")
    parser.add_option("-d", "--dir", type="string", help="json file directory on server", dest="InPath", default="/pub/misc/openstreetmap/openseamap/charts/kap")
    parser.add_option("-f", "--filename", type="string", help="filename of the kap file archive", dest="kapfilename", default="sample/7z/OSM-OpenCPN2-KAP-Adria-20180629-0337.7z")
    parser.add_option("-p", "--project", type="string", help="filename of the chart bundler project file", dest="ProjectFile", default="sample/atlas/osmcb/sea/osmcb-catalog-Adria.xml")
    parser.add_option("-z", "--zoom", type="int", help="zoom level", dest="zoom", default=12)

    options, arguments = parser.parse_args()

    # get timestamp from filename of the kap file archive
    date = options.kapfilename[-16:-3]
    date = HandleDate(date)

    # get size ( from kap file archive )
    filesize = os.path.getsize(options.kapfilename)

    # get chart name ( from project file )
    atlas, mapname = ExtractMapsFromAtlas(options.ProjectFile)

    # create polygon ( from project file )
    points = list()
    for chart in atlas:
        # print(area)
        if(chart.zoom >= options.zoom):
            points.append((chart.NE.lon, chart.NE.lat))
            points.append((chart.NW.lon, chart.NW.lat))
            points.append((chart.SE.lon, chart.SE.lat))
            points.append((chart.SW.lon, chart.SW.lat))
        else:
            print("skip chart {}".format(chart.name))

    huell = convexhull(points)
    huell.append(huell[0])

    outfilename = options.kapfilename[:-3] + '.geojson'

    url = "{}{}/{}".format(
        options.url,
        options.InPath,
        os.path.basename(options.kapfilename))

    # generate geojson object
    jsonres = Feature(geometry=Polygon([huell]),
                      properties={"name:en": mapname,
                                  "format": "KAP",
                                  "app": "OpenCPN",
                                  "app:url": 'https://opencpn.org/',
                                  "url": url,
                                  "date": date,
                                  "filesize": filesize})

    # print created geojson object to output file
    with open(outfilename, 'w') as f:
        f.write(geojson.dumps(jsonres, indent=4, sort_keys=True))
