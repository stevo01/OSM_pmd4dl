'''
Created on 25.12.2017

@author: stevo
'''
import unittest
import geojson
from geojson.geometry import Polygon, MultiPolygon, GeometryCollection
from geojson.feature import Feature

class Test(unittest.TestCase):


    def testSimplePolygon(self):
        
        NW = (12.0,50.0)
        SW = (12.0,49.0)
        SE = (13.0,49.0)
        NE = (13.0,50.0)
        
        sample_obj = Polygon([[NW, SW, SE, NE, NW]],properties={"name": "area1","date": "12.12.2017"}) 
        
        expectedRes = '{"coordinates": [[[12.0, 50.0], [12.0, 49.0], [13.0, 49.0], [13.0, 50.0], [12.0, 50.0]]], "properties": {"date": "12.12.2017", "name": "area1"}, "type": "Polygon"}'
        #              {"coordinates": [[[-9.84375, 36.597889133070225], [-7.734375, 33.43144133557529], [-7.03125, 33.43144133557529], [11.6015625, 34.59704151614417], [14.765625, 35.74651225991851], [15.46875, 36.597889133070225], [16.875, 38.8225909761771], [16.875, 39.36827914916013], [15.8203125, 40.17887331434696], [15.1171875, 40.713955826286046], [10.1953125, 44.33956524809714], [9.4921875, 44.59046718130883], [8.4375, 44.59046718130883], [3.8671875, 43.58039085560783], [2.8125, 43.32517767999296], [-9.66796875, 37.02009820136811], [-9.84375, 36.87962060502676], [-9.84375, 36.597889133070225]]], "type": "Polygon"}
        
        if sample_obj.is_valid != True:
            print(sample_obj.errors())
        
        self.assertEqual(sample_obj.is_valid, True)
        self.assertEqual(expectedRes, geojson.dumps(sample_obj, sort_keys=True))
    
    def testMultiPolygon(self):
        
        NW1 = (12.0,50.0)
        SW1 = (12.0,49.0)
        SE1 = (13.0,49.0)
        NE1 = (13.0,50.0)
        
        NW2 = (14.0,50.0)
        SW2 = (14.0,49.0)
        SE2 = (15.0,49.0)
        NE2 = (15.0,50.0)
        
        sample_obj = MultiPolygon([([NW1, SW1, SE1, NE1, NW1],),([NW2, SW2, SE2, NE2, NW2],)])
        
        expectedRes = '{"coordinates": [[[[12.0, 50.0], [12.0, 49.0], [13.0, 49.0], [13.0, 50.0], [12.0, 50.0]]], [[[14.0, 50.0], [14.0, 49.0], [15.0, 49.0], [15.0, 50.0], [14.0, 50.0]]]], "type": "MultiPolygon"}'

        if sample_obj.is_valid != True:
            print(sample_obj.errors())
        
        self.assertEqual(sample_obj.is_valid, True)
        self.assertEqual(expectedRes, geojson.dumps(sample_obj, sort_keys=True))
        
    def testGeometrieCollection(self):
        
        NW1 = (12.0,50.0)
        SW1 = (12.0,49.0)
        SE1 = (13.0,49.0)
        NE1 = (13.0,50.0)
        
        NW2 = (14.0,50.0)
        SW2 = (14.0,49.0)
        SE2 = (15.0,49.0)
        NE2 = (15.0,50.0)
        
        collection = list()
        collection.append(  Polygon([[NW1, SW1, SE1, NE1, NW1]],properties={"name": "area1"})) 
        collection.append(  Polygon([[NW2, SW2, SE2, NE2, NW2]],properties={"name": "area2"}) )

        sample_obj = GeometryCollection(collection)
         
        expectedRes = '{"geometries": [{"coordinates": [[[12.0, 50.0], [12.0, 49.0], [13.0, 49.0], [13.0, 50.0], [12.0, 50.0]]], "properties": {"name": "area1"}, "type": "Polygon"}, '
        expectedRes += '{"coordinates": [[[14.0, 50.0], [14.0, 49.0], [15.0, 49.0], [15.0, 50.0], [14.0, 50.0]]], "properties": {"name": "area2"}, "type": "Polygon"}], "type": "GeometryCollection"}'
        
        if sample_obj.is_valid != True:
            print(sample_obj.errors())
        
        self.assertEqual(sample_obj.is_valid, True)
        self.assertEqual(expectedRes, geojson.dumps(sample_obj, sort_keys=True))
        
        pass
    
    
    def testgeojsonmetadata(self):

        expectedRes = '{"geometry": {"coordinates": [[[0, 55.77657302], [0, 40.97989807], [-11.25, 40.97989807], [-11.25, 55.77657302], [0, 55.77657302]]], "properties": {"app": "OpenCPN", "app:url": "http://opencpn.org/ocpn/", "date": "2016-05-17T20:59:00.000Z", "filesize": 12345, "format": "KAP", "name:de": "Golf von Biskaya", "name:en": "Gulf of Biscay", "url": "ftp://ftp5.gwdg.de/pub/misc/openstreetmap/openseamap/chartbundles/kap/OSM-OpenCPN-KAP2-GulfOfBiscay-20160515-1145.7z"}, "type": "Polygon"}, "properties": {}, "type": "Feature"}'
        
        NW1 = (12.0,50.0)
        SW1 = (12.0,49.0)
        SE1 = (13.0,49.0)
        NE1 = (13.0,50.0)
        
        [0, 55.77657302],
        [0, 40.97989807],
        [-11.25, 40.97989807],
        [-11.25, 55.77657302],
        [0, 55.77657302]
                
        sample_obj = Polygon([[(0, 55.77657302), (0, 40.97989807), (-11.25, 40.97989807), (-11.25, 55.77657302), ( 0, 55.77657302)]],
                             properties={"name:en": "Gulf of Biscay",
                                         "name:de": "Golf von Biskaya",
                                         "format": "KAP",
                                         "app": "OpenCPN",
                                         "app:url": "http://opencpn.org/ocpn/",
                                         "url": "ftp://ftp5.gwdg.de/pub/misc/openstreetmap/openseamap/chartbundles/kap/OSM-OpenCPN-KAP2-GulfOfBiscay-20160515-1145.7z",
                                         "date": "2016-05-17T20:59:00.000Z",
                                         "filesize": 12345
                                         }) 
        
        sample_obj = Feature(geometry=sample_obj)
    
        if sample_obj.is_valid != True:
            print(sample_obj.errors())
        
        self.assertEqual(sample_obj.is_valid, True)
        self.assertEqual(expectedRes, geojson.dumps(sample_obj, sort_keys=True))
        
        pass

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
