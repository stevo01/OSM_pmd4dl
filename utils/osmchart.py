'''
Created on 24.12.2017

@author: stevo
'''

from math import fabs
from utils.convex_huell import convexhull
import geojson

# Latidude - Breitengrade 180
# (parallel to equator)

# Longitude Laengengrade  360
# 

class osmchart_atlas(object):
    def __init__(self,filename):
        self.name=filename;
        self.chartlist = list();
        with open(filename) as f:
            content = f.read()
            
            gj_data = geojson.loads(content)
            
            if gj_data.is_valid != True:
                print(gj_data.errors())
            
            for tmp_area in gj_data.get("geometry").get("geometries"):
                coordlist = tmp_area.get("coordinates")
                self.chartlist.append(area(json_obj=tmp_area.get("coordinates")))
                
            self.properties = gj_data.properties
    
    
    def CalcHull(self, level):
        NumberOfCharts=0
        NumberOfFiltered=0
        points = list()
        
        for chart in self.chartlist:
            NumberOfCharts+=1
            area = chart.GetArea()  
            #print(area)
            if(area<level):
                NumberOfFiltered+=1
                points.append((chart.NE.lon, chart.NE.lat) )
                points.append((chart.NW.lon, chart.NW.lat) )
                points.append((chart.SE.lon, chart.SE.lat) )
                points.append((chart.SW.lon, chart.SW.lat) )
            
        ret = convexhull(points)
        ret.append(ret[0])
        
        return ret               
    
    
    def __str__(self):
        out = "number of charts={}".format(len(self.chartlist))
        return out 
    
    def dump(self):
        for entry in self.chartlist:
            print(entry);
                

# storage for coordinates for a single point
class coordinate(object):

    def __init__(self, lat, lon):
        self.lon=lon
        self.lat=lat
        
    def __str__(self):
        out = "lon={}, lat={}".format(self.lon, self.lat)
        return out
 
# storage for coordinates of a given area   
class area(object):
    
    # lat0 lon0 is a left,top     (NW) point 
    # lat1 lon1 is a right,bottom (SE) point         
    def __init__(self, lat0=None, lon0=None, lat1=None, lon1=None, name=None, zoom=None, json_obj=None ):
        if json_obj==None:
            self.NW=coordinate(lat0, lon0)
            self.SW=coordinate(lat1, lon0)
            self.NE=coordinate(lat0, lon1)
            self.SE=coordinate(lat1, lon1)
            self.zoom = zoom
            self.name = name
        else:
            self.SW=coordinate(json_obj[0][0][1], json_obj[0][0][0])
            self.NW=coordinate(json_obj[0][1][1], json_obj[0][1][0])
            self.NE=coordinate(json_obj[0][2][1], json_obj[0][2][0])
            self.SE=coordinate(json_obj[0][3][1], json_obj[0][3][0])
            self.zoom = None
            self.name = None
            
    def GetArea(self):
        dx = fabs(self.NW.lon - self.SE.lon)
        dy = fabs(self.NW.lat - self.SE.lat)
        ret = dx*dy
        
        return ret; 
        
    def __str__(self):
        out = "{}\n".format(self.name) 
        out += "SE lat={}, lon={}\n".format(self.NW.lat, self.NW.lon)
        out += "SW lat={}, lon={}\n".format(self.SW.lat, self.SW.lon)
        out += "NE lat={}, lon={}\n".format(self.NE.lat, self.NE.lon)
        out += "NW lat={}, lon={}  ".format(self.SE.lat, self.SE.lon)
        return out 
    