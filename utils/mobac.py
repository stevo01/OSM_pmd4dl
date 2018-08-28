#!/usr/bin/python3
# encoding: utf-8
'''
implements access to OMAC project file

Copyright (C) 2017  Steffen Volkmann

This file is part of SeaMapCreator.

Foobar is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

Foobar is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with Foobar.  If not, see <http://www.gnu.org/licenses/>.

'''
from xml.dom import minidom
from utils.Helper import area
from utils.Conversions import num2deg


def DetectType(xmldoc):

    try:
        xmldoc.getElementsByTagName('atlas')[0]
        return "atlas"
    except:

        try:
            xmldoc.getElementsByTagName('catalog')[0]
            return "catalog"
        except:
            pass

    return "unknown"


# this function parses a mobac projekt file and returns list with tile information for each found map/chart
def ExtractMapsFromAtlas(filename):
    xmldoc = minidom.parse(filename)

    doctype = DetectType(xmldoc)
    if doctype == "atlas":
        item = xmldoc.getElementsByTagName('atlas')[0]

        atlasname = item.attributes['name'].value

        itemlist = xmldoc.getElementsByTagName('Map')
        ret = list()
        for item in itemlist:
            name = item.attributes['name'].value
            name = name.replace(" ", "_")
            zoom = int(item.attributes['zoom'].value)

            minTileCoordinate = item.attributes['minTileCoordinate'].value  # NW
            x_min, y_min = minTileCoordinate.split('/')
            x_min = int(x_min) / 256
            y_min = int(y_min) / 256
            lat_min, lon_min = num2deg(x_min, y_min, zoom)

            maxTileCoordinate = item.attributes['maxTileCoordinate'].value  # SO
            x_max, y_max = maxTileCoordinate.split('/')
            x_max = (int(x_max) / 256)
            y_max = (int(y_max) / 256)
            lat_max, lon_max = num2deg(x_max, y_max, zoom)

            a = area(lat_min, lon_min, lat_max, lon_max, name, zoom)
            ret.append(a)

    elif doctype == "catalog":
        item = xmldoc.getElementsByTagName('catalog')[0]

        atlasname = item.attributes['name'].value

        layerlist = xmldoc.getElementsByTagName('Layer')

        ret = list()

        for layer in layerlist:

            zoom = int(layer.attributes['zoomLvl'].value)

            itemlist = layer.getElementsByTagName('Map')

            for item in itemlist:
                name = item.attributes['name'].value
                name = name.replace(" ", "_")

                minTileCoordinate = item.attributes['minTileCoordinate'].value  # NW
                y_min, x_min = minTileCoordinate.split('/')
                x_min = int(x_min)  # / 256
                y_min = int(y_min)  # / 256
                lat_min, lon_min = num2deg(x_min, y_min, zoom)

                maxTileCoordinate = item.attributes['maxTileCoordinate'].value  # SO
                y_max, x_max = maxTileCoordinate.split('/')
                x_max = int(x_max)  # / 256)
                y_max = int(y_max)  # / 256)
                lat_max, lon_max = num2deg(x_max, y_max, zoom)

                a = area(lat_min, lon_min, lat_max, lon_max, name, zoom)
                ret.append(a)
    else:
        assert(0)

    return ret, atlasname
